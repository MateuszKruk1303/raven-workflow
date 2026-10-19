# Durable E2E: plan → generate → review → verify

Internal raven-test procedure, following [working on GitHub tasks](../../../../raven-workflow/references/git-workflow.md). Read the requirements (issue, plan), test-stack, the existing seed and only the references you need. Tests are created together with the implementation, and the normal review of the change covers them together with the code.

## Setup and risk selection

Establish the sources of Expected, the scope and the scenarios protected at browser level. Do not pick a new independent scope. Confirm the existing runner and that the app can be started. If something is missing, apply [e2e-setup](../e2e-setup/procedure.md) within the approved scope. Do not install a second runner and do not configure CI on the side.

Check existing coverage: reuse an effective test instead of duplicating assertions. If unit/integration protects the risk better, pick that layer. Skipping a new E2E needs real evidence of protection or a justification of inadequacy; do not tick an unrun test as PASS. Before-change tests may show EXPECTED_RED.

## Plan and generate

1. Read the [quality rules](references/e2e-quality-rules.md), [anti-patterns](references/e2e-anti-patterns.md) and the [seed pattern](references/seed-test-pattern.md). Every scenario has a requirement/risk source, conditions/data, steps and an independent Expected set before observing output.
2. For exploration apply [browser-driven generation](references/browser-driven-generation.md) and [tool wiring](../e2e-setup/references/tool-wiring.md). By default Playwright CLI in a separate session; switching to the personal browser needs an instruction or consent per raven-browser. First actually open and prepare the page, then read the accessibility snapshot. Do not invent locators. Use screenshots for visual risk, not as a substitute for the accessibility tree.
3. Start build/preview from the test-stack/webServer commands and port; `E2E_PORT` takes precedence when the config supports it. If required external APIs are mocked, apply [mocking](references/mocking-external-apis.md) before build/exploration. Do not perform real payments or messages based on access alone. Manage your own processes and stop them before the actual VERIFY if the runner manages the server.
4. Go through the happy path and a significant error/boundary. Generate tests based on observed roles/names, on the seed pattern and the [generation template](references/e2e-prompt-template.md). Prefer stable accessible locators; avoid arbitrary sleeps, brittle selectors, order dependence and shared mutable state. Use test accounts and unique records with cleanup.

## Review and verify

Check every generated test: does the assertion detect the failure, does Expected have an independent source, does the mock not bypass the contract under test, and do the locator and wait represent the user. The internal self-check during generation is not an independent final review. The normal reviewer of the change can cover this dimension without a separate agent.

Run new/changed tests and the relevant regressions with the right configuration. Do a repeated E2E run to check isolation and cleanup. Accidental success, retry without reproduction and runner errors do not prove correctness. When assertion effectiveness is uncertain, make a controlled perturbation in isolation and always restore the code. A syntax error is not evidence of protecting behavior.

Fix confirmed defects within the requested scope. Do not weaken a test for green. After two unsuccessful attempts at one problem, stop and report the reproduction and the blocker. A new requirement or uncovered action goes back to the user.

Give commands, results and gaps in chat. Commit tests with deliberate staging. Return the result to raven-test; E2E by itself does not publish a PR, merge or start further stages automatically.
