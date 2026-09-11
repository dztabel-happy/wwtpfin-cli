#!/usr/bin/env python3
"""Run synthetic workflow acceptance against an installed CLI, without core imports."""
import argparse
import json
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cli", type=Path, required=True)
    parser.add_argument("--assets", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    cli, assets, out = args.cli.resolve(), args.assets.resolve(), args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    if any(out.iterdir()):
        parser.error("output must be empty")
    evidence = assets / "examples/minimal_complete/evidence.json"
    contract = assets / "examples/three_stage/decision-contract.yaml"

    def run(*parts, expect=0):
        command = [str(cli), *map(str, parts)]
        # Windows npm launchers are .cmd; execute the shipped Node wrapper directly.
        if cli.suffix == ".cmd":
            wrapper = cli.parent.parent / "@dztabel/wwtpfin/npm/wwtp-fin.cjs"
            command = ["node", str(wrapper), *map(str, parts)]
        result = subprocess.run(command, cwd=out, capture_output=True, text=True,
                                encoding="utf-8")
        if result.returncode != expect:
            raise RuntimeError(f"{command[1]}: expected {expect}, got {result.returncode}\n"
                               + result.stdout + result.stderr)

    run("compare", "-p", assets / "examples/minimal_complete/project.yaml",
        "--evidence", evidence, "--contract", contract,
        "--schemes", assets / "examples/three_stage/scheme-set.yaml", "-o", out / "comparison")
    comparison = out / "comparison/scheme-comparison.json"
    data = json.loads(comparison.read_text(encoding="utf-8"))
    rows = {row["id"]: row for row in data["candidates"]}
    assert not rows["cash_gap"]["numerically_feasible"]
    assert rows["conditional"]["readiness"] == "conditions_pending"
    assert data["selectable_shortlist"] == ["complete"]
    helper = assets / "skills/wwtpfin-consulting-core/scripts/record-selection.py"
    subprocess.run([sys.executable, str(helper), str(comparison), "complete",
                    str(out / "selection.json"), "--confirmed-by", "synthetic acceptance",
                    "--confirmed-at", "2026-09-11", "--reference", "synthetic://acceptance",
                    "--purpose", "workflow_validation"], check=True, capture_output=True)
    selection = out / "selection.json"
    final = out / "run-0001"
    run("finalize", "--comparison", comparison, "--selection", selection,
        "--contract", contract, "--evidence", evidence, "-o", final)
    run("verify-final-run", final)
    payload = json.loads((final / "deliverable/result.json").read_text(encoding="utf-8"))
    assert payload["selected_scheme"]["selection"]["purpose"] == "workflow_validation"
    assert payload["params"] == rows["complete"]["resolved_params"]
    assert payload["tables"] and "decision_boundaries" in payload["analysis"]
    run("finalize", "--comparison", comparison, "--selection", selection,
        "--contract", contract, "--evidence", evidence, "-o", final, expect=1)
    print("three-stage installed acceptance passed: constraints, conditions, selection, full run, immutable output")


if __name__ == "__main__":
    main()
