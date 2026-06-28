# Evaluate by Experiment

Evaluate by Experiment is a Codex/agent skill for judging contestable artifacts
with tests that can fail. It is for prompts, methods, skills, specs,
architecture proposals, and claims such as "this approach will work" where a
confident opinion would be cheap and weak.

The core move is:

```text
claim -> smallest failing world -> planted trap -> naive baseline -> instrument
```

A candidate passing one test is not enough by itself. The useful receipt is a
contrast: the naive baseline fails on the same case where the candidate passes,
and a concrete instrument scores the result.

## When To Use It

Use this skill when you need to know whether an arguable artifact is fit for
purpose:

- a methodology claims it finds real bugs
- a prompt claims it resists hallucination
- a refactor claims it preserves output
- an automation claims it is safe
- a proposal claims a design will work

Skip it for simple factual lookups and pure taste questions with no testable
claim.

## Test Plan Shape

Write the experiment plan before building the test:

```text
Claim under test : the method preserves output bytes
Smallest world   : one fixture with a load-bearing trailing newline
Planted trap     : a cleanup that strips the newline
Baseline         : naive strip-and-compare on the same fixture
Instrument       : byte-for-byte diff
Pass criterion   : candidate output matches and baseline differs
Coverage note    : does not test unrelated parser branches
```

Validate that a filled plan has the required deterministic shape:

```bash
cp assets/experiment-plan-template.txt /tmp/experiment-plan.txt
$EDITOR /tmp/experiment-plan.txt
python3 scripts/check_experiment_plan.py /tmp/experiment-plan.txt
```

The checker only validates shape. It does not prove the experiment is sufficient
or clever.

## How It Works With The Other Two Skills

These three skills are useful independently:

- `fable-method`: locks and verifies the engineering slice
- `evaluate-by-experiment`: tests a contestable claim with a falsifiable setup
- `recursive-self-improvement`: iterates one verified improvement in the
  current session without spawning child model sessions

They also compose well:

```text
Fable Method decides what must be true before work can ship.
Evaluate by Experiment tests the riskiest claim under that standard.
Recursive Self-Improvement uses the result to make one verified improvement,
then repeats only when another measurable target remains.
```

That composition keeps "looks better" separate from "proved better on this
case."

## Install

Clone this repository or copy it into a Codex/agent skill surface:

```bash
cp -a evaluate-by-experiment ~/.codex/skills/evaluate-by-experiment
```

For project-local agent surfaces, use the project convention, such as:

```text
.agents/skills/evaluate-by-experiment
```

## Verify

This package uses only Python standard-library checks:

```bash
python3 scripts/self_test.py
sha256sum -c SHA256SUMS.txt
```

`BUILD_RECEIPT.md` records the package-shape evidence and the limits of that
evidence.
