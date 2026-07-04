import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.complex_division_generator import ComplexDivisionGenerator
from helpers import DELIM


def parse_int_cx(text):
    """'3 + 4i', '-2 - i' -> (re, im) ints."""
    m = re.fullmatch(r"(-?\d+) ([+-]) (?:(\d+))?i", text)
    if m:
        im = int(m.group(3) or 1) * (1 if m.group(2) == "+" else -1)
        return int(m.group(1)), im
    m = re.fullmatch(r"(-?)(?:(\d+))?i", text)
    if m:
        return 0, (-1 if m.group(1) == "-" else 1) * int(m.group(2) or 1)
    return int(text), 0


def parse_frac_cx(text):
    """Standard form with possible fraction parts -> (Fraction, Fraction)."""
    t = text
    m = re.fullmatch(
        r"(?:(-?\d+(?:/\d+)?) )?"          # real part (optional)
        r"(?:([+-]) )?"                    # separator sign (optional)
        r"(-?)\(?(\d+(?:/\d+)?)?\)?i", t)
    if m and "i" in t:
        re_p = Fraction(m.group(1)) if m.group(1) else Fraction(0)
        mag = Fraction(m.group(4)) if m.group(4) else Fraction(1)
        neg = (m.group(2) == "-") or (m.group(3) == "-")
        return re_p, -mag if neg else mag
    return Fraction(t), Fraction(0)


def oracle_value(example):
    """(a+bi)/(c+di) computed exactly with Fractions."""
    m = re.fullmatch(r"Divide: \((.+?)\)/\((.+?)\)\. Give the answer in "
                     r"standard form\.", example["problem"])
    assert m, example["problem"]
    a, b = parse_int_cx(m.group(1))
    c, d = parse_int_cx(m.group(2))
    den = c * c + d * d
    return (Fraction(a * c + b * d, den),
            Fraction(b * c - a * d, den))


class TestComplexDivisionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ComplexDivisionGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "complex_division")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_value_from_problem_text(self):
        """A9 oracle: exact quotient equals the parsed answer."""
        for _ in range(600):
            result = self.gen.generate()
            want = oracle_value(result)
            got = parse_frac_cx(result["final_answer"])
            self.assertEqual(got, want,
                             (result["problem"], result["final_answer"]))

    def test_conjugate_is_correct(self):
        for _ in range(300):
            result = self.gen.generate()
            conj = next(s for s in result["steps"]
                        if s.startswith(f"CONJUGATE{DELIM}"))
            f = conj.split(DELIM)
            c1, d1 = parse_int_cx(f[1])
            c2, d2 = parse_int_cx(f[2])
            self.assertEqual((c1, -d1), (c2, d2), conj)

    def test_denominator_is_sum_of_squares(self):
        for _ in range(300):
            result = self.gen.generate()
            m = re.search(r"/\((.+?)\)\.", result["problem"])
            c, d = parse_int_cx(m.group(1))
            den = next(s for s in result["steps"]
                       if s.startswith(f"EVAL{DELIM}denominator{DELIM}"))
            self.assertEqual(int(den.split(DELIM)[2]), c * c + d * d)

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)
                elif f[0] == "E":
                    self.assertEqual(int(f[1]) ** int(f[2]), int(f[3]), s)
                elif f[0] == "FRAC_REDUCE":
                    n, d = f[1].split("/")
                    self.assertEqual(Fraction(int(n), int(d)),
                                     Fraction(f[2]), s)

    def test_reduced_parts(self):
        """Any fraction appearing in the answer is in lowest terms."""
        for _ in range(400):
            result = self.gen.generate()
            for n, d in re.findall(r"(-?\d+)/(\d+)", result["final_answer"]):
                self.assertEqual(str(Fraction(int(n), int(d))), f"{n}/{d}",
                                 result["final_answer"])

    def test_integer_and_fraction_answers_occur(self):
        kinds = set()
        for _ in range(300):
            kinds.add("/" in self.gen.generate()["final_answer"])
        self.assertEqual(kinds, {True, False})


if __name__ == "__main__":
    unittest.main()
