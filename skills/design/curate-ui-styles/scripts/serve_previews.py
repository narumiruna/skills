# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Serve one UI style interview's HTML previews on loopback."""

import argparse
from http import server as http_server
import pathlib
import re

HOST = "127.0.0.1"
PREVIEW_PATH = re.compile(r"/[a-z0-9]+(?:-[a-z0-9]+)*\.html")


def serve(preview_dir: pathlib.Path) -> None:
    """Print the local origin and serve direct HTML children until stopped."""

    class PreviewHandler(http_server.BaseHTTPRequestHandler):
        """Serve generated previews without directory listings or writes."""

        timeout = 5

        def do_GET(self) -> None:
            self._send_preview(send_body=True)

        def do_HEAD(self) -> None:
            self._send_preview(send_body=False)

        def _send_preview(self, *, send_body: bool) -> None:
            # Reject requests routed to loopback under a different hostname.
            if self.headers.get_all("Host") != [authority]:
                self.send_error(400)
                return

            request_path = self.path.partition("?")[0]
            if not PREVIEW_PATH.fullmatch(request_path):
                self.send_error(404)
                return

            preview = preview_dir / request_path[1:]
            try:
                if preview.is_symlink() or not preview.is_file():
                    self.send_error(404)
                    return
                content = preview.read_bytes()
            except OSError:
                self.send_error(404)
                return

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header(
                "Content-Security-Policy",
                "default-src 'none'; style-src 'unsafe-inline'; img-src data:; "
                "form-action 'none'; base-uri 'none'",
            )
            self.end_headers()
            if send_body:
                self.wfile.write(content)

    with http_server.ThreadingHTTPServer((HOST, 0), PreviewHandler) as server:
        authority = f"{HOST}:{server.server_port}"
        print(f"http://{authority}", flush=True)
        server.serve_forever()


def main() -> None:
    """Validate the preview directory and start the local server."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "preview_dir",
        type=pathlib.Path,
        help="directory containing the generated HTML previews for one interview",
    )
    parser.epilog = (
        "Open the printed URL plus /<preview-name>.html. Press Ctrl+C to stop."
    )
    args = parser.parse_args()
    try:
        preview_dir = args.preview_dir.resolve(strict=True)
        if not preview_dir.is_dir():
            parser.error("preview directory must be a directory")
    except (OSError, RuntimeError):
        parser.error(f"cannot resolve preview directory: {args.preview_dir}")
    try:
        serve(preview_dir)
    except KeyboardInterrupt:
        pass
    except OSError as error:
        parser.exit(1, f"Could not run the preview server: {error}\n")


if __name__ == "__main__":
    main()
