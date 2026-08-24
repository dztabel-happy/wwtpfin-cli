# Conversion discipline

1. Build a source-to-field ledger before writing values.
2. Read `schema --kind input`, `schema --kind project-evidence`, `docs/INTAKE.md`, and the minimal complete example before field mapping.
3. Map only source-backed facts. Keep source, date, provider, locator and evidence state. Keep tables in `supporting[]` with `table_role` and `{columns, rows}`.
4. Put uncertain readings in the conversion log. Put missing project evidence in `unresolved` or `required_user_inputs`; do not use placeholder numbers, arbitrary enum values, or industry norms.
5. Run `build`, read `warnings.json`, then either correct the input or record the limitation. Run `verify-deliverable` before handoff.

The CLI determines calculation and structured semantics. The agent determines only the transparent, source-backed mapping into the contract.
