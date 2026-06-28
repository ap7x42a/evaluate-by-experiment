#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_experiment_plan


GOOD = """\
Claim under test : the method preserves output bytes
Smallest world   : one fixture with a load-bearing trailing newline
Planted trap     : a cleanup that strips the newline
Baseline         : naive strip-and-compare on the same fixture
Instrument       : byte-for-byte diff
Pass criterion   : candidate output matches and baseline differs
Coverage note    : does not test unrelated parser branches
"""


def assert_errors(text: str, expected: str) -> None:
    errors = "\n".join(check_experiment_plan.check_plan(text))
    assert expected in errors, errors


def main() -> int:
    assert check_experiment_plan.check_plan(GOOD) == []
    assert_errors(GOOD.replace("Baseline         : naive strip-and-compare on the same fixture", ""), "Baseline")
    assert_errors(GOOD.replace("Instrument       : byte-for-byte diff", "Instrument       : <diff>"), "Instrument")

    with tempfile.TemporaryDirectory() as temp:
        path = Path(temp) / "plan.txt"
        path.write_text(GOOD, encoding="utf-8")
        assert check_experiment_plan.main(["check_experiment_plan.py", str(path)]) == 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
