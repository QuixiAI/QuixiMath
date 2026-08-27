import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.chi_square_generator import ChiSquareGenerator, exact
from helpers import DELIM


def oracle_chi(problem):
    """Recompute χ² from the counts in the problem text alone."""
    m = re.search(r"observed counts by category: (.*?); each expected "
                  r"count is (\d+)", problem)
    if m:
        obs = [int(value) for value in re.findall(r"=([0-9]+)", m.group(1))]
        E = int(m.group(2))
        return sum(Fraction((o - E) ** 2, E) for o in obs)
    m = re.search(r"counts: (\d+), (\d+); (\d+), (\d+); N = (\d+)",
                  problem)
    assert m, problem
    o11, o12, o21, o22, N = (int(g) for g in m.groups())
    R1, R2 = o11 + o12, o21 + o22
    C1, C2 = o11 + o21, o12 + o22
    Es = [Fraction(R1 * C1, N), Fraction(R1 * C2, N),
          Fraction(R2 * C1, N), Fraction(R2 * C2, N)]
    Os = [o11, o12, o21, o22]
    return sum(Fraction((o - e) ** 2) / e for o, e in zip(Os, Es))


def oracle_check(example):
    p = example["problem"]
    ans = example["final_answer"]
    chi = oracle_chi(p)
    crit = Fraction(re.search(r"critical value of ([\d.]+)", p).group(1))
    if "test statistic" in p:
        return ans == exact(chi)
    want = "reject H0" if chi > crit else "fail to reject H0"
    ans = ans.split(" (")[0]
    return ans == want


class TestChiSquareGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ChiSquareGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        """A9 oracle: recompute χ² and the decision from the text."""
        for _ in range(1000):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_critical_value_and_formula(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertRegex(result["problem"], r"critical value of [\d.]+")
            self.assertTrue(any(s.startswith(f"CHI_FORMULA{DELIM}")
                                for s in result["steps"]))

    def test_expected_table_for_independence(self):
        for v in ("independence_stat", "independence_decision"):
            gen = ChiSquareGenerator(v)
            for _ in range(50):
                result = gen.generate()
                exp = [s for s in result["steps"]
                       if s.startswith(f"EXP_CELL{DELIM}")]
                self.assertEqual(len(exp), 4, result["steps"])

    def test_both_decisions_occur(self):
        for v in ("gof_decision", "independence_decision"):
            gen = ChiSquareGenerator(v)
            verdicts = {gen.generate()["final_answer"] for _ in range(400)}
            heads = {v.split(" (")[0] for v in verdicts}
            self.assertIn("reject H0", heads)
            self.assertIn("fail to reject H0", heads)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 4)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            ChiSquareGenerator("bogus")

    def test_step_arithmetic_and_expected_cells(self):
        for _ in range(500):
            result = self.gen.generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "EXP_CELL":
                    match = re.fullmatch(r"\((\d+)·(\d+)\)/(\d+)", fields[1])
                    self.assertIsNotNone(match, raw)
                    row, column, total = map(int, match.groups())
                    self.assertEqual(Fraction(row * column, total),
                                     Fraction(fields[2]), raw)
                elif fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw)

    def test_widened_labels_and_phrasings_vary(self):
        problems = {self.gen.generate()["problem"] for _ in range(1000)}
        self.assertGreater(len(problems), 990)
        joined = "\n".join(problems)
        self.assertIn("observed counts by category", joined)
        self.assertIn("Independence table data", joined)


if __name__ == "__main__":
    unittest.main()
