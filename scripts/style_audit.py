#!/usr/bin/env python3
"""Interpretable bilingual diagnostics for formulaic academic prose.

This tool evaluates observable language patterns. It cannot determine authorship.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
from collections import Counter
from pathlib import Path


PATTERNS = {
    "manufactured_contrast": [
        r"(?:并非|不是|不再)[^。！？!?\n]{0,32}(?:而是|只是)",
        r"\bnot\s+(?:merely|simply|only)?[^.!?\n]{0,80}\bbut\b",
        r"\brather than (?:merely|simply|being)\b",
    ],
    "paired_escalation": [
        r"不仅[^。！？!?\n]{0,32}(?:而且|还|更)",
        r"\bnot only\b[^.!?\n]{0,100}\bbut also\b",
    ],
    "ceremonial_frame": [
        r"随着[^。！？!?\n]{0,28}(?:发展|进步|演进)",
        r"在[^。！？!?\n]{0,24}(?:背景|语境|时代)下",
        r"近年来[^。！？!?\n]{0,20}(?:关注|发展|兴起)",
        r"综上所述|由此可见|总而言之|值得注意的是|需要指出的是",
        r"\bin (?:today'?s|the) rapidly (?:evolving|changing)\b",
        r"\b(?:it is worth noting|in conclusion|to sum up)\b",
    ],
    "generic_significance": [
        r"具有[^。！？!?\n]{0,24}(?:重要|重大)[^。！？!?\n]{0,16}(?:意义|价值)",
        r"为[^。！？!?\n]{0,30}提供(?:了)?(?:新的?|全新的?)(?:视角|路径|框架|思路)",
        r"\b(?:underscores|highlights) the (?:critical |crucial |vital )?importance\b",
        r"\boffers? (?:a |an )?(?:novel|new|transformative) (?:lens|framework|pathway)\b",
    ],
    "navigation_marker": [
        r"首先|其次|再次|此外|最后|一方面|另一方面",
        r"\b(?:firstly|secondly|thirdly|furthermore|moreover|additionally|notably)\b",
    ],
    "inflated_lexicon": [
        r"深刻|显著|重要|关键|复杂|多维|全面|系统性|创新性|赋能|重塑|颠覆",
        r"\b(?:delve|realm|underscore|pivotal|profound|intricate|transformative|robust|holistic|multifaceted|landscape)\w*\b",
    ],
    "vague_action": [
        r"进行了?[^。！？!?\n]{0,12}(?:研究|探讨|分析|考察)",
        r"实现了?[^。！？!?\n]{0,16}(?:提升|优化|转变)",
        r"促进了?[^。！？!?\n]{0,16}(?:发展|提升|融合)",
        r"呈现出[^。！？!?\n]{0,18}(?:趋势|特征|态势)",
        r"\b(?:facilitate|foster|leverage|utilize)(?:s|d|ing)?\b",
        r"\bconduct(?:ed|s|ing)? (?:a |an )?(?:systematic |in-depth )?(?:investigation|analysis|examination)\b",
        r"\bundertook (?:a |an )?(?:systematic |in-depth )?(?:investigation|analysis|examination)\b",
    ],
    "abstract_shell": [
        r"[^。！？!?\n]{0,16}的[^。！？!?\n]{0,12}性[^。！？!?\n]{0,18}的(?:发生|实现|提升|变化)",
        r"\b(?:the (?:occurrence|realization|achievement) of (?:a |the )?|a reduction in the stability of the continuity of)\b",
    ],
    "modifier_stack": [
        r"(?:[\u4e00-\u9fff]{2,10}的[、，,]?){3,}[\u4e00-\u9fff]{2,12}",
        r"\b(?:[a-z-]+,\s+){3,}(?:and\s+)?[a-z-]+\s+[a-z-]+\b",
    ],
    "empty_transition": [
        r"在此基础上[^。！？!?\n]{0,24}(?:从另一个层面|进一步而言)",
        r"从另一个层面来看|进一步而言",
        r"\bon this basis,?[^.!?\n]{0,50}\b(?:from another perspective|furthermore)\b",
    ],
    "overclaim": [
        r"(?:充分|有力地?)(?:证明|证实)|从根本上(?:改变|重塑|决定)|决定了?[^。！？!?\n]{0,20}(?:效率|行为|结果)",
        r"\b(?:conclusively proves?|fundamentally reshapes?|determines?)[^.!?\n]{0,60}\b",
    ],
    "conclusion_echo": [
        r"因此[，,]?[^。！？!?\n]{0,20}(?:本段|上述结果|研究结果)(?:表明|说明)",
        r"\btherefore,? (?:this paragraph|the paragraph|the results?|these findings?) (?:shows?|demonstrates?|indicates?)\b",
    ],
}


def sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[。！？.!?])\s*|\n+", text) if s.strip()]


def paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?|[\u4e00-\u9fff]", text.lower())


def coefficient_of_variation(values: list[int]) -> float:
    if len(values) < 2 or statistics.mean(values) == 0:
        return 0.0
    return statistics.pstdev(values) / statistics.mean(values)


def audit_text(text: str) -> dict:
    chars = len(re.sub(r"\s+", "", text))
    sents = sentences(text)
    paras = paragraphs(text)
    toks = tokens(text)
    pattern_hits = {}
    examples = {}
    for category, expressions in PATTERNS.items():
        matches = []
        for expression in expressions:
            matches.extend(m.group(0) for m in re.finditer(expression, text, re.I))
        pattern_hits[category] = len(matches)
        examples[category] = matches[:3]

    openings = []
    for sent in sents:
        opening_tokens = tokens(sent)[:3]
        if opening_tokens:
            openings.append("".join(opening_tokens))
    repeated_openings = sum(count - 1 for count in Counter(openings).values() if count > 1)

    sent_lengths = [len(tokens(s)) for s in sents if tokens(s)]
    para_lengths = [len(tokens(p)) for p in paras if tokens(p)]
    unique_ratio = len(set(toks)) / len(toks) if toks else 0.0
    citations = len(re.findall(r"\([^)]*\b(?:19|20)\d{2}[a-z]?[^)]*\)|\[[0-9,;\-– ]+\]", text))
    numeric_anchors = len(re.findall(r"(?<!\d)\d+(?:\.\d+)?%?(?!\d)", text))
    total_hits = sum(pattern_hits.values()) + repeated_openings
    density = total_hits * 1000 / max(chars, 1)

    # A single construction is a review cue, not a verdict. Risk rises mainly
    # when several categories cluster or the same template recurs.
    category_weights = {
        "manufactured_contrast": 6.0,
        "paired_escalation": 6.0,
        "ceremonial_frame": 7.0,
        "generic_significance": 7.0,
        "navigation_marker": 2.0,
        "inflated_lexicon": 2.0,
        "vague_action": 4.0,
        "abstract_shell": 5.0,
        "modifier_stack": 3.0,
        "empty_transition": 4.0,
        "overclaim": 7.0,
        "conclusion_echo": 3.0,
    }
    lexical_component = sum(
        category_weights[key] * min(count, 3) for key, count in pattern_hits.items()
    )
    active_categories = sum(count > 0 for count in pattern_hits.values())
    if active_categories >= 3:
        lexical_component += min(12.0, (active_categories - 2) * 3.0)
    lexical_component = min(60.0, lexical_component)
    repetition_component = min(20.0, repeated_openings * 4.0)
    uniformity_component = 0.0
    sent_cv = coefficient_of_variation(sent_lengths)
    para_cv = coefficient_of_variation(para_lengths)
    if len(sent_lengths) >= 4 and sent_cv < 0.22:
        uniformity_component += 10.0
    if len(para_lengths) >= 3 and para_cv < 0.18:
        uniformity_component += 8.0
    low_variety_component = 0.0
    if len(toks) >= 80 and unique_ratio < 0.38:
        low_variety_component = min(12.0, (0.38 - unique_ratio) * 80)
    risk = round(min(100.0, lexical_component + repetition_component + uniformity_component + low_variety_component), 1)

    return {
        "disclaimer": "Language-pattern diagnostic only; not an AI-authorship detector.",
        "characters_no_space": chars,
        "sentences": len(sents),
        "paragraphs": len(paras),
        "tokens": len(toks),
        "formulaic_hits": total_hits,
        "formulaic_hits_per_1000_chars": round(density, 2),
        "formulaic_risk_0_100": risk,
        "pattern_hits": pattern_hits,
        "examples": {k: v for k, v in examples.items() if v},
        "repeated_sentence_openings": repeated_openings,
        "sentence_length_mean": round(statistics.mean(sent_lengths), 2) if sent_lengths else 0.0,
        "sentence_length_cv": round(sent_cv, 3),
        "paragraph_length_cv": round(para_cv, 3),
        "token_variety_ratio": round(unique_ratio, 3),
        "citation_markers": citations,
        "numeric_anchors": numeric_anchors,
    }


def to_markdown(result: dict, label: str) -> str:
    lines = [f"# Language audit: {label}", "", f"> {result['disclaimer']}", ""]
    lines += [
        f"- Formulaic risk: **{result['formulaic_risk_0_100']}/100**",
        f"- Pattern density: **{result['formulaic_hits_per_1000_chars']} per 1,000 non-space characters**",
        f"- Sentences / paragraphs: {result['sentences']} / {result['paragraphs']}",
        f"- Sentence-length CV: {result['sentence_length_cv']}",
        f"- Token variety ratio: {result['token_variety_ratio']}",
        "",
        "## Pattern counts",
        "",
    ]
    for key, value in result["pattern_hits"].items():
        lines.append(f"- {key}: {value}")
    if result["examples"]:
        lines += ["", "## Examples to inspect", ""]
        for key, values in result["examples"].items():
            lines.append(f"- {key}: " + "; ".join(f"`{v}`" for v in values))
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args()
    text = args.path.read_text(encoding="utf-8")
    result = audit_text(text)
    if args.format == "markdown":
        print(to_markdown(result, args.path.name))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
