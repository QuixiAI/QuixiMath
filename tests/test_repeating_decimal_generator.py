import re
import unittest
from fractions import Fraction
from unittest.mock import patch

from generators.repeating_decimal_generator import RepeatingDecimalGenerator
from helpers import DELIM


def decimal_to_fraction(text):
    """Exact value of '0.8(3)'-style or plain decimal text; returns
    (value, is_repeating)."""
    match = re.fullmatch(r"0\.(\d*)\((\d+)\)", text)
    if match:
        prefix, repetend = match.groups()
        value = (Fraction(int(prefix), 10 ** len(prefix))
                 if prefix else Fraction(0))
        value += Fraction(int(repetend),
                          (10 ** len(repetend) - 1) * 10 ** len(prefix))
        return value, True
    return Fraction(text), False


class TestRepeatingDecimalGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = RepeatingDecimalGenerator()

    def test_terminating(self):
        with patch("generators.repeating_decimal_generator.random.choice", return_value=8), \
             patch("generators.repeating_decimal_generator.random.randint", return_value=1):
            res = self.gen.generate()
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(res["final_answer"], "0.125 (terminating)")

    def test_repeating_uses_repetend_notation(self):
        with patch("generators.repeating_decimal_generator.random.choice", return_value=3), \
             patch("generators.repeating_decimal_generator.random.randint", return_value=1):
            res = self.gen.generate()
        # 1/3 is exactly 0.(3), never a rounded 0.333333
        self.assertEqual(res["final_answer"], "0.(3) (repeating)")

    def test_oracle_exact_value_and_classification(self):
        """A9 oracle: the decimal text must equal the fraction exactly
        (repetend notation converted back algebraically), and the
        terminating/repeating label must match the true denominator."""
        for _ in range(500):
            res = self.gen.generate()
            n, d = (int(x) for x in re.search(
                r"if (\d+)/(\d+) is", res["problem"]).groups())
            dec_text, kind = re.fullmatch(
                r"(.+) \((terminating|repeating)\)",
                res["final_answer"]).groups()
            value, is_repeating = decimal_to_fraction(dec_text)
            self.assertEqual(value, Fraction(n, d), res["problem"])
            self.assertEqual(kind == "repeating", is_repeating,
                             res["problem"])
            # classification must match the reduced denominator's factors
            reduced_den = Fraction(n, d).denominator
            while reduced_den % 2 == 0:
                reduced_den //= 2
            while reduced_den % 5 == 0:
                reduced_den //= 5
            self.assertEqual(kind == "terminating", reduced_den == 1)

    def test_prime_steps_are_prime(self):
        for _ in range(300):
            res = self.gen.generate()
            for s in res["steps"]:
                if s.startswith(f"PF_PRIME{DELIM}"):
                    p = int(s.split(DELIM)[1])
                    self.assertTrue(
                        p > 1 and all(p % k for k in range(2, int(p**0.5) + 1)),
                        s)


if __name__ == "__main__":
    unittest.main()
