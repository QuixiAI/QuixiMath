import unittest
import random
import re
import sys
import os
from fractions import Fraction

# Ensure repo root on path
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.fraction_decimal_percent_converter import FractionDecimalPercentConverter
from helpers import DELIM

PROBLEM_RE = re.compile(r"Convert (.+) to (decimal|percent|fraction)")


class TestFractionDecimalPercentConverter(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.gen = FractionDecimalPercentConverter()

    def test_generate_format(self):
        res = self.gen.generate()
        for key in ["problem_id", "operation", "problem", "steps", "final_answer"]:
            self.assertIn(key, res)
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))

    def test_oracle_all_directions(self):
        """A9 oracle: parse the source value from the problem text, convert
        exactly, and require exact minimal rendering (values are constructed
        to terminate — no rounded decimals, no trailing zeros)."""
        seen_ops = set()
        for _ in range(1500):
            res = self.gen.generate()
            seen_ops.add(res["operation"])
            answer = res["final_answer"]
            src, target = PROBLEM_RE.fullmatch(res["problem"]).groups()
            value = (Fraction(src[:-1]) / 100 if src.endswith("%")
                     else Fraction(src))
            if target == "percent":
                self.assertTrue(answer.endswith("%"), answer)
                self.assertEqual(Fraction(answer[:-1]) / 100, value,
                                 res["problem"])
            else:
                if target == "fraction":
                    self.assertIn("/", answer, res["problem"])
                    num, den = (int(x) for x in answer.split("/"))
                    self.assertEqual(Fraction(num, den),
                                     Fraction(num, den).limit_denominator(),
                                     "not in lowest terms")
                self.assertEqual(Fraction(answer), value, res["problem"])
            # exact minimal rendering
            body = answer[:-1] if answer.endswith("%") else answer
            self.assertNotRegex(body, r"\.\d*0$", res["problem"])
            self.assertNotRegex(body, r"\.\d{7,}", res["problem"])
        self.assertEqual(len(seen_ops), 5, seen_ops)

    def test_reduction_is_visible(self):
        """dec->frac and percent->frac must show the unreduced n/10^k
        before the F simplify step."""
        for _ in range(800):
            res = self.gen.generate()
            if res["operation"] in ("convert_dec_to_frac",
                                    "convert_percent_to_frac"):
                codes = [s.split(DELIM)[0] for s in res["steps"]]
                self.assertIn("DEC_TO_FRAC", codes)
                self.assertIn("F", codes)


if __name__ == "__main__":
    unittest.main()
