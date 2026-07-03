import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.arithmetic_sequence_generator import (
    ArithmeticSequenceGenerator,
)
from helpers import DELIM


def oracle_answer(example):
    """Independently recomputes from the shown terms alone."""
    p = example["problem"]
    m = re.match(
        r"The arithmetic sequence (-?\d+), (-?\d+), (-?\d+), (-?\d+), "
        r"\.\.\. continues\. (.+)$", p)
    assert m, p
    t = [int(m.group(i)) for i in range(1, 5)]
    d = t[1] - t[0]
    assert t[2] - t[1] == d and t[3] - t[2] == d
    q = m.group(5)

    mm = re.fullmatch(r"Find the (\d+)\w\w term\.", q)
    if mm:
        n = int(mm.group(1))
        return str(t[0] + (n - 1) * d)
    mm = re.fullmatch(r"Which term of the sequence equals (-?\d+)\?", q)
    if mm:
        target = int(mm.group(1))
        n, rem = divmod(target - t[0], d)
        assert rem == 0
        return str(n + 1)
    mm = re.fullmatch(r"Find the sum of the first (\d+) terms\.", q)
    assert mm, q
    n = int(mm.group(1))
    return str(sum(t[0] + i * d for i in range(n)))


class TestArithmeticSequenceGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ArithmeticSequenceGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: recompute every variant from the shown terms."""
        for _ in range(600):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_common_diff_computed_and_verified(self):
        for _ in range(300):
            result = self.gen.generate()
            cd = next(s for s in result["steps"]
                      if s.startswith(f"COMMON_DIFF{DELIM}"))
            a, b = (int(v.strip("()")) for v in
                    cd.split(DELIM)[1].split(" - "))
            self.assertEqual(a - b, int(cd.split(DELIM)[2]), cd)
            chk = next(s for s in result["steps"]
                       if s.startswith(f"CHECK{DELIM}"))
            f = chk.split(DELIM)
            x, rest = f[2].split(" - ")
            y, claimed = rest.split(" = ")
            self.assertEqual(int(x) - int(y.strip("()")), int(claimed), chk)
            self.assertEqual(claimed, f[3], chk)

    def test_step_arithmetic(self):
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "S":
                    self.assertEqual(int(f[1]) - int(f[2]), int(f[3]), s)
                elif f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)
                elif f[0] == "D":
                    self.assertEqual(int(f[1]), int(f[2]) * int(f[3]), s)

    def test_formula_stated_before_applied(self):
        for _ in range(200):
            result = self.gen.generate()
            ops = [s.split(DELIM)[0] for s in result["steps"]]
            self.assertLess(ops.index("SEQ_FORMULA"), ops.index("SEQ_APPLY"))

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"arithmetic_sequence_nth_term",
                               "arithmetic_sequence_which_term",
                               "arithmetic_sequence_partial_sum"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            ArithmeticSequenceGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
