import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
from style_audit import audit_text


class StyleAuditTests(unittest.TestCase):
    def test_formulaic_chinese_scores_higher(self):
        formulaic = "随着数字技术的不断发展，建筑学发生了深刻变化。这不仅重塑了设计，而且赋能了实践。综上所述，该研究具有重要意义。"
        specific = "团队在三次评图中使用实时渲染调整材质参数。访谈记录显示，修改集中在评图后的二十分钟内；这一结果只适用于该课程。"
        self.assertGreater(audit_text(formulaic)["formulaic_risk_0_100"], audit_text(specific)["formulaic_risk_0_100"])

    def test_formulaic_english_scores_higher(self):
        formulaic = "In today's rapidly evolving landscape, this study not only delves into a multifaceted realm but also offers a transformative framework."
        specific = "The study compares logs from two museum interfaces and reports three recurring navigation errors."
        self.assertGreater(audit_text(formulaic)["formulaic_risk_0_100"], audit_text(specific)["formulaic_risk_0_100"])

    def test_disclaimer_is_present(self):
        self.assertIn("not an AI-authorship detector", audit_text("测试。")['disclaimer'])

    def test_single_warranted_contrast_is_only_a_low_risk_cue(self):
        text = "这不是承重墙，而是后期加建的隔墙；现场拆除记录与材料接缝均支持这一判断。"
        result = audit_text(text)
        self.assertEqual(result["pattern_hits"]["manufactured_contrast"], 1)
        self.assertLessEqual(result["formulaic_risk_0_100"], 10)

    def test_new_language_detail_patterns_are_visible(self):
        text = "在此基础上，从另一个层面来看，数据连续性的稳定性下降带来了效率变化的发生。因此，本段表明这一关系十分关键。"
        result = audit_text(text)
        self.assertGreater(result["pattern_hits"]["empty_transition"], 0)
        self.assertGreater(result["pattern_hits"]["abstract_shell"], 0)
        self.assertGreater(result["pattern_hits"]["conclusion_echo"], 0)

    def test_chinese_numeric_anchors_adjacent_to_characters(self):
        result = audit_text("共记录42次任务，其中7次中断，耗时增加18%。")
        self.assertEqual(result["numeric_anchors"], 3)


if __name__ == "__main__":
    unittest.main()
