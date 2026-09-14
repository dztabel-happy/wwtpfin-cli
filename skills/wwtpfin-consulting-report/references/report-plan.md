# Report plan contract

`report-plan.json` is the module, coverage and routing ledger for one verified run. It closes the full report architecture before it closes semantic blocks, tables, figures, warnings, unresolved items, required user inputs and registered supplements.

The initializer and checker actively invoke the selected `wwtp-fin` executable (`--cli`, default `wwtp-fin`). `report_purpose` is `current` by default: its exact run must pass `verify-final-run --case`. Explicit `historical` verifies historical package integrity and carries a history-only notice. Explicit `baseline` requires an unselected package and, within a case, its current baseline registration. Explicit `conditional_research` requires a selected conditional-research run and checks current selection when a case is present. A new case input or source therefore invalidates an existing current, baseline or conditional plan at its next check.

`source_context` binds the case, exact run, selection scope, synthetic/real selection purpose and pending-condition count. `required_notice` must match that verified context and appear intact in the visible manuscript. It preserves purpose and pending/synthetic labels through export. Plans made before these fields existed must be initialized again with an explicit source purpose. `mode` controls report content completeness only; `final` never declares an implementation approved.

```json
{
  "schema": "wwtpfin/report-plan/4",
  "report_kind": "full_consulting_report",
  "source_run": "run-0001",
  "deliverable": "/absolute/path/to/runs/run-0001/deliverable",
  "mode": "draft",
  "report_purpose": "current",
  "source_context": {
    "case": "/absolute/path/to/case",
    "run": "/absolute/path/to/runs/run-0001",
    "selection_scope": "implementation",
    "selection_purpose": "selected_scheme",
    "pending_conditions": 0
  },
  "required_notice": "本报告使用案例当前登记的选定成果；报告内容完成不代表实施已获批准。",
  "transaction_mode": "BOT",
  "modules": [
    {"module_id": "construction_scope_schedule", "disposition": "user_required", "reason": "可研及建设计划未提供"}
  ],
  "blocks": [
    {"source_ref": "document.json#/sections/0/blocks/0", "disposition": "body", "section": "执行摘要"}
  ],
  "tables": [
    {"table_id": "key_indicators", "disposition": "body", "section": "财务评价"}
  ],
  "figures": [
    {"figure_id": "cash_balance", "disposition": "chart_source", "section": "现金流分析"}
  ],
  "warnings": [
    {"source_ref": "warnings.json#/warnings/0", "warning_id": "D7-07", "disposition": "body", "section": "测算边界"}
  ],
  "unresolved": [
    {"source_ref": "evidence.json#/unresolved/0", "evidence_id": "external:unresolved:E-1", "disposition": "body", "section": "资料限制"}
  ],
  "required_inputs": [
    {"source_ref": "evidence.json#/items/12", "evidence_id": "external:required-input:N-1", "disposition": "user_required"}
  ],
  "supplements": [
    {"source": "sources/example.pdf#page=3", "disposition": "body", "section": "项目背景"}
  ]
}
```

Allowed artifact dispositions are `body`, `appendix`, `chart_source`, `workpaper_only`, `audit_only`, `user_required`, and `not_applicable`. Module dispositions are `body`, `appendix`, `user_required`, or `not_applicable`. Each required shared and mode-specific module appears exactly once. A selected body, appendix or chart source needs a destination section; an appendix also needs a client-use reason. A `workpaper` defaults to `workpaper_only` and may enter the client report only with a specific reason. A client-facing table may not be downgraded to workpaper or audit material. `not_applicable` requires a reason. Required inputs may only be `user_required` or `not_applicable`. For a table with non-display-ready columns selected for body or appendix, add `localized_columns` as an object from column ID to Chinese label.

`user_required` closes the coverage ledger without creating manuscript content. Its module heading is omitted by default, and all such requests are summarized once. It becomes a placeholder heading only when the user explicitly requests a report skeleton.

The plan checker caps selected client tables at 32 and appendix source tables at 12. The manuscript checker independently caps rendered Markdown tables at 40 and requires at least 250 narrative characters per table. These are anti-dump limits, not page-count targets; the verified run retains every excluded workpaper.
