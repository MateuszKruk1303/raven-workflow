# Raven repository instructions

<!-- CLAUDE.md imports this file with `@AGENTS.md`. Keep shared instructions here. -->

Do not put paths specific to the user's machine in AGENTS.md or CLAUDE.md. Use repository-relative paths or describe how to find the location from the current environment.

Maintain Raven skills in this repository and install them in the projects that need them. Do not install or sync them globally without an explicit request from the user. Changing skills here does not update their copies in other projects.

Write skill files in English. Skills target Claude Code: use `/raven-<name>` invocation and Claude Code frontmatter (`disable-model-invocation` and similar). Project instructions support both formats: AGENTS.md holds the shared content and CLAUDE.md imports it with `@AGENTS.md`.
