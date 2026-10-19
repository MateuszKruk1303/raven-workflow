---
name: raven-research
description: "Investigate a question about the code or the feasibility of a change and write a local research.md with evidence. No task issues."
argument-hint: "[change-id] [question]"
disable-model-invocation: true
---

# Raven Research

Follow [working on GitHub tasks](../raven-workflow/references/git-workflow.md). Rebuild the local change and sources; a new report may create a folder without an issue/Project. Do not prepare a plan or implementation during research itself. Talk to the user in their language; write the report in the user's language unless the project already uses another.

## 1. Establish evidence and scope

- If the user mentions specific files (tickets, documents, JSON), read them first IN FULL (no limit/offset).
- **CRITICAL**: read those files yourself in the main context before launching any subtasks.

Read the PRD, relevant documentation, `context/foundation/architecture.md` and `context/foundation/lessons.md` if they exist, and treat lessons entries as already known patterns while shaping the research areas — recurring rules the team has accepted narrow what is worth re-investigating.

Keep a concise list of questions to answer, existing evidence, unresolved contradictions and next checks. A focused question may need a single local lookup; a comprehensive scope by default needs coverage of every agreed area, delegated in parallel (step 2).

Clarify only an ambiguity that would materially change the investigation, with the `AskUserQuestion` tool: short headers (max 12 characters) and concrete options with descriptions. An unambiguous research request needs no interview. User preferences are decisions; verify corrected factual claims against the given source.

## 2. Choose and run the investigation

Work locally for a single located fact or sequential reasoning. Comprehensive or multi-area research is delegated by default, not as an exception. Before the first delegation read [references/task-orchestration.md](references/task-orchestration.md) and use its bounded assignments, capability checks, failure fallback and evidence requirements. Launch subagents in parallel in one message only for independent gaps you can use right away (usually 1–2, at most 4), each for a different research dimension and each asked for `file:line` anchors — for example one finding every file related to X, one looking for earlier decisions about Y in documents and Git, one analyzing how subsystem Z works. Delegate less only when the scope really concerns one area or a gap depends on a prerequisite that is still unsettled. Use `Explore` subagents for locating code and `general-purpose` for analysis. Use task tracking when it helps coordinate several areas; otherwise a working list is enough.

The main agent owns the question and the synthesis. Subagents investigate read-only and return anchors, uncertainty and the actual coverage. Do not ask every worker to read the whole repository or the same large documents. Continue independent work while they run; check significant evidence as results arrive. Before the synthesis wait for the workers whose result the agreed questions need; a required result that did not finish is an explicit gap, not an answer. Cancel tasks that are no longer needed instead of waiting for them.

On a follow-up or scope correction, update the questions and the affected workers, keeping unrelated findings. A late answer based on superseded scope cannot override a new decision. Address the specific gap instead of restarting broad discovery.

## 3. Synthesize and close discovery

Combine the evidence into an answer to the original question. Distinguish observed behavior, inference and unsettled facts. Check decisive/contradictory code paths and callers; no search results alone does not prove absence. For a negative finding, cite the checked scope. Widen the scope only when it can settle an agreed question or a significant contradiction, not to fill an optional document section.

When recommendations are requested, keep the established requirements and reject options that weaken required guarantees. Distinguish settled decisions, real choices and missing evidence.

Finish when the agreed questions have sufficient evidence and significant conflicts are resolved. Close or cancel stale tasks. Still-missing required evidence means a partial finding with the gap and its impact named; do not claim completion and do not run equivalent searches endlessly. Do not run builds or tests unless their results answer a concrete research question and the host allows it.

## 4. Write and verify the research artifact

Save the report in `context/changes/<id>/research.md` following the [report format](references/research-document.md). Git history keeps earlier versions; a follow-up updates the findings and points to new evidence, it does not publish snapshots to comments. Do not change the execution plan or start implementation.

Before saving, apply the bounded-assertion and prose/JSON checks from that reference. Every quantitative or universal claim in prose needs an explicit condition, quantifier (exact set, count or "this inspected path") and a source anchor. Do not write "always", "never", "every", "only" or "on the first attempt" unless the named condition and the checked path really have that scope. Settle every historical claim separately: a document stale in its counts may still be correct in another field; a positive list is not an exclusive set unless the source says so.

When structured facts (JSON or a table) were requested, run a separate prose-versus-JSON pass before publishing either representation: for every leaf write the prose sentence that value would mean if true, confirm the same sentence is in the report, and confirm the JSON value matches the same source. JSON agreement does not certify the surrounding prose. If JSON was requested, prepare temporary report and facts files outside the repo just for the check; in the end keep the requested results in the local report. Run the bundled Node checker once:

```sh
node <skill-dir>/scripts/prose-json-check.mjs <research.md> <facts.json>
```

It only checks that every JSON number and boolean appears in the prose; it does not prove the quantifiers are right. Missing leaves or extra universal phrasing still need manual correction. If Node is unavailable, run the same checklist by hand.

Collect metadata from the real repository and the current clock once; do not invent a branch, commit, timestamp or researcher identity. Report metadata describes the inspected repo, the real HEAD/branch, dirty state, time and author. Mark missing data as unknown.

Review the final artifact once to check its answer, citations, gaps and metadata: re-read the saved content, or review the complete draft while presenting it unsaved in the conversation. In the same pass re-run the bounded-assertion and prose/JSON checklist (do not skip it because the first draft already existed):

- Tie a numeric example to its named inputs, units and conditions before deriving its result; distinguish totals from additional operations. Do not derive a value's meaning only from a field name or a familiar number.
- For every significant boolean, phrase the claim it would mean if true, then check that the inspected source supports that claim before assigning the value. A field describing whether a historical claim is supported answers the question of that support, not whether the historical document contains the claim.
- Correct historical claims individually. Some claims in a stale document may still be true: attach a current verdict to every significant historical claim instead of marking the whole paragraph stale. Trace significant consumers before calling a shared rule exclusive to one component. Prefer the exactly observed set or predicate over broader phrasing such as "all errors" or "every status in a class".

Reuse source anchors and calculations already verified. A mismatch triggers only a check and correction of the affected source/caller in every result, not a new discovery pass. If it remains unresolved, qualify the claim and consistently name the gap. By default this check needs no extra artifact, worker or test run.

Use concise validation output instead of printing it repeatedly. Run all applicable repository document checks once. Add commit permalinks only when the cited bytes match that commit and the remote certainly contains it; local uncommitted evidence keeps local file:line references. Do not build a permalink from a branch name.

If the host forbids writes, present the research and an explicit not-saved status in the conversation. Do not create a substitute file or delegate the write. Resume saving in a write-enabled mode in the same conversation after checking the current target file and the available context; do not restart a settled investigation or promise to recover missing conversation content.

## 5. Present findings and handle follow-ups

Start with the answer, the artifact location or not-saved state, decisive references and significant limitations. Research does not order planning or implementation. When handing off to planning, expose settled facts, their sources, covered contracts and unresolved product choices, so `raven-plan` builds on them in the same change without re-discovery. The report names the input requirements and their version/hash, the code SHA and dirty state, fit with architecture.md, options with a recommendation and trade-offs, risks, gaps and questions needing the user's decision. The researcher's recommendation is not an accepted decision. Do not write out implementation steps or per-file contracts; that is the result of later planning.

Record follow-up findings as an update of the Git-versioned file, with current metadata, a link to the previous version and a note of the conclusions superseded by new evidence. Reuse unchanged results; investigate only new or invalidated questions. Keep the scope, host permissions and any intermediate edits made by people.

## Brownfield: Deep Focus

When the question concerns an existing feature, read the current local raven-repo-map map if available. Check its scope/SHA and use its entry points and risk zones to narrow the work; do not treat the map as evidence of current behavior. A missing map does not block the research and does not automatically trigger mapping the whole repo.

Trace the specific flow from input through rules, data and side effects to the result. Check module boundaries, error paths, existing tests and decision history. For structural questions use available AST tools when they give better evidence than text matching. Document path:line, SHA, limitations and differences from the map.

The report in an existing change separates confirmed behavior, risks, unknowns and possible improvements by impact. Point to what is worth protecting before a refactor, without implementing tests or production changes. Updating the map and the plan remain separate requests. Do not force full DDD for a local fix.
