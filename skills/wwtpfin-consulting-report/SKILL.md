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

## Preconditions

1. Select the explicitly confirmed final `run-NNNN`; require `wwtp-fin verify-final-run`, passing `quality.json` and `wwtp-fin verify-deliverable` now. A baseline or conditional report may use an exact run explicitly identified for that purpose; never silently substitute the newest trial. Retain `workflow_validation` labels for synthetic acceptance.
2. Bind all work to `exports/run-NNNN/report/`. The plan initializer records deliverable, parameter and selection hashes; the checker rejects changed source content. Never mix runs.
3. Read the user goal and all supplied source materials before deciding the report structure. Default to a source-backed draft: include supported modules, omit unsupported modules from the manuscript, and keep their requests in the routing ledger and one consolidated data-request section.

## Compile the report

1. Inventory every block in `document.json`, every entry in `tables/index.json` and `figures/index.json`, and every warning, unresolved item and required user input.
2. Run `scripts/init_report_plan.py` to create `report-plan.json`. Complete both ledgers: every required report module and every artifact gets one disposition. `body` is client-facing, `appendix` requires an explicit client use, `workpaper` stays in the verified run unless a stated decision need justifies promotion, and `audit` never enters the report. Follow [content routing](references/content-routing.md) and the [plan contract](references/report-plan.md).
3. Determine the effective transaction mode from the verified input, then design the full argument before drafting. Use the shared report modules and the applicable mode modules; do not mirror file order. Read [mode routing](references/mode-routing.md), [benchmark-derived methods](references/benchmark-methods.md), and [report architecture](references/report-architecture.md). For each analytical subject, connect question, basis, facts, calculation, judgement, risk or limitation, and action.
4. Incorporate non-financial content only when project material supplies it: project necessity, engineering boundary, transaction responsibilities, compliance, performance, risk, guarantees, termination and handover. Mark an unsupported applicable module `user_required`, omit its heading and placeholder prose from the manuscript, and record the exact source request once. Retain empty module headings only when the user explicitly requests a report skeleton.
5. Write `report.md` as the source-backed report manuscript. Treat the CLI `report.md` as the deterministic financial core and `document.json` as the complete semantic source; organize them with supplied project material rather than copying either file wholesale. Keep conclusions and decisive tables in the body; include only client-useful schedules in appendices. Preserve source locations and distinguish verified facts, shared rules and user-required material. Translate client-visible enum values, role names and metric IDs into Chinese; raw machine identifiers belong only in the routing ledger or non-client files.
6. Run `scripts/format_report_tables.py report.md` once after drafting. It normalizes plain numeric cells and percentage-like fields for readable Word tables without changing the underlying deliverable.
7. Validate the plan with `scripts/check_report_plan.py`, then validate `report.md` with `scripts/check_report_manuscript.py`. Resolve every module, missing disposition, table-budget failure, machine identifier, weak analysis-to-table ratio and audit leak before rendering.
8. Render materially useful figures through `chartkit-report-figure`, using the selected briefs and matching CSV files. Write them under `exports/run-NNNN/report/charts/`.
9. Replace figure placeholders with verified image paths, then invoke `docxkit` with the organized `report.md`. Write editable sources, diagnostics, and the final Word file under `exports/run-NNNN/report/docx/`. Render the Word file page by page with the available document renderer and inspect the cover, contents, portrait pages, landscape pages and ending. Structural QA alone is not acceptance; reject missing glyphs, broken contents, near-empty pages and unreadable table splits.
10. Before delivery, compare the manuscript's chapter, narrative and table breadth with the benchmark ranges in `benchmark-methods.md`. Treat a large unexplained collapse as a failed report, even when DocxKit and the plan checker are green.

Before drafting or delivering an interactive case report, run `wwtp-fin case status CASE` and `wwtp-fin verify-final-run RUN --case CASE` for a selected scheme. Historical verification does not prove current validity. If inputs, sources, conditions or the current comparison have changed, return to modeling/iteration; do not deliver an old selected result as current. Standalone historical or conditional reports remain possible when explicitly requested and labeled.

## Non-negotiable rules

- Preserve calculated values, bases, evidence states, decision directions, warnings, and unresolved limits exactly.
- Use `columns[].label`, `unit`, `format`, and `priority` from `tables/index.json`, never raw machine column IDs. A column with `display_ready:false` needs an explicit Chinese label in the plan or stays out of the report.
- Client-visible prose and tables must not expose snake_case identifiers, enum literals, internal role codes, raw floating-point noise, or scientific notation. Translate meaning and format display values; never change the verified source value.
- `report_role:audit` never enters the client report. `report_role:workpaper` stays outside Word by default. A `body` or `appendix` table never becomes audit or workpaper material; a workpaper enters Word only with a specific client purpose and destination.
- A figure exists to support a stated conclusion. Do not render every brief.
- Supplemental content follows [supplement rules](references/supplemental-content.md). Anything that changes a calculation or decision requires a new wwtp-fin run.
- Treat only TOT, BOT, and separated government-construction-plus-BOT-operation patterns as benchmark-observed. Other modes use the conservative semantic routing in `mode-routing.md`; never imply that an unobserved mode was benchmark-validated.
- Source-backed draft mode omits `user_required` modules from the manuscript and consolidates their requests once. Use `[待用户补充]` headings only for an explicitly requested report skeleton. Final mode requires all included claims to be evidence-complete and never invents missing content.
- Page count is not a target, but a full report must cover the applicable modules and client-facing table families. Passing technical QA alone is not report acceptance.
- Keep process scripts outside `exports/run-NNNN/report/`. The report directory contains only the routing ledger, manuscript, selected chart directories and DocxKit output; remove obsolete chart renders before final validation.

## Deliverables

```text
exports/run-NNNN/report/
  report-plan.json             # module + artifact routing ledger
  report.md
  charts/
  docx/
```

```bash
python scripts/init_report_plan.py RUN/deliverable EXPORT/report-plan.json --source-run run-NNNN
python scripts/format_report_tables.py EXPORT/report.md
python scripts/check_report_plan.py RUN/deliverable EXPORT/report-plan.json
python scripts/check_report_manuscript.py EXPORT/report.md --plan EXPORT/report-plan.json
# 仅用户明确要求报告骨架时：追加 --allow-placeholders
```

Report the source run, final Word path, omitted workpapers and audit material, unresolved limitations, and any user-required sections that remain incomplete.
