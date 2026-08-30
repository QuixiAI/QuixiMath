"""Prompt-only oracle for PipelineCompositionGenerator (depth strand)."""
import random
import re
import unittest

from generators.pipeline_composition_generator import (
    PipelineCompositionGenerator)
from helpers import DELIM
from depth_common import TIER_FLOORS
from applied_common import method_word_hits
from tests.conventions_common import assert_contract, assert_pipe_safe
from tests.depth_oracle import (chain_depth, milestone_violations,
                                parse_count, record_chars)

_START = re.compile(r"(?:starts at|from|order of|Track) (\d+) items")

#: sentence grammar -> the exact transformation it encodes
_SENTENCES = (
    (re.compile(r"demand grows the count by (\d+) for every 100"),
     lambda v, m: v + v * int(m.group(1)) // 100),
    (re.compile(r"spoilage removes (\d+) of every 100"),
     lambda v, m: v - v * int(m.group(1)) // 100),
    (re.compile(r"only (\d+) of every (\d+) items pass inspection"),
     lambda v, m: v * int(m.group(1)) // int(m.group(2))),
    (re.compile(r"a delivery adds (\d+) items"),
     lambda v, m: v + int(m.group(1))),
    (re.compile(r"(\d+) items are set aside"),
     lambda v, m: v - int(m.group(1))),
    (re.compile(r"each item is repacked into (\d+) smaller packs"),
     lambda v, m: v * int(m.group(1))),
    (re.compile(r"the lot is divided evenly (\d+) ways; keep one share"),
     lambda v, m: v // int(m.group(1))),
)

_SKILL_BY_INDEX = ("percent_change", "percent_change", "ratio_split",
                   "fixed_adjustment", "fixed_adjustment",
                   "unit_conversion", "ratio_split")


def _stages(problem):
    """(transform, skill) per stage — grammar-driven: the seven sentence
    shapes are matched directly across the text in positional order, so
    template punctuation (colons vs parens) cannot break parsing."""
    found = []
    for index, (pattern, fn) in enumerate(_SENTENCES):
        for match in pattern.finditer(problem):
            found.append((match.start(),
                          lambda v, fn=fn, m=match: fn(v, m),
                          _SKILL_BY_INDEX[index]))
    found.sort(key=lambda item: item[0])
    assert found, problem[:120]
    return [(transform, skill) for _, transform, skill in found]


def oracle_answer(example):
    problem = example["problem"]
    value = int(_START.search(problem).group(1))
    stages = _stages(problem)
    for transform, _ in stages:
        value = transform(value)
    if example["operation"].startswith("pipeline_composition_stage_audit"):
        return f"{value} items; {len(stages)} stages"
    return str(value)


class TestPipelineCompositionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = PipelineCompositionGenerator()

    def test_output_contract_and_depth(self):
        for _ in range(20):
            result = self.gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            tier = result["operation"].rsplit("_", 1)[1]
            self.assertGreaterEqual(chain_depth(result["steps"]),
                                    TIER_FLOORS[tier])
            self.assertFalse(milestone_violations(result["steps"]))
            self.assertLessEqual(record_chars(result), 16_000)
            self.assertIsNotNone(parse_count(result["problem"]))

    def test_oracle_recomputes_from_problem_text(self):
        for variant in PipelineCompositionGenerator.VARIANTS:
            gen = PipelineCompositionGenerator(variant)
            for _ in range(30):
                result = gen.generate()
                self.assertEqual(result["final_answer"],
                                 oracle_answer(result),
                                 result["problem"][:180])

    def test_skills_metadata_matches_the_stage_sentences(self):
        gen = PipelineCompositionGenerator("final_count", tier="d100")
        for _ in range(15):
            result = gen.generate()
            expected = [skill for _, skill in _stages(result["problem"])]
            self.assertEqual(result["skills"], expected)
            markers = [s.split(DELIM)[2] for s in result["steps"]
                       if s.startswith(f"PIPE_STAGE{DELIM}")]
            self.assertEqual(markers, expected)

    def test_story_never_names_a_method(self):
        for _ in range(60):
            result = self.gen.generate()
            self.assertEqual(method_word_hits(result["problem"]), [],
                             result["problem"][:120])

    def test_every_arithmetic_link_is_exact(self):
        gen = PipelineCompositionGenerator("final_count", tier="d200")
        for _ in range(5):
            result = gen.generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]), raw)
                elif fields[0] == "D":
                    self.assertEqual(int(fields[1]) // int(fields[2]),
                                     int(fields[3]), raw)
                    self.assertEqual(int(fields[1]) % int(fields[2]),
                                     0, raw)  # exact splits only
                elif fields[0] == "A":
                    self.assertEqual(int(fields[1]) + int(fields[2]),
                                     int(fields[3]), raw)
                elif fields[0] == "S":
                    self.assertEqual(int(fields[1]) - int(fields[2]),
                                     int(fields[3]), raw)

    def test_counts_stay_bounded(self):
        gen = PipelineCompositionGenerator("final_count", tier="d200")
        for _ in range(5):
            result = gen.generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] in ("M", "D", "A", "S"):
                    self.assertTrue(1 <= int(fields[3]) <= 2_000_000, raw)

    def test_tier_difficulty_bump(self):
        for tier, expected in (("d50", 4), ("d100", 5), ("d200", 5)):
            result = PipelineCompositionGenerator("final_count",
                                                  tier=tier).generate()
            self.assertEqual(result["difficulty"], expected)

    def test_all_variants_and_tiers_reachable(self):
        seen = set()
        for _ in range(200):
            seen.add(self.gen.generate()["operation"])
        self.assertEqual(len(seen), 6)  # 2 variants x 3 tiers

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            PipelineCompositionGenerator("bogus")
        with self.assertRaises(ValueError):
            PipelineCompositionGenerator(tier="dq")


if __name__ == "__main__":
    unittest.main()
