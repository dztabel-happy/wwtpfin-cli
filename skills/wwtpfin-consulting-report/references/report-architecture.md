# Report architecture

Build the report around the user's purpose, not the artifact directory. The financial core is one part of the deliverable. A complete report normally covers:

1. Executive conclusion: overall judgement, decisive metrics, binding limitations and immediate actions.
2. Project overview and preparation basis: scope, mode, period, parties, source status and applicable basis.
3. Necessity and feasibility: demand, capacity, engineering boundary, implementation conditions and operating requirements.
4. Concession-mode feasibility and transaction structure: responsibilities, charging, asset rights, participant interest and comparative advantages.
5. Concession arrangement: scope, term, investment, financing, construction or transfer, operation, performance, supervision, guarantees, adjustment, termination and handover.
6. Financial analysis: volume, tariff, cost, tax, cash flow, profitability, solvency, break-even, sensitivity and decision boundaries.
7. Compliance and risk: policy basis, approvals, risk allocation, public affordability and evidence limitations.
8. Conclusions, implementation conditions and evidence requests.
9. Client appendices: selected financial schedules, supporting data, performance or risk matrices and sourced attachments needed to use or review the report. The verified run, not the Word file, remains the complete calculation archive.

This is a coverage architecture, not fixed wording. Adapt and merge supported headings. An applicable but unsupported module remains `user_required` in `report-plan.json`, is omitted from the manuscript, and appears once in the consolidated data-request section with its effect and exact source request. Only an explicitly requested report skeleton may retain `[待用户补充]` headings. Select mode additions through [mode routing](mode-routing.md); do not infer project facts merely from the mode label.

## Analytical paragraph pattern

Use a coherent sequence rather than block concatenation:

`question → applicable basis → project facts → calculation/table/figure → judgement → risk or limitation → action`

Not every paragraph needs every element, but a judgement must expose its basis and decisive facts. Do not repeat the same evidence qualification in every paragraph; state it once at the nearest useful scope.

## Semantic layers

- The CLI `report.md` supplies the fixed financial analytical spine; `document.json` retains complete machine semantics and evidence links.
- Project facts explain what was calculated and why the result applies.
- Normative material supports a specific judgement; it is not a freestanding law catalog.
- Structural text supplies headings and transitions only.
- Audit and apparatus text stays outside the client manuscript.

The manuscript itself is the organized consulting deliverable that DocxKit formats. It remains suitable for downstream editing, but it must already contain the complete sourced argument and client-facing appendices rather than only a short semantic core.
