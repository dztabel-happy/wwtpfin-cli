# Downstream handoff

Run downstream tools when the user requests a rendered chart, Word report, or finished document. Select the explicitly confirmed final run according to [workspace management](workspace.md), or an exact baseline/conditional run requested for that purpose. Never use the newest trial as the final scheme. For a selected scheme require `verify-final-run RUN --case CASE`: it includes deliverable integrity, current selection and the `CURRENT.md` refresh. Reuse that successful check for the unchanged handoff; changes to inputs, sources or artifacts require a new check. Preserve `workflow_validation` labels on simulated acceptance.

Invoke `wwtpfin-consulting-report` first. It inventories the complete run and source materials, closes the full report-module ledger, records the disposition of every semantic block, table and figure, and writes the complete report manuscript. It then uses ChartKit for selected figures and DocxKit for the final Word file. Neither downstream product recalculates financial results.

Pass the bound `cost_goal`, `decision_review` and `research_review` with the selected result. The report must use the actual cost perspective and common service period, retain service/compliance/return requirements and distinguish evidence-backed conditions from implementation approval. A saving against a conditional baseline must retain that baseline's provenance; do not relabel it as the source document's own measured total.

Pass the existing modeling workpaper's derivation of decisive savings and unresolved judgments as well. Before drafting, reconcile the proposed explanation with the selected run's period ledgers and effective inputs. Verification binds the supplied model; it does not prove that a described measure was implemented in that model. If an effect, duration or related payment is missing, return to research and recompute instead of repairing only the prose.

For continuation service, hand over the original `deliverable/`, separate `continuation-deliverable/`, and `cost-comparison.json` / `cost-cashflows.csv` from the same verified run. The combined ledger keeps both contracts' actual timing and terminal obligations. Each contract's financial and cash results remain separate; continuation evidence and declared indicators must not be borrowed from the original contract. `verify-final-run` binds the whole set; a report-plan check of one package is not a substitute for that verification.

## ChartKit

Read `deliverable/figures/index.json`, the selected `figures/*.json` briefs, and their matching `figures/data/*.csv`. Invoke the installed `chartkit-report-figure` skill and write each ChartKit job under `exports/run-NNNN/charts/<figure-id>/`.

Render only figures that materially support the requested document. Do not render every brief by default. Require ChartKit's quality result to pass. Its handoff is the final image path plus caption text; do not bake figure numbers into the image.

## DocxKit

Use the organized manuscript from `wwtpfin-consulting-report`, not the raw deterministic `report.md`, as DocxKit's content input. Keep `document.json`, selected tables, source references and verified ChartKit assets as traceable supporting inputs. Invoke the installed `docxkit` skill under `exports/run-NNNN/docx/`.

DocxKit owns editable Word layout, numbering, captions, cross-references and page structure. Run its build gate and structural QA. Deliver only the returned `docx_path`; keep its editable source and diagnostics in the same run-bound export directory.

## Invariants

- Do not alter wwtp-fin values, calculation bases, evidence states, unresolved items, or decision wording during chart or document production.
- Do not promote a warning or missing input into a conclusion.
- Do not combine assets from different runs.
- Do not paste audit tables or raw machine column names into the report.
- Report the source run number with every export.
- Keep model scope beside each financial verdict, cost comparison and decisive table. Do not rely on a separate README or chat to correct the report's identity or the purpose of its headline conclusion. Correct underlying semantics through a new bound run when necessary; never edit a verified source package in place.
- For a funding schedule, use `cash_funding_summary` with `cash_funding_components`; retain the period, sources, uses, net movement and closing balance. Do not reconstruct only selected components such as operating income and loan payments. Compare every displayed amount with the verified source and check opening balance + sources - uses = closing balance. A separate reserve arrangement must reconcile to these balances and disclose its authorization; do not describe unrestricted cash as an established reserve.
- Preserve `financing_review` separately from ratio displays. A current-period cash shortfall may be a conditional cash-availability issue when cumulative cash closes, while a real cumulative deficit or an explicit covenant failure still blocks selection. Carry any original/continuation availability condition into the report; neither an arithmetic balance nor a `not_applicable` label certifies funds can be used for debt service. No independent restricted-cash or debt-service reserve account is modeled by this review.

Do not introduce code integration between the products. The agent coordinates files and preserves source references.
