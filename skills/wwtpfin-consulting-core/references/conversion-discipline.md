# Conversion discipline

These rules preserve faithful source extraction. They do not require every research proposal to have already appeared in an original financial model. Keep the source ledger intact; for authorized estimates and design choices, follow [modeling and iteration](modeling-iteration.md) and build a separately identified conditional working input. Never relabel those proposals as source facts or approved terms.

## Required conversion records

Read `schema --kind input`, `schema --kind project-evidence`, `docs/INTAKE.md`, and the minimal complete example before field mapping. Build these sections in `input/conversion-log.md` before writing canonical values:

1. A source register describing each file's project applicability, purpose, date, provider, issue or approval status and relevant scope.
2. A source-to-field ledger preserving the source wording or value, locator, normalized basis and unit, target contract field and evidence state.
3. A conflict ledger recording every comparable disagreement, the accepted or unresolved disposition, the reason, the excluded calculation or conclusion, and the decision owner.
4. A conversion-completeness matrix covering calculation fields and consulting facts.

Keep source tables in `supporting[]` with `table_role` and `{columns, rows}`. Do not turn them into prose or detached scalars.

## Meaning before mapping

Check the full sentence, table heading, footnote and time basis before assigning a number to a model field. Preserve qualifiers in the source-to-field ledger. In particular:

- A peak, rainy-season, design or permitted capacity is not an annual average operating volume. A forecast endpoint is not an observed annual series. Deriving a working series requires an explicit method and independently stated assumptions about utilization, seasonality, growth and allocation.
- A funded portion is not automatically the full funding requirement. When a source states an amount as a share, distinguish the total requirement, the portion included in the investment estimate and the remaining amount to finance. For initial working capital (铺底流动资金), preserve the stated percentage and account for the remainder or explicitly justify a different operating-capital estimate; do not silently treat the funded portion as all working capital.
- A whole-system amount is not automatically the incremental project's amount. Record the existing assets, shared services and incremental boundary before allocating quantities or costs.
- A stated asset life is not necessarily a project-calendar replacement date. Relate commissioning, operating age, renewal scope and the comparison end date; explain whether terminal value or a late renewal is included.
- A nominal amount, constant-price amount, tax-inclusive amount, accounting item and cash payment can share a label without sharing a calculation basis. Preserve both the original basis and the transformation.

A reverse calculation can identify a possible method, not uniquely recover missing terms. Before declaring a source contradiction, distinguish an explicit conflicting statement from a value that can be reproduced under several timing, allocation or financing assumptions. Keep the latter as a method uncertainty and test it when it could change the recommendation.

If the source does not establish the required meaning, leave that source fact unresolved. An authorized research estimate may fill a separately labeled working input, but its `basis` must explain the transformation, alternatives and uncertainty rather than repeat the source title. For material estimates or design choices, bind the affected canonical paths to `research.assumptions` and actual comparison scenarios. A narrow numerical range cannot cure a wrong interpretation of the source.

A future forecast is still an estimate even when quoted faithfully from a feasibility study. For a research assumption classified as `source_fact`, register `supporting.value.type: parameter_basis` with matching `kind`, current resolved `baseline_values`, `source_refs` and `method`; the source references must resolve to valid source snapshots. Preserve unit conversion and qualifiers, and bind all affected paths, including continuation when relevant. Typed estimate/design-choice packets must also match their current baseline and classification. These checks prevent label-only reclassification, not semantic mistakes; see [modeling and iteration](modeling-iteration.md) and package `docs/RESEARCH_REVIEW.md`.

For marginal water-volume pricing, preserve cumulative thresholds, units, multiplier basis and contractual status. A binding, source-backed rule may enter `revenue.marginal_volume_tiers`. In source reproduction, a proposed rule enters `source_declared_baseline` only when that source actually uses it; retain `proposed_not_binding`. A separately authorized proposed pricing arrangement may enter a conditional research candidate when its thresholds, multipliers, rationale and implementation conditions are explicit. The tiers are marginal: a higher-tier multiplier never applies retroactively to lower-tier volume.

## Source authority and conflict gate

Normalize scope, basis, unit and effective period before treating two statements as comparable. Decide authority per field, in this order:

1. applicability to the project and the same calculation or contractual basis;
2. formal authority and issue, approval or adoption status;
3. an internally consistent explicit statement over a derived value;
4. effective date when the earlier criteria do not decide the matter.

File type, source count, newest date or a convenient calculation result cannot decide authority by themselves. A clearly final or adopted source may displace a draft, superseded, legacy or out-of-scope source only when the status and scope are recorded in the conflict ledger. Otherwise keep the conflict unresolved: do not write either value as the accepted source fact, silently choose a reading, average the values or present either reading as an actionable measure. If the user has authorized research, separately identified interpretations can support conditional calculations when their meaning, methods and limits are explicit; they do not resolve the source conflict.

Use `unresolved`, `required_user_inputs`, `declared_basis`, or an applicable declaration channel for unresolved material. A statement in a supplied report remains source-backed at its actual evidence state even when the underlying primary attachment is absent; map the statement and register the missing primary evidence separately. Do not relabel the supplied statement as `source_absent`. To reproduce the supplied scheme, explicit terms and assumptions actually used by its calculation may enter `source_declared_baseline` with their original evidence state, including `proposed_not_binding`; this is reproduction, not confirmation, recommendation or proof of contractual effect.

For a policy used to adopt or exclude a measure, read the authoritative provision, its surrounding qualifications and its effective/repeal rules. Follow the attachment when the notice only announces it. Match percentages, ceilings, eligible expenditure, payment schedules and applicant conditions to that exact version. Preserve the permitted arrangements and exceptions alongside any prohibition; a restriction on one funding method or subject does not prohibit every arrangement with a similar name. A search excerpt, a recent title or an evidence ID containing a recent year does not establish the current rule.

Preserve the source snapshot and reproducible provision locator in the existing evidence record when a structural exclusion relies on it; use the installed evidence schema and `docs/RESEARCH_REVIEW.md`. An extracted passage must come from the saved source, not a model-written summary. Keep project eligibility uncertainty separate from missing policy text. A clearly labelled conditional amount may be researched while eligibility is pending, but an unread or superseded provision cannot close an alternative as prohibited. The CLI checks source binding and references; the agent remains responsible for authenticity, context and interpretation.

## Reproducible original excerpts

Save original source bytes under `sources/`. Use the source locator command first to inspect positions, then extract the required complete passage or table. Previews are truncated navigation aids, not source evidence.

```bash
wwtp-fin source-snapshot sources/report.docx --extractor docx-body/1
wwtp-fin source-snapshot sources/report.docx --extractor docx-body/1 --offset 100 --limit 100
wwtp-fin source-snapshot sources/report.docx --extractor docx-body/1 --selector '{"start":12,"end":15}' --evidence-dir input
wwtp-fin source-snapshot sources/policy.html --extractor html-element/1 --selector '{"tag":"table","index":0}' --evidence-dir input
```

Use the returned object unchanged as `supporting[].value`; add the actual source address, date and provider to the supporting record. Choose positions from the actual file, not these example numbers. The evidence schema permits adding the separately justified `scope`. Keep table headers and adjacent qualifying paragraphs with the excerpt; put your interpretation and estimation method in their own workpapers. Do not rewrite an excerpt to make its units or amounts match a preferred interpretation.

`artifact.path` is relative to the evidence file's directory, independent of the command's working directory. When copying evidence into a new run input directory before `build`, preserve that relationship or update its relative path before comparison/selection; never edit an already bound final input. The CLI archives referenced original bytes and re-extracts from the archive during verification. Archive verification does not search the old workspace or fetch the URL.

New complete research requires file binding for the external snapshots it uses. Genuine dialogue constraints used for the decision contract or explicitly fixed parameter leaves retain their dialogue status; they are not certified external documents and cannot be reused as proof of a policy or an external numerical reading. The initial extractors cover native DOCX body blocks and saved static UTF-8 HTML elements. Unsupported formats remain an explicit source-binding limitation: ordinary conditional calculations can continue, but do not claim that external source verification or the complete research gate has passed. Do not manufacture an HTML or Word "original" from your own summary to bypass this boundary.

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

Map source-backed facts at their actual evidence state. Put missing project evidence in `unresolved` or `required_user_inputs`; do not use placeholders or arbitrary enum values. An authorized conditional working input can also contain supported estimates and explicit proposals, with their method, uncertainty and intended use recorded separately. Run `build`, read every `warnings.json` item, then either correct the input or record the limitation. Run `verify-deliverable` before handoff.

The CLI determines financial calculation and structured semantics. The agent handles source interpretation, supported engineering estimates and authorized proposal design, while keeping those evidence categories distinct.

Do not treat the existence of a source locator, an evidence identifier, an `unverified` label or a successful calculation as proof of a sound estimate. Check the source semantics and estimation method first; then use common scenarios to examine the consequence of remaining uncertainty.

续期、付款方或实施条件的外部报价/条款同样须绑定原件；不能改成普通字符串跳过检查。若目前只能估算，让模型的 `evidence_refs` 引用已在 `research.assumptions` 登记并通过现有估算/设计选择审查的 `parameter_basis`，保留来源、方法及所需情景；不要把自写估算底稿伪称为外部原文。
