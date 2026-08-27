---
name: wwtpfin-consulting-core
description: >-
  Convert wastewater-treatment project materials into verified structured financial consulting
  semantics with wwtp-fin, then hand the deliverable to DocxKit and ChartKit. Use for污水处理财务测算、
  特许经营财务评价、BOT/TOT/ROT/BOOT/DBFOT/O&M 项目咨询内容包、财务可行性与项目材料转化。
---

# wwtp-fin Consulting Core

Use this CLI when the task needs deterministic wastewater-project financial calculation, checks, evidence-aware findings, structured report content, tables, or figure briefs. Do not use it to write an unconstrained narrative, make a Word file, draw a chart, infer missing facts, or replace an engineering/design study.

## Project workspace

The user supplies materials, not folders. Before conversion, create or reuse one case directory and place files according to [workspace management](references/workspace.md). Copy source files into `sources/`; never move, rename, edit, or delete the user's originals.

Maintain one editable input set under `input/`. Every accepted input revision gets a numbered run containing an input snapshot and the CLI deliverable. A run becomes immutable after quality and deliverable verification pass. Downstream exports must be bound to the exact verified run that produced them.

## Workflow

1. Create or resume the case workspace. Copy the supplied Word, Excel, PDF and other source files into `sources/` while preserving their names.
2. Read `wwtp-fin --help`, the current input and evidence schemas, `docs/INTAKE.md`, and `examples/minimal_complete/`.
3. Convert `sources/` into `input/project-draft.yaml`, `input/evidence.json`, and `input/conversion-log.md`. Preserve source wording, locator, date and evidence state.
4. Run `wwtp-fin intake -p input/project-draft.yaml -o input/intake-advice.json`. If it is not ready, ask the user one prioritized batch of questions. Explain why each answer matters. For `source_required`, request evidence and never suggest a value. For `confirm_default`, show the exact suggestion and condition, and use it only after confirmation.
5. Once ready, save the canonical parameters as `input/project.yaml`. Create the next `runs/run-NNNN/`, copy `input/` into its `input/` snapshot, and build into its empty `deliverable/` directory.
6. Inspect every `warnings.json` item and `quality.json`, then run `verify-deliverable`. Read `document.json` / `report.md`, `result.json`, checks, decisions, tables and figure briefs together; never promote a warning, missing input, or unverified benchmark into a conclusion.
7. Stop after the verified run unless the user requests a Word report or rendered charts. For an export request, select the latest verified run and follow [downstream handoff](references/handoff.md).

```bash
wwtp-fin schema --kind input
wwtp-fin schema --kind project-evidence
wwtp-fin intake -p input/project-draft.yaml -o input/intake-advice.json
wwtp-fin build -p runs/run-0001/input/project.yaml --evidence runs/run-0001/input/evidence.json -o runs/run-0001/deliverable
wwtp-fin verify-deliverable runs/run-0001/deliverable
```

## Required conversion discipline

- Financing is especially strict: when unusable, state that and do not supply loan terms.
- Never suggest project-specific numbers for scale, period, water, tariff, investment, cost, financing, tax, discount rate, or benchmark. A product default is a labeled proposal, not a fact and not permission to auto-fill.
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

## Final response

State the selected run number, result summary, and output paths. List every remaining input warning and material unresolved limitation, even when build, quality, charts, and Word QA pass. Never let “build passed” imply that project evidence or input assumptions are complete.

For command exit meanings and output contract, use `docs/contract-surface.md`. For current implementation limits, use `docs/boundary.md`; do not present unimplemented probability analysis, new operating-period long-term debt, mixed-use VAT adjustment, generic scenario groups, or a complete statutory VfM study as available.
