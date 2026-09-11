#!/usr/bin/env python3
"""Record an already-given user decision; never invent confirmation or choose a candidate."""
import argparse
import hashlib
import json
from pathlib import Path


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("comparison", type=Path)
    parser.add_argument("candidate_id")
    parser.add_argument("output", type=Path)
    parser.add_argument("--confirmed-by", required=True)
    parser.add_argument("--confirmed-at", required=True)
    parser.add_argument("--reference", required=True)
    parser.add_argument("--purpose", required=True,
                        choices=("selected_scheme", "workflow_validation"))
    args = parser.parse_args()
    comparison = json.loads(args.comparison.read_text(encoding="utf-8"))
    if args.candidate_id not in comparison.get("selectable_shortlist", []):
        parser.error("candidate is not eligible for selection; continue iteration or resolve conditions")
    candidate = next(row for row in comparison["candidates"] if row["id"] == args.candidate_id)
    if digest(candidate["resolved_params"]) != candidate["resolved_params_sha256"]:
        parser.error("candidate parameter hash mismatch")
    selection = {
        "schema": "wwtp-fin/scheme-selection/1", "decision": "confirmed",
        "purpose": args.purpose, "candidate_id": args.candidate_id,
        "confirmed_by": args.confirmed_by, "confirmed_at": args.confirmed_at,
        "confirmation_reference": args.reference,
        "comparison_sha256": digest(comparison),
        "resolved_params_sha256": candidate["resolved_params_sha256"],
    }
    # Exclusive creation preserves existing confirmation records.
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(selection, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(args.output)


if __name__ == "__main__":
    main()
