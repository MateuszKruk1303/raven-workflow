---
name: raven-browser
description: >-
  Verify the running application by default through Playwright CLI in a separate session. Switch to Brave via Playwright MCP, keeping its profile and sign-ins, only on the user's explicit instruction or consent to use the browser. Also use automatically when implementing or fixing web app functionality that needs browser verification: interactions, forms, navigation, sign-in, responsiveness and appearance. Do not use for documentation-only or backend-only changes without a browser scenario.
---

# Raven Browser

Talk to the user in their language.

## Choosing the mode

By default use **Playwright CLI** in a separate test session. Automatic UI verification, the instruction "check the app", invoking `raven-browser` alone or another skill's instruction to check in the browser do not mean choosing the personal browser.

Choose **Brave via MCP** only when the user clearly instructed to use the browser, e.g. "use the browser", "check in my Brave" or "use Brave MCP". Respect such a choice from earlier in the current task until the user changes it. An explicit choice of the CLI or another specific tool takes precedence over the general word "browser". Consent given to the agent's justified request described below also selects MCP mode. The skill invoking raven-browser passes on the user's actual choice; it does not create consent for MCP itself.

## Default: Playwright CLI

1. Check the available `playwright-cli --help` and the tool version. Use the project's or environment's existing installation; if it is missing, use `npx -y @playwright/cli --help` and the same prefix in further commands, without a global install. Respect the project's pinned version.
2. Use a separate named session for the project and task (`-s=<project-task>` on every call), without connecting the personal profile or a CDP endpoint. Open the app URL with `playwright-cli -s=<project-task> open <url>`; the default mode is headless.
3. Take a `snapshot`, read the needed parts of the file named in the output and run `click`, `fill`, `press` on refs from the current snapshot. Check other commands in `--help`. Screenshots also serve to judge appearance; a snapshot does not confirm layout.
4. For sign-in use a test account or an existing test `storageState` (after opening the session: `state-load <file>`). Do not copy cookies from the personal browser. Keep snapshots, logs and session state outside tracked code; check that `.playwright-cli/` is ignored before using it in a repo. Do not display secrets from files or command output.
5. When done, close only your own session (`playwright-cli -s=<project-task> close`), unless it is needed for further work. Do not close other tasks' sessions in bulk.

Report a missing CLI, shell or inability to start a session as a concrete blocker. Do not switch automatically to the personal Brave/MCP and do not run its setup script. The CLI is for exploration; durable tests are still run by the project's runner. If `raven-auto-implement` needs to replay UI interactions, it may use the technique below in the current agent, without delegation or separate QA.

### Replaying interactions in auto-implement

Under the [auto-implement UI guidance](../raven-auto-implement/references/browser-review.md), after getting to know the UI the implementer may write temporary Playwright scenarios and run them through the available CLI or an existing library/runner. The runner's separate browser context satisfies the isolated-session requirement here; do not connect it to the personal profile. For such a replay, do not require a snapshot before every action or re-exploring the page: use verified stable locators, assertions and explicit setup/cleanup. A selector failure requires re-observing the relevant part of the UI, not guessing or weakening Expected. The code/config stays temporary; the requested change defines the scope of checking. Do not automatically fix an unrelated pre-existing locator/harness; judge the limitation and alternative channel per that guidance.

The boundaries of the invoking skill take precedence over the regression-fix instruction in "Verifying implemented functionality": read-only skills (`raven-manual-qa`, `raven-implement-review`) report the defect and do not change the product or the durable suite. An explicit choice of the personal Brave/MCP still applies; do not carry that profile over to the runner.

### Exceptional request for the personal browser

If a concrete, confirmed CLI limitation prevents reliably checking the required scenario, you may ask the user to use their Brave via MCP. This applies e.g. to a problem reproducible only in the existing profile, a dependency on an extension or an SSO/device session that cannot be recreated on a test account, or a CLI failure that the available MCP lets you avoid. Do not assume MCP will solve the problem: state why it should help in this case.

First check the cause and a feasible CLI solution within the task (e.g. the right command, a test account or headed mode). Do not repeat unsuccessful attempts. A missing global install, convenience, slower operation or a single failed test does not justify switching to the personal session.

The request should name: the unverifiable scenario, the observed blocker and the attempts made, the reason for using the personal browser and the concrete scope (URL, account/role, planned actions). Cite this section of raven-browser as the basis of the request.

Wait for explicit consent before connecting, starting or configuring the personal browser. Do not ask again if the user already authorized the same scope. Until the decision you may continue independent checks; the blocked scenario stays BLOCKED/NOT VERIFIED. Refusal or no answer is not consent. Consent to use the browser does not extend the scope of data operations and does not automatically mean consent to restart a running session. A check in the personal session does not replace a repeatable run of durable E2E in the test environment.

Command documentation: [Playwright CLI](https://github.com/microsoft/playwright-cli).

## On explicit instruction or consent: Brave via MCP

Only in this mode work in the user's real Brave through the `brave` MCP server. The default connection is `http://127.0.0.1:9222`; a normal Brave launch from its icon does not open that port. Do not substitute a separate Chromium, an in-app browser or a new profile without agreement — the goal is the user's existing session.

### Brave/MCP environment requirements

This variant is built for macOS and Brave in `/Applications/Brave Browser.app`. It needs Python 3 and an available `brave` Playwright MCP server in Claude Code; MCP configuration belongs to the user's Claude Code setup and does not travel by copying skills. The Brave launch script supports macOS. On another system, report that this connection variant is unavailable and agree on how to access the browser, keeping the user's preference; do not silently replace their profile. Other Raven stages do not require macOS.

### Brave/MCP connection

1. Discover the available `brave` MCP tools and check the connection with `browser_tabs`. If it works, use it without a restart.
2. When the endpoint does not respond, run `python3 <skill-dir>/scripts/ensure_brave.py`. The script reuses an active endpoint or starts a closed Brave with port 9222.
3. If Brave is already running without the port, a restart is needed. If the user requested starting/restarting Brave for MCP, tell them and run the script with `--restart`. During automatic verification do not close an ongoing private session without existing authorization; ask only for the necessary restart. Never force quit and never discard unsaved forms. The script stops when the browser does not quit gracefully.
4. Verify `browser_tabs` again. A listening port or a written config alone does not mean a working MCP.

If the server is missing, check `claude mcp get brave`. Add the missing entry (mind write permissions outside the repository):

```sh
claude mcp add --scope user brave -- npx -y @playwright/mcp@latest --cdp-endpoint http://127.0.0.1:9222
```

Do not overwrite a different existing configuration without checking its purpose. If the entry exists but the tools are not available in the current session, tell the user to restart Claude Code (or reconnect via `/mcp`). Do not treat this as a page error.

After a failed start, check the process parameters and the script message. Do not repeat restarts in a loop. Do not copy cookies or the profile, do not read passwords and do not bypass profile restrictions by disabling protections. If the Brave version rejects debugging of the current profile, report that specific problem instead of promising to keep the session in a new profile.

## Verifying implemented functionality

After a change of behavior visible in the browser, use this skill without waiting for a separate "test it" instruction.

- Read the project's start command, port and routing; use an existing server or start the right one. In a multi-organization app, open the host and organization the task covers, not a random localhost.
- In CLI mode use your own named session; in Brave/MCP mode create your own test tab via `browser_tabs` with `action: new` and remember it. Keep the user's private tabs and do not navigate unrelated accounts.
- Take a snapshot before interacting. Use refs and selectors from the currently observed page. Perform navigation, clicks, forms and screenshots with the tool chosen per the rule above: CLI by default, MCP on the user's explicit instruction or consent.
- Go through the real scenario of the changed functionality. Check the result after the action, not just that a button is visible: e.g. a write, reading the data back, validation of wrong input or a URL change. Pick cases for the change's risk.
- For appearance changes look at a screenshot and check a relevant mobile and desktop size; when resizing a shared window, restore the previous size. For forms include the keyboard and visibility of messages.
- Check console errors and failed requests related to the scenario. Do not treat every warning from an external service as an app regression.
- Use test data. Being signed in to the personal profile is not consent to buy, send a message, publish or delete real data. The scope of actions follows from the user's task.
- If the invoking skill implements the change, fix a found regression and recheck the affected scenario; a read-only skill only reports it. Current verification via CLI or MCP does not replace the project's required tests.
- Save screenshots and logs in the project's existing artifacts directory or a temporary directory; do not add private data to the repository. Close only your own test tabs, unless they are needed to review the result. Leave the browser to the user.

In the summary give the checked scenario, the result and significant limitations. Do not claim passed verification if it was blocked by sign-in, a missing chosen tool, a server that does not work or missing data. Mention the use of the personal Brave briefly, without repeating the whole setup instruction.
