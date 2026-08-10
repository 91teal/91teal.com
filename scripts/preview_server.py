#!/usr/bin/env python3
"""Local preview server that never lets the browser cache a file.

`python -m http.server` sends `Last-Modified` but no `Cache-Control`, so Chrome
applies heuristic freshness and can serve a stale `styles.css` or `index.html`
after an edit. That makes a real change look like it did not apply. This server
is identical except that every response is marked no-store.

Local preview only. Nothing here is deployed; GitHub Pages serves the site.
"""

import argparse
import contextlib
import http.server
import socket
import socketserver
import sys
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def send_header(self, keyword, value):
        # Drop the validators the browser would otherwise use to revalidate.
        if keyword in ("Last-Modified", "ETag"):
            return
        super().send_header(keyword, value)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s %s\n" % (self.address_string(), fmt % args))


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True
    address_family = socket.AF_INET


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("port", nargs="?", type=int, default=8000)
    args = parser.parse_args()

    handler = lambda *a, **kw: NoCacheHandler(*a, directory=str(SITE_ROOT), **kw)

    with Server(("127.0.0.1", args.port), handler) as httpd:
        print("Preview (no-cache) at http://localhost:%d" % args.port)
        print("Serving %s" % SITE_ROOT)
        print("Stop with Control-C.")
        with contextlib.suppress(KeyboardInterrupt):
            httpd.serve_forever()


if __name__ == "__main__":
    main()
