# Technical UI check

Use only when the changed behavior needs a browser. The scope follows from the specific change; this file introduces no separate QA, critical path or report.

The isolated-session technique is described in [raven-browser](../../raven-browser/SKILL.md). Use it in the current agent, without delegation or a separate QA process. Prefer an existing test or an isolated Playwright session; the personal browser requires the user's authorization.

Check the observable effect of the interaction. When the change concerns a durable write, confirm it by reading back; for appearance, look at the render. For retries you may keep a small temporary scenario with verified locators and assertions. Do not introduce a new framework or fix an unrelated harness. Report a blocked test as a limitation; an alternative channel confirms only the behavior it actually observes.

Use your own test data and clean up only that. Do not perform real payments, shipments, publications or operations on other people's data without authorization; do not reset a shared database and do not reveal secrets.
