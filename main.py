#!/usr/bin/env python3
"""Copy the finished news image to the grader's output path.

Standard library only. The image bytes are read once and written unchanged,
so repeated runs produce identical output.
"""

import sys
from pathlib import Path


def main() -> int:
    source = Path(__file__).with_name("entry.png")
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/output/entry.png")
    data = source.read_bytes()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
