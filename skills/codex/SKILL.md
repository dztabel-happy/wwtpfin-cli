---
name: wwtpfin-consulting-core
description: Use wwtp-fin for deterministic wastewater-treatment financial consulting semantics: material conversion, structured calculation, evidence-aware findings, report package verification, and DocxKit/ChartKit handoff.
---

# wwtp-fin Consulting Core

Use for wastewater-treatment financial consulting work that needs a structured, auditable core. Do not use for free-form report prose, Word generation, image generation, engineering design, or filling missing project facts.

```bash
wwtp-fin schema --kind input
wwtp-fin schema --kind project-evidence
wwtp-fin build -p project.yaml --evidence evidence.json -o deliverable
wwtp-fin verify-deliverable deliverable
```

Before conversion, read `docs/INTAKE.md`, `docs/spec-reference.md`, the live schemas, and `examples/minimal_complete/`. Produce parameters, evidence, and a conversion log. Preserve source and evidence state; send ambiguity and gaps to `unresolved`, `required_user_inputs`, or `declared_basis`. Never invent financing, tax eligibility, benchmarks, values, or a conclusion.

After `build`, inspect `quality.json`, every `warnings.json` item, `result.json`, `document.json`, tables, and figure briefs. `document.json` is authoritative; `report.md` is only its deterministic projection.

Handoff: convert `document.json` to DocxKit's `report.json`, then send report semantics and tables; send `figures/*.json` plus matching `figures/data/*.csv` to ChartKit. DocxKit owns Word layout and numbering; ChartKit owns image rendering. Neither downstream tool recalculates financial results.

Current limits are binding: no probability/Monte Carlo analysis, mixed-use long-term-asset VAT adjustment, non-capitalized construction interest, operating-period new long-term debt, generic multi-scheme scenario-group orchestration, or complete statutory VfM study. Read `docs/boundary.md` and `docs/contract-surface.md` for the live contract.
