# Supplemental content

Some report content cannot be produced by wwtp-fin: engineering design, site investigation, local history, approval originals, organization-specific wording, maps, process diagrams, or user conclusions outside the financial model.

## Route by effect

- If the material changes a parameter, calculation basis, evidence state, decision or warning, return it to the case `sources/`, update `input/`, and create a new verified run. Do not patch the report around an old run.
- If it supplies narrative context without changing the verified run, register its source and locator in `report-plan.json` and integrate it without changing financial semantics.
- If it is still missing, use `user_required`. Omit the unsupported module from the manuscript and consolidate the exact request once; only an explicitly requested skeleton retains a placeholder.
- Missing material does not erase an applicable module from the routing ledger. State what is missing, why it matters, what can still be concluded and which exact source is required without manufacturing a client chapter.

## Final checks

- User text and CLI semantics must not contradict each other.
- A project-specific fact needs a source locator.
- Shared policy or method material must be labelled as shared reference, not project evidence.
- User-supplied prose may be edited for organization and style, not upgraded in evidence status.
