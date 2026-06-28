# Build Receipt

## Experiment Plan

Claim under test : the current `evaluate-by-experiment` bundle is a keepable, harnessed Codex skill rather than receipt-shaped shelfware
Smallest world   : the two allowed skill roots, the live GrimWatch prompt contract, and the docs/unit tests that require `.agents/skills/evaluate-by-experiment` plus `agents/openai.yaml`
Planted trap     : a stale receipt can claim a self-test or baseline while the package lacks runnable checks, a manifest, or a Codex discovery surface
Baseline         : the prose-only form would rely on inline template reconstruction and would not satisfy the create-harness static gate
Instrument       : create-harness audit, static harness validation, reviewed self-test execution, root-to-root diff, and targeted Codex skill-surface tests
Pass criterion   : both roots validate as harnessed, self-test exits 0, root copies stay byte-identical, and receipts avoid unverified authorship/provenance claims
Coverage note    : this proves package shape and the deterministic plan-shape checker; it does not prove that any future experiment plan is sufficient or well designed

## Verified

- Existing pre-harness baseline snapshot was observed at `/tmp/evaluate-by-experiment.skill.baseline`; it was not modified during this pass.
- The package contains a deterministic experiment-plan shape checker in `scripts/check_experiment_plan.py`.
- The package contains a self-test in `scripts/self_test.py` with positive and negative assertions.
- The fillable test-design template lives in `assets/experiment-plan-template.txt`.
- `agents/openai.yaml` exposes the skill as a Codex project-skill surface.

## Unverified

- The static harness gate does not prove the quality of any particular experiment plan.
- The `/tmp` baseline snapshot is not publisher provenance and was not re-created because the current write scope is limited to the two `evaluate-by-experiment` skill roots.
