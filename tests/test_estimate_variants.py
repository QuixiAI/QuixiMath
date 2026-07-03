import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.long_division_generator import LongDivisionGenerator
from generators.multi_digit_multiplication_generator import (
    MultiDigitMultiplicationGenerator,
    sig1,
)
from helpers import DELIM


class TestEstimateVariants(unittest.TestCase):
    def test_sig1(self):
        for n, expected in ((14, 10), (15, 20), (95, 100), (7, 7),
                            (44444, 40000), (99999, 100000), (250, 300)):
            self.assertEqual(sig1(n), expected, n)

    def test_multiplication_estimate_oracle(self):
        """ESTIMATE must round each factor to 1 sig fig; ESTIMATE_CHECK must
        carry the true estimate and exact product; ratio stays sane."""
        random.seed(7)
        gen = MultiDigitMultiplicationGenerator(estimate=True)
        for _ in range(300):
            res = gen.generate()
            self.assertEqual(res["operation"],
                             "multi_digit_multiplication_estimated")
            self.assertEqual(res["grade_level"], "middle")
            top, bottom = (int(v) for v in res["problem"].split(" * "))
            est_step = next(s for s in res["steps"]
                            if s.startswith(f"ESTIMATE{DELIM}"))
            f = est_step.split(DELIM)
            m = re.fullmatch(r"(\d+) × (\d+) ≈ (\d+) × (\d+)", f[1])
            self.assertIsNotNone(m, est_step)
            self.assertEqual((int(m.group(1)), int(m.group(2))), (top, bottom))
            self.assertEqual((int(m.group(3)), int(m.group(4))),
                             (sig1(top), sig1(bottom)))
            self.assertEqual(int(f[2]), sig1(top) * sig1(bottom))

            chk = next(s for s in res["steps"]
                       if s.startswith(f"ESTIMATE_CHECK{DELIM}"))
            cf = chk.split(DELIM)
            self.assertEqual(int(cf[1]), int(f[2]))
            self.assertEqual(int(cf[2]), int(res["final_answer"]))
            ratio = int(res["final_answer"]) / int(f[2])
            self.assertTrue(0.25 < ratio < 4, chk)

    def test_division_estimate_oracle(self):
        """The compatible number must divide evenly and be the closest such
        round number; the check compares against the exact quotient."""
        random.seed(9)
        gen = LongDivisionGenerator(estimate=True)
        checked = 0
        for _ in range(300):
            res = gen.generate()
            dividend, divisor = (int(v) for v in res["problem"].split(" / "))
            if dividend < divisor:
                continue
            est_step = next(s for s in res["steps"]
                            if s.startswith(f"ESTIMATE{DELIM}"))
            f = est_step.split(DELIM)
            m = re.fullmatch(r"(\d+) ÷ (\d+) ≈ (\d+) ÷ (\d+)", f[1])
            self.assertIsNotNone(m, est_step)
            est_dividend, est_q = int(m.group(3)), int(f[2])
            self.assertEqual(est_dividend % divisor, 0)
            self.assertEqual(est_dividend // divisor, est_q)
            # est_q is m×10^t with a single significant digit
            self.assertRegex(str(est_q), r"^[1-9]0*$")

            chk = next(s for s in res["steps"]
                       if s.startswith(f"ESTIMATE_CHECK{DELIM}"))
            cf = chk.split(DELIM)
            exact_q = int(res["final_answer"].split(" R")[0])
            self.assertEqual(int(cf[1]), est_q)
            self.assertEqual(int(cf[2]), exact_q)
            checked += 1
        self.assertGreater(checked, 250)

    def test_base_instances_unchanged(self):
        random.seed(3)
        for gen in (MultiDigitMultiplicationGenerator(),
                    LongDivisionGenerator()):
            for _ in range(50):
                res = gen.generate()
                self.assertNotIn("estimated", res["operation"])
                self.assertFalse(any(s.startswith(f"ESTIMATE{DELIM}") or
                                     s.startswith(f"ESTIMATE_CHECK{DELIM}")
                                     for s in res["steps"]))


if __name__ == "__main__":
    unittest.main()
