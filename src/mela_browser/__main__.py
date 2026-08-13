from __future__ import annotations

import argparse
import sys

from mela_browser.server import serve
from mela_cli.discovery import discover_mela
from mela_cli.store import MelaStore


def main() -> int:
    parser = argparse.ArgumentParser(description="Browse Mela recipes in a web browser.")
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        metavar="HOST",
        help="Address to listen on (default: 127.0.0.1). Use 0.0.0.0 to allow remote access, e.g. in a container.",
    )
    parser.add_argument("--port", type=int, default=8080, metavar="PORT", help="Port to listen on (default: 8080).")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode with auto-reload.")
    args = parser.parse_args()

    discovery = discover_mela()
    if discovery.db_path is None or not discovery.db_path.exists():
        print("error: Could not find Mela database. Run 'mela doctor' for details.", file=sys.stderr)
        return 1

    store = MelaStore(db_path=discovery.db_path, support_dir=discovery.support_dir)
    try:
        serve(store, host=args.host, port=args.port, debug=args.debug)
    finally:
        store.close()
    return 0


sys.exit(main())
