import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.proportion_word_problem_generator import (
    ProportionWordProblemGenerator,
)
from generators.exponential_model_generator import money
from helpers import DELIM


def oracle_answer(problem):
    """Recompute from the problem text alone (A9).

    The core (up to the first '?') holds exactly three numbers; the
    scenario keyword fixes which are numerator/denominator/query.
    """
    core = problem[: problem.index("?") + 1]
    nums = [int(n) for n in re.findall(r"\d+", core)]
    n0, n1, n2 = nums
    if "miles" in core:
        x, unit = Fraction(n0 * n2, n1), "mi"
    elif "cups" in core:
        x, unit = Fraction(n0 * n2, n1), "cups"
    elif "pounds" in core:
        x, unit = Fraction(n1 * n2, n0), "money"
    else:  # ratio table
        x, unit = Fraction(n1 * n2, n0), "plain"
    if unit == "money":
        return money(x)
    if unit == "plain":
        return str(x.numerator) if x.denominator == 1 else str(x)
    return f"{x.numerator if x.denominator == 1 else x} {unit}"


class TestProportionWordProblemGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ProportionWordProblemGenerator()
        self.dgen = ProportionWordProblemGenerator(distractor=True)

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_recompute_plain(self):
        """A9 oracle: recompute from the problem text."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result["problem"]),
                             result["final_answer"], result["problem"])

    def test_oracle_recompute_with_distractor(self):
        for _ in range(500):
            result = self.dgen.generate()
            self.assertEqual(oracle_answer(result["problem"]),
                             result["final_answer"], result["problem"])

    def test_cross_multiplication_steps(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertTrue(any(s.startswith(f"PROP_SETUP{DELIM}")
                                for s in result["steps"]))
            self.assertTrue(any(s.startswith(f"D{DELIM}")
                                for s in result["steps"]))

    def test_division_is_exact(self):
        """The cross-product must divide evenly (integer answer)."""
        for _ in range(300):
            result = self.gen.generate()
            d_step = next(s for s in result["steps"]
                          if s.startswith(f"D{DELIM}"))
            _, num, den, quot = d_step.split(DELIM)
            self.assertEqual(int(num) % int(den), 0, result["problem"])
            self.assertEqual(int(num) // int(den), int(quot))

    def test_distractor_first_step_selects_data(self):
        for _ in range(200):
            result = self.dgen.generate()
            self.assertTrue(result["steps"][0]
                            .startswith(f"SELECT_RELEVANT{DELIM}"))

    def test_multiple_phrasings_occur(self):
        openings = {self.gen.generate()["problem"][:16]
                    for _ in range(300)}
        self.assertGreaterEqual(len(openings), 6)

    def test_fixed_flag_constructor(self):
        gen = ProportionWordProblemGenerator(distractor=True)
        self.assertTrue(gen.generate()["operation"].endswith("distractor"))


if __name__ == "__main__":
    unittest.main()
