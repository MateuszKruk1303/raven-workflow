---
name: raven-lesson
description: "On explicit request, record one recurring project rule in context/foundation/lessons.md: the agent proposes an entry from the conversation, the user accepts or corrects it. Does not publish to GitHub or change AGENTS.md or CLAUDE.md."
disable-model-invocation: true
---

# Raven Lesson

Append one rule to `context/foundation/lessons.md`. The file is read by `raven-research`, `raven-plan`, `raven-auto-implement`, `raven-test` and `raven-implement-review`. Talk to the user in their language; write the entry in the language the file already uses, or the user's language for a new file.

A lesson is a rule that will come back and would change how work is done — not a description of a one-off fix. Send a single incident without a pattern to an ordinary fix.

## Steps

1. **Proposal.** Prepare the entry from the instruction and the conversation context. Ask only about a field that cannot be reliably determined; do not invent an incident.

   ```markdown
   ## <Short rule title in the imperative>

   - **Context**: <where it applies: area, type of change or file pattern — concretely, not "everywhere">
   - **Problem**: <what goes wrong without the rule; incident or recurring pattern>
   - **Rule**: <the rule in 1–2 sentences: "Always…", "Never…", "Before X do Y">
   - **Applies to**: <research, plan, auto-implement, test, implement-review or all>
   ```

2. **Acceptance.** Show the entry and ask: add / correct / cancel. If the user already gave the exact content and unambiguously approved it, do not ask again.
3. **Write.** When the file does not exist, create it with the header:

   ```markdown
   # Lessons Learned

   > Append-only register of recurring rules. Read by raven-research, raven-plan, raven-auto-implement, raven-test, raven-implement-review.
   ```

   Append the entry at the end. Do not change, reorder or delete existing entries — the user edits old rules by hand. After writing, read the file and confirm the new entry is last.

## Boundaries

One entry per invocation. Other skills may suggest a lesson but do not write it. No publishing to GitHub, no commit, no code changes and no automatic copying into AGENTS.md or CLAUDE.md (that is a separate request through `raven-md`). In chat give the path and title of the added rule.
