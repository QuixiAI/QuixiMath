"""Flag TODO.md backlog items whose generator already exists.

A backlog line looks like:

    - [ ] Description of the item · `ClassNameGenerator` · grade · d4

When a generator ships, its line must be deleted. This tool scans
every unchecked line for the contract ClassName (the backticked name
sitting between two "·" separators) and fails if that class is
already registered in ALL_GENERATORS — the same honesty check that
`gen_opcode_legend.py --check` provides for OPCODES.md.

Usage: uv run python tools/check_backlog.py
Exits 1 and lists offenders if any are found.
"""
import os
import re
import sys

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

ITEM_RE = re.compile(r"·\s*`(\w+)`\s*·")


def scan(todo_text, registered):
    """Return contract ClassNames on unchecked lines that are already
    registered."""
    hits = []
    for line in todo_text.splitlines():
        if not line.lstrip().startswith("- [ ]"):
            continue
        m = ITEM_RE.search(line)
        if m and m.group(1) in registered:
            hits.append(m.group(1))
    return hits


def main():
    from dolphin_math_datagen import ALL_GENERATORS
    registered = {type(g).__name__ for g in ALL_GENERATORS}
    with open(os.path.join(repo_root, "TODO.md"),
              encoding="utf-8") as fh:
        todo = fh.read()
    hits = scan(todo, registered)
    if hits:
        print("Backlog items already registered in ALL_GENERATORS "
              "(delete their TODO.md lines):")
        for name in hits:
            print(f"  - {name}")
        return 1
    print("TODO.md backlog is clean: no shipped generator is still "
          "listed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
