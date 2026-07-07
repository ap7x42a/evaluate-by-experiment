#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

FIELDS = (
    "Claim under test",
    "Smallest world",
    "Planted trap",
    "Baseline",
    "Instrument",
    "Pass criterion",
    "Coverage note",
)

FIELD_RE = re.compile(
    r"^\s*(" + "|".join(re.escape(field) for field in FIELDS) + r")\s*:\s*(.*?)\s*$",
    re.I,
)
PLACEHOLDER_RE = re.compile(r"^<[^>]+>$|^(?:tbd|todo|n/a|none)$", re.I)


def parse_fields(text: str) -> dict[str, str]:
    found: dict[str, str] = {}
    canonical = {field.lower(): field for field in FIELDS}
    for line in text.splitlines():
        match = FIELD_RE.match(line)
        if match:
            found[canonical[match.group(1).lower()]] = match.group(2).strip()
    return found


def check_plan(text: str) -> list[str]:
    found = parse_fields(text)
    errors: list[str] = []
    for field in FIELDS:
        value = found.get(field, "")
        if not value:
            errors.append(f"missing or empty field: {field}")
        elif PLACEHOLDER_RE.fullmatch(value):
            errors.append(f"placeholder field: {field}")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: check_experiment_plan.py PLAN", file=sys.stderr)
        return 2
    path = Path(argv[1])
    try:
        errors = check_plan(path.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"could not read {path}: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("experiment plan shape: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
