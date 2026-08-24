#!/usr/bin/env python3
"""Verify corpus size and copyediting invariants."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


def numbers(text: str) -> Counter:
    return Counter(re.findall(r"\d+(?:\.\d+)?", text))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    cases = [json.loads(line) for line in args.path.read_text(encoding="utf-8").splitlines() if line.strip()]
    errors = []
    if len(cases) < 300:
        errors.append(f"expected at least 300 cases, found {len(cases)}")
    if len({c["paper_id"] for c in cases}) < 10:
        errors.append("expected at least 10 imitation papers")
    for case in cases:
        if numbers(case["control"]) != numbers(case["treatment"]):
            errors.append(f"{case['id']}: number drift between control and treatment")
        if numbers(case["source"]) != numbers(case["treatment"]):
            errors.append(f"{case['id']}: number drift between source and treatment")
        if case.get("scope_anchor") not in case["treatment"]:
            errors.append(f"{case['id']}: treatment lost scope anchor {case.get('scope_anchor')!r}")
        if case["risk_type"] == "legitimate_contrast" and case["control"] != case["treatment"]:
            errors.append(f"{case['id']}: warranted contrast was changed")
        if case["risk_type"] == "hedge_preservation":
            if case["language"] == "zh" and ("可能" not in case["control"] or "可能" not in case["treatment"]):
                errors.append(f"{case['id']}: Chinese hedge lost")
            if case["language"] == "en" and ("may" not in case["control"].lower() or "may" not in case["treatment"].lower()):
                errors.append(f"{case['id']}: English hedge lost")
    summary = {
        "cases": len(cases),
        "paragraphs": len(cases) * 2,
        "papers": len({c["paper_id"] for c in cases}),
        "languages": dict(Counter(c["language"] for c in cases)),
        "sections": dict(Counter(c["section"] for c in cases)),
        "risk_types": dict(Counter(c["risk_type"] for c in cases)),
        "errors": errors,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
