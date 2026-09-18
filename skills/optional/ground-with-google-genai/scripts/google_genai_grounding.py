# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "google-genai>=2.3.0",
#   "python-dotenv>=1.0.0",
# ]
# ///
"""Run one stateless Google GenAI grounding request and emit evidence as JSON."""

from __future__ import annotations

import argparse
import ipaddress
import json
import os
import sys
from collections.abc import Sequence
from typing import Any
from urllib.parse import urlsplit

DEFAULT_MODEL = "gemini-3.5-flash"
MAX_URLS = 20


def load_api_key() -> str | None:
    """Load a local .env file without overriding the process environment."""
    from dotenv import load_dotenv

    load_dotenv(override=False)
    return os.environ.get("GEMINI_API_KEY")


def _validate_url(url: str) -> str:
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError(f"URL must be a complete http:// or https:// URL: {url}")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError(f"URL must not contain credentials: {url}")

    hostname = parsed.hostname.lower().rstrip(".")
    if hostname == "localhost" or hostname.endswith(".localhost"):
        raise ValueError(f"URL must be publicly accessible, not localhost: {url}")
    try:
        address = ipaddress.ip_address(hostname)
    except ValueError:
        return url
    if not address.is_global:
        raise ValueError(f"URL must not target a private or local address: {url}")
    return url


def build_interaction_request(
    *,
    mode: str,
    prompt: str,
    model: str = DEFAULT_MODEL,
    urls: Sequence[str] | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
) -> dict[str, Any]:
    """Build validated keyword arguments for ``client.interactions.create``."""
    prompt = prompt.strip()
    if not prompt:
        raise ValueError("Prompt must be non-empty")
    if not model.strip():
        raise ValueError("Model must be non-empty")

    if mode == "search":
        tools = [{"type": "google_search"}]
        input_text = prompt
    elif mode == "maps":
        if (latitude is None) != (longitude is None):
            raise ValueError("Maps latitude and longitude must be provided together")
        tool: dict[str, Any] = {"type": "google_maps"}
        if latitude is not None and longitude is not None:
            if not -90 <= latitude <= 90:
                raise ValueError("Maps latitude must be between -90 and 90")
            if not -180 <= longitude <= 180:
                raise ValueError("Maps longitude must be between -180 and 180")
            tool.update(latitude=latitude, longitude=longitude)
        tools = [tool]
        input_text = prompt
    elif mode == "url":
        supplied_urls = list(urls or ())
        if not supplied_urls:
            raise ValueError("URL Context requires at least one URL")
        if len(supplied_urls) > MAX_URLS:
            raise ValueError(f"URL Context accepts at most {MAX_URLS} URLs")
        validated_urls = [_validate_url(url) for url in supplied_urls]
        url_list = "\n".join(f"- {url}" for url in validated_urls)
        input_text = f"{prompt}\n\nURLs to retrieve:\n{url_list}"
        tools = [{"type": "url_context"}]
    else:
        raise ValueError(f"Unsupported grounding mode: {mode}")

    return {
        "model": model,
        "input": input_text,
        "tools": tools,
        "store": False,
    }


def _summarize_tool_step(step: dict[str, Any]) -> dict[str, Any]:
    summary: dict[str, Any] = {"type": step.get("type")}
    for key in ("is_error", "search_type", "queries", "latitude", "longitude"):
        if key in step:
            summary[key] = step[key]

    arguments = step.get("arguments")
    if isinstance(arguments, dict):
        kept_arguments = {
            key: arguments[key]
            for key in ("queries", "latitude", "longitude", "urls")
            if key in arguments
        }
        if kept_arguments:
            summary["arguments"] = kept_arguments

    retrievals: list[dict[str, Any]] = []

    def collect(value: Any) -> None:
        if isinstance(value, dict):
            retrieval = {
                key: value[key]
                for key in (
                    "retrieved_url",
                    "url",
                    "status",
                    "url_retrieval_status",
                    "title",
                    "name",
                    "place_id",
                )
                if key in value and isinstance(value[key], (str, int, float, bool))
            }
            if retrieval and any(
                key in retrieval
                for key in ("retrieved_url", "url", "status", "url_retrieval_status")
            ):
                retrievals.append(retrieval)
            for child in value.values():
                collect(child)
        elif isinstance(value, list):
            for child in value:
                collect(child)

    collect(step.get("result"))
    if retrievals:
        summary["retrievals"] = retrievals
    return summary


def normalize_interaction(
    interaction: Any,
    *,
    mode: str,
    model: str,
) -> dict[str, Any]:
    """Return answer text, citations, tool evidence, and usage as JSON data."""
    raw = interaction.model_dump(mode="json", exclude_none=True)
    steps = raw.get("steps") or []
    citations: list[dict[str, Any]] = []
    tool_steps: list[dict[str, Any]] = []

    for step in steps:
        if not isinstance(step, dict):
            continue
        step_type = str(step.get("type", ""))
        if step_type == "model_output":
            for block in step.get("content") or []:
                if not isinstance(block, dict) or block.get("type") != "text":
                    continue
                citations.extend(
                    annotation
                    for annotation in block.get("annotations") or []
                    if isinstance(annotation, dict)
                )
        elif any(
            marker in step_type
            for marker in ("google_search", "google_maps", "url_context")
        ):
            tool_steps.append(_summarize_tool_step(step))

    return {
        "interaction_id": raw.get("id"),
        "mode": mode,
        "model": model,
        "text": interaction.output_text or "",
        "citations": citations,
        "tool_steps": tool_steps,
        "usage": raw.get("usage"),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Query Google GenAI with Search, Maps, or URL Context grounding."
    )
    subparsers = parser.add_subparsers(dest="mode", required=True)

    search = subparsers.add_parser("search", help="Ground with Google Search")
    search.add_argument("prompt")
    search.add_argument("--model", default=DEFAULT_MODEL)

    maps = subparsers.add_parser("maps", help="Ground with Google Maps")
    maps.add_argument("prompt")
    maps.add_argument("--latitude", type=float)
    maps.add_argument("--longitude", type=float)
    maps.add_argument("--model", default=DEFAULT_MODEL)

    url = subparsers.add_parser("url", help="Ground with specific public URLs")
    url.add_argument("prompt")
    url.add_argument("--url", action="append", required=True, dest="urls")
    url.add_argument("--model", default=DEFAULT_MODEL)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        request = build_interaction_request(
            mode=args.mode,
            prompt=args.prompt,
            model=args.model,
            urls=getattr(args, "urls", None),
            latitude=getattr(args, "latitude", None),
            longitude=getattr(args, "longitude", None),
        )
    except ValueError as exc:
        parser.error(str(exc))

    api_key = load_api_key()
    if not api_key:
        parser.error("GEMINI_API_KEY must be set in the environment")

    try:
        from google import genai

        with genai.Client(api_key=api_key) as client:
            interaction = client.interactions.create(**request)
    except Exception as exc:
        message = str(exc).replace(api_key, "[REDACTED]")
        print(f"Google GenAI request failed: {message}", file=sys.stderr)
        return 1

    result = normalize_interaction(
        interaction,
        mode=args.mode,
        model=args.model,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
