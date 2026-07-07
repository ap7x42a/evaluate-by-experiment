---
name: evaluate-by-experiment
description: >-
  A procedure for evaluating or improving a contestable artifact — a methodology,
  prompt, skill, spec, architecture proposal, or "does this approach actually
  work" claim — by building a falsifiable test instead of offering an opinion.
  Use it whenever you're asked "is this any good / will this work / what do you
  think of this / can you improve this" about something whose quality is arguable
  and where a plausible-sounding answer would be cheap and unverifiable. Skip it
  for simple factual lookups or matters of pure taste with no testable claim.
compatibility: Requires Python 3.8+ for the optional plan checker.
metadata:
  self_test: "python3 scripts/self_test.py"
---

# Evaluate by Experiment

A procedure for judging or improving a contestable artifact by building a check that can fail — not by giving a confident read.

> **The one rule.** If you cannot construct a case where the claim would come out false, you have not evaluated it; you have described it. An opinion costs nothing and proves nothing. A failed naive baseline next to a passing candidate is evidence.

## The core move: reconstruct the smallest world where the claim can fail

Most evaluation is reading plus eloquence. This procedure replaces that with a minimal reproduction:

- Take the artifact's central claim: "this method finds the real bug," "this prompt will not hallucinate," "this refactor preserves output," or "this automation is safe."
- Build the smallest concrete scenario in which, if the claim were false, the test would say so. Usually this means planting a trap: a red-herring commit, a non-instance the extractor must refuse, a load-bearing quirk a cleanup would break, or a destructive edge case.
- Run a naive baseline against the same scenario. "The good approach passes" proves little by itself; "the naive approach fails on identical input where the method passes" is a receipt.
- Let an instrument score it: a diff, acceptance harness, status code, revert-and-rerun, stress invariant, or other failable check.

If you cannot make the claim fail under any setup, either the claim is trivial or you have not found the real test yet. Say which is true.

## Procedure

1. **Read the standard first.** Find the rubric, spec, contract, or intended job the artifact is supposed to satisfy. Judging from intuition silently imports your own taste as the standard.
2. **Separate craft from fitness.** A thing can be beautifully made and still not work. Say which you are assessing. The useful question is usually fitness: does it do the job under test?
3. **Name the observer problem honestly.** If you cannot run a clean trial — you are the author, you have prior knowledge, the sample is tiny, the effect is subjective — say so and pick the least-bad real instrument. Theater that cannot fail is worse than an acknowledged imperfect test.
4. **If the artifact bundles many claims, select before testing.** Rank claims by stakes × likelihood-of-being-false. Test the top one or two. Name skipped claims in the coverage note.
5. **Test each selected claim by experiment.** Use one trap, one naive baseline, and one scoring instrument per claim.
6. **Run diverse cases, then synthesize the pattern.** One passing test is an anecdote. Several cases that stress different facets can support a pattern.
7. **State coverage.** Say which claims are grounded by receipts and which remain carried/untested. Green checks for a few claims do not validate the whole artifact.
8. **Decide and execute when authorized.** If the ask includes acting on the finding, act and ground the decision in receipts plus the governing standard. Then test what you ship.

The loop runs backward too: if executing the fix changes the artifact, re-run tests the change could invalidate.

## Test-design template

Fill `assets/experiment-plan-template.txt` before building the test. When the plan
is written down, `scripts/check_experiment_plan.py path/to/plan.txt` can catch a
missing baseline, instrument, trap, criterion, or coverage note before you spend
time building the wrong receipt.

The checker is a guardrail for the deterministic plan shape only. It does not
judge whether the experiment is clever, sufficient, or worth running.

## Worked receipt

This skill is distilled from four applications (n=4; treat it as map, not universal proof until you re-ground it further):

1. A coding-methodology skill was evaluated by reconstructing minimal worlds with planted traps: a red-herring commit, a refactor with load-bearing output bytes, and an extraction task with a non-instance trap. The naive approaches failed while the instrumented approaches passed, grounding the finding that the skill was really a set of task-specific playbooks with a small shared spine.
2. A shadow-first automation claim was tested against filesystem mutation. A naive immediate-delete cleanup scored 0/3 and destroyed a human-authored file; the shadow-first version scored 3/3. That run also exposed a flaw in the procedure: the artifact bundled several claims, so claim-selection was added.
3. A named-entity-resolution claim was tested against a real registry. A plausible package name returned 404 while a verified alternative resolved, proving the value of checking before depending. It also confirmed a boundary: some claims, such as adversarial reasoning quality, do not have clean mechanical instruments and belong in coverage notes.
4. A proposed concurrency play was validated before being written down. A non-atomic counter passed single-threaded, failed under contention, and passed when guarded by a lock on the same invariant harness.

No step rests on "it looks right." The receipts do not prove the whole method universally; they prove the tested claims under the tested worlds.

## When NOT to use this

For a plain factual lookup or a matter of pure taste with no testable claim, answer directly. When a claim is genuinely untestable with the instruments available, say that plainly rather than staging a test that cannot actually fail.

## Relation to other methods

This shares DNA with engineering discipline — instruments over intuition, no consequential claim without a receipt — but aims at a different target: evaluating and improving an artifact or claim rather than shipping software. The additions that make it distinct are reading the governing standard first, using a naive-baseline contrast, naming the observer problem, and stating coverage.
