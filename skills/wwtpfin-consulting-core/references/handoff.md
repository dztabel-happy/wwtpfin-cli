# Downstream handoff

Run downstream tools when the user requests a rendered chart, Word report, or finished document. Select the explicitly confirmed final run according to [workspace management](workspace.md), or an exact baseline/conditional run requested for that purpose. Never use the newest trial as the final scheme. For a selected scheme require both `verify-final-run` and `verify-deliverable`; preserve `workflow_validation` labels on simulated acceptance.

Invoke `wwtpfin-consulting-report` first. It inventories the complete run and source materials, closes the full report-module ledger, records the disposition of every semantic block, table and figure, and writes the complete report manuscript. It then uses ChartKit for selected figures and DocxKit for the final Word file. Neither downstream product recalculates financial results.

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

Do not introduce code integration between the products. The agent coordinates files and preserves source references.
