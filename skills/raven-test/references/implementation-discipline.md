# Execution discipline

- Derive expected behavior from the requirements; code and current output do not change the requirements.
- Learn the patterns before editing. Make the smallest fix that completes the required outcome, with its errors and guarantees. Do not add infrastructure in advance.
- Before an unprotected refactor, lock in the behavior. A bug test should expose the regression on the old version when practical. EXPECTED_RED before a bugfix is not a final PASS.
- Tests, configuration and documentation needed for things to work are part of the implementation. Pick the cheapest effective layer and reuse existing tests; do not mandatorily check the same behavior at unit + integration + E2E. Do not duplicate the implementation in assertions.
- Evidence refers to a concrete tree, configuration and environment. A change invalidates the affected result, not necessarily all independent checks.
- Preserve other people's changes/staging, stage deliberately and review the diff. Group commits logically.
- A small correction is within scope; a change of a significant decision or requirement goes back to the user. Distinguish a defect from a new wish.
- Two unsuccessful attempts at one problem stop the dependent loop. Report expected and observed behavior and the attempts.
- Do not weaken assertions or disable tests for a PASS. Update a stale test after an accepted behavior change only with a justification and Expected from the new requirement.
