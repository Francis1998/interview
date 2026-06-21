#!/usr/bin/env python3
"""Verify that relative markdown links in topic files point to existing files."""

from __future__ import annotations

import re
import sys
from pathlib import Path

LINK_PATTERN = re.compile(r"\]\(\./([^)#]+)")


def check_links(root: Path) -> list[str]:
    """Return list of broken link error messages."""
    errors: list[str] = []
    md_files = [p for p in root.glob("*.md") if p.name not in ("CHANGELOG.md", "SECURITY.md")]

    for md_file in md_files:
        text = md_file.read_text(encoding="utf-8")
        for match in LINK_PATTERN.finditer(text):
            target = root / match.group(1)
            if not target.exists():
                errors.append(f"{md_file.name}: broken link -> ./{match.group(1)}")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    errors = check_links(root)
    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        return 1
    print(f"All internal links OK ({root})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
