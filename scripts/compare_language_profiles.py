#!/usr/bin/env python3
"""Compare synthetic no-skill papers with a local-literature language profile."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from profile_local_literature import aggregate, metric


CORE_METRICS = [
    "formulaic_hits_per_10k",
    "manufactured_contrast_per_10k",
    "paired_escalation_per_10k",
    "ceremonial_frame_per_10k",
    "inflated_lexicon_per_10k",
    "navigation_marker_per_10k",
    "vague_action_per_10k",
    "abstract_shell_per_10k",
    "modifier_stack_per_10k",
    "empty_transition_per_10k",
    "overclaim_per_10k",
    "conclusion_echo_per_10k",
    "direct_verbs_per_10k",
    "hedges_per_10k",
    "numeric_anchors_per_10k",
    "citation_markers_per_10k",
    "parenthesis_per_10k",
    "sentence_length_cv",
]


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def percent_delta(value: float, reference: float) -> float | None:
    if reference == 0:
        return None
    return round((value - reference) * 100 / reference, 1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("literature_profile", type=Path)
    parser.add_argument("noskill_jsonl", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    literature = json.loads(args.literature_profile.read_text(encoding="utf-8"))
    records = read_jsonl(args.noskill_jsonl)
    grouped: dict[tuple[str, str], list[str]] = defaultdict(list)
    titles: dict[str, str] = {}
    for record in records:
        grouped[(record["language"], record["paper_id"])].append(record["noskill"])
        titles[record["paper_id"]] = record["paper_title"]

    paper_metrics = []
    for (lang, paper_id), paragraphs in grouped.items():
        paper_metrics.append({"paper_id": paper_id, "paper_title": titles[paper_id], **metric("\n\n".join(paragraphs), lang)})

    comparison = {}
    for lang in ("zh", "en"):
        no_skill = aggregate([item for item in paper_metrics if item["language"] == lang])
        local = literature["aggregate_by_language"][lang]
        no_skill_medians = no_skill["median_document_metrics"]
        local_medians = local["median_document_metrics"]
        deltas = {}
        for key in CORE_METRICS:
            n = no_skill_medians.get(key, 0)
            r = local_medians.get(key, 0)
            deltas[key] = {"no_skill": n, "local_literature": r, "difference": round(n - r, 3), "percent_vs_local": percent_delta(n, r)}
        comparison[lang] = {
            "local_documents": local["documents"],
            "no_skill_papers": no_skill["documents"],
            "median_metric_comparison": deltas,
        }

    output = {
        "cautions": [
            "Local publication is a calibration corpus, not an authorship ground truth.",
            "PDF text-order noise is controlled by document medians and visual spot checks.",
            "Differences describe this corpus and should not be universalized.",
        ],
        "records": {"local_profiled": literature["method"]["documents_profiled"], "no_skill_paragraphs": len(records), "no_skill_papers": len(grouped)},
        "comparison": comparison,
        "no_skill_paper_metrics": paper_metrics,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(output["records"], ensure_ascii=False))


if __name__ == "__main__":
    main()
