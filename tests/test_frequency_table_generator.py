import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.frequency_table_generator import FrequencyTableGenerator
from helpers import DELIM


def parse_table(problem):
    """All (label, freq) pairs in the embedded table."""
    return [(lbl, int(f))
            for lbl, f in re.findall(r"([\w-]+): (\d+)", problem)]


def oracle_check(example):
    p = example["problem"]
    ans = example["final_answer"]
    pairs = parse_table(p)
    labels = [lbl for lbl, _ in pairs]
    freqs = [f for _, f in pairs]
    if "in total" in p:
        return ans == str(sum(freqs))
    if "the mode" in p:
        top = max(freqs)
        return (freqs.count(top) == 1 and
                ans == labels[freqs.index(top)])
    m = re.search(r"relative frequency of (\w+)\?", p)
    if m:
        cat = m.group(1)
        f = dict(pairs)[cat]
        return ans == str(Fraction(f, sum(freqs)))
    m = re.search(r"through the ([\w-]+) bin", p)
    if m:
        cut = labels.index(m.group(1))
        return ans == str(sum(freqs[:cut + 1]))
    m = re.search(r"at least (\d+)\?", p)
    assert m, p
    lo = int(m.group(1))
    total = sum(f for lbl, f in pairs
                if int(lbl.split("-")[0]) >= lo)
    return ans == str(total)


class TestFrequencyTableGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = FrequencyTableGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_recompute_from_table(self):
        """A9 oracle: recompute every answer from the embedded table."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_setup_step_present_and_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(result["steps"][0]
                            .startswith(f"FREQ_SETUP{DELIM}"))
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)

    def test_mode_is_unique(self):
        gen = FrequencyTableGenerator("mode")
        for _ in range(200):
            result = gen.generate()
            freqs = [f for _, f in parse_table(result["problem"])]
            top = max(freqs)
            self.assertEqual(freqs.count(top), 1, result["problem"])

    def test_relative_is_reduced_fraction(self):
        gen = FrequencyTableGenerator("relative")
        for _ in range(200):
            result = gen.generate()
            frac = Fraction(result["final_answer"])
            self.assertEqual(str(frac), result["final_answer"])

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(200):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 5)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            FrequencyTableGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
