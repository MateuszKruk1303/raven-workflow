# The `thorough` level

Must prove: the feature works, does not break its area and withstands typical errors. Shared rules, "Checking it works" and the final message format stay as in [SKILL.md](../SKILL.md); this file replaces only the level steps.

## Steps

1. **Baseline.** Before editing, run the tests of the affected area to separate pre-existing failures from introduced ones.
2. **Implementation.**
3. **Static checks.** Lint and typecheck of all affected workspaces.
4. **Area tests.** All unit and e2e tests of the affected area (the module's whole spec, not just the new case); compare the result with the baseline.
5. **Checking it works** as a full end-to-end path from input to durable effect, plus at least one error scenario chosen for the change's risk.
6. **Independent review** (by default, one round — below).

Approximate verification overhead: ~25–45 min, including review with fixes ~10–20 min.

## Independent review

Launch one fresh subagent without the author's transcript. Give it the user's instruction, the given issue, plan or ticket content as read (key, link, description, AC), the diff from the base SHA to HEAD together with uncommitted changes and new files, and the check results. The reviewer works read-only and assesses requirement fit, correctness and test effectiveness, pointing to concrete locations.

Do one round of fixes for confirmed findings and rerun the checks that concern the fixed code. Do not hide findings you do not fix: they go into the final message with a justification. Do not run further review rounds. When the host cannot launch a fresh subagent, report the missing review in the final message as a limitation; the author's self-assessment is not a review.

## Additions to the final message

Besides the elements from SKILL.md, give:

- residual risks;
- the review result and what was done with it (fixed / rejected with justification);
- a negative step in the acceptance instructions: what should fail and what that looks like.
