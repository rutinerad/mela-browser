from __future__ import annotations

import sys

from mela_browser.server import serve
from mela_cli.discovery import discover_mela
from mela_cli.store import MelaStore


def main() -> int:
    discovery = discover_mela()
    if discovery.db_path is None or not discovery.db_path.exists():
        print("error: Could not find Mela database. Run 'mela doctor' for details.", file=sys.stderr)
        return 1

    store = MelaStore(db_path=discovery.db_path, support_dir=discovery.support_dir)
    try:
        serve(store)
    finally:
        store.close()
    return 0


sys.exit(main())
