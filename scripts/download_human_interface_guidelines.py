#!/usr/bin/env -S uv run --script
# /// script
# dependencies = []
# ///
"""Archive Apple's complete Human Interface Guidelines DocC corpus.

The public HIG site is a DocC single-page application. Its HTML alone is only a
renderer shell, so this script uses the site's navigation index to enumerate
every HIG page, downloads each page's source JSON, and downloads every media or
file reference used by those pages.

Run from anywhere:

    uv run scripts/download_human_interface_guidelines.py

The default destination is ``docs/human-interface-guidelines`` at the repository
root. A manifest with SHA-256 hashes makes the archive auditable and allows a
later ``--verify-only`` run to detect missing or corrupted files.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import sys
import threading
import time
from collections.abc import Iterable, Mapping
from datetime import UTC, datetime
from email.message import Message
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, urlunsplit
from urllib.request import Request, urlopen

HIG_ROOT_PATH = "/design/human-interface-guidelines"
HIG_SOURCE_URL = f"https://developer.apple.com{HIG_ROOT_PATH}"
DATA_BASE_URL = "https://developer.apple.com/tutorials/data"
NAVIGATION_INDEX_URL = f"{DATA_BASE_URL}/index/design--human-interface-guidelines"
DEFAULT_OUTPUT = (
    Path(__file__).resolve().parents[1] / "docs" / "human-interface-guidelines"
)
DEFAULT_WORKERS = 8
DEFAULT_TIMEOUT = 60.0
DEFAULT_RETRIES = 5
USER_AGENT = (
    "Mozilla/5.0 (compatible; Apple-HIG-Archiver/1.0; "
    "+https://developer.apple.com/design/human-interface-guidelines)"
)
RESOURCE_REFERENCE_TYPES = {
    "audio",
    "download",
    "file",
    "image",
    "resource",
    "video",
}
RETRYABLE_HTTP_STATUSES = {408, 425, 429, 500, 502, 503, 504}
MANIFEST_SCHEMA_VERSION = 1

_PRINT_LOCK = threading.Lock()


class DownloadError(RuntimeError):
    """Raised when an artifact cannot be downloaded after all retries."""


def log(message: str) -> None:
    """Print one complete progress line when workers are running concurrently."""
    with _PRINT_LOCK:
        print(message, flush=True)


def collect_hig_paths(index: Mapping[str, Any]) -> list[str]:
    """Return every unique HIG page path from the complete navigator tree."""
    paths: list[str] = []
    seen: set[str] = set()

    def add_path(raw_path: str) -> None:
        parsed = urlsplit(raw_path)
        path = parsed.path.rstrip("/") or "/"
        if path != HIG_ROOT_PATH and not path.startswith(f"{HIG_ROOT_PATH}/"):
            return
        if path not in seen:
            seen.add(path)
            paths.append(path)

    def walk(value: Any) -> None:
        if isinstance(value, Mapping):
            path = value.get("path")
            if isinstance(path, str):
                add_path(path)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    # A malformed or temporarily changed index should never make the landing page
    # disappear from an otherwise complete archive.
    add_path(HIG_ROOT_PATH)
    walk(index)
    return paths


def _absolute_http_urls(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        parsed = urlsplit(value)
        if parsed.scheme in {"http", "https"} and parsed.netloc:
            # Fragments do not identify separate downloadable artifacts.
            yield urlunsplit(
                (parsed.scheme, parsed.netloc, parsed.path, parsed.query, "")
            )
    elif isinstance(value, Mapping):
        for child in value.values():
            yield from _absolute_http_urls(child)
    elif isinstance(value, list):
        for child in value:
            yield from _absolute_http_urls(child)


def collect_asset_urls(page: Mapping[str, Any]) -> list[str]:
    """Collect media/file URLs without following ordinary external topic links."""
    urls: set[str] = set()
    references = page.get("references", {})
    if not isinstance(references, Mapping):
        return []

    for reference in references.values():
        if not isinstance(reference, Mapping):
            continue
        reference_type = reference.get("type")
        if reference_type not in RESOURCE_REFERENCE_TYPES:
            continue
        urls.update(_absolute_http_urls(reference))
    return sorted(urls)


def _safe_segment(segment: str) -> str:
    if segment in {"", ".", ".."}:
        return "_"
    # Keep URL percent escapes intact while preventing filesystem separators and
    # control characters from changing the archive layout.
    return "".join(
        character if character >= " " and character not in {"/", "\\", ":"} else "_"
        for character in segment
    )


def local_path_for_url(url: str, prefix: Path = Path("assets")) -> Path:
    """Map an absolute URL to a collision-resistant relative archive path."""
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"not an absolute HTTP URL: {url}")

    host = _safe_segment(parsed.netloc.lower())
    path_segments = [_safe_segment(part) for part in parsed.path.split("/") if part]
    if not path_segments or parsed.path.endswith("/"):
        path_segments.append("index")

    filename = path_segments[-1]
    if parsed.query:
        digest = hashlib.sha256(parsed.query.encode()).hexdigest()[:12]
        suffix = Path(filename).suffix
        stem = filename[: -len(suffix)] if suffix else filename
        path_segments[-1] = f"{stem}--{digest}{suffix}"

    return prefix / host / Path(*path_segments)


def page_data_path(path: str) -> Path:
    """Return the local path corresponding to a HIG DocC JSON endpoint."""
    normalized = urlsplit(path).path.rstrip("/")
    if normalized != HIG_ROOT_PATH and not normalized.startswith(f"{HIG_ROOT_PATH}/"):
        raise ValueError(f"path is outside the HIG: {path}")
    return Path(f"data{normalized}.json".lstrip("/"))


def page_data_url(path: str) -> str:
    return f"{DATA_BASE_URL}{urlsplit(path).path.rstrip('/')}.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _retry_delay(attempt: int, headers: Message | None = None) -> float:
    if headers is not None:
        retry_after = headers.get("Retry-After")
        if retry_after:
            try:
                return min(float(retry_after), 60.0)
            except ValueError:
                pass
    return min(2**attempt, 30.0)


def fetch_bytes(
    url: str,
    *,
    timeout: float = DEFAULT_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
) -> tuple[bytes, str]:
    """Fetch a URL with bounded retries and return bytes plus content type."""
    request = Request(
        url,
        headers={
            "Accept": "*/*",
            "User-Agent": USER_AGENT,
        },
    )
    last_error: BaseException | None = None

    for attempt in range(retries + 1):
        try:
            with urlopen(request, timeout=timeout) as response:
                content_type = response.headers.get_content_type()
                return response.read(), content_type
        except HTTPError as error:
            last_error = error
            if error.code not in RETRYABLE_HTTP_STATUSES or attempt >= retries:
                break
            delay = _retry_delay(attempt, error.headers)
        except (TimeoutError, URLError, OSError) as error:
            last_error = error
            if attempt >= retries:
                break
            delay = _retry_delay(attempt)

        log(f"retry {attempt + 1}/{retries}: {url} in {delay:.0f}s")
        time.sleep(delay)

    raise DownloadError(f"failed to download {url}: {last_error}") from last_error


def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(
        f".{path.name}.part-{os.getpid()}-{threading.get_ident()}"
    )
    try:
        temporary.write_bytes(content)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _artifact_record(
    *,
    output: Path,
    relative_path: Path,
    url: str,
    kind: str,
    content_type: str,
) -> dict[str, Any]:
    absolute_path = output / relative_path
    return {
        "kind": kind,
        "url": url,
        "path": relative_path.as_posix(),
        "content_type": content_type,
        "size": absolute_path.stat().st_size,
        "sha256": sha256_file(absolute_path),
    }


def _download_json_artifact(
    *,
    output: Path,
    relative_path: Path,
    url: str,
    kind: str,
    timeout: float,
    retries: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    content, content_type = fetch_bytes(url, timeout=timeout, retries=retries)
    try:
        parsed = json.loads(content)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise DownloadError(f"invalid JSON from {url}: {error}") from error
    if not isinstance(parsed, dict):
        raise DownloadError(f"expected a JSON object from {url}")
    _atomic_write(output / relative_path, content)
    return parsed, _artifact_record(
        output=output,
        relative_path=relative_path,
        url=url,
        kind=kind,
        content_type=content_type,
    )


def _load_previous_artifacts(output: Path) -> dict[str, dict[str, Any]]:
    manifest_path = output / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text())
    except (FileNotFoundError, UnicodeDecodeError, json.JSONDecodeError):
        return {}
    artifacts = manifest.get("artifacts", [])
    if not isinstance(artifacts, list):
        return {}
    return {
        artifact["url"]: artifact
        for artifact in artifacts
        if isinstance(artifact, dict) and isinstance(artifact.get("url"), str)
    }


def _matches_record(output: Path, record: Mapping[str, Any]) -> bool:
    relative = record.get("path")
    expected_size = record.get("size")
    expected_sha = record.get("sha256")
    if not isinstance(relative, str) or not isinstance(expected_size, int):
        return False
    if not isinstance(expected_sha, str):
        return False
    path = output / relative
    return (
        path.is_file()
        and path.stat().st_size == expected_size
        and sha256_file(path) == expected_sha
    )


def _download_asset(
    *,
    output: Path,
    url: str,
    timeout: float,
    retries: int,
    previous: Mapping[str, Mapping[str, Any]],
    force: bool,
) -> dict[str, Any]:
    relative_path = local_path_for_url(url)
    previous_record = previous.get(url)
    if (
        not force
        and previous_record is not None
        and previous_record.get("path") == relative_path.as_posix()
        and _matches_record(output, previous_record)
    ):
        return dict(previous_record)

    content, content_type = fetch_bytes(url, timeout=timeout, retries=retries)
    _atomic_write(output / relative_path, content)
    return _artifact_record(
        output=output,
        relative_path=relative_path,
        url=url,
        kind="asset",
        content_type=content_type,
    )


def _parallel_map(
    function: Any,
    items: list[Any],
    *,
    workers: int,
    label: str,
) -> list[Any]:
    results: list[Any] = []
    failures: list[str] = []
    total = len(items)
    completed = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_item = {executor.submit(function, item): item for item in items}
        for future in concurrent.futures.as_completed(future_to_item):
            item = future_to_item[future]
            try:
                results.append(future.result())
            except BaseException as error:  # Report every failed URL/path together.
                failures.append(f"{item}: {error}")
            completed += 1
            if completed == total or completed % 25 == 0:
                log(f"{label}: {completed}/{total}")

    if failures:
        details = "\n".join(f"- {failure}" for failure in failures)
        raise DownloadError(f"{label} failed:\n{details}")
    return results


def _write_manifest(output: Path, manifest: Mapping[str, Any]) -> None:
    content = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    _atomic_write(output / "manifest.json", content)


def download_archive(
    output: Path,
    *,
    workers: int = DEFAULT_WORKERS,
    timeout: float = DEFAULT_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
    force_assets: bool = False,
) -> dict[str, Any]:
    """Download every indexed HIG page and every referenced resource."""
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    previous = _load_previous_artifacts(output)

    log(f"navigation: {NAVIGATION_INDEX_URL}")
    navigation_path = Path("data/index/design--human-interface-guidelines.json")
    navigation, navigation_record = _download_json_artifact(
        output=output,
        relative_path=navigation_path,
        url=NAVIGATION_INDEX_URL,
        kind="navigation-index",
        timeout=timeout,
        retries=retries,
    )
    paths = collect_hig_paths(navigation)
    if not paths:
        raise DownloadError("the navigation index did not contain any HIG pages")
    log(f"discovered {len(paths)} HIG pages")

    def download_page(path: str) -> tuple[str, dict[str, Any], dict[str, Any]]:
        page, record = _download_json_artifact(
            output=output,
            relative_path=page_data_path(path),
            url=page_data_url(path),
            kind="page-json",
            timeout=timeout,
            retries=retries,
        )
        return path, page, record

    page_results = _parallel_map(
        download_page,
        paths,
        workers=workers,
        label="pages",
    )
    page_results.sort(key=lambda result: result[0])

    asset_urls: set[str] = set()
    page_records: list[dict[str, Any]] = []
    for _, page, record in page_results:
        page_records.append(record)
        asset_urls.update(collect_asset_urls(page))
    sorted_asset_urls = sorted(asset_urls)
    log(f"discovered {len(sorted_asset_urls)} referenced assets")

    def download_asset(url: str) -> dict[str, Any]:
        return _download_asset(
            output=output,
            url=url,
            timeout=timeout,
            retries=retries,
            previous=previous,
            force=force_assets,
        )

    asset_records = _parallel_map(
        download_asset,
        sorted_asset_urls,
        workers=workers,
        label="assets",
    )
    asset_records.sort(key=lambda record: record["url"])

    artifacts = [navigation_record, *page_records, *asset_records]
    artifacts.sort(key=lambda record: (record["kind"], record["path"]))
    manifest: dict[str, Any] = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "source": HIG_SOURCE_URL,
        "navigation_index": NAVIGATION_INDEX_URL,
        "downloaded_at": datetime.now(UTC).isoformat(),
        "counts": {
            "pages": len(page_records),
            "assets": len(asset_records),
            "artifacts": len(artifacts),
            "bytes": sum(record["size"] for record in artifacts),
        },
        "page_paths": sorted(paths),
        "artifacts": artifacts,
    }
    _write_manifest(output, manifest)

    verification_errors = verify_archive(output)
    if verification_errors:
        details = "\n".join(f"- {error}" for error in verification_errors)
        raise DownloadError(f"post-download verification failed:\n{details}")
    return manifest


def verify_archive(output: Path) -> list[str]:
    """Verify every manifest artifact by path, byte size, and SHA-256 hash."""
    output = output.resolve()
    manifest_path = output / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text())
    except FileNotFoundError:
        return ["manifest.json is missing"]
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        return [f"manifest.json is invalid: {error}"]

    errors: list[str] = []
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        return ["manifest contains no artifacts"]

    seen_paths: set[str] = set()
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, Mapping):
            errors.append(f"artifact {index} is not an object")
            continue
        relative = artifact.get("path")
        expected_size = artifact.get("size")
        expected_sha = artifact.get("sha256")
        if not isinstance(relative, str):
            errors.append(f"artifact {index} has no valid path")
            continue
        if relative in seen_paths:
            errors.append(f"duplicate artifact path: {relative}")
            continue
        seen_paths.add(relative)
        path = output / relative
        if not path.is_file():
            errors.append(f"missing: {relative}")
            continue
        actual_size = path.stat().st_size
        if not isinstance(expected_size, int) or actual_size != expected_size:
            errors.append(
                f"size mismatch: {relative} (expected {expected_size}, got {actual_size})"
            )
            continue
        actual_sha = sha256_file(path)
        if not isinstance(expected_sha, str) or actual_sha != expected_sha:
            errors.append(f"SHA-256 mismatch: {relative}")

    counts = manifest.get("counts", {})
    if isinstance(counts, Mapping):
        expected_artifacts = counts.get("artifacts")
        if isinstance(expected_artifacts, int) and expected_artifacts != len(artifacts):
            errors.append(
                "artifact count mismatch: "
                f"manifest says {expected_artifacts}, lists {len(artifacts)}"
            )
        expected_pages = counts.get("pages")
        page_paths = manifest.get("page_paths")
        if (
            isinstance(expected_pages, int)
            and isinstance(page_paths, list)
            and expected_pages != len(page_paths)
        ):
            errors.append(
                f"page count mismatch: manifest says {expected_pages}, "
                f"lists {len(page_paths)} paths"
            )
    return errors


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Download every Apple Human Interface Guidelines DocC page and "
            "all referenced media into a verified local archive."
        )
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"archive directory (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=DEFAULT_WORKERS,
        help=f"parallel requests (default: {DEFAULT_WORKERS})",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"per-request timeout in seconds (default: {DEFAULT_TIMEOUT:g})",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=DEFAULT_RETRIES,
        help=f"retries after a failed request (default: {DEFAULT_RETRIES})",
    )
    parser.add_argument(
        "--force-assets",
        action="store_true",
        help="redownload assets even when a verified prior manifest entry exists",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="verify the existing manifest and files without downloading",
    )
    args = parser.parse_args(argv)
    if args.workers < 1:
        parser.error("--workers must be at least 1")
    if args.timeout <= 0:
        parser.error("--timeout must be greater than 0")
    if args.retries < 0:
        parser.error("--retries cannot be negative")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    output: Path = args.output

    if args.verify_only:
        errors = verify_archive(output)
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1
        manifest = json.loads((output / "manifest.json").read_text())
        counts = manifest.get("counts", {})
        print(
            f"verified {counts.get('artifacts')} artifacts "
            f"({counts.get('pages')} pages, {counts.get('assets')} assets) "
            f"in {output.resolve()}"
        )
        return 0

    try:
        manifest = download_archive(
            output,
            workers=args.workers,
            timeout=args.timeout,
            retries=args.retries,
            force_assets=args.force_assets,
        )
    except (DownloadError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    counts = manifest["counts"]
    print(
        f"downloaded and verified {counts['artifacts']} artifacts "
        f"({counts['pages']} pages, {counts['assets']} assets, "
        f"{counts['bytes']:,} bytes) in {output.resolve()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
