## Example AskUserQuestion probing

`AskUserQuestion` stands for the host's structured question tool; in another host use its equivalent, or ask in chat with the same options.

### Example: UI feature (pagination)

AskUserQuestion with questions:

- question: "What should the user see while new items load?"
  header: "Loading UX"
  options:
  - label: "Skeleton screens (Recommended)"
    description: "Placeholder shapes matching item layout. · Strength: Perceived performance is 30-40% better — matches existing LoadingSkeleton component pattern. · Tradeoff: Requires a skeleton variant per item type; breaks if layout changes."
  - label: "Inline spinner"
    description: "Small spinner below existing content. · Strength: User keeps seeing current items, minimal UI work. · Tradeoff: Feels slower than skeleton — users see a generic spinner instead of content shape."
  - label: "Full-page spinner"
    description: "Replace content with spinner. · Strength: Simplest to implement — one component, no layout concerns. · Tradeoff: Blocks all interaction; feels broken on slow connections."
  multiSelect: false
- question: "How many items should this handle gracefully?"
  header: "Scale"
  options:
  - label: "Hundreds (Recommended)"
    description: "Standard offset pagination. · Strength: Simple, well-understood, works with existing SQL queries. · Tradeoff: Breaks down past ~5k items — acceptable given current data volumes."
  - label: "Thousands"
    description: "Cursor-based pagination + virtual scrolling. · Strength: Handles growth without performance cliff. · Tradeoff: 2-3x more implementation work; changes API contract."
  - label: "Tens of thousands"
    description: "Server-side filtering + virtual list + search. · Strength: Scales indefinitely. · Tradeoff: Significant complexity; requires search index and new API design."
  multiSelect: false

**Note**: Questions focus on **WHAT should happen** (requirements, behavior, outcomes) — NOT **HOW to implement it** (code patterns, specific tools); settle technical details yourself. The `(Recommended)` option comes first and is grounded in the code and context — the user always has the final say.

## Undefined terms in the request

Ranking, selection and state words carry a decision the request never makes. Run this pass before choosing interview questions.

| Term shape        | Examples                                      | Build the smallest case by                                                                             |
| ----------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Ordered selection | "top 5", "latest", "first", "winner", "best"  | placing equal comparison values across the cutoff — the Nth and the N+1th tie exactly                    |
| Counted set       | "all", "how many", "per user", "duplicate"    | varying the identity rule — are two rows sharing an email one item or two, and does a soft-deleted row count |
| State threshold   | "active", "overdue", "until the end of the month" | varying inclusivity and the governing clock — exactly at the boundary instant, in whose timezone      |

**Keep a working note, one line per term, before looking up the implementation**: the term, the case, and what the user would see differently under each reading. Then read the code and add its answer as one more line. A tiebreak the code performs by id, insertion order or array position is not a decision anyone made, so it never closes the note. The note is scaffolding for the interview — it is not a plan section and nothing carries it into the plan.

**Phrasing the question.** Put the concrete data in it, never the category name. When the code already implements one reading, mark that option `(current behaviour)` inside its label so the user sees a choice rather than a given. That option takes `(Recommended)` and first position only when its outcome is one the user would defend without mentioning the implementation; otherwise star the reading you would argue for and list the current behaviour below it.

AskUserQuestion with questions:

- question: "Orders 4 and 5 share the same `created_at` to the second. Which one does 'the latest order' mean?"
  header: "Tiebreak"
  options:
  - label: "Higher id wins (current behaviour) (Recommended)"
    description: "On equal timestamps the larger primary key is selected. · Strength: Deterministic and already what `getLatestOrder` returns, so no existing caller changes behaviour — and for an auto-increment key the higher id really is the later insert. · Tradeoff: Silently wrong for backfilled or imported rows, whose ids do not follow insertion time."
  - label: "Most recently updated wins"
    description: "Break the tie on `updated_at`, falling back to id when that is equal too. · Strength: Matches what users mean by 'latest' when they have just edited one of the two orders. · Tradeoff: An unrelated status edit reorders the pair, so the answer moves without a new order being placed."
  - label: "Return both and let the caller decide"
    description: "Surface the tie instead of resolving it. · Strength: No hidden rule — the ambiguity reaches whoever has the context to settle it. · Tradeoff: Every call site now handles a list where it expected one order; the dashboard and the invoice job both need a branch."
  multiSelect: false

**Where the answer lands.** A term the user settles becomes an AC in "Kryteria odbioru" or a named test in "Kroki"; a term the user declines to handle goes into "Zakres" as consciously out of scope, so a reviewer sees a decision rather than an omission. Neither gets a section of its own.
