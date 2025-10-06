#!/usr/bin/env python3
"""Lightweight HTTP checker utility.

This module exposes a ``main`` function that can be used as a script to
perform a minimal HTTP request using sockets.  The previous version of this
file was written for Python 2 and relied on ``raw_input``/``input`` while also
hard-coding the request payload.  The new implementation embraces Python 3,
offers a small command line interface and provides better error handling so the
tool behaves predictably when the target host is unreachable.
"""

from __future__ import annotations

import argparse
import socket
from dataclasses import dataclass
from typing import Optional

__all__ = ["HttpRequest", "perform_request", "main", "__version__"]
__version__ = "1.0.0"


@dataclass
class HttpRequest:
    """Representation of a minimal HTTP request.

    Attributes
    ----------
    host:
        Hostname or IP address that will receive the request.
    port:
        TCP port where the HTTP service listens.
    path:
        Resource path that will be requested.  Defaults to ``"/"``.
    method:
        HTTP method to be used when talking to the server.  Defaults to
        ``"GET"``.
    headers:
        Additional headers to be appended to the request.
    """

    host: str
    port: int
    path: str = "/"
    method: str = "GET"
    headers: Optional[list[str]] = None

    def to_bytes(self) -> bytes:
        """Serialize the request into a raw HTTP payload."""

        request_line = f"{self.method} {self.path} HTTP/1.1\r\n"
        base_headers = [f"Host: {self.host}", "Connection: close"]
        serialized_headers = "\r\n".join(base_headers + (self.headers or []))
        payload = f"{request_line}{serialized_headers}\r\n\r\n"
        return payload.encode("ascii", errors="ignore")


def perform_request(request: HttpRequest, timeout: float = 5.0) -> str:
    """Send the request and return the raw HTTP response."""

    with socket.create_connection((request.host, request.port), timeout) as sock:
        sock.sendall(request.to_bytes())
        chunks: list[bytes] = []
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            chunks.append(chunk)
    return b"".join(chunks).decode("utf-8", errors="replace")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Minimal HTTP response checker")
    parser.add_argument("host", help="Target host or IP address")
    parser.add_argument(
        "-p", "--port", default=80, type=int, help="Port where the server listens"
    )
    parser.add_argument(
        "--path", default="/", help="Resource path to request (default: '/')"
    )
    parser.add_argument(
        "-X", "--method", default="GET", help="HTTP method to use (default: GET)"
    )
    parser.add_argument(
        "-H",
        "--header",
        action="append",
        default=[],
        metavar="HEADER",
        help="Additional header lines to send (can be repeated)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Socket timeout in seconds (default: 5)",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"httpcheck {__version__}",
        help="Show program's version number and exit",
    )
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    request = HttpRequest(
        host=args.host,
        port=args.port,
        path=args.path,
        method=args.method.upper(),
        headers=args.header or None,
    )

    try:
        response = perform_request(request, timeout=args.timeout)
    except (socket.timeout, ConnectionError, OSError) as exc:  # pragma: no cover - best effort
        parser.error(f"Failed to connect to {request.host}:{request.port} -> {exc}")
    else:
        print(response)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
