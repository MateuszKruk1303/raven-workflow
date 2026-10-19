# Raven browser tools

The tool choice is defined by [raven-browser](../../../../../raven-browser/SKILL.md). Read it before exploring: by default Playwright CLI in a separate named session; Brave/MCP only on an explicit instruction or the user's consent to use the browser. An E2E request alone or a missing CLI does not mean choosing MCP. Keep the user's explicit choice from the current task.

Use the project's or environment's existing CLI and check `--help`. If it is missing, use `npx -y @playwright/cli --help` and the same prefix in further commands, respecting the project's pinned version. Do not install a global CLI, additional skills or a workflow installer manifest. Test setup does not promise installing the tool in the agent's environment.

Use a dedicated session named for the project and task on every call; do not drive the global `default` session. No shell or ability to run the CLI means an exploration blocker, without an automatic switch to MCP. If a confirmed CLI limitation prevents a reliable test, apply the "Exceptional request for the personal browser" section of raven-browser: justify the need, describe the scope and wait for consent. When the user chose MCP, connect per raven-browser; a missing MCP is also reported as a blocker, not a passed check.

Durable tests use isolated accounts and data. Do not export a private session into the repo or CI. Specs are run by the project's runner, usually Playwright Test, per the lockfile and config. Installing the runner and its browser in the setup procedure is separate from choosing the exploration tool. An exploration result does not replace running the suite.

Logs, screenshots and storageState may contain sensitive data: keep them outside tracked code and publish only the needed redacted evidence. Close only the session started for this task.
