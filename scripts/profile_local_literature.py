#!/usr/bin/env python3
"""Build a copyright-safe language profile from local scholarly PDFs.

The output contains aggregate and document-level metrics, never full extracted text.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

import pypdfium2 as pdfium

sys.path.insert(0, str(Path(__file__).parent))
from style_audit import audit_text, sentences, tokens  # noqa: E402


ZH_HEDGES = ["可能", "或许", "一定程度", "尚不能", "有待", "推测", "似乎", "倾向于"]
EN_HEDGES = ["may", "might", "could", "suggest", "likely", "appears", "possibly", "cannot establish"]
ZH_DIRECT = ["发现", "记录", "测得", "表明", "比较", "采用", "识别", "观察", "验证"]
EN_DIRECT = ["found", "recorded", "measured", "shows", "compared", "used", "identified", "observed", "tested"]
ZH_META = ["本文旨在", "本研究旨在", "值得注意的是", "需要指出的是", "综上所述", "由此可见"]
EN_META = ["this study aims to", "it is worth noting", "it should be noted", "in conclusion", "overall"]


def clean_text(text: str) -> str:
    text = text.replace("\x00", " ").replace("\u00ad", "")
    text = re.sub(r"(?<=\w)-\s*\n\s*(?=\w)", "", text)
    text = re.sub(r"(?<![。！？.!?:;：；])\s*\n\s*(?!\n)", " ", text)
    text = re.split(r"\n\s*(?:References|REFERENCES|参考文献)\s*\n", text, maxsplit=1)[0]
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def count_terms(text: str, terms: list[str]) -> int:
    low = text.lower()
    return sum(len(re.findall(re.escape(term.lower()), low)) for term in terms)


def language(text: str) -> str:
    cjk = len(re.findall(r"[\u4e00-\u9fff]", text))
    latin = len(re.findall(r"[A-Za-z]", text))
    return "zh" if cjk > latin * 0.35 else "en"


def source_group(path: Path) -> str:
    parts = [p.lower() for p in path.parts]
    if "journals" in parts:
        idx = parts.index("journals")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    if "wenxian" in parts:
        idx = parts.index("wenxian")
        return "wenxian-" + (parts[idx + 1] if idx + 1 < len(parts) else "root")
    return path.parent.name.lower()


def metric(text: str, lang: str) -> dict:
    audit = audit_text(text)
    sents = sentences(text)
    sent_lengths = [len(tokens(s)) for s in sents if tokens(s)]
    chars = max(audit["characters_no_space"], 1)
    per10k = lambda n: round(n * 10000 / chars, 3)
    openings = []
    for sent in sents:
        ts = tokens(sent)[:4]
        if ts:
            openings.append("".join(ts))
    return {
        "language": lang,
        "characters": chars,
        "sentences": len(sents),
        "sentence_length_mean": round(statistics.mean(sent_lengths), 2) if sent_lengths else 0,
        "sentence_length_median": round(statistics.median(sent_lengths), 2) if sent_lengths else 0,
        "sentence_length_cv": audit["sentence_length_cv"],
        "formulaic_hits_per_10k": per10k(audit["formulaic_hits"]),
        "manufactured_contrast_per_10k": per10k(audit["pattern_hits"]["manufactured_contrast"]),
        "paired_escalation_per_10k": per10k(audit["pattern_hits"]["paired_escalation"]),
        "ceremonial_frame_per_10k": per10k(audit["pattern_hits"]["ceremonial_frame"]),
        "inflated_lexicon_per_10k": per10k(audit["pattern_hits"]["inflated_lexicon"]),
        "navigation_marker_per_10k": per10k(audit["pattern_hits"]["navigation_marker"]),
        "vague_action_per_10k": per10k(audit["pattern_hits"]["vague_action"]),
        "abstract_shell_per_10k": per10k(audit["pattern_hits"]["abstract_shell"]),
        "modifier_stack_per_10k": per10k(audit["pattern_hits"]["modifier_stack"]),
        "empty_transition_per_10k": per10k(audit["pattern_hits"]["empty_transition"]),
        "overclaim_per_10k": per10k(audit["pattern_hits"]["overclaim"]),
        "conclusion_echo_per_10k": per10k(audit["pattern_hits"]["conclusion_echo"]),
        "hedges_per_10k": per10k(count_terms(text, ZH_HEDGES if lang == "zh" else EN_HEDGES)),
        "direct_verbs_per_10k": per10k(count_terms(text, ZH_DIRECT if lang == "zh" else EN_DIRECT)),
        "explicit_meta_per_10k": per10k(count_terms(text, ZH_META if lang == "zh" else EN_META)),
        "semicolon_per_10k": per10k(text.count(";") + text.count("；")),
        "colon_per_10k": per10k(text.count(":") + text.count("：")),
        "parenthesis_per_10k": per10k(text.count("(") + text.count("（")),
        "numeric_anchors_per_10k": per10k(audit["numeric_anchors"]),
        "citation_markers_per_10k": per10k(audit["citation_markers"]),
        "token_variety_ratio": audit["token_variety_ratio"],
        "common_openings": Counter(openings).most_common(5),
    }


def aggregate(items: list[dict]) -> dict:
    if not items:
        return {"documents": 0}
    numeric_keys = [k for k, v in items[0].items() if isinstance(v, (int, float)) and k not in {"characters", "sentences"}]
    return {
        "documents": len(items),
        "characters": sum(i["characters"] for i in items),
        "sentences": sum(i["sentences"] for i in items),
        "median_document_metrics": {k: round(statistics.median(i[k] for i in items), 3) for k in numeric_keys},
        "mean_document_metrics": {k: round(statistics.mean(i[k] for i in items), 3) for k in numeric_keys},
    }


def extract_pdf(path: Path, max_pages: int) -> tuple[str, int, int]:
    """Extract a bounded page sample with PDFium and close native handles promptly."""
    document = pdfium.PdfDocument(str(path))
    total = len(document)
    sampled = min(total, max_pages)
    chunks: list[str] = []
    try:
        for index in range(sampled):
            page = document[index]
            textpage = page.get_textpage()
            try:
                chunks.append(textpage.get_text_range() or "")
            finally:
                textpage.close()
                page.close()
    finally:
        document.close()
    return "\n\n".join(chunks), total, sampled


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roots", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-pages", type=int, default=10)
    parser.add_argument("--min-chars", type=int, default=1800)
    args = parser.parse_args()
    docs, failures = [], []
    pdfs = sorted({p for root in args.roots for p in root.rglob("*.pdf")})
    for index, path in enumerate(pdfs, start=1):
        try:
            raw_text, pages_total, pages_profiled = extract_pdf(path, args.max_pages)
            text = clean_text(raw_text)
            if len(text) < args.min_chars:
                failures.append({"file": path.name, "reason": "insufficient_extractable_text", "characters": len(text)})
                continue
            lang = language(text)
            docs.append({
                "source_id": hashlib.sha256(str(path).encode("utf-8")).hexdigest()[:12],
                "file": path.name,
                "group": source_group(path),
                "pages_total": pages_total,
                "pages_profiled": pages_profiled,
                **metric(text, lang),
            })
        except Exception as exc:
            failures.append({"file": path.name, "reason": type(exc).__name__})
        if index % 25 == 0 or index == len(pdfs):
            print(f"profiled {index}/{len(pdfs)} PDFs", file=sys.stderr, flush=True)
    by_language = {lang: aggregate([d for d in docs if d["language"] == lang]) for lang in ("zh", "en")}
    by_group = {group: aggregate([d for d in docs if d["group"] == group]) for group in sorted({d["group"] for d in docs})}
    output = {
        "method": {
            "pdfs_discovered": len(pdfs), "documents_profiled": len(docs), "documents_excluded": len(failures),
            "max_pages_per_pdf": args.max_pages, "min_extractable_characters": args.min_chars,
            "copyright": "Metrics only; extracted full text is not stored.",
        },
        "aggregate_by_language": by_language,
        "aggregate_by_group": by_group,
        "documents": docs,
        "excluded": failures,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"discovered": len(pdfs), "profiled": len(docs), "excluded": len(failures), "zh": by_language["zh"]["documents"], "en": by_language["en"]["documents"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
