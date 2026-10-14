#!/usr/bin/env python
"""Inventory the pinned IGREFire source snapshot deterministically."""
import csv
import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sources" / "IGREFire"
OUTPUT = ROOT / "docs" / "phase-0" / "igrefire-source-file-inventory.csv"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    if not (SOURCE / ".git").exists():
        raise SystemExit(f"missing source snapshot: {SOURCE}")
    commit = subprocess.check_output(
        ["git", "-C", str(SOURCE), "rev-parse", "HEAD"], text=True
    ).strip()
    tracked = subprocess.check_output(
        ["git", "-C", str(SOURCE), "ls-files", "-z"],
    ).decode("utf-8").split("\0")
    rows = []
    for relative in sorted(filter(None, tracked)):
        item = SOURCE / relative
        rows.append([relative.replace("\\", "/"), item.stat().st_size, sha256(item), commit])
    with OUTPUT.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["relative_path", "size_bytes", "sha256", "source_commit"])
        writer.writerows(rows)
    print(f"wrote={OUTPUT}")
    print(f"commit={commit} files={len(rows)}")


if __name__ == "__main__":
    main()
