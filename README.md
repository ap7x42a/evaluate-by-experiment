# Evaluate By Experiment

Evaluate By Experiment is an agent skill for judging contestable artifacts by
building a test that can fail. It is for prompts, methods, specs, skills,
architecture proposals, safety claims, and "will this work?" assertions where a
well-written opinion would be cheap and weak.

The core move:

```text
claim -> smallest failing world -> planted trap -> naive baseline -> instrument
```

The important evidence is not "the candidate passed once". The useful receipt is
a contrast: the naive baseline fails on the same case where the candidate passes,
and a concrete instrument scores the result.

## Use It When

- A methodology claims it finds real bugs.
- A prompt claims it prevents hallucination or bad behavior.
- A refactor claims it preserves output.
- An automation claims it is safe.
- A design proposal claims it will work under realistic conditions.
- A skill or process doc "feels better" but needs proof that it changes behavior.

Skip it for plain factual lookups and pure taste judgments that have no
testable claim.

## What The Package Includes

- `SKILL.md` - the procedure and trigger guidance.
- `assets/experiment-plan-template.txt` - a fill-in plan for the claim, trap,
  baseline, instrument, criterion, and coverage note.
- `scripts/check_experiment_plan.py` - a deterministic shape checker for filled
  experiment plans.
- `scripts/self_test.py` - regression tests proving the checker rejects missing
  baselines, instruments, traps, criteria, and coverage notes.
- `BUILD_RECEIPT.md` and `SHA256SUMS.txt` - package receipt and drift manifest.

## Minimal Example

```text
Claim under test : the converter preserves output bytes
Smallest world   : one fixture with a load-bearing trailing newline
Planted trap     : a cleanup that strips the newline
Baseline         : naive strip-and-compare on the same fixture
Instrument       : byte-for-byte diff
Pass criterion   : candidate output matches and baseline differs
Coverage note    : does not test unrelated parser branches
```

The shape checker catches missing pieces before you build the wrong experiment:

```bash
cp assets/experiment-plan-template.txt /tmp/experiment-plan.txt
$EDITOR /tmp/experiment-plan.txt
python3 scripts/check_experiment_plan.py /tmp/experiment-plan.txt
```

The checker does not judge whether the experiment is sufficient. It only ensures
the plan has the minimum falsifiable shape.

## Install As An Agent Skill

```bash
git clone https://github.com/ap7x42a/evaluate-by-experiment.git
cp -a evaluate-by-experiment ~/.codex/skills/evaluate-by-experiment
```

For a project-local skill surface, copy the directory into the project location
your runtime uses, such as `.agents/skills/evaluate-by-experiment`.

## Verify The Package

```bash
python3 scripts/self_test.py
sha256sum -c SHA256SUMS.txt
```

## Limits

This skill does not make subjective work fully objective. It forces the agent to
name the claim, build a falsifiable scenario, compare against a naive baseline,
and state what the experiment did not cover.
