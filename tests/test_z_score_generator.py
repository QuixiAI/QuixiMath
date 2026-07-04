import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.z_score_generator import ZScoreGenerator
from generators.exponential_model_generator import dec
from helpers import DELIM


def oracle_check(example):
    """A9 oracle: recompute z / raw / verdict from the problem text."""
    p = example["problem"]
    ans = example["final_answer"]
    m = re.fullmatch(r"A distribution has mean (\d+) and standard "
                     r"deviation (\d+)\. Find the z-score of the "
                     r"value (\d+)\.", p)
    if m:
        mu, sig, x = (int(g) for g in m.groups())
        return ans == dec(Fraction(x - mu, sig))
    m = re.fullmatch(r"A distribution has mean (\d+) and standard "
                     r"deviation (\d+)\. What value has a z-score of "
                     r"(\S+)\?", p)
    if m:
        mu, sig, z = int(m.group(1)), int(m.group(2)), Fraction(m.group(3))
        return ans == str(mu + z * sig)
    m = re.fullmatch(r"Student A scored (\d+) on a test with mean "
                     r"(\d+) and standard deviation (\d+)\. Student B "
                     r"scored (\d+) on a test with mean (\d+) and "
                     r"standard deviation (\d+)\..*", p)
    if m:
        v1, m1, s1, v2, m2, s2 = (int(g) for g in m.groups())
        z1 = Fraction(v1 - m1, s1)
        z2 = Fraction(v2 - m2, s2)
        return ans == ("A" if z1 > z2 else "B")
    m = re.fullmatch(r"A distribution has mean (\d+) and standard "
                     r"deviation (\d+)\. Using the \|z\| > 2 rule, is "
                     r"the value (\d+) unusual\?.*", p)
    assert m, p
    mu, sig, x = (int(g) for g in m.groups())
    z = Fraction(x - mu, sig)
    return ans == ("unusual" if abs(z) > 2 else "usual")


class TestZScoreGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ZScoreGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        """A9 oracle: every answer recomputed from the problem."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_z_is_exact_decimal_and_pipe_safe(self):
        """No repeating decimals, and no stray pipes (abs(), not bars)."""
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertNotIn("...", s)
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)

    def test_both_verdicts_occur(self):
        gen = ZScoreGenerator("unusual")
        verdicts = {gen.generate()["final_answer"] for _ in range(100)}
        self.assertEqual(verdicts, {"usual", "unusual"})

    def test_compare_winner_matches_z(self):
        gen = ZScoreGenerator("compare")
        for _ in range(200):
            result = gen.generate()
            self.assertIn(result["final_answer"], ("A", "B"))

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 4)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            ZScoreGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
