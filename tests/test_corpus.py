import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class CorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = [json.loads(line) for line in (ROOT / "benchmark" / "generated-360.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]

    def test_scale_and_balance(self):
        self.assertEqual(len(self.cases), 360)
        self.assertEqual(sum(c["language"] == "zh" for c in self.cases), 180)
        self.assertEqual(sum(c["language"] == "en" for c in self.cases), 180)
        self.assertEqual(len({c["paper_id"] for c in self.cases}), 12)

    def test_all_sections_present(self):
        self.assertEqual({c["section"] for c in self.cases}, {"abstract", "introduction", "literature", "methods", "case-analysis", "discussion"})

    def test_legitimate_contrasts_are_preserved(self):
        cases = [c for c in self.cases if c["risk_type"] == "legitimate_contrast"]
        self.assertGreater(len(cases), 0)
        self.assertTrue(all(c["control"] == c["treatment"] for c in cases))

    def test_treatments_keep_scope_anchor(self):
        self.assertTrue(all(c["scope_anchor"] in c["treatment"] for c in self.cases))


if __name__ == "__main__":
    unittest.main()
