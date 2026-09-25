"""Bootstrap entrypoint for the CS2 Skin Price Sniper desktop app."""
from __future__ import annotations

import sys

from cs2_sniper.app import run_desktop


def main() -> int:
    try:
        return run_desktop(sys.argv[1:])
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())