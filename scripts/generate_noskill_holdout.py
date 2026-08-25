#!/usr/bin/env python3
"""Generate ten synthetic no-skill imitation papers for language comparison.

The corpus contains 300 paragraphs. All entities and observations are fictional.
It is a held-out baseline: no preferred rewrites are embedded in the records.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


PAPERS = [
    {"id": "zh-soundscape", "language": "zh", "title": "交通站厅声景与停留行为", "object": "交通站厅", "device": "声压传感器", "actor": "候车者", "site": "三座换乘站"},
    {"id": "zh-digital-twin", "language": "zh", "title": "校园数字孪生中的维护记录", "object": "校园运维", "device": "数字孪生面板", "actor": "维护人员", "site": "两处大学校园"},
    {"id": "zh-lighting", "language": "zh", "title": "展厅照度反馈与观看节奏", "object": "展厅观看", "device": "自适应照明系统", "actor": "参观者", "site": "四个临时展厅"},
    {"id": "zh-robotic-fabrication", "language": "zh", "title": "机器人砌筑中的误差回传", "object": "机器人砌筑", "device": "视觉校准模块", "actor": "操作员", "site": "两个实验工位"},
    {"id": "zh-community-screen", "language": "zh", "title": "社区屏幕与公共议题参与", "object": "社区议题讨论", "device": "公共信息屏", "actor": "居民", "site": "三个街道广场"},
    {"id": "en-soundscape", "language": "en", "title": "Station soundscapes and dwell behavior", "object": "station waiting", "device": "sound-pressure sensor", "actor": "passengers", "site": "three interchange stations"},
    {"id": "en-digital-twin", "language": "en", "title": "Maintenance records in campus digital twins", "object": "campus maintenance", "device": "digital-twin dashboard", "actor": "maintenance staff", "site": "two university campuses"},
    {"id": "en-lighting", "language": "en", "title": "Illuminance feedback and viewing pace", "object": "gallery viewing", "device": "adaptive lighting system", "actor": "visitors", "site": "four temporary galleries"},
    {"id": "en-robotic-fabrication", "language": "en", "title": "Error feedback in robotic masonry", "object": "robotic masonry", "device": "vision-calibration module", "actor": "operators", "site": "two experimental cells"},
    {"id": "en-community-screen", "language": "en", "title": "Community screens and civic participation", "object": "neighborhood discussion", "device": "public information screen", "actor": "residents", "site": "three street squares"},
]

SECTIONS = ["abstract", "introduction", "related-work", "methods", "results", "discussion"]
HABITS = [
    "manufactured_contrast", "paired_escalation", "ceremonial_frame", "navigation_chain",
    "inflated_significance", "vague_action", "uniform_opening", "term_drift",
    "abstract_noun_stack", "modifier_stack", "paragraph_end_echo", "balanced_tricolon",
    "empty_transition", "overclaim", "synonym_roulette",
]


def numbers(paper: dict, index: int) -> tuple[int, int, int]:
    total = 28 + (index * 13 + len(paper["id"])) % 61
    events = 3 + (index * 5) % 12
    change = 6 + (index * 7) % 29
    return total, events, change


def source_payload(paper: dict, index: int) -> str:
    total, events, change = numbers(paper, index)
    if paper["language"] == "zh":
        return f"在{paper['site']}记录{total}次{paper['object']}活动。{paper['device']}出现{events}次数据缺口；缺口出现后，{paper['actor']}的任务时长平均增加{change}%。相关关系不能说明因果，结论限于所观察场地。"
    return f"We recorded {total} episodes of {paper['object']} at {paper['site']}. The {paper['device']} had {events} data gaps; mean task duration for {paper['actor']} rose by {change}% after a gap. The association does not establish causality and is limited to the observed sites."


def zh_noskill(p: dict, i: int, habit: str) -> str:
    total, events, change = numbers(p, i)
    obj, dev, actor, site = p["object"], p["device"], p["actor"], p["site"]
    core = f"研究共采集{total}次活动，其中{dev}出现{events}次数据缺口，缺口后{actor}的任务时长平均增加{change}%。"
    variants = {
        "manufactured_contrast": f"{dev}的数据缺口不是一个单纯的技术异常，而是连接{obj}过程与行为变化的关键事件。{core}这一关联并不等于因果，且只适用于{site}。",
        "paired_escalation": f"本研究不仅关注{site}的{obj}过程，而且进一步揭示{dev}对于{actor}行为节奏的深层影响。{core}不过，有限样本尚不能支持因果判断。",
        "ceremonial_frame": f"随着数字技术的快速发展，在智慧环境不断演进的时代背景下，{obj}日益成为值得关注的重要议题。{core}研究结论限于{site}。",
        "navigation_chain": f"首先，本研究在{site}开展观察。其次，共获得{total}次记录。此外，{dev}出现{events}次数据缺口。最后，缺口后任务时长平均增加{change}%，但该关联不代表因果。",
        "inflated_significance": f"通过全面、系统且深入的考察，本研究揭示了{dev}在{obj}中的关键作用与深远价值。{core}这一重要发现为相关领域提供了全新的视角，但仍受场地范围限制。",
        "vague_action": f"本研究对{site}的{obj}进行了系统分析，并对{dev}数据缺口所带来的行为变化进行了深入考察。{core}目前只能确认相关关系。",
        "uniform_opening": f"研究记录了{total}次活动。研究发现了{events}次数据缺口。研究测得任务时长增加{change}%。研究认为这一结果只适用于{site}，且研究不能确认因果。",
        "term_drift": f"{actor}在{obj}中使用{dev}。该数字平台在{total}次记录中出现{events}次缺口；这一交互媒介失效后，智能装置所对应的任务时长平均增加{change}%。该结果仅见于{site}。",
        "abstract_noun_stack": f"{dev}数据连续性的稳定性下降带来了{obj}任务执行效率变化的发生。{core}关于作用机制的因果性解释尚缺乏证据支撑。",
        "modifier_stack": f"研究考察了{site}中持续运行的、实时响应的、数据驱动的、面向使用者的{dev}。{core}结果不能外推至其他场地。",
        "paragraph_end_echo": f"在{site}，{core}这一结果只描述相关关系，并不构成因果证据。因此，本段表明数据缺口与任务时长存在相关关系，而不是因果关系。",
        "balanced_tricolon": f"{dev}改变了信息读取、任务判断与行动组织，也影响了时间分配、注意转移与操作节奏。{core}这些变化具有多层次、多尺度和多维度特征，但因果关系尚未建立。",
        "empty_transition": f"在此基础上，从另一个层面来看，进一步而言，{obj}呈现出新的变化趋势。{core}需要指出的是，这一关联只适用于{site}。",
        "overclaim": f"{core}这一结果充分证明{dev}决定了{actor}的行为效率，并从根本上重塑了{obj}。尽管如此，样本仅来自{site}。",
        "synonym_roulette": f"{actor}通过{dev}参与{obj}。该界面在{total}次活动中产生{events}次缺口；这一平台中断后，相关媒介所支持的任务时长平均增加{change}%。观察限于{site}，不能说明因果。",
    }
    return variants[habit]


def en_noskill(p: dict, i: int, habit: str) -> str:
    total, events, change = numbers(p, i)
    obj, dev, actor, site = p["object"], p["device"], p["actor"], p["site"]
    core = f"The study collected {total} episodes; the {dev} had {events} data gaps, after which mean task duration for {actor} increased by {change}%."
    variants = {
        "manufactured_contrast": f"The data gap was not merely a technical anomaly but a pivotal event connecting {obj} to behavioral change. {core} The association does not establish causality and applies only to {site}.",
        "paired_escalation": f"This study not only examines {obj} at {site} but also reveals the deeper influence of the {dev} on behavioral rhythms. {core} The limited sample does not support a causal claim.",
        "ceremonial_frame": f"In today's rapidly evolving digital landscape, {obj} has become an increasingly important concern. {core} The result is limited to {site}.",
        "navigation_chain": f"Firstly, observations were conducted at {site}. Secondly, {total} episodes were obtained. Moreover, the {dev} had {events} gaps. Finally, duration rose by {change}%, although the association is not causal.",
        "inflated_significance": f"A comprehensive, robust, and in-depth investigation reveals the pivotal and profound role of the {dev} in {obj}. {core} This transformative finding offers a novel lens, although it remains site-bound.",
        "vague_action": f"The study conducted a systematic investigation of {obj} and undertook an in-depth analysis of behavioral change following gaps in the {dev}. {core} Only an association can presently be inferred.",
        "uniform_opening": f"The study recorded {total} episodes. The study identified {events} data gaps. The study measured a {change}% increase in duration. The study limits the result to {site} and does not infer causality.",
        "term_drift": f"{actor.capitalize()} used the {dev} during {obj}. This digital platform had {events} gaps in {total} episodes; after the interactive medium failed, task duration supported by the smart device rose by {change}%. The result is limited to {site}.",
        "abstract_noun_stack": f"A reduction in the stability of the continuity of {dev} data resulted in the occurrence of a change in the efficiency of task performance during {obj}. {core} Evidence for causal mechanism attribution remains absent.",
        "modifier_stack": f"The study examined the continuously operating, real-time, data-driven, user-oriented, environmentally responsive {dev} at {site}. {core} The result cannot be generalized beyond these sites.",
        "paragraph_end_echo": f"At {site}, {core} The result describes association and provides no causal evidence. Therefore, the paragraph shows an associative, rather than causal, relationship between gaps and duration.",
        "balanced_tricolon": f"The {dev} shapes information reading, task judgment, and action organization while influencing time allocation, attention switching, and operational rhythm. {core} These multidimensional and multiscalar changes do not establish causality.",
        "empty_transition": f"On this basis, from another perspective, and furthermore, {obj} presents a new tendency. {core} It should be noted that the association applies only to {site}.",
        "overclaim": f"{core} This result conclusively proves that the {dev} determines behavioral efficiency and fundamentally reshapes {obj}. Nevertheless, the sample is limited to {site}.",
        "synonym_roulette": f"{actor.capitalize()} used the {dev} during {obj}. The interface had {events} gaps across {total} episodes; after the platform stopped, duration for tasks supported by the medium rose by {change}%. Observation is limited to {site} and does not establish causality.",
    }
    return variants[habit]


def generate() -> list[dict]:
    records: list[dict] = []
    for paper in PAPERS:
        for index in range(30):
            habit = HABITS[(index + len(paper["id"])) % len(HABITS)]
            records.append({
                "id": f"{paper['id']}-{index + 1:02d}",
                "paper_id": paper["id"],
                "paper_title": paper["title"],
                "language": paper["language"],
                "section": SECTIONS[index // 5],
                "paragraph_index": index + 1,
                "habit": habit,
                "source": source_payload(paper, index),
                "noskill": (zh_noskill if paper["language"] == "zh" else en_noskill)(paper, index, habit),
            })
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    records = generate()
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "no-skill-300.jsonl").write_text(
        "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n", encoding="utf-8"
    )
    paired = [
        {
            "id": record["id"], "paper_id": record["paper_id"], "language": record["language"],
            "section": record["section"], "risk_type": record["habit"], "source": record["source"],
            "control": record["noskill"], "treatment": record["source"],
        }
        for record in records
    ]
    (args.output / "holdout-300-paired.jsonl").write_text(
        "\n".join(json.dumps(record, ensure_ascii=False) for record in paired) + "\n", encoding="utf-8"
    )
    papers_dir = args.output / "no-skill-papers"
    papers_dir.mkdir(exist_ok=True)
    for paper in PAPERS:
        selected = [r for r in records if r["paper_id"] == paper["id"]]
        lines = [f"# {paper['title']}", "", "> Synthetic no-skill imitation paper; all observations are fictional.", ""]
        current = ""
        for record in selected:
            if record["section"] != current:
                current = record["section"]
                lines.extend([f"## {current}", ""])
            lines.extend([record["noskill"], ""])
        (papers_dir / f"{paper['id']}.md").write_text("\n".join(lines), encoding="utf-8")
    print("generated 10 no-skill papers and 300 paragraphs")


if __name__ == "__main__":
    main()
