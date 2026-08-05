#!/usr/bin/env python3
"""Align pipe-table columns in Markdown files.

Rewrites GFM pipe tables so the pipes line up across rows. Non-last columns
are always padded to the widest cell. The last column is padded only when
its cells are close in size; a last column with one cell much longer than
the others (or with a uniformly long prose column) is left unpadded so the
raw document does not bloat.

Usage:
    align-tables.py FILE [FILE ...]

Each file is edited in place. If a file's last column exceeds the guards, the
whole table keeps its alignment for the non-last columns and the last column
is emitted trimmed.
"""

import re
import sys

WIDTH_CAP = 80
OUTLIER_FACTOR = 2.0


def cell_width(cell: str) -> int:
    """Width of a cell: the longest line, stripped."""
    return max(len(line) for line in cell.split("\n"))


def split_row(line):
    """Split a table row line into cells."""
    line = line.strip()
    if not line.startswith("|"):
        return None
    inner = line[1:]
    if inner.endswith("|"):
        inner = inner[:-1]
    return [c.strip() for c in inner.split("|")]


def is_divider(cells):
    return all(re.fullmatch(r":?-+:?", c) for c in cells)


def build_row(cells, widths, align_last):
    """Render a data row; widths list of per-column padded widths.

    The last column is the value of align_last; if False it stays trimmed.
    """
    parts = []
    for i, cell in enumerate(cells):
        if i == len(cells) - 1 and not align_last:
            parts.append(cell)
        else:
            parts.append(cell.ljust(widths[i]))
    return "| " + " | ".join(parts) + " |"


def align_table(lines):
    """Return aligned lines for a stand-alone table (not inside a code fence)."""
    if len(lines) < 2:
        return lines
    rows = [split_row(l) for l in lines]
    if any(r is None for r in rows):
        return lines
    if not is_divider(rows[1]):
        return lines

    ncols = max(len(r) for r in rows)
    # Normalize row widths (tolerate ragged rows).
    norm = [r + [""] * (ncols - len(r)) for r in rows]

    col_widths = [0] * ncols
    for row in norm:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], cell_width(cell))

    # Decide whether the last column is padded. Skip the divider row, whose
    # synthetic dashes would otherwise skew the "second widest" signal.
    last_cells = [r[-1] for r in norm if not is_divider(r)]
    widths = sorted(cell_width(c) for c in last_cells)
    w = col_widths[-1]
    second = widths[-2] if len(widths) >= 2 else (widths[-1] if widths else 0)
    align_last = w <= WIDTH_CAP and w <= outlier_bound(w, second)

    rendered = [build_row(r, col_widths, align_last) + "\n" for r in norm]
    return rendered


def outlier_bound(widest, second):
    return second * OUTLIER_FACTOR if second else widest


def is_code_fence(line):
    return line.strip().startswith("```")


def align_file(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    out = []
    buffer = []
    in_fence = False

    def flush():
        nonlocal buffer
        if len(buffer) >= 2:
            out.extend(align_table(buffer))
        else:
            out.extend(buffer)
        buffer = []

    for line in text.splitlines(keepends=True):
        if is_code_fence(line):
            flush()
            out.append(line)
            in_fence = not in_fence
            continue
        if in_fence:
            out.append(line)
            continue
        if line.strip() == "":
            flush()
            out.append(line)
            continue
        if line.strip().startswith("|"):
            buffer.append(line)
        else:
            flush()
            out.append(line)
    flush()

    result = "".join(out)
    if result != text:
        with open(path, "w", encoding="utf-8") as f:
            f.write(result)
        return True
    return False


def main():
    if not sys.argv[1:]:
        print("usage: align-tables.py FILE [FILE ...]", file=sys.stderr)
        return 1
    changed = 0
    for path in sys.argv[1:]:
        if align_file(path):
            changed += 1
            print(f"aligned {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
