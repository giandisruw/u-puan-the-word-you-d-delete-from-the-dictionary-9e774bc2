#!/usr/bin/env python3
"""The Word You'd Delete From the Dictionary — make.fun entry.

Writes the winning one-word pick to /output/entry.txt. The word is
"irregardless" (12 characters, gate: 1 to 77), chosen by a local
pairwise tournament judged against the bounty's published judge brief
(see README.md for the tournament table).

Revision (v2): the first test run passed the gate, but it exposed two
gaps. First, v1's validate() checked length, blankness and single-line
only — it would have accepted a multi-word string, which the judge
brief's criterion 5 ("one word, spelled correctly, with nothing added
around it") forbids, so validate() now also requires exactly one word:
no whitespace anywhere and letters only. Second, v1's write was a
plain open/write with no proof the bytes landed, so write_entry()
now performs an atomic write (temp file + flush + fsync + os.replace
+ directory fsync) and verify_written() reads the file back from disk
and compares it byte-for-byte against the intended word before the
run reports success, so a truncated or corrupted entry can never be
submitted silently.
"""

import os

# Winning word (tournament winner — see README.md).
# Local tournament: 14 candidates, Swiss 4 rounds (28 games) + final,
# 58 judge calls on the Caffeine Inference router, every game played
# in both label orders. #2 led the Swiss at 3.05 and won the final
# against #3 ("literally") 0.8-0.2.
ENTRY = "irregardless"


def output_dir() -> str:
    """Grader output dir: MAKEFUN_OUTPUT_DIR when set, else /output."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def validate(word: str) -> str:
    """Check `word` against the kit's sealed-scorer gate, verbatim,
    plus the judge brief's exactness rule (criterion 5).

    competition.yaml: "/output/entry.txt is UTF-8 text of 1 to 77
    characters, not only white space". Single-word follows from the
    task itself (one word, with nothing else attached) and from
    criterion 5: one word, spelled correctly, nothing added around
    it — so the word must contain no whitespace at all and be
    letters only. Returns the word unchanged; raises ValueError on
    any gate violation.
    """
    if not isinstance(word, str):
        raise ValueError("entry must be a string")
    word.encode("utf-8")  # must be valid UTF-8
    if not 1 <= len(word) <= 77:
        raise ValueError(f"length {len(word)} outside 1-77")
    if not word.strip():
        raise ValueError("entry is only white space")
    if "\n" in word or "\r" in word:
        raise ValueError("entry must be one line")
    if any(ch.isspace() for ch in word):
        raise ValueError("entry must be exactly one word (no whitespace)")
    if not word.isalpha():
        raise ValueError("entry must be one word of letters only")
    return word


def write_entry(word: str, out_dir: str) -> str:
    """Atomically write `word` to entry.txt inside `out_dir`.

    Writes to a temp file in the same directory, flushes and fsyncs
    it, then renames it into place so the grader never observes a
    half-written entry, and fsyncs the directory so the rename itself
    is durable. Returns the final path.
    """
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    tmp = target + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8", newline="") as f:
            f.write(word)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, target)
        dir_fd = os.open(out_dir, os.O_DIRECTORY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    return target


def verify_written(path: str, expected: str) -> None:
    """Read-back gate: entry.txt on disk must match `expected` exactly.

    Compares both the raw bytes and the decoded text; any mismatch
    raises RuntimeError so a corrupted or truncated entry fails loudly
    instead of being submitted.
    """
    expected_bytes = expected.encode("utf-8")
    with open(path, "rb") as f:
        actual_bytes = f.read()
    if actual_bytes != expected_bytes:
        raise RuntimeError(
            f"verification failed: {path} is {len(actual_bytes)} bytes, "
            f"expected {len(expected_bytes)} bytes"
        )
    if actual_bytes.decode("utf-8") != expected:
        raise RuntimeError(f"verification failed: {path} content mismatch")


def main() -> None:
    word = validate(ENTRY)
    out_dir = output_dir()
    path = write_entry(word, out_dir)
    verify_written(path, word)
    print(f"Wrote {len(word)} characters to {path}")


if __name__ == "__main__":
    main()
