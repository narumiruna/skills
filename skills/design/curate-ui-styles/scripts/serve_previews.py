# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Serve one UI style interview and collect its A/B/C answers on loopback."""

import argparse
from http import server as http_server
import json
import pathlib
import re
import tempfile
import threading
import time

HOST = "127.0.0.1"
PREVIEW_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\.html")
CHOICES = ("A", "B", "C")
WAIT_SECONDS = 180
ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"
VIEWER_POLICY = (
    "default-src 'none'; script-src 'self'; style-src 'unsafe-inline'; "
    "connect-src 'self'; frame-src 'self'; frame-ancestors 'none'; "
    "form-action 'none'; base-uri 'none'"
)
PREVIEW_POLICY = (
    "sandbox; default-src 'none'; style-src 'unsafe-inline'; img-src data:; "
    "frame-ancestors 'self'; form-action 'none'; base-uri 'none'"
)


def _regular_file(path: pathlib.Path) -> bool:
    return not path.is_symlink() and path.is_file()


def _valid_preview(directory: pathlib.Path, name: str) -> bool:
    return (
        len(name) <= 128
        and bool(PREVIEW_NAME.fullmatch(name))
        and _regular_file(directory / name)
    )


def _read_state(path: pathlib.Path) -> str:
    if not _regular_file(path):
        return ""
    try:
        with path.open(encoding="ascii") as stream:
            return stream.read(256)
    except (OSError, UnicodeError):
        return ""


def _write_state(path: pathlib.Path, value: str) -> None:
    """Replace one state file without letting readers see a partial write."""
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="ascii", dir=path.parent, delete=False
    ) as stream:
        temporary = pathlib.Path(stream.name)
        try:
            stream.write(value)
            stream.close()
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)


def _current(directory: pathlib.Path) -> tuple[str, str] | None:
    mode, _, name = _read_state(directory / ".current-preview").partition(" ")
    if mode in ("question", "review") and _valid_preview(directory, name):
        return mode, name
    return None


def _answer_path(directory: pathlib.Path, name: str) -> pathlib.Path:
    return directory / f".{name}.answer"


def _wait_for_answer(directory: pathlib.Path, name: str) -> bool:
    """Print the answer for exactly this question, or return false on timeout."""
    deadline = time.monotonic() + WAIT_SECONDS
    while True:
        answer = _read_state(_answer_path(directory, name))
        if answer in CHOICES:
            print(answer)
            return True
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return False
        time.sleep(min(0.25, remaining))


def serve(directory: pathlib.Path) -> None:
    """Start the viewer and expose only its assets, previews, and answer API."""
    viewer = (ASSETS / "interview-viewer.html").read_bytes()
    javascript = (ASSETS / "interview-viewer.js").read_bytes()
    answer_lock = threading.Lock()

    class PreviewHandler(http_server.BaseHTTPRequestHandler):
        """Handle a single local preview or answer request."""

        timeout = 5

        def log_request(self, code="-", size="-") -> None:
            if self.path != "/state" or code != 200:
                super().log_request(code, size)

        def do_GET(self) -> None:
            self._get()

        def do_HEAD(self) -> None:
            self._get()

        def do_POST(self) -> None:
            if not self._check_host():
                return
            if self.path != "/answer":
                self.send_error(404)
                return
            if self.headers.get_all("Origin") != [f"http://{authority}"]:
                self.send_error(403)
                return
            if self.headers.get_content_type() != "application/json":
                self.send_error(415)
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= 256:
                    raise ValueError("invalid answer length")
                payload = json.loads(self.rfile.read(length))
                name = payload["preview"]
                choice = payload["choice"]
                if not isinstance(name, str) or choice not in CHOICES:
                    raise ValueError("invalid answer")
            except (ValueError, TypeError, KeyError):
                self.send_error(400)
                return
            with answer_lock:
                if _current(directory) != ("question", name):
                    self.send_error(409, "This question is no longer active")
                    return
                path = _answer_path(directory, name)
                if path.exists() or path.is_symlink():
                    self.send_error(409, "This question already has an answer")
                    return
                try:
                    _write_state(path, choice)
                except OSError:
                    self.send_error(500, "Could not save the answer")
                    return
            self._send(204, b"", "text/plain")

        def _check_host(self) -> bool:
            if self.headers.get_all("Host") == [authority]:
                return True
            self.send_error(400)
            return False

        def _get(self) -> None:
            if not self._check_host():
                return
            route = self.path.partition("?")[0]
            if route == "/":
                self._send(200, viewer, "text/html", VIEWER_POLICY, "DENY")
            elif route == "/viewer.js":
                self._send(200, javascript, "text/javascript")
            elif route == "/state":
                current = _current(directory)
                state = None
                if current:
                    mode, name = current
                    answer = _read_state(_answer_path(directory, name))
                    state = {
                        "mode": mode,
                        "preview": name,
                        "answer": answer if answer in CHOICES else None,
                    }
                self._send(200, json.dumps(state).encode("ascii"), "application/json")
            elif route.startswith("/") and _valid_preview(directory, route[1:]):
                try:
                    content = (directory / route[1:]).read_bytes()
                except OSError:
                    self.send_error(404)
                    return
                self._send(200, content, "text/html", PREVIEW_POLICY, "SAMEORIGIN")
            else:
                self.send_error(404)

        def _send(
            self, code: int, content: bytes, media_type: str, policy="", framing=""
        ) -> None:
            self.send_response(code)
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            if code != 204:
                self.send_header("Content-Type", f"{media_type}; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
            if policy:
                self.send_header("Content-Security-Policy", policy)
                self.send_header("X-Frame-Options", framing)
            self.end_headers()
            if self.command != "HEAD" and content:
                self.wfile.write(content)

    with http_server.ThreadingHTTPServer((HOST, 0), PreviewHandler) as server:
        authority = f"{HOST}:{server.server_port}"
        print(f"http://{authority}", flush=True)
        server.serve_forever()


def main() -> int:
    """Serve, show a preview, or wait for one answer from the browser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "preview_dir", type=pathlib.Path, help="one interview's previews/"
    )
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument(
        "--show-question", metavar="HTML", help="show an A/B/C question"
    )
    actions.add_argument(
        "--show-review", metavar="HTML", help="show a read-only review"
    )
    actions.add_argument(
        "--wait-for-answer",
        metavar="HTML",
        help="print A/B/C, or exit 3 after 180 seconds",
    )
    parser.epilog = "Without an option, open the printed URL. Press Ctrl+C to stop."
    args = parser.parse_args()
    try:
        directory = args.preview_dir.resolve(strict=True)
    except (OSError, RuntimeError):
        parser.error(f"cannot resolve preview directory: {args.preview_dir}")
    if not directory.is_dir():
        parser.error("preview directory must be a directory")
    try:
        if args.wait_for_answer is not None:
            name = args.wait_for_answer
            if _current(directory) != ("question", name):
                parser.error("show this question before waiting for its answer")
            return 0 if _wait_for_answer(directory, name) else 3
        for mode, name in (
            ("question", args.show_question),
            ("review", args.show_review),
        ):
            if name is not None:
                if not _valid_preview(directory, name):
                    parser.error(
                        "provide the filename of an existing preview HTML, not a path"
                    )
                _write_state(directory / ".current-preview", f"{mode} {name}")
                return 0
        serve(directory)
    except KeyboardInterrupt:
        return 130
    except OSError as error:
        parser.exit(1, f"Preview command failed: {error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
