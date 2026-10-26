# Parallel implementers

The goal is a shorter time to a working change. You decide whether to spawn implementers and how many; by default you spawn none.

## When

- One part, a few files, mostly one layer: work alone. A handoff costs more than it saves.
- A substantial backend and UI behind one contract: once the contract compiles, spawn one implementer for one side and do the other yourself.
- Several independent slices (the plan marks dependencies, or they touch disjoint modules and contracts): one implementer per independent slice. Dependent slices go in sequence.
- At most 3 implementers at once. Beyond that, reconciling the parts costs more than the time saved.

Before spawning, state the split in one sentence: who does which part, which files and why. If the work does not split cleanly, do it alone.

## Preconditions

- The contract the implementers depend on is written and compiles. Do not change it while they work. An implementer that needs a change stops and reports it; you decide.
- Each implementer owns a disjoint set of files named in its brief. Shared registration points (route or router indexes, registries, translation files, snapshots, lockfiles) are edited only by you, before or after.
- Work in the same working tree. A separate worktree needs its own dependency install, so use one only when ownership cannot be separated.

## Brief

Each implementer is a fresh subagent. Give it paths, not copied code:

- the instruction and the acceptance criteria of its part;
- the contract files;
- the files it owns;
- the project instructions that apply to them;
- the quick checks it may run;
- what to return: changed files, checks run with their results, deviations and open problems.

An implementer does not run git write commands (commit, add, stash, checkout, reset, restore), install dependencies, run repo-wide formatters, `--fix` linters or code generators, run migrations or seeds or write to the shared database or external services, start the dev server, use the browser, run test suites, update snapshots, edit files outside its ownership or spawn further agents. It may run quick checks scoped to its own files, such as a typecheck of its package or a single test file; a typecheck may show errors in files still in progress elsewhere, which it ignores.

## Integration

While an implementer works, do not edit its files. You own the result. Read each implementer's diff (`git diff -- <its files>`) instead of trusting its summary, and close the gaps between the parts. Then continue from "See it work" in the order of work. An implementer's report of a passing check is not a check.
