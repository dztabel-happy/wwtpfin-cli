# Modeling, research and selection

## Establish the question

Separate facts, mandatory rules, design proposals, negotiated arrangements and estimates. Record their meaning, locator, current values and uncertainty in the existing conversion/modeling workpaper; avoid duplicating the same explanations in several ledgers. A preliminary report provides a starting point, not a set of immutable choices.

Use a source-declared baseline when available, otherwise an authorized conditional baseline. Explain supported estimates and missing facts. Different defensible methods may produce different numbers from the same Word document; record the methods and calculate whether they alter the decision. Do not force agreement by choosing the same unsupported default.

Create the decision contract with `cost_goal`, primary and optional ordered secondary objectives, actual constraints and implementation conditions. Read `docs/COST_PERSPECTIVES.md` for the four perspectives. State the common service period and nominal/present-value basis. A return requirement applies when the transaction requires it; do not copy an example's FIRR into an unrelated mode. Tolerance is a substantive tradeoff, not just a display precision.

## Research and recompute

Develop measures through **source → applicability → action → linked inputs → impact, cost and responsibility**. Engineering quantities, quotations, policies and proposed contracts can all support a measure. A draft's assumption is neither a binding restriction nor permission to invent a cheaper value.

Read current primary sources where policy governs the proposal. Preserve exceptions and qualifications. For exclusions most likely to change the choice, examine the full provision or complete counterfactual. A local tax balance of zero does not establish zero overall benefit.

Use `intake.research_plan` and comparison `plan_review` for actual model exposures. The six broad directions remain discovery prompts; introduce new measures whenever supported. Do not manufacture a candidate per direction or interpret a passed finite comparison as an exhaustive search.

For an influential assumption, distinguish amount uncertainty from method uncertainty. Apply common conditions consistently to candidates; recompute dependent engineering quantities. A genuine alternate method needs its own values and rationale. Keep untested ideas and missing evidence visible in the recommendation.

The financial model supports four responses to a proposed mechanism:
- Express it directly and calculate it.
- First derive engineering/tax inputs in a sourced upstream workpaper.
- Calculate an explicitly limited approximation or bound.
- Identify a genuinely unrepresentable mechanism and explain which conclusion remains unavailable.

For each actual combination, recompute the whole model. Read `combination_coverage` for remaining registered measures and use `replaced_candidate_ids` when one measure replaces another. An unfavorable complete test can support non-adoption; a copied result, isolated delta or unrelated combination cannot. A failed eligibility condition requires a fully calculated fallback, not a savings estimate borrowed from another plan.

## Bind once, reuse correctly

The scheme set holds assumptions, directions, scenarios and combinations. The evidence packet holds `parameter_basis` with exact values, source references and methods. Unchanged candidate values inherit baseline evidence. Use `research.candidate_bases` for actual candidate/combination differences; candidates may share a packet when its values and applicable scenarios match.

Estimates bind uncertainty and derivation; source facts bind original text. A design proposal can state its intended values without claiming an approved quotation, but relabeling an estimate cannot replace its method. For exact field syntax read the current schemas and `docs/RESEARCH_REVIEW.md`; do not transcribe this reference into more case ledgers.

Candidate scenario binding checks common values and that candidate's own overrides/continuation. It need not repeat unrelated candidate changes. Pure display metadata is outside numerical research coverage; explicit source/value records and full input history still remain binding. `material` is optional and does not waive real input research.

## Pricing is a design choice

Choose the pricing question from the user's goal, required return, cash needs and transaction structure. A minimum cash balance, investor FIRR and starting tariff are different quantities. `solve` handles one declared variable/target; a mathematical solution is not commercial optimality.

For the specific supported method “one fee per candidate covering the registered cash-floor scenarios,” use `research.pricing_rules` and:

```bash
wwtp-fin price-schemes -p input/project.yaml --schemes comparisons/compare-0001/scheme-set.yaml -o comparisons/pricing-0001
```

Read `pricing-proposal.json`: declared bounds, protected and excluded scenarios, each boundary, rounded price and before/after changes. On success, `project.json` and `scheme-set.json` are new drafts. The command never edits originals, contracts or evidence. Adopt only the intended changes, revise affected basis records honestly, and compare with the current contract/evidence. The command preserves existing candidate/scenario settings and replays its generated fees; failure emits diagnostics without usable parameter drafts. It does not resolve investor-return or continuation pricing, or select a scheme.

## Explain and close

Read `decision-brief.md/json`, numerical constraints, `model_eligibility`, decision and research reviews. Separate numerical feasibility, support for a recommendation and implementation readiness. Missing policy eligibility evidence can permit a conditional study, but an actual model gap, contradictory policy setting or cumulative funding deficit is not fixed by a user's preference.

Use `ranking_explanation` to distinguish the strict primary-cost result from the result under the registered tolerance and secondary goals. Explain the accepted cost difference and basis for the rule; the diagnostic does not silently change the objective. A reversal under plausible assumptions requires a conditional branch, tie or evidence-gathering recommendation.

Stop when the advice is sufficiently supported within its disclosed scope, not after a fixed number of trials or a green check. Explain why recommended, why alternatives were not adopted, what changes the choice and what happens if a key condition fails. An open opportunity that could change the recommendation warrants further work.

## Selected result

After the user's actual choice, use `scripts/record-selection.py` to bind the exact comparison and candidate without copying hashes. Use `conditional_research` only when that is the confirmed scope; preserve pending conditions. Synthetic acceptance uses `purpose=workflow_validation`.

Follow `docs/CASE_WORKFLOW.md` for checkpoint → `finalize` → current-run verification. The unchanged-input selection transition keeps the current comparison attached. New facts, goals or methods instead return to research. `finalize` fully recomputes the selected inputs and generates bound original/continuation deliverables where applicable.

Use that exact run for the requested report; follow [workspace management](workspace.md) and [handoff](handoff.md). A report cannot strengthen a conditional numerical result into an approved implementation plan. For non-integer periods read `docs/TIME_AXIS.md`; for differing contract terms read the continuation interface in `docs/COST_PERSPECTIVES.md`.
