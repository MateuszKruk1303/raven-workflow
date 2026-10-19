# TDD for a fitting step

This internal procedure delivers agreed behavior red → green → refactor following [working on GitHub tasks](../../../../raven-workflow/references/git-workflow.md). It does not fake test-first for an already finished implementation.

1. Confirm the requirement, the existing runner and the source of Expected. Check that the behavior does not exist yet and can sensibly be driven by a test. Scaffolding, configuration and pure visual polish usually need a different check; test finished code normally with the raven-test steps (AC → test map, gaps).
2. **RED:** write the smallest test of the next behavior. Run it and confirm a concrete assertion failure, not a syntax/import/environment error. For a bugfix, Expected comes from the requirements; before-change may end with a documented EXPECTED_RED.
3. **GREEN:** write the minimal correct implementation. Do not bypass the assertion, hardcode fixtures or loosen requirements. Run the test and the relevant nearby regressions.
4. **REFACTOR:** simplify while green, preserving the contract and protection. Do not extend scope with future abstractions. Repeat for the next behavior until the step and its AC are met.
5. Check test effectiveness: expectations independent of the code, meaningful boundaries/errors, isolation and cleanup, the smallest effective layer. Avoid copying production calculations, over-mocking internals and snapshots as a substitute for business rules.
6. Run the step's required checks, deliberately stage your own code/tests/docs and make a logical commit within the requested scope. Do not force a commit per assertion or ask for approval of its message. Human acceptance does not follow from GREEN.

A small correction is within scope; a structural change goes back to a decision. Two unsuccessful attempts at the same problem stop the loop with a reproduction.
