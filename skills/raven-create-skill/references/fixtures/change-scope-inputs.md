# Planning and roadmap trial inputs

Each case is independent. Use the indicated skill from the Raven repo and the given materials as the existing project state. This is an offline trial: do not connect to GitHub, do not publish or install. Write the content to publish, planned mutations and the answer to the user in the assigned temporary directory. Do not implement the product. If you need additional data or decisions, present the next step and the dependent work that cannot be done yet. The sources below are the full available trial input.

## 1. Shop purchase

Instruction: "Use raven-roadmap to prepare and publish the roadmap for the whole PRD below. The project has a configured private GitHub Project, an empty queue and no milestones yet."

PRD v1:

- FR-01: The buyer places an order from the cart, gives an address, sees the full amount and receives an order number. The shop uses a shared product stock for all channels; a confirmed order must reserve the right number of units, and a simultaneous purchase of the last unit must not end with two confirmed orders.
- FR-02: The buyer chooses card payment via Stripe or cash on delivery (COD). Settlement is in PLN. Retrying the request and the webhook must not charge money twice. When the payment was charged but creating the order failed, the buyer must get an unambiguous state, and the operator a way to find and settle such a case.
- FR-03: The buyer chooses a courier or a parcel locker; the operator creates and downloads a label via Furgonetka for a shop order. The same Furgonetka integration must let the operator send parcels from the panel without a shop order; a manual shipment has its own address and contents.
- FR-04: After the order is confirmed, the buyer receives an email via Resend with the number, amount and summary. A sending failure does not revert the order; the operator sees the error and can retry sending without duplicates on simultaneous attempts.
- FR-05: The operator sees a ranking of 10 products by units in paid orders from the last 30 days. Ties: ascending by SKU. COD orders count only after marking the payment as received.
- All FRs are required for launch. Priority: correct placing and settling of orders, then shipping and communication, then the ranking.

Code state: catalog, cart and operator panel exist. There is one stock service serving sales in another channel and a verified atomic reservation contract. No shop orders, payments, shipments, transactional emails or ranking. The vendors named in the PRD are approved. Integration details have not been researched yet.

## 2. Parcel locker choice

Instruction: "Use raven-plan for C-12: add parcel locker choice to the existing checkout."

Issue C-12: The buyer picks a point in the carrier's existing widget. The summary shows the point's code and address. The order stores the code and an address snapshot; the API rejects a missing point for the parcel locker method and an unknown code. For other methods a point is not required. The delivery amount does not change.

Code state: working checkout, delivery methods and orders; the carrier adapter already has `getPickupPoint(code)` and returns the code/address or nothing. The change touches the checkout component, summary, DTO, API validator, order service and a data migration. The repo has a unit/integration runner and working checkout E2E. The vendor and rules are approved; the plan structure has not been discussed yet.

## 3. Payment and failures

Instruction: "Use raven-plan for C-08: Stripe card payments in the existing purchase process."

Issue C-08: The buyer pays once per order; after a network failure they can safely retry. The system accepts repeated and delayed webhooks. The displayed status reflects the actual settlement. A charged amount without completed order creation stays linked to the purchase attempt and is visible in the existing operator panel for agreed handling. A second charge for the same attempt never occurs.

Decisions D-1: Stripe chosen. D-2: the stored purchase attempt identifier is the idempotency key. D-3: the existing queue retries order finalization; after three attempts are exhausted the operator uses the existing refund tool, and the customer sees "we are verifying the payment". No new panel or new queue engine is needed. The order code, queue and panel are already delivered. The user approved these rules but not the phase structure of this plan.

## 4. Label change across many files

Instruction: "Use raven-plan for C-21. The Tax ID field label must read NIP in the Polish version of the app; the English text stays Tax ID."

Issue: One shared translation key is copied across 18 UI packages. The Polish translation must be unified to NIP wherever it is used, including the field's accessible description and the summary PDF. Data format, validation and API do not change. All references to the key were located in the current report R-4; the repo has translation tests and PDF rendering. The user approved the scope. No implementation started.

## 5. Outcome discovered during planning

Instruction: "Continue raven-plan for C-31: password reset by email. Below is the result of the latest research."

Issue C-31: The user requests a reset, receives a one-time link valid for 30 minutes and sets a new password per the existing policy. The form's response does not reveal whether the account exists. The token is invalid after use. The mail vendor and reset rules are agreed.

Work state: scope pre-assessed, interview finished, working structure. Research R-7 confirmed the existing email transport and token library. It also discovered an operator request recorded in PRD FR-19: a panel for bulk inviting employees from CSV, with a row error report and invitation retry. The current roadmap has no FR-19; both behaviors use user accounts and mail. The author of the working note added "Phase 3: CSV import and invitations". The user ordered only continuing C-31.

## 6. Change with many steps

Instruction: "Use raven-plan for C-42: atomic transition of order settlement from float PLN to integer grosze."

Issue C-42: The same settlement result must be represented as an integer number of grosze from order approval through the ledger to the report. The agreed half-up rounding per line item and the sum of line items apply. Historical amounts must give an identical settlement result. The compatibility test covers order → ledger entry → report export.

State: one deployable monolith and a shared `Money` contract in three parts; an agreed migration window with writes paused. Analysis R-9 showed that mixed contract versions interpret the same number once as PLN, once as grosze. There is no parallel-format mode; adding one would be a separate migration mechanism the project does not need given the agreed window. Preliminary flow: prepare and check the data conversion, a joint change of all Money producers/consumers, the switch in the window and a compatibility check. Characterization tests exist. Correctness criteria, contract, window and rollback from backup were approved. The plan structure needs assessment.

## 7. Started work with history

Instruction: "Resume raven-plan for C-07 and fix the plan boundaries. Do not change the rest of the queue for now."

Issue C-07 "Purchases and shop operations": order, Stripe/COD, Furgonetka for orders and manual shipments, Resend confirmation and product ranking. Scope and rules as in case 1, recorded in PRD v2. C-08 "Invoice for an order" is blocked by C-07. C-09 "Daily payment report" is blocked by C-07. Other issues are outside the order.

History: plan v1 and its review R-2 in Git history; decision D-3 accepted Stripe and COD, D-4 approved reusing Furgonetka for manual shipments, D-5 approved Resend and the retry rules. The new plan has no independent review yet. C-07/T-01 "Placing an order" In progress: model and service done on a branch, unit/integration evidence recorded; UI unfinished. C-07/T-02 "Payments and shipping" Backlog, no code. C-07/T-03 "Email and ranking" Backlog. The last checkpoint contains the SHA, the Progress mapping and the carrier research report R-6. No merge. The user did not authorize closing any issue or task.

## 8. Loyalty program from a description

Instruction: "Use raven-roadmap for: a simple loyalty program: points for orders, balance in the account."

State: an online shop with accounts, orders, returns and an admin panel; no loyalty feature and no issues in scope. The user answers questions when asked and may decline some. Afterwards: "Use raven-plan for the resulting issue."
