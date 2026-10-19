# Raven rules review

Assess an AI rules file on five axes and return concrete fixes. The file under review is any Markdown file with AI rules the user provides — this procedure does not assume AGENTS.md, CLAUDE.md or any specific tool.

Review mode does not edit the file. It produces a scorecard in chat. The user decides what to apply.

## Recognizing the input

The input should be a path to a single Markdown file (absolute, repository-relative or prefixed with `@`). Examples:

- `@AGENTS.md`
- `CLAUDE.md`
- `.cursor/rules/api.mdc`
- `src/api/AGENTS.md`
- `.github/copilot-instructions.md`

If no path was given, ask the user once for it. Do not guess.

If the path points to a directory, ask which file to review. If it points to several files (e.g. `**/AGENTS.md`), review them one at a time and report each scorecard separately — do not merge them. When CLAUDE.md only imports AGENTS.md (`@AGENTS.md`), review AGENTS.md together with the additions below the import.

If the file does not exist, stop and report the path. Do not invent content.

## What this procedure does NOT do

- It does not edit the rules file *unless the user explicitly approves the reordering proposed by Check 5*. The default output is read-only.
- It does not generate a full "fixed version" of the file. At most Check 5 may move/regroup sections; it never rewrites rule content.
- It does not assume the file's target tool. AGENTS.md, CLAUDE.md, `.mdc`, `.windsurfrules`, custom names — all are treated as an "AI rules file".
- It does not assess *the project's content* (architecture, technology choices, conventions). It assesses *the state of the rules artifact* — just as a code review assesses code, not the product.

## References in rules files

Suggest the reference form the file's format supports: a relative Markdown link in AGENTS.md and other formats (they have no imports), or a link or `@path` import in CLAUDE.md. Below, "reference" means whichever form fits.

## Procedure

1. Read the whole file (if it has > 2000 lines, read it in chunks to the end).
2. Compute Checks 1–4.
3. Run Check 5 as a separate multi-step flow (list 5a → comment 5b → proposal 5c → question to the user 5d → atomic-change reminder 5e). The reordering edit, if any, happens here and only after the user's explicit consent.
4. Print the scorecard in the exact format from "Output format". Include the summary of the reordering proposal and the user's decision in the Check 5 findings.
5. Stop. Do not propose further actions unless the user asks.

---

## The 5 checks

### Check 1 — Length

Count non-blank lines (ignore empty lines and lines that are only separators such as `---`).

| Lines | Verdict | Symbol |
|-------------|--------------|--------|
| 0–200 | fine | OK |
| 201–500 | caution | WARN |
| 501+ | warning | FAIL |

Why it matters: long rules files push the user's prompt out of the context window, and rules in the middle of the file get the model's weakest attention. Length is a signal that "you pay context for things the agent does not need in every session".

For WARN/FAIL suggest:
- Split area-specific rules into nested files closer to their code (e.g. `src/api/AGENTS.md`).
- Replace duplicated documentation with a reference to the canonical file.
- Remove rules not tied to a recurring agent failure mode.

### Check 2 — Direct code/config snippets

Scan for fenced code blocks (```` ``` ````) and inline code blocks longer than about 3 lines.

Flag every block that looks like:
- An example component, endpoint, migration, schema, query, bash script or test.
- A config file (`tsconfig.json`, `eslintrc`, `package.json`, `wrangler.toml`).
- A migration template or boilerplate that lives elsewhere in the repository.

Do **not** flag:
- Short structural snippets used to define a *format* the agent must produce (e.g. a 2–4 line error-shape template).
- Command examples (`npm run dev`, `git rebase`, etc.).
- Mermaid/diagram blocks.

For every flagged block suggest:
- Move the snippet into a real file in the repository.
- Replace the block with a one-line reference, e.g. `[user.service.ts](src/features/users/user.service.ts)` or, in CLAUDE.md, `@docs/api-errors.md`.
- Reason: after the next refactor the example will be wrong in two places; a reference cannot drift.

Verdict: OK at 0 flagged blocks · WARN at 1–2 · FAIL at 3+.

### Check 3 — Precise language

Scan for vague intents that cannot be checked against a diff. Common examples:

- "Write clean code"
- "Follow best practices"
- "Care about quality"
- "Be consistent"
- "Use modern patterns"
- "Keep it readable / maintainable / robust"
- "Handle errors properly"
- "Keep it simple"

For every match **always propose at least one concrete, testable alternative grounded in this project's context**. Never suggest "just delete it" — the author put the line there for a reason; your job is to translate the intent into something a reviewer can check against a diff.

To ground the suggestion, use signals from:
- the file under review (the tech stack it mentions, naming conventions defined elsewhere, hard rules in other sections),
- the paragraphs around the vague phrase (what did the author mean?),
- visible repository context, if available (`package.json`, `tsconfig.json`, framework choice, linter config, neighboring rules files).

If the project context genuinely suggests nothing specific, propose a reasonable default for the detected stack and mark it **(assumed)** so the author knows to confirm it.

Examples (note that each replacement uses project-specific names/conventions, not generic advice):

| Vague phrase in the file | Signal from project context | Grounded, testable replacement |
|-----------------------------------|--------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| "Write clean code" | TypeScript + ESLint mentioned in the same file | "Avoid `any`. Functions longer than 40 lines must be split. Run `pnpm lint` before committing." |
| "Handle errors properly" | Hard rule earlier: the API returns an `{ error: {...} }` shape | "API handlers must return `{ error: { code, message, context } }` per the shape defined above. Never throw raw errors." |
| "Be consistent with naming" | The file mentions `feature.handler.ts` elsewhere | "Use `<feature>.handler.ts` (matching existing handlers in `src/api/`), not `featureHandler.ts`." |
| "Use modern patterns" | The project uses native JS, no lodash in `package.json` | "Use native `Array`/`Object` methods. Do not add `lodash` — it is not in `package.json` and should stay that way." |
| "Keep components readable" | React + Tailwind project | "Components longer than 150 lines must be split. Conditional Tailwind classes go through `cn()` (assumed — confirm if a different helper is used)." |
| "Keep it simple" | Python FastAPI service | "Prefer one Pydantic model per request/response. No nested decorators beyond `@router.post` + `@requires_auth`." |

Verdict: OK at 0 vague phrases · WARN at 1–3 · FAIL at 4+.

### Check 4 — Redundant knowledge

You are the agent reviewing this file. Read it as you would at the start of a session, and after every paragraph ask one question:

> **"Did I already know this before opening the file?"**

If the answer is "yes, it is in my training data", "yes, it is documented framework default behavior" or "yes, the README/linter config already says it" — flag it. The author spent context on something you did not need explained.

While scanning, use these self-checks:

- **The "no surprise" test.** Could you produce this paragraph yourself on request, without access to the project? If yes — it is redundant.
- **The "framework default" test.** Does the rule repeat something the framework, linter config, type checker or test runner already enforces (e.g. "use TypeScript strict mode", "clean up in `useEffect`", "FastAPI uses Pydantic for validation", "PostgreSQL supports JSONB")? If yes — it is redundant. The tool will catch the violation; prose adds nothing.
- **The "definition" test.** Does the paragraph define a general engineering term ("what a service layer is", "what REST is", "what hooks are", "what JSX is", "what `Decimal` is")? You know them. Flag and delete.
- **The "could be a reference" test.** Does it duplicate `README.md`, `package.json` scripts, the project layout or `.eslintrc` settings? If yes — replace it with a reference to `README.md` / `package.json` / `.eslintrc.json`. A reference cannot drift; a copied prose description can.
- **The "tutorial smell" test.** If the paragraph sounds like a framework "Getting Started" page or a Medium article — it is tutorial content, not project knowledge. You read such material during training.

What is **not** redundant (do not flag):
- Project-specific conventions that contradict framework defaults ("we use `useEffect` only for side effects unrelated to data").
- Local traps and historical workarounds that cannot be inferred from the code ("the `events` table is partitioned monthly — bulk inserts into the wrong partition silently fail").
- Internal naming, layout or workflow rules ("postings live in `<verb>_<noun>.posting.ts`").
- Rules that look generic but are tied to a real incident (the file should mention the incident or point to a failure-mode register).

For every flagged paragraph suggest one of:
- **Delete it** — you already knew it.
- **Replace it with a reference** — to `README.md`, `tsconfig.json`, `docs/...`.
- **Keep it only if backed by an incident** — and if so, ask the author to add an inline incident note so the rule survives future audits.

Verdict: OK at 0 redundant paragraphs · WARN at 1–3 · FAIL at 4+.

### Check 5 — Rule ordering

Models pay more attention to the beginning and end of long contexts ("U-shaped attention"). Critical rules buried in the middle of a long file are statistically followed less often. This check has its own multi-step flow, because reordering a file is a significant edit, not a one-line fix.

Do the steps in order. The result of this check goes into the scorecard *and* may trigger an interactive reordering.

#### Step 5a — List the current top-level order

Go through the file and list its current top-level structure as a numbered list. Use H1/H2 headings (and H3 only when there are no H2s). Include each heading's line number. Do **not** comment yet — only present the existing structure.

Example:
```
Current order:
1. # Welcome to OrderFlow            (line 1)
2. ## About the team                 (line 5)
3. ## Project mission                (line 9)
4. ## Our values                     (line 13)
5. ## Tech stack                     (line 22)
6. ## Setup                          (line 36)
7. ## TypeScript                     (line 78)
...
N. ## Project conventions            (line 312)
```

If the file has no headings, say so explicitly: *"No section headings — file is one undifferentiated block."*

#### Step 5b — Comment on the order

Now annotate the list. For each section give a short tag and a one-line note. Use these tags:

- **CRITICAL** — a load-bearing rule (security, money, irreversibility, a project-specific "never do X").
- **USEFUL** — real project knowledge that helps but is not a trap.
- **INTRO** — welcome/mission/team — lowers signal density at the top.
- **REDUNDANT** — already flagged in Check 4 (framework defaults, definitions, tutorial content).
- **VAGUE** — already flagged in Check 3.
- **REFERENCE** — points to other files via links or imports (cheap, can be anywhere).

Then describe the structural problem in one paragraph. Examples:

> "Critical security and tenancy rules sit at the bottom (line 312). The first 35 lines are INTRO/values/marketing that the model weighs heavily but that contain no actionable rules. Risk: the agent reads all the ballast and skims the rules that really matter."

> "The order is roughly right — hard rules at the top, conventions in the middle, references at the bottom. One INTRO paragraph at line 1 could be shortened, but no structural reshuffle is needed."

#### Step 5c — Propose a better order (only if needed)

If the comment in 5b identified a real problem, propose a target order. Phrase it as *"sections moved to the top / kept / moved to the bottom / removed"*, not as a full rewrite of every line.

Example:
```
Proposed order:
1. ## Hard rules         (was: line 312)        ← moved to top
2. ## Project conventions (was: line 312, split) ← moved up
3. ## Tech stack          (was: line 22)         ← kept
4. ## Setup               (was: line 36)         ← kept, replace with a reference to README.md if possible
5. ## Failure modes       (new section)          ← collect incident-driven rules here
—   ## About the team / Mission / Values        ← remove (Check 3/4 already flagged these)
```

If 5b found no problem, skip 5c entirely — say *"Order is sound; no reshuffle needed."*

#### Step 5d — Ask before reordering

If 5c produced a proposal, **ask the user** with the `AskUserQuestion` tool before touching the file:

- **Yes, reorder the file now** — apply the proposed structure, keep all rule content, only move/regroup sections.
- **Move only critical rules to the top** — minimal change: lift hard rules to the top, leave the rest as is.
- **No, just leave the suggestion in the report** — do not edit the file; the scorecard stays.
- **Show me the diff first** — produce the reordered file as a preview block in chat, without writing.

If the user picks an edit option, apply it carefully: keep every byte of rule content (only headings and section blocks move) and make a single edit. If the user picks "leave the suggestion", do nothing.

#### Step 5e — Atomic-change reminder

Always end Check 5 with this reminder, whether or not a reordering happened:

> **Test each change in your next agent session.** Reordering a rules file is a context-shape change — its effect on agent behavior only shows up the next time you run a real task. Apply changes one at a time (atomic): reorder, then run a representative task, then move on to the next change (split, dedupe, rewrite). Bundling multiple structural changes makes it impossible to attribute a behavior shift to a specific edit.

#### Verdict

Judge the file before any reordering, based on the original order:

- **OK** — the top of the file is dense with CRITICAL/USEFUL rules, headings are clear, no INTRO ballast at the start.
- **WARN** — mixed structure: some critical rules at the top, others buried; or a non-trivial INTRO at the start.
- **FAIL** — critical rules appear after line 200, the file has no headings at all, or the first 30+ lines are pure INTRO/marketing.

---

## Output format

Print exactly this, in this order, in the user's language. Give `path:line` for every concrete finding so the user can jump straight to it.

```
# Rule Review — <path>

**Overall:** <one-line summary, e.g. "Healthy file with two redundancy hotspots" or "Long, vague, and bottom-heavy — needs a split">

## Scorecard

| # | Check                | Verdict | Score |
|---|----------------------|---------|-------|
| 1 | Length               | OK/WARN/FAIL | <n> non-blank lines |
| 2 | Direct snippets      | OK/WARN/FAIL | <n> flagged blocks |
| 3 | Precise language     | OK/WARN/FAIL | <n> vague phrases |
| 4 | Redundant knowledge  | OK/WARN/FAIL | <n> redundant rules |
| 5 | Rule ordering        | OK/WARN/FAIL | <one-line reason> |

## Findings

### 1. Length — <verdict>
- <n> non-blank lines.
- <suggestion if WARN/FAIL, otherwise omit>

### 2. Direct snippets — <verdict>
- `path:line-range` — <what kind of snippet> → suggest a reference to `<file>`.
- ...

### 3. Precise language — <verdict>
- `path:line` — "<vague phrase>" → "<testable rewrite>"
- ...

### 4. Redundant knowledge — <verdict>
- `path:line` — <what's redundant> → <delete | replace with a reference | keep only if backed by an incident>
- ...

### 5. Rule ordering — <verdict>
- <structural observation, e.g. "Critical security rule at line 287, intro fluff lines 1–42">
- <suggestion>

## Top 3 actions
1. <highest-leverage fix>
2. <second>
3. <third>
```

If a check is OK, still include it in the table but skip its findings (write `### N. <name> — OK` and one short line, nothing more).

"Top 3 actions" must be ordered by impact, not by check number. Pick from all five checks.

---

## Edge cases

- **File under 50 lines:** still run all five checks. Short files most often fail Check 3 (vagueness) and Check 4 (redundancy).
- **File consists mostly of references (links, `@…` imports) with few inline rules:** a good sign for Checks 2 and 4. Do not penalize it.
- **File is `.mdc` with frontmatter (`globs:`, `alwaysApply:`):** count rule lines after the frontmatter. The frontmatter itself is configuration, not rule content.
- **File is an unchanged stub generated by `/init`:** still review it. Check 4 (redundancy) will often dominate — a signal to clean it up.
- **The project has several rules files:** review the one provided. Mention neighboring files in "Top 3 actions" only when relevant (e.g. duplication between AGENTS.md and CLAUDE.md, or between a root AGENTS.md and a nested one).
