---
name: aligned-markdown-tables
description: Use when writing or editing README, doc, or plan files that contain pipe tables, or after a table has been edited by hand and left misaligned. Keeps raw Markdown tables column-aligned so they read cleanly without a renderer.
---

# Aligned Markdown Tables

Human-readable pipe tables: the `|` separators line up across rows in the raw
file, no renderer required.

## Rule

- Non-last columns are always padded to their widest cell.
- The last column is padded only when it is safe to do so:
  - **Outlier guard** — no single cell is much longer than the rest. Padded
    only when `widest ≤ 2 × second-widest` (a lone enormous cell would force
    every row to its width).
  - **Width cap** — the widest cell is ≤ 80 characters. A uniformly long prose
    column padded just adds trailing whitespace.

Otherwise the last column stays trimmed (single space before the closing `|`).
This keeps long `Contents`/`Purpose`-style columns from bloating the document.

## When to use

- You are adding or editing a pipe table in any Markdown file.
- A hand-edited table has drifted out of alignment.
- Verification step after touching a document with tables.

## Using the script

The pack ships `scripts/align-tables.py`. Run it on any Markdown file; code
fences and non-table lines are left untouched:

```bash
python3 scripts/align-tables.py path/to/file.md
```

The script is idempotent: running it on an already-aligned file is a no-op.

## Quick reference

| File | Contents |
|---|---|
| `SKILL.md` | This skill: the alignment rule and when it applies |
| `scripts/align-tables.py` | Pads pipe-table columns; skips code fences; idempotent |

## Common mistakes

- **Padding the last column blindly.** Short tables look fine, but a table
  whose last column holds one very long cell or uniformly long prose turns into
  a wall of trailing whitespace. Apply the two guards — if in doubt, leave the
  last column trimmed.
- **Hand-aligning after every edit.** Use the script instead; it recomputes
  widths from the current content.
- **Running on files with tables inside code fences.** Expected behavior is to
  skip them — the script already does.
