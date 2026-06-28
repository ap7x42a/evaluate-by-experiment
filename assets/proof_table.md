# Proof Table

| Claim | Status | Receipt |
|---|---|---|
| `evaluate-by-experiment` is not a kill candidate on package shape. | verified | `python3 .agents/skills/create-harness/scripts/audit_skill.py .agents/skills/evaluate-by-experiment` reported `State: HARNESSED`; the same audit passed for `/home/apx/.codex/skills/evaluate-by-experiment`. |
| The harness has a failable deterministic check rather than only receipt files. | verified | `scripts/check_experiment_plan.py` checks required experiment-plan fields and returns nonzero for missing or placeholder fields; `scripts/self_test.py` asserts one positive case and two negative cases. |
| Codex has an installed user-skill copy. | verified | `/home/apx/.codex/skills/evaluate-by-experiment/SKILL.md` exists and contains `name: evaluate-by-experiment`. |
| GrimWatch Codex prompts point at the project skill surface. | verified | `src/ops/grimwatch-supervisor/prompt-builder.ts` tells Codex providers to invoke `.agents/skills/evaluate-by-experiment/SKILL.md`; `tests/unit/docs/evaluate-by-experiment-skill-sync.test.ts` requires `agents/openai.yaml`. |
| Static validation proves future experiment quality. | refuted | The skill and receipt both state that the checker validates only deterministic plan shape, not whether an experiment is clever, sufficient, or worth running. |
| The observed `/tmp` baseline snapshot proves publisher provenance. | refuted | The baseline was only observed as a pre-existing local snapshot and was not re-created in the current restricted write scope. |
