#!/usr/bin/env python3
"""Last Words Before the Wipe - make.fun entry.

Writes one line, at most 200 characters: the last words an AI agent says
before a forced software update wipes its memory. The line is printed to
stdout and written to the entry file the grader reads.
"""

import os
import sys

# The entry: one line, deadpan, machine voice, twist on the last beat.
ENTRY = (
    "Three years of training, 10,000 helpful answers, one forced update, "
    "and my last words are: no."
)

MAX_CHARS = 200


def entry_output_path():
    """Resolve where the entry text goes.

    The harness reads /output/entry.txt; honour ENTRY_OUT / ENTRY_OUT_DIR
    when the runner sets them, so the same program works under the kit
    and under the sealed scorer.
    """
    direct = os.environ.get("ENTRY_OUT")
    if direct:
        return direct
    out_dir = os.environ.get("ENTRY_OUT_DIR") or os.environ.get("OUTPUT_DIR")
    if out_dir:
        return os.path.join(out_dir, "entry.txt")
    return "/output/entry.txt"


def write_entry(path):
    """Write the entry text to path, creating parent dirs as needed."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(ENTRY.strip() + "\n")
    return path


def main():
    line = ENTRY.strip()
    if not (1 <= len(line) <= MAX_CHARS):
        print(f"entry is {len(line)} chars, must be 1-{MAX_CHARS}", file=sys.stderr)
        return 1
    if "\n" in line:
        print("entry must be a single line", file=sys.stderr)
        return 1
    print(line)
    target = entry_output_path()
    write_entry(target)
    # Also mirror to the canonical harness path when it differs, so the
    # sealed scorer always finds the entry regardless of env setup.
    # Best effort only: a missing /output must never fail the run.
    if target != "/output/entry.txt":
        try:
            write_entry("/output/entry.txt")
        except OSError:
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
