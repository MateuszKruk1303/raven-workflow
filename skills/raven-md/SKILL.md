---
name: raven-md
description: "Create, update or review AGENTS.md and CLAUDE.md (or another AI instructions file) from the project's real files, commands and conventions. AGENTS.md holds the shared content, CLAUDE.md imports it. Review gives a scorecard without rewriting rules. Does not initialize context folders or the stack."
argument-hint: "[directory | file | review <file>]"
---

# Raven MD

Two modes: **create/update** (default) and **review** — when the user asks for an assessment of an instructions file. In review mode follow the [review procedure](references/review.md): five checks (length, code/config snippets, precision, redundant knowledge, ordering), a scorecard with `path:line` and Top 3 actions in chat, with no edits to the file except an approved reordering. Do not copy private global instructions into the repo.

Talk to the user in their language. Keep the language of the existing document; for a new one use the user's language. Title of a new AGENTS.md: `# Repository Guidelines`.

## Both formats

Project instructions support AGENTS.md and CLAUDE.md together:

- **AGENTS.md** holds the shared content: project, commands, conventions, links. Other agents read it directly.
- **CLAUDE.md** next to it starts with the line `@AGENTS.md`, so Claude Code loads the same content. Below the import it may hold only Claude Code–specific additions (e.g. notes on skills, hooks or MCP); do not duplicate AGENTS.md content there.

Depending on the existing state:

- Neither file → create AGENTS.md and CLAUDE.md with the import.
- Only AGENTS.md → update it and add CLAUDE.md with the import.
- Only CLAUDE.md with content → keep it. Propose moving the shared content to AGENTS.md and leaving the import plus Claude-specific additions in CLAUDE.md; do the move after the user's consent, otherwise update CLAUDE.md in place.
- Both files → make sure CLAUDE.md imports AGENTS.md, and move content duplicated in CLAUDE.md into AGENTS.md without losing anything.

The same pair applies in subdirectories. In AGENTS.md use relative Markdown links (other agents do not resolve `@` imports); in CLAUDE.md `@path` imports are fine.

## Target and scope

- Without arguments use the root of the current repository (`git rev-parse --show-toplevel`); outside Git use the project directory the user names or the cwd.
- An explicit directory argument means `<directory>/AGENTS.md` + `<directory>/CLAUDE.md`. An explicit Markdown file path means exactly that file (and its pair, if it is AGENTS.md or CLAUDE.md). Resolve the path before writing; a symlink must not implicitly redirect the write to another project.
- Read the applicable parent instructions and the existing target files. Nested instruction files apply to their subtrees: do not carry their local prohibitions over to the whole repo without justification.
- The root document describes working in the repository. A subdirectory document describes local patterns and differences from the parent instructions.
- Invoking the skill authorizes creating or deliberately updating the documents. Do not add a routine draft-approval gate; ask about a significant contradiction the sources do not settle.

## Gather evidence

Use `rg --files` to learn the structure, skipping dependencies, build output and `.git`. Read only the sources needed for the guide:

1. README, existing agent instructions, the documentation index and architecture documents.
2. Manifests, scripts, the declared package manager, lockfile and workspace config. Do not assume the Raven stack just because of the skill's name.
3. Formatting, linting, type, test config and relevant CI workflows.
4. Representative source files and tests confirming structure, naming and module boundaries.
5. Short Git history, if it exists and commit conventions are needed. An observed habit is not automatically a mandatory rule.

Independent reads can run in parallel. Do not run installs, migrations, a server or the whole test battery just to document the available commands. Distinguish a command found in config from one actually run and passed. Do not read secret values; variable names from safe templates and links to instructions are enough to describe configuration.

For a subdirectory focus on neighboring files, local config and one good example of a new unit. Do not repeat the global monorepo map, commit history or all CI commands. Point to the parent guide with a real relative path.

## Raven context

If the project uses Raven, read the relevant documents in `context/foundation/` (PRD, architecture, tech-stack, test-stack, lessons). Record only the rules a future agent needs and links to canonical sources; do not copy skill instructions.

Do not create dependencies on personal paths such as `~/.claude/skills`. Do not impose agent models, process, test-editing bans or archive structure on a project that has not adopted them. Do not initialize `context/` while editing instructions; the right Raven stage creates the directories it needs.

## Create or update

**New file:** briefly describe the project, then the most important constraints and commands. Pick other sections to match the evidence:

- map of the code and module boundaries;
- dev/build/lint/typecheck/test commands with the directory to run them in and relevant conditions;
- local conventions not visible from framework defaults alone;
- required CI checks and testing rules, if they exist;
- commit and PR rules only if established;
- links to architecture, configuration and context documents.

**Existing file:** read it in full and check uncommitted changes. Keep correct content, style and manual decisions. Verify listed paths and commands against the current tree, including untracked files. The history of the last edit and the diff since that commit may help find changes, but do not replace checking the current configuration.

Make targeted fixes: keep current information, fix stale information, fill in significant gaps. Remove claims only after confirming they are stale. A rule not being enforced in code does not prove the user withdrew it. Surface a contradiction with manual decisions instead of silently replacing them. Rewrite the document from scratch only on explicit request or when it is empty; do not treat a short file as an empty template.

If the repo is empty, use the user's description and product documents. Record only known facts, without invented commands and folders. When even the project's goal is missing, ask for a short description before writing content.

## Checks before and after writing

- Every claim follows from a checked source or an explicit user decision. Do not add generic code quality advice.
- Aim for 200–400 words for the root AGENTS.md and 120–250 for a local one. Do not pad for the lower bound or drop significant rules for the upper one.
- The most important constraints and frequent commands are near the top. Skip empty sections, framework tutorials and large code blocks.
- Use relative links to existing files instead of copying documentation. Check links against the target directory. Do not link a file to itself.
- Commands use the real package manager and existing scripts; in a monorepo give the right directory or filter. Do not claim checks passed that were not run.
- Before writing, make sure the document has not changed since reading; if it has, re-read it and keep the new decisions. After writing, check content, links, the `@AGENTS.md` import in CLAUDE.md and the diff, if Git is available.

Edit only the target documents. Do not modify code, configuration, nested instructions or Raven documents on the side. Finish with the paths, word count and a short note on what was created or changed and which data remains unconfirmed. The effectiveness of instructions can be judged later on a real task; validating the document does not replace that observation.
