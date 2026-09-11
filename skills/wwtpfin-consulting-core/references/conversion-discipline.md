# Conversion discipline

## Required conversion records

Read `schema --kind input`, `schema --kind project-evidence`, `docs/INTAKE.md`, and the minimal complete example before field mapping. Build these sections in `input/conversion-log.md` before writing canonical values:

1. A source register describing each file's project applicability, purpose, date, provider, issue or approval status and relevant scope.
2. A source-to-field ledger preserving the source wording or value, locator, normalized basis and unit, target contract field and evidence state.
3. A conflict ledger recording every comparable disagreement, the accepted or unresolved disposition, the reason, the excluded calculation or conclusion, and the decision owner.
4. A conversion-completeness matrix covering calculation fields and consulting facts.

Keep source tables in `supporting[]` with `table_role` and `{columns, rows}`. Do not turn them into prose or detached scalars.

For marginal water-volume pricing, preserve cumulative thresholds, units, multiplier basis and contractual status. A binding, source-backed rule may enter `revenue.marginal_volume_tiers`. A proposed rule may enter only a `source_declared_baseline` when the supplied scheme's own calculation demonstrably applies it; retain `proposed_not_binding` and do not present it as a contract term. Proposed alternatives not used by that calculation remain unresolved. The tiers are marginal: a higher-tier multiplier never applies retroactively to lower-tier volume.

## Source authority and conflict gate

Normalize scope, basis, unit and effective period before treating two statements as comparable. Decide authority per field, in this order:

1. applicability to the project and the same calculation or contractual basis;
2. formal authority and issue, approval or adoption status;
3. an internally consistent explicit statement over a derived value;
4. effective date when the earlier criteria do not decide the matter.

File type, source count, newest date or a convenient calculation result cannot decide authority by themselves. A clearly final or adopted source may displace a draft, superseded, legacy or out-of-scope source only when the status and scope are recorded in the conflict ledger. Otherwise keep the conflict unresolved: do not write either value into a calculation field, silently choose a reading, average the values or turn either value into a candidate.

Use `unresolved`, `required_user_inputs`, `declared_basis`, or an applicable declaration channel for unresolved material. A statement in a supplied report remains source-backed at its actual evidence state even when the underlying primary attachment is absent; map the statement and register the missing primary evidence separately. Do not relabel the supplied statement as `source_absent`. To reproduce the supplied scheme, explicit terms and assumptions actually used by its calculation may enter `source_declared_baseline` with their original evidence state, including `proposed_not_binding`; this is reproduction, not confirmation, recommendation or proof of contractual effect.

## Spreadsheet formula and label gate

Inspect the label, formula, referenced cells, cached result, unit and surrounding table together. A formula-derived value is usable only when its required references are populated and accessible, it has no spreadsheet error, its dimensions are coherent, and it agrees with the applicable labels and source narrative.

When a label, formula, cached result or narrative conflicts, record each reading and keep the field unresolved unless a separate higher-authority source independently resolves it. Do not infer a financing term, grace period, repayment method or tranche structure solely from a column count, an initial zero payment, a repeated amount or formula shape. Unusable financing belongs in the financing declaration and evidence gaps, not in calculation loan fields. When the declaration says financing is unusable, omit `loan_tranches`, `operating_loan_tranches` and partial loan defaults rather than supplying an incomplete object.

## Conversion-completeness gate

Before `intake`, give every material source item exactly one disposition: `mapped`, `conflict`, `unresolved`, or `not_applicable` with a reason. The matrix must cover:

- calculation inputs and declared results for project scale and period, volume and revenue basis, tariff, investment, cost components and adjustment groups, financing and financing costs, tax, discount rate and financial targets;
- source material on risk allocation, performance supervision, termination and compensation, and transfer or handover.

Do not mark a category `source_absent` until all supplied sources, including narrative and tables, have been checked. Source-present facts must not be rendered as “no material” merely because their primary attachment is missing or they do not change a calculation. `intake` readiness, a successful build and a passing quality gate do not replace this completeness gate.

For `opex_items`, explicit annual series and formula paths have different input needs. With `annual_amounts_wan`, do not invent `base_wan`, `scales_with_volume` or `annual_growth_rate`; with a derived item, keep those formula fields neutral. `price_adj_group` is material only when tariff adjustment is active. `vat_scope` is material only when by-product revenue exists. The CLI contract is the final authority for these conditional requirements.

The adopted source scheme enters modeling as `source_declared_baseline`. It is neither a recommendation nor a candidate. Apply the candidate and user-confirmation rules in [modeling and iteration](modeling-iteration.md).

## Build and handoff

Map only source-backed facts. Put missing project evidence in `unresolved` or `required_user_inputs`; do not use placeholder numbers, arbitrary enum values or industry norms. Run `build`, read every `warnings.json` item, then either correct the input or record the limitation. Run `verify-deliverable` before handoff.

The CLI determines calculation and structured semantics. The agent determines only the transparent, source-backed mapping into the contract.
