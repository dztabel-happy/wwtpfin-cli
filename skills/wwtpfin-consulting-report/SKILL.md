---
name: wwtpfin-consulting-report
description: >-
  Build a complete Chinese wastewater-project consulting report from a verified
  wwtp-fin run and source-backed supplemental materials, then export an editable
  Word file through DocxKit. Use after wwtp-fin calculation when the user requests
  a 咨询报告、特许经营方案、Word成果文件 or complete report manuscript.
---

# wwtp-fin Complete Consulting Report

Turn the verified semantic package and user materials into a complete consulting deliverable. The financial core is the analytical spine, not the whole report. Do not recalculate, copy source prose, dump artifacts mechanically, or treat the raw deterministic `report.md` as the final manuscript.

## Bind the report source

Use the exact run and reporting purpose requested. Initialize `report-plan.json` with the bundled helper: it invokes the CLI to verify the source and case currentness. Use `historical` for an old result, and preserve baseline, conditional-study and synthetic notices. For a selected scheme, read its selection context, decision brief and outstanding conditions; a complete manuscript cannot upgrade its implementation status.

Put the manuscript under `exports/run-NNNN/report/` and scripts under its sibling `scripts/`; use the core skill's workspace reference for input changes and currentness. Read the user goal and project sources to design the argument. Supported modules enter the draft; missing material belongs in the routing ledger and one consolidated request section.

For continuation service, read the common-period cost ledger and both separately calculated deliverables. Preserve each contract's financial scope and the combined cost horizon. The run's final verification binds the combined package.

Read the modeling workpaper alongside decisive cost and cash-flow schedules before writing the recommendation. Verify that the explanation's actions, timing, duration and associated payments appear in the selected calculation. Keep alternative cost perspectives as explicitly named tradeoffs; they do not invalidate or replace the bound primary objective. A mismatch requires a return to the core workflow and a new calculation, not an independent report-side adjustment.

## Compile the report

1. Inventory every block in `document.json`, every entry in `tables/index.json` and `figures/index.json`, and every warning, unresolved item and required user input.
2. Run `scripts/init_report_plan.py` to create `report-plan.json`. Complete both ledgers: every required report module and every artifact gets one disposition. `body` is client-facing, `appendix` requires an explicit client use, `workpaper` stays in the verified run unless a stated decision need justifies promotion, and `audit` never enters the report. Follow [content routing](references/content-routing.md) and the [plan contract](references/report-plan.md).
3. Determine the effective transaction mode from the verified input, then design the full argument before drafting. Use the shared report modules and the applicable mode modules; do not mirror file order. Read [mode routing](references/mode-routing.md), [benchmark-derived methods](references/benchmark-methods.md), and [report architecture](references/report-architecture.md). For each analytical subject, connect question, basis, facts, calculation, judgement, risk or limitation, and action.
4. Incorporate non-financial content only when project material supplies it: project necessity, engineering boundary, transaction responsibilities, compliance, performance, risk, guarantees, termination and handover. Mark an unsupported applicable module `user_required`, omit its heading and placeholder prose from the manuscript, and record the exact source request once. Retain empty module headings only when the user explicitly requests a report skeleton.
5. Write `report.md` as the source-backed report manuscript. Copy the plan's `required_notice` intact into the visible opening prose; retain its historical/baseline/conditional and synthetic labels. Treat the CLI `report.md` as the deterministic financial core and `document.json` as the complete semantic source; organize them with supplied project material rather than copying either file wholesale. Keep conclusions and decisive tables in the body; include only client-useful schedules in appendices. Preserve source locations and distinguish verified facts, shared rules and user-required material. Translate client-visible enum values, role names and metric IDs into Chinese; raw machine identifiers belong only in the routing ledger or non-client files.
6. Run `scripts/format_report_tables.py report.md` once after drafting. It normalizes plain numeric cells and percentage-like fields for readable Word tables without changing the underlying deliverable.
7. Validate the plan with `scripts/check_report_plan.py`, then validate `report.md` with `scripts/check_report_manuscript.py`. Resolve every module, missing disposition, table-budget failure, machine identifier, weak analysis-to-table ratio and audit leak before rendering.
8. Render materially useful figures through `chartkit-report-figure`, using the selected briefs and matching CSV files. Write them under `exports/run-NNNN/report/charts/`.
9. Replace figure placeholders with verified image paths, then invoke `docxkit` with the organized `report.md`. Write editable sources, diagnostics, and the final Word file under `exports/run-NNNN/report/docx/`. Render the Word file page by page with the available document renderer and inspect the cover, contents, portrait pages, landscape pages and ending. Structural QA alone is not acceptance; reject missing glyphs, broken contents, near-empty pages and unreadable table splits.
10. Before delivery, compare the manuscript's chapter, narrative and table breadth with the benchmark ranges in `benchmark-methods.md`. Treat a large unexplained collapse as a failed report, even when DocxKit and the plan checker are green.

Before drafting or delivering an interactive case report, run `wwtp-fin verify-final-run RUN --case CASE` for a selected scheme. This includes deliverable integrity and current selection, and refreshes `CURRENT.md`; a successful check covers the unchanged handoff. Historical verification without `--case` does not prove current validity. If inputs, sources, conditions or the current comparison have changed, return to modeling/iteration; do not deliver an old selected result as current. Standalone historical or conditional reports remain possible when explicitly requested and labeled.

## Non-negotiable rules

- Preserve calculated values, bases, evidence states, decision directions, warnings, and unresolved limits exactly.
- A forecast printed in a source report remains an estimate. Preserve the bound `parameter_basis` classification and method when explaining its use; matching baseline values and source-snapshot hashes do not certify the forecast or its interpretation. Do not describe a metadata-only difference as an economic measure, or a valid financial-input test with zero numerical effect as no test at all.
- State the bound cost perspective, unit, nominal/present-value basis, common horizon and baseline provenance beside the main saving claim. Project cash cost, investment/operating outlay, service/grant payments and scoped payer outflow answer different questions and cannot be added together or renamed. A baseline built from source engineering quantities plus estimates is a conditional research baseline, not the source document's own full-life estimate.
- Put each decisive financial conclusion's model scope and applicable criteria next to that conclusion. Do not ask readers to correct the report by remembering a chat or reading a separate README. A reference-price account deficit remains a real conditional result; a fiscal expenditure schedule does not establish that the account receives those funds. Return requirements that are inapplicable to the chosen mode must not be presented as the scheme's failure. If the underlying selected semantics or applicability is wrong, return to modeling and binding instead of changing a verdict during layout.
- Preserve `ranking_groups` ties and the full `best_candidates`; display order is not a preference. A conflicting source total is not a confirmed amount: retain its unresolved status and distinguish the computed total instead of selecting a convenient declaration.
- A complete report does not convert a selected tradeoff into an optimal recommendation. An option not preferred numerically is not thereby legally prohibited or structurally incompatible. Keep the conclusion within the original provision and complete tested comparison; a zero amount in one tax or accounting line cannot establish zero overall economic effect. State the evaluated alternatives, why the selected scheme was chosen, the tested scope in which the recommendation holds, and the conditions that change it. Preserve ties and ranking reversals; do not label a single-case minimum or a user-selected conditional plan as the robust winner. If material research is unfinished, return to the consulting-core workflow instead of concealing the gap in polished prose.
- Use `columns[].label`, `unit`, `format`, and `priority` from `tables/index.json`, never raw machine column IDs. A column with `display_ready:false` needs an explicit Chinese label in the plan or stays out of the report.
- Client-visible prose and tables must not expose snake_case identifiers, enum literals, internal role codes, raw floating-point noise, or scientific notation. Translate meaning and format display values; never change the verified source value.
- `report_role:audit` never enters the client report. `report_role:workpaper` stays outside Word by default. A `body` or `appendix` table never becomes audit or workpaper material; a workpaper enters Word only with a specific client purpose and destination.
- A figure exists to support a stated conclusion. Do not render every brief.
- Supplemental content follows [supplement rules](references/supplemental-content.md). Anything that changes a calculation or decision requires a new wwtp-fin run.
- For differing contract terms, show the complete original contract, the separately calculated continuation and their common-horizon cost together, including end-of-contract obligations. Keep each contract's return and cash results distinct from the combined cost total. Do not manufacture continuity by truncating schedules, filling post-contract service with zeros or annualizing an average fee. Both sets of schedules and their precise sources belong to the same verified selected run, not to two separately chosen alternatives.
- Use the verified `cash_funding_summary` and `cash_funding_components` for funding schedules, including capital contributions, new borrowings, grants and recoveries. A simplified table must retain every nonzero cash category, individually or in explicit other-sources/other-uses totals, so each displayed period reconciles opening cash + all sources − all uses = closing cash. Check this against the native tables before delivery; do not call a schedule complete when its visible columns omit cash flows. State the modeled account and funding assumptions; a cash balance or project-finance decision does not establish a government budget approval or an available reserve.
- Distinguish a current operating-cash DSCR shortfall from a cumulative cash deficit and from breach of an explicit financing covenant. There is no automatic universal DSCR≥1 implementation verdict. Where cumulative funding closes, carry forward `financing_review` and any triggered original/continuation cash-availability condition; pending availability supports only conditional research. `not_applicable` cannot waive it, and valid evidence for `satisfied` remains a responsible-party declaration. Do not rename modeled retained cash as an approved debt-service reserve, omit restricted-use uncertainty, or imply the CLI models a DSRA account or approves a loan.
- Treat only TOT, BOT, and separated government-construction-plus-BOT-operation patterns as benchmark-observed. Other modes use the conservative semantic routing in `mode-routing.md`; never imply that an unobserved mode was benchmark-validated.
- Source-backed draft mode omits `user_required` modules from the manuscript and consolidates their requests once. Use `[待用户补充]` headings only for an explicitly requested report skeleton. Final mode requires all included claims to be evidence-complete and never invents missing content.
- `--mode draft/final` describes content completeness only. A complete baseline, historical or conditional report can use `final`; this never changes selection scope, settles pending conditions, or establishes implementation approval.
- Page count is not a target, but a full report must cover the applicable modules and client-facing table families. Passing technical QA alone is not report acceptance.
- Keep process scripts in `exports/run-NNNN/scripts/`, outside `exports/run-NNNN/report/` and the bound `input/` tree. The report directory contains only the routing ledger, manuscript, selected chart directories and DocxKit output; remove obsolete chart renders before final validation.

## Deliverables

For a selected scheme, read the run-root `decision-brief.md/json` alongside the verified deliverable. Preserve its recommendation versus user-choice distinction, goal order, conditional branches, nominal/present-value and period labels. Cite the selected run's computed figures; do not independently rank alternatives in the manuscript or use a different combination's savings as the selected fallback. This summary does not waive source, engineering or policy review.

```text
exports/run-NNNN/report/
  report-plan.json             # module + artifact routing ledger
  report.md
  charts/
  docx/
```

```bash
python scripts/init_report_plan.py RUN/deliverable EXPORT/report-plan.json --source-run run-NNNN --case CASE
python scripts/format_report_tables.py EXPORT/report.md
python scripts/check_report_plan.py RUN/deliverable EXPORT/report-plan.json
python scripts/check_report_manuscript.py EXPORT/report.md --plan EXPORT/report-plan.json
# 仅用户明确要求报告骨架时：追加 --allow-placeholders
# 明确的独立用途：初始化时追加 --purpose historical、baseline 或 conditional_research
# 冻结环境：init 和 check 均可追加 --cli /absolute/path/to/matching/wwtp-fin
```

Report the source run, final Word path, omitted workpapers and audit material, unresolved limitations, and any user-required sections that remain incomplete.
