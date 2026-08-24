---
name: wwtpfin-consulting-core
description: >-
  Convert wastewater-treatment project materials into verified structured financial consulting
  semantics with wwtp-fin, then hand the deliverable to DocxKit and ChartKit. Use for污水处理财务测算、
  特许经营财务评价、BOT/TOT/ROT/BOOT/DBFOT/O&M 项目咨询内容包、财务可行性与项目材料转化。
---

# wwtp-fin Consulting Core

Use this CLI when the task needs deterministic wastewater-project financial calculation, checks, evidence-aware findings, structured report content, tables, or figure briefs. Do not use it to write an unconstrained narrative, make a Word file, draw a chart, infer missing facts, or replace an engineering/design study.

## Workflow

1. Read `wwtp-fin --help`, the current input and evidence schemas, `docs/INTAKE.md`, and `examples/minimal_complete/`.
2. Convert source materials into one parameter file, one evidence file, and a conversion log. Preserve source wording, locator, date and evidence state. Unknown, ambiguous, or missing information goes to `unresolved`, `required_user_inputs`, or `declared_basis`; never invent a value.
3. Build, then inspect every `warnings.json` item and `quality.json` before claiming a result.
4. Verify the completed package. Read `document.json` / `report.md`, `result.json`, checks, decisions, tables and figure briefs together; never promote a warning, missing input, or unverified benchmark into a conclusion.
5. Convert `document.json` to DocxKit's `report.json`, then hand off report semantics and tables; hand off `figures/*.json` briefs and matching `figures/data/*.csv` to ChartKit. See [handoff](references/handoff.md).

```bash
wwtp-fin schema --kind input
wwtp-fin schema --kind project-evidence
wwtp-fin build -p project.yaml --evidence evidence.json -o deliverable
wwtp-fin verify-deliverable deliverable
```

## Required conversion discipline

- Financing is especially strict: when unusable, state that and do not supply loan terms.
- Do not elevate evidence state, turn a table into prose, serialize raw JSON into the report, or use a shared rule catalog as project evidence.
- Record full material qualifications in `declared_basis`; retain declared totals and targets in `declared_scalars`.
- Keep pre-tax, after-tax and target bases distinct. A financial benchmark must record its source, date, provider and evidence state.
- Review `D7-*` warnings individually. A successful exit code does not erase a warning.

Read [conversion discipline](references/conversion-discipline.md) before material conversion.

## Read the result correctly

- `quality.json`: whether the completed content package passed its quality gate.
- `warnings.json`: input-shape information requiring correction, an explicit limitation, or an unresolved registration.
- `result.json`: calculation, checks, analysis, decisions, evidence and downstream data.
- `document.json`: authoritative report semantics; `report.md` is its deterministic projection.

For command exit meanings and output contract, use `docs/contract-surface.md`. For current implementation limits, use `docs/boundary.md`; do not present unimplemented probability analysis, new operating-period long-term debt, mixed-use VAT adjustment, generic scenario groups, or a complete statutory VfM study as available.
