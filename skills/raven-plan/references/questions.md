## Example AskUserQuestion probing

`AskUserQuestion` stands for the host's structured question tool; in another host use its equivalent, or ask in chat with the same options. At most 4 questions per round.

Used by `raven-roadmap` and `raven-issue-update` for business rules only, and by `raven-plan` for business gaps and technical decisions.

### Example: UI feature (pagination, raven-plan)

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

**Note**: The `(Recommended)` option comes first and is grounded in the source, the code and the context — the user always has the final say. Every option names its strength and its cost.

### Example: business rule (loyalty points)

Before the issue exists, ask in domain terms only — no code, package or field names. For loyalty points the minimum is: earning rate, what the base includes (shipping, tax, discount), when points are granted, what happens on cancellation and return, whether guests earn, multiple currencies, and how the balance is shown.

AskUserQuestion with questions:

- question: "A customer pays 200 PLN: 185 PLN of products after a 20 PLN discount plus 15 PLN shipping, VAT included. How many points do they earn?"
  header: "Points base"
  options:
  - label: "185 points: products after discount (Recommended)"
    description: "1 point per 1 PLN of products actually paid for, without shipping. · Strength: The customer earns for what they bought; discounts and shipping promotions do not distort the balance. · Cost: The customer sees a total of 200 PLN and may expect 200 points."
  - label: "200 points: whole amount paid"
    description: "1 point per 1 PLN of the order total. · Strength: The simplest rule to explain — the number matches the receipt. · Cost: Shipping earns points, so heavier or distant orders earn more for the same products."
  - label: "Net amount without VAT"
    description: "Points from the net product value. · Strength: Same points for the same products across markets with different VAT. · Cost: The number matches nothing the customer sees at checkout."
  multiSelect: false
- question: "The order is placed today and delivered in 5 days; the customer may still return it for 14 days. When do the points appear in their balance?"
  header: "Timing"
  options:
  - label: "After the return period ends (Recommended)"
    description: "Points shown as pending until then. · Strength: No clawback, no negative balance after a return. · Cost: The customer waits about three weeks for the reward."
  - label: "When the order is delivered"
    description: "· Strength: Quick reward after receiving the goods. · Cost: A return requires taking points back, possibly already spent."
  - label: "When the order is placed"
    description: "· Strength: Instant gratification at checkout. · Cost: Cancellations and returns both need clawback; the most exposed to abuse."
  multiSelect: false

### Example: technical decision (raven-plan only)

Ask only when there is a real alternative with a consequence the user cares about; settle minor details yourself. Ground the options in the code and the current docs.

AskUserQuestion with questions:

- question: "Loyalty points: should we install the official loyalty plugin or build our own module?"
  header: "Approach"
  options:
  - label: "Official plugin (Recommended)"
    description: "· Strength: Maintained upstream, admin screens included, the agreed rules fit its configuration. · Cost: The return-period timing needs a custom extension; plugin upgrades follow its release cycle."
  - label: "Own module"
    description: "· Strength: Full control of the rules and data, no third-party dependency. · Cost: About 2–3x more work, including the admin screens, and we maintain it ourselves."
  multiSelect: false

## Undefined terms in the request

Ranking, selection and state words carry a decision the request never makes. Run this pass before choosing interview questions.

| Term shape        | Examples                                      | Build the smallest case by                                                                             |
| ----------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Ordered selection | "top 5", "latest", "first", "winner", "best"  | placing equal comparison values across the cutoff — the Nth and the N+1th tie exactly                    |
| Counted set       | "all", "how many", "per user", "duplicate"    | varying the identity rule — are two rows sharing an email one item or two, and does a soft-deleted row count |
| State threshold   | "active", "overdue", "until the end of the month" | varying inclusivity and the governing clock — exactly at the boundary instant, in whose timezone      |

**Keep a working note, one line per term, before looking up the implementation**: the term, the case, and what the user would see differently under each reading. Then, in `raven-plan`, read the code and add its answer as one more line; in `raven-roadmap` and `raven-issue-update` skip this line. A tiebreak the code performs by id, insertion order or array position is not a decision anyone made, so it never closes the note. The note is scaffolding for the interview — it is not a plan section and nothing carries it into the plan.

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

When writing an issue (`raven-roadmap`, `raven-issue-update`), phrase the case in domain data — orders, customers, amounts, dates — without code names or a "current behaviour" taken from the implementation.

## Where the answer lands

- **In the issue** (`raven-roadmap`, `raven-issue-update`): a settled rule goes into "Business rules" and an observable AC. A rule the user declines to handle goes into "Out of scope" as consciously unhandled; one they cannot answer yet goes into "Open questions". Never into an assumption made by the agent.
- **In the plan** (`raven-plan`): a technical decision goes into "Decisions and approach", a technical criterion into "Verification". A settled business term becomes an AC or a named test, and the user is offered to record it in the issue through `raven-issue-update`; a declined term goes into "Scope" as consciously out of scope, so a reviewer sees a decision rather than an omission. Neither gets a section of its own.
