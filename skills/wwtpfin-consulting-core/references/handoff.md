# Downstream handoff

## DocxKit

Convert `document.json` into the `report.json` required by DocxKit, then pass that result, tables and final figure assets. DocxKit owns editable Word layout, numbering, captions, cross-references and page structure. Do not alter wwtp-fin financial values or decision wording during layout.

## ChartKit

Pass `figures/index.json`, each selected `figures/*.json`, and the matching `figures/data/*.csv`. ChartKit chooses and renders the visual grammar. It returns image files and captions. The document layer owns the figure number and placement.

Do not introduce code integration between the products. The agent coordinates files and preserves source references.
