# Technical UI check

Use only when the changed behavior needs a browser. The scope follows from the specific change; this file introduces no separate QA, critical path or report.

The isolated-session technique is described in [raven-browser](../../raven-browser/SKILL.md). Use it in the current agent, not in implementers, without a separate QA process. Prefer an existing test or an isolated Playwright session; the personal browser requires the user's authorization.

Check once, after integration, the observable effect of each changed behavior in one session. Sign in once per needed account and reuse the saved session state per [raven-browser](../../raven-browser/SKILL.md); do not sign in again before every check. When the change concerns a durable write, confirm it by reading back; for appearance, look at the render. The verified locators serve the flow test written afterwards. Do not introduce a new framework or fix an unrelated harness. Report a blocked test as a limitation; an alternative channel confirms only the behavior it actually observes.

Use your own test data and clean up only that. Do not perform real payments, shipments, publications or operations on other people's data without authorization; do not reset a shared database and do not reveal secrets.

## Recording

Only on the user's request (`--recording`). The recording is a run of the finished feature after the final checks, not of work in progress.

- In the Playwright CLI session run `video-start <file>`, `video-show-actions`, then one `video-chapter "AC<n>: <what>"` per acceptance criterion, and `video-stop`. Add `tracing-start`/`tracing-stop` when network or console behavior is part of a criterion. When the installed version lacks a command, check `--help` and use what it offers.
- Show the full user path for each criterion and end it with a reload or read-back, so the durable effect is visible, not just a success message.
- Look at the recording, or its frames at the chapter marks, before reporting. A recording that does not show the criterion working is a failed check.
- Save the files in a temporary directory, never in the repository. A trace keeps request headers, so record only test accounts.

The recording shows that the recorded paths work. It is not a review and not acceptance. When it could not be made, say so in the final message; the browser check itself keeps its own result.
