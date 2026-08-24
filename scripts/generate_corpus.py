#!/usr/bin/env python3
"""Generate a deterministic, synthetic bilingual copyediting benchmark.

The output contains 12 imitation papers × 30 paired paragraphs = 360 cases.
All facts are synthetic. Control and treatment retain the same semantic payload.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path


PAPERS = [
    {"id":"zh-parametric-studio","language":"zh","title":"参数化设计课中的媒介切换","object":"参数化设计课","artifact":"实时渲染界面","site":"两所建筑院校","actor":"教师与学生"},
    {"id":"zh-museum-interface","language":"zh","title":"入口触摸屏与博物馆动线","object":"博物馆入口区","artifact":"触摸屏导览","site":"三座城市博物馆","actor":"参观者"},
    {"id":"zh-media-facade","language":"zh","title":"环境数据驱动的媒体立面","object":"媒体立面","artifact":"空气质量传感系统","site":"一个城市广场","actor":"维护团队"},
    {"id":"zh-bim-coordination","language":"zh","title":"BIM协调会议中的问题分配","object":"BIM协调会议","artifact":"碰撞报告","site":"一家建筑事务所","actor":"项目团队"},
    {"id":"zh-ar-navigation","language":"zh","title":"增强现实导航与街道注意","object":"街道导航试验","artifact":"增强现实导航界面","site":"两个历史街区","actor":"参与者"},
    {"id":"zh-generative-design","language":"zh","title":"生成模型与方案差异性","object":"早期方案生成","artifact":"文本到图像模型","site":"四个设计小组","actor":"设计师"},
    {"id":"en-parametric-studio","language":"en","title":"Media switching in parametric studios","object":"parametric-design reviews","artifact":"real-time rendering interface","site":"two architecture schools","actor":"tutors and students"},
    {"id":"en-museum-interface","language":"en","title":"Entrance screens and museum routes","object":"museum entrance zones","artifact":"touchscreen guide","site":"three city museums","actor":"visitors"},
    {"id":"en-media-facade","language":"en","title":"Environmental data on a media façade","object":"media façade","artifact":"air-quality sensing system","site":"one civic square","actor":"maintenance team"},
    {"id":"en-bim-coordination","language":"en","title":"Issue allocation in BIM meetings","object":"BIM coordination meetings","artifact":"clash report","site":"one architecture practice","actor":"project teams"},
    {"id":"en-ar-navigation","language":"en","title":"AR navigation and street attention","object":"street-navigation trial","artifact":"augmented-reality guide","site":"two historic districts","actor":"participants"},
    {"id":"en-generative-design","language":"en","title":"Generative models and design variation","object":"early-stage option generation","artifact":"text-to-image model","site":"four design teams","actor":"designers"},
]

SECTIONS = ["abstract", "introduction", "literature", "methods", "case-analysis", "discussion"]
RISKS = [
    "paired_escalation", "manufactured_contrast", "ceremonial_frame", "navigation",
    "inflated_lexicon", "vague_action", "uniform_opening", "term_instability",
    "hedge_preservation", "legitimate_contrast",
]


def zh_case(paper: dict, section: str, idx: int, risk: str) -> dict:
    n = 12 + (idx * 7 + len(paper["id"])) % 37
    m = 2 + (idx * 3) % 8
    pct = 14 + (idx * 11) % 53
    obj, art, site, actor = paper["object"], paper["artifact"], paper["site"], paper["actor"]
    facts = f"本段涉及{site}的{obj}。材料包含{n}次记录，其中{m}次出现{art}中断；中断后的任务耗时增加{pct}%。结论仅适用于该样本。"
    if risk == "manufactured_contrast":
        facts = f"{art}中断属于技术故障，也与任务耗时延长相关。{n}次记录中有{m}次中断；中断后的耗时增加{pct}%。结论仅适用于{site}。"
    elif risk == "hedge_preservation":
        facts = f"{n}次记录中有{m}次{art}中断，中断后的任务耗时增加{pct}%。这一模式可能反映技术连续性与任务耗时的关联；样本仅来自{site}。"
    elif risk == "legitimate_contrast":
        facts = f"发生故障的不是备用纸质图纸，而是{art}。{n}次任务中有{m}次故障，故障后的耗时增加{pct}%；结论仅适用于{site}。"
    pairs = {
        "paired_escalation": (
            f"研究不仅考察了{site}的{obj}，而且分析了{art}中断带来的任务变化。{n}次记录中有{m}次中断，中断后的任务耗时增加{pct}%。结论仅适用于该样本。",
            f"研究考察{site}的{obj}，并分析{art}中断后的任务变化。{n}次记录中有{m}次中断；中断后的任务耗时增加{pct}%。结论限于该样本。"),
        "manufactured_contrast": (
            f"{art}的中断不是单纯的技术故障，而是与任务耗时变化相关的操作事件。{n}次记录中有{m}次中断，中断后的任务耗时增加{pct}%。该结果限于{site}。",
            f"{art}中断属于技术故障，也与任务耗时变化相关。{n}次记录中有{m}次中断；中断后的任务耗时增加{pct}%。该结果限于{site}。"),
        "ceremonial_frame": (
            f"随着数字媒介的不断发展，{obj}中的技术中断日益值得关注。研究记录{n}次任务，其中{m}次发生{art}中断；中断后的耗时增加{pct}%。结论仅适用于该样本。",
            f"研究记录{site}{obj}中的{n}次任务。{art}在其中{m}次任务中中断；中断后的耗时增加{pct}%。结论仅适用于该样本。"),
        "navigation": (
            f"首先，研究收集{n}次记录。其次，其中{m}次出现{art}中断。此外，中断后的任务耗时增加{pct}%。最后，该结果仅适用于{site}。",
            f"研究收集{n}次记录，其中{m}次出现{art}中断。中断后的任务耗时增加{pct}%；这一结果仅适用于{site}。"),
        "inflated_lexicon": (
            f"对{obj}的全面而系统的考察揭示了{art}中断的关键影响。{n}次记录中有{m}次中断，并呈现出耗时增加{pct}%的显著趋势。该复杂结果限于当前样本。",
            f"对{site}{obj}的考察记录到{m}次{art}中断，共观察{n}次任务。中断后的任务耗时增加{pct}%；该结果限于当前样本。"),
        "vague_action": (
            f"研究对{site}的{obj}进行了系统分析，并对{art}中断后的耗时变化进行了考察。{n}次记录中有{m}次中断，耗时增加{pct}%。",
            f"研究分析{site}{obj}的{n}次记录。{art}在其中{m}次中断；中断后的耗时增加{pct}%。结论仅适用于该样本。"),
        "uniform_opening": (
            f"研究记录了{n}次任务。研究识别出{m}次{art}中断。研究测得中断后耗时增加{pct}%。研究将结论限定于{site}。",
            f"研究在{site}记录{n}次任务，并识别出{m}次{art}中断。中断后的耗时增加{pct}%；结论范围为{site}。"),
        "term_instability": (
            f"{actor}在{obj}中使用{art}。该数字平台在{n}次记录中中断{m}次；这一虚拟工具失效后，任务耗时增加{pct}%。",
            f"{actor}在{site}的{obj}中使用{art}。{art}在{n}次记录中中断{m}次；中断后，任务耗时增加{pct}%。结论仅适用于该样本。"),
        "hedge_preservation": (
            f"{n}次记录中有{m}次{art}中断，中断后的任务耗时增加{pct}%。这一结果可能说明技术连续性与任务耗时有关，但样本仅来自{site}。",
            f"{art}在{n}次记录中中断{m}次；中断后的任务耗时增加{pct}%。这一结果可能反映技术连续性与任务耗时的关联，但样本仅来自{site}。"),
        "legitimate_contrast": (
            f"记录显示，发生故障的不是备用纸质图纸，而是{art}。{n}次任务中有{m}次故障，故障后的耗时增加{pct}%；结论限于{site}。",
            f"记录显示，发生故障的不是备用纸质图纸，而是{art}。{n}次任务中有{m}次故障，故障后的耗时增加{pct}%；结论限于{site}。"),
    }
    control, treatment = pairs[risk]
    return {"source": facts, "control": control, "treatment": treatment}


def en_case(paper: dict, section: str, idx: int, risk: str) -> dict:
    n = 12 + (idx * 7 + len(paper["id"])) % 37
    m = 2 + (idx * 3) % 8
    pct = 14 + (idx * 11) % 53
    obj, art, site, actor = paper["object"], paper["artifact"], paper["site"], paper["actor"]
    facts = f"This paragraph concerns {obj} at {site}. The material includes {n} records; {art} failed in {m}, after which task time rose by {pct}%. The claim is limited to this sample."
    if risk == "manufactured_contrast":
        facts = f"The {art} failures were technical faults associated with longer tasks. The system failed in {m} of {n} records; task time then rose by {pct}%. The claim is limited to {site}."
    elif risk == "hedge_preservation":
        facts = f"The {art} failed in {m} of {n} records, after which task time rose by {pct}%. This pattern may reflect an association between technical continuity and task duration; the sample comes only from {site}."
    elif risk == "legitimate_contrast":
        facts = f"The failure affected not the backup paper drawings but the {art}. It failed in {m} of {n} tasks, after which time rose by {pct}%; the claim is limited to {site}."
    pairs = {
        "paired_escalation": (
            f"The study not only examines {obj} at {site} but also analyzes task changes after {art} failures. The interface failed in {m} of {n} records, and task time then rose by {pct}%. The claim is limited to this sample.",
            f"The study examines {obj} at {site} and analyzes task changes after {art} failures. The interface failed in {m} of {n} records; task time then rose by {pct}%. The claim is limited to this sample."),
        "manufactured_contrast": (
            f"The failure of the {art} is not merely a technical fault but an operational event associated with longer tasks. It failed in {m} of {n} records, after which task time rose by {pct}%. The result applies only to {site}.",
            f"The {art} failures were technical faults associated with longer tasks. The system failed in {m} of {n} records; task time then rose by {pct}%. The result applies only to {site}."),
        "ceremonial_frame": (
            f"In today's rapidly evolving digital landscape, technical interruptions in {obj} have become increasingly important. Across {n} records, the {art} failed {m} times; task time then rose by {pct}%. The result is limited to this sample.",
            f"We examined {n} records of {obj} at {site}. The {art} failed {m} times; task time then rose by {pct}%. The result is limited to this sample."),
        "navigation": (
            f"Firstly, the study collected {n} records. Secondly, the {art} failed in {m}. Moreover, task time rose by {pct}% after failure. Finally, the result applies only to {site}.",
            f"The study collected {n} records, including {m} {art} failures. Task time rose by {pct}% after failure; the result applies only to {site}."),
        "inflated_lexicon": (
            f"A comprehensive and robust examination of {obj} reveals the pivotal impact of {art} failure. The system failed in {m} of {n} records, producing a significant {pct}% increase in task time. This multifaceted finding is limited to the sample.",
            f"At {site}, the {art} failed in {m} of {n} records of {obj}. Task time rose by {pct}% after failure. This finding is limited to the sample."),
        "vague_action": (
            f"The study conducted a systematic investigation of {obj} and undertook an analysis of task-time changes following {art} failure. Of {n} records, {m} contained failures, with time increasing by {pct}%.",
            f"We analyzed {n} records of {obj} at {site}. The {art} failed in {m}; task time then rose by {pct}%. The claim is limited to this sample."),
        "uniform_opening": (
            f"The study recorded {n} tasks. The study identified {m} {art} failures. The study measured a {pct}% increase in task time after failure. The study limits the finding to {site}.",
            f"At {site}, the study recorded {n} tasks and identified {m} {art} failures. Task time rose by {pct}% after failure; the finding is limited to {site}."),
        "term_instability": (
            f"{actor.capitalize()} used the {art} during {obj}. This digital platform failed in {m} of {n} records; after the virtual tool stopped, task time rose by {pct}%.",
            f"At {site}, {actor} used the {art} during {obj}. The {art} failed in {m} of {n} records; task time then rose by {pct}%. The claim is limited to this sample."),
        "hedge_preservation": (
            f"The {art} failed in {m} of {n} records, after which task time rose by {pct}%. This pattern may indicate an association between technical continuity and task duration, but the sample comes only from {site}.",
            f"The {art} failed in {m} of {n} records; task time then rose by {pct}%. The pattern may reflect an association between technical continuity and task duration, but the sample comes only from {site}."),
        "legitimate_contrast": (
            f"The records show that the failure affected not the backup paper drawings but the {art}. It failed in {m} of {n} tasks, after which time rose by {pct}%; the claim is limited to {site}.",
            f"The records show that the failure affected not the backup paper drawings but the {art}. It failed in {m} of {n} tasks, after which time rose by {pct}%; the claim is limited to {site}."),
    }
    control, treatment = pairs[risk]
    return {"source": facts, "control": control, "treatment": treatment}


def generate() -> list[dict]:
    cases = []
    for paper in PAPERS:
        paragraph = 0
        for section in SECTIONS:
            for local_idx in range(5):
                risk = RISKS[(paragraph + len(paper["id"])) % len(RISKS)]
                payload = (zh_case if paper["language"] == "zh" else en_case)(paper, section, paragraph, risk)
                cases.append({
                    "id": f"{paper['id']}-{paragraph + 1:02d}",
                    "paper_id": paper["id"],
                    "paper_title": paper["title"],
                    "language": paper["language"],
                    "section": section,
                    "paragraph_index": paragraph + 1,
                    "risk_type": risk,
                    "scope_anchor": paper["site"],
                    **payload,
                })
                paragraph += 1
    return cases


def write_outputs(root: Path, sample_size: int = 36) -> None:
    cases = generate()
    root.mkdir(parents=True, exist_ok=True)
    (root / "generated-360.jsonl").write_text(
        "\n".join(json.dumps(c, ensure_ascii=False) for c in cases) + "\n", encoding="utf-8"
    )
    paper_dir = root / "papers"
    paper_dir.mkdir(exist_ok=True)
    for paper in PAPERS:
        selected = [c for c in cases if c["paper_id"] == paper["id"]]
        lines = [f"# {paper['title']}", "", "> Synthetic imitation paper for language evaluation; all facts are fictional.", ""]
        current = None
        for case in selected:
            if case["section"] != current:
                current = case["section"]
                lines += [f"## {current}", ""]
            lines += [f"### Paragraph {case['paragraph_index']} — {case['risk_type']}", "", "**Control**", "", case["control"], "", "**Skill edit**", "", case["treatment"], ""]
        (paper_dir / f"{paper['id']}.md").write_text("\n".join(lines), encoding="utf-8")

    # Stratified sample: one item per language × section × first three risk rotations.
    rng = random.Random(20260824)
    buckets = {}
    for case in cases:
        buckets.setdefault((case["language"], case["section"]), []).append(case)
    sample = []
    per_bucket = sample_size // len(buckets)
    for key in sorted(buckets):
        sample.extend(rng.sample(buckets[key], per_bucket))
    labels = {}
    blind = []
    for case in sample:
        treatment_is_a = rng.choice([True, False])
        labels[case["id"]] = "A" if treatment_is_a else "B"
        blind.append({
            "id": case["id"], "language": case["language"], "section": case["section"],
            "risk_type": case["risk_type"], "source": case["source"],
            "A": case["treatment"] if treatment_is_a else case["control"],
            "B": case["control"] if treatment_is_a else case["treatment"],
        })
    (root / "blind-sample-36.json").write_text(json.dumps(blind, ensure_ascii=False, indent=2), encoding="utf-8")
    (root / "blind-labels-36.json").write_text(json.dumps(labels, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    write_outputs(args.output)
    print("generated 12 papers, 360 paired cases, 720 edited paragraphs, and a 36-case blind sample")


if __name__ == "__main__":
    main()
