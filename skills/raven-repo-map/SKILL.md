---
name: raven-repo-map
description: "Build or refresh a map of an existing repo from Git history, dependencies and product areas. Wide Scan before brownfield work; report and evidence in the repo, no refactoring."
argument-hint: "[area] [history window]"
---

# Raven Repo Map

The Wide Scan procedure creates a map of the existing repo in `context/foundation/repo-map.md`. The map helps choose where to analyze further; it does not replace reading the code of a specific change. Talk to the user in their language; write the map in the user's language unless the project already uses another.

Read the [brownfield report contract](references/github-brownfield.md). Accept the repo, an optional area and history window, and an existing map report. For a new project map, write one local report per the contract. For a task limited to one module, do not impose mapping the whole system.

## Wide Scan

1. Establish repo_root, HEAD, dirty state, scope and history availability. Read instructions, manifests, entry points and the directory layout. Exclude vendored dependencies, generated files and secrets. Do not read the whole repo into context.
2. Gather cheap, reproducible CLI signals: history/churn, co-change of files, imports and dependencies, area authors. Use existing tools; record commands, date range, exclusions and the raw results needed for justification. With a shallow clone note the limitations; do not infer missing history. Static imports do not prove all runtime dependencies; co-change does not prove causation.
3. For a large repo, delegate independent read-only analyses of history, dependencies and authorship to subagents. Pass the identical scope/SHA; only the coordinating agent publishes. Without delegation run the same analyses sequentially and state the limitation. Optionally use available PR history, reverts and issues; their unavailability does not block a map of the local code.
4. Combine the results around product features and flows, not a list of folders. Check representative code for conclusions. Distinguish evidence, interpretation and unknown; frequent changes or the number of authors alone do not mean bad code. Authorship points to a possible person to talk to, not current responsibility or an employee assessment. Do not contact these people.
5. Save the map and evidence in the repo; Git keeps the history. On a refresh, give the differences from the previous version and re-verify changed areas; do not overwrite history.

## Result

Metadata per the contract, then:
- **TL;DR**: where to start and the most important constraints.
- **Terrain**: features, core/periphery, module boundaries and activity.
- **Real connections**: dependencies, co-change, layers, cycles with evidence.
- **Risk zones**: concrete scenarios and impact, not file rankings without interpretation.
- **Who to ask**: signals from history with a caveat about currency.
- **Day one**: 5–8 entry files, or fewer for a small scope, and the reason for the choice.
- **Limitations**: history window, tools, unknowns, cost of further verification.

Finish with a link to the map and a proposal of one Deep Focus area through `/raven-research`. Do not run research, planning, refactoring or changes to AGENTS.md/CLAUDE.md automatically.
