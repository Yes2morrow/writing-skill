#!/usr/bin/env python3
"""Evaluate paired source/control/skill-edited benchmark passages."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from style_audit import audit_text  # noqa: E402


def load_cases(path: Path) -> list[dict]:
    cases = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        item = json.loads(line)
        required = {"id", "source", "control", "treatment"}
        missing = required - item.keys()
        if missing:
            raise ValueError(f"line {line_no}: missing {sorted(missing)}")
        cases.append(item)
    if not cases:
        raise ValueError("benchmark has no cases")
    return cases


def evaluate(cases: list[dict]) -> dict:
    rows = []
    for case in cases:
        control = audit_text(case["control"])
        treatment = audit_text(case["treatment"])
        c = control["formulaic_risk_0_100"]
        t = treatment["formulaic_risk_0_100"]
        rows.append({
            "id": case["id"],
            "language": case.get("language", "unknown"),
            "genre": case.get("genre", case.get("section", "unknown")),
            "control_risk": c,
            "treatment_risk": t,
            "risk_delta": round(t - c, 1),
            "relative_risk_reduction_pct": round((c - t) * 100 / c, 1) if c else 0.0,
        })
    deltas = [r["risk_delta"] for r in rows]
    reductions = [r["relative_risk_reduction_pct"] for r in rows]
    return {
        "disclaimer": "Synthetic paired benchmark; measures configured language patterns, not authorship or publication quality.",
        "case_count": len(rows),
        "mean_risk_delta": round(statistics.mean(deltas), 2),
        "median_relative_risk_reduction_pct": round(statistics.median(reductions), 2),
        "wins_ties_losses": {
            "wins": sum(d < 0 for d in deltas),
            "ties": sum(d == 0 for d in deltas),
            "losses": sum(d > 0 for d in deltas),
        },
        "cases": rows,
    }


def markdown(result: dict, details: bool = False) -> str:
    lines = [
        "# Paired language benchmark",
        "",
        f"> {result['disclaimer']}",
        "",
        f"- Cases: {result['case_count']}",
        f"- Mean treatment-minus-control risk: {result['mean_risk_delta']}",
        f"- Median relative risk reduction: {result['median_relative_risk_reduction_pct']}%",
        f"- Win/tie/loss: {result['wins_ties_losses']['wins']}/{result['wins_ties_losses']['ties']}/{result['wins_ties_losses']['losses']}",
    ]
    if details:
        lines += ["", "| Case | Language | Genre | Control | Skill | Delta | Reduction |", "|---|---|---|---:|---:|---:|---:|"]
        for row in result["cases"]:
            lines.append(
                f"| {row['id']} | {row['language']} | {row['genre']} | {row['control_risk']} | "
                f"{row['treatment_risk']} | {row['risk_delta']} | {row['relative_risk_reduction_pct']}% |"
            )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--details", action="store_true", help="include every case in Markdown output")
    parser.add_argument("--output", type=Path, help="write the report to a UTF-8 file")
    args = parser.parse_args()
    result = evaluate(load_cases(args.path))
    rendered = markdown(result, args.details) if args.format == "markdown" else json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
