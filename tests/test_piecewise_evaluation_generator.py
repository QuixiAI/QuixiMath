import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.piecewise_evaluation_generator import (
    PiecewiseEvaluationGenerator,
)
from helpers import DELIM


def cents(dollars_txt):
    """'$8.50' -> 850; '$2600' -> 260000."""
    t = dollars_txt.lstrip("$")
    if "." in t:
        whole, frac = t.split(".")
        return int(whole) * 100 + int(frac)
    return int(t) * 100


def oracle_answer(example):
    """Independently evaluates the piecewise rule from the text alone."""
    p = example["problem"]
    op = example["operation"]

    if op == "piecewise_evaluation":
        m = re.fullmatch(
            r"Given [a-z]\(([a-z])\) = \{ (-?\d+)\1 ([+-]) (\d+) "
            r"if \1 < (-?\d+); \1\^2 if (-?\d+) <= \1 <= (-?\d+); "
            r"(-?\d+) if \1 > (-?\d+) \}, find [a-z]\((-?\d+)\)\.", p)
        assert m, p
        a1 = int(m.group(2))
        b1 = int(m.group(4)) * (1 if m.group(3) == "+" else -1)
        c1, c1b, c2 = int(m.group(5)), int(m.group(6)), int(m.group(7))
        p3, c2b, k = int(m.group(8)), int(m.group(9)), int(m.group(10))
        assert c1 == c1b and c2 == c2b
        if k < c1:
            return str(a1 * k + b1)
        if k <= c2:
            return str(k * k)
        return str(p3)

    if op == "piecewise_shipping":
        m = re.fullmatch(
            r"Shipping costs \$([\d.]+) for packages up to (\d+) lb, "
            r"\$([\d.]+) for over \2 lb up to (\d+) lb, and \$([\d.]+) for "
            r"over \4 lb\. Find the cost to ship a ([\d.]+) lb package\.", p)
        assert m, p
        p1, cut1 = cents("$" + m.group(1)), int(m.group(2))
        p2, cut2, p3 = cents("$" + m.group(3)), int(m.group(4)), \
            cents("$" + m.group(5))
        w = Fraction(m.group(6))
        price = p1 if w <= cut1 else (p2 if w <= cut2 else p3)
        return f"${price // 100}.{price % 100:02d}"

    if op == "piecewise_billing":
        m = re.fullmatch(
            r"A phone plan costs \$([\d.]+) per month including (\d+) "
            r"minutes, plus \$([\d.]+) for each additional minute\. "
            r"Find the bill for (\d+) minutes\.", p)
        assert m, p
        base = cents("$" + m.group(1))
        included, used = int(m.group(2)), int(m.group(4))
        rate = cents("$" + m.group(3))
        total = base if used <= included \
            else base + (used - included) * rate
        return f"${total // 100}.{total % 100:02d}"

    m = re.fullmatch(
        r"A tax is (\d+)% on the first \$(\d+) of income and (\d+)% on "
        r"income above \$\2\. Find the tax on an income of \$(\d+)\.", p)
    assert m, p
    r1, bracket, r2, income = (int(v) for v in m.groups())
    if income <= bracket:
        tax = Fraction(income * r1, 100)
    else:
        tax = Fraction(bracket * r1, 100) + \
            Fraction((income - bracket) * r2, 100)
    assert tax.denominator == 1
    return f"${tax.numerator}"


def condition_holds(cond):
    """Evaluates 'a < b', 'a <= b', 'a > b', or 'a <= b <= c' exactly."""
    m = re.fullmatch(r"(-?[\d.]+) <= (-?[\d.]+) <= (-?[\d.]+)", cond)
    if m:
        a, b, c = (Fraction(v) for v in m.groups())
        return a <= b <= c
    m = re.fullmatch(r"(-?[\d.]+) < (-?[\d.]+) <= (-?[\d.]+)", cond)
    if m:
        a, b, c = (Fraction(v) for v in m.groups())
        return a < b <= c
    m = re.fullmatch(r"(-?[\d.]+) (<=|<|>) (-?[\d.]+)", cond)
    assert m, cond
    a, b = Fraction(m.group(1)), Fraction(m.group(3))
    return {"<=": a <= b, "<": a < b, ">": a > b}[m.group(2)]


class TestPiecewiseEvaluationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = PiecewiseEvaluationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: re-evaluate every variant from the text."""
        for _ in range(600):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_branch_tests_are_truthful_and_ordered(self):
        """Every BRANCH_TEST verdict is correct; 'no'* then one 'yes'."""
        for _ in range(500):
            result = self.gen.generate()
            verdicts = []
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "BRANCH_TEST":
                    self.assertEqual(f[2],
                                     "yes" if condition_holds(f[1]) else "no",
                                     s)
                    verdicts.append(f[2])
            self.assertGreaterEqual(len(verdicts), 1, result["steps"])
            self.assertTrue(all(v == "no" for v in verdicts[:-1]),
                            result["steps"])
            if verdicts[-1] == "no":
                # only two-branch rules may fall through on a final 'no'
                self.assertIn(result["operation"],
                              ("piecewise_billing", "piecewise_tax"),
                              result["steps"])
                self.assertEqual(len(verdicts), 1, result["steps"])

    def test_step_arithmetic(self):
        for _ in range(500):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] in ("M", "A", "S") and len(f) == 4:
                    x, y, z = (Fraction(v) for v in f[1:])
                    got = {"M": x * y, "A": x + y, "S": x - y}[f[0]]
                    self.assertEqual(got, z, s)
                elif f[0] == "E":
                    self.assertEqual(int(f[1].strip("()")) ** int(f[2]),
                                     int(f[3]), s)

    def test_boundary_inputs_occur(self):
        """Inputs landing exactly on a cut must appear (the hard part)."""
        boundary = 0
        gen = PiecewiseEvaluationGenerator("abstract")
        for _ in range(300):
            result = gen.generate()
            m = re.search(r"if (-?\d+) <= [a-z] <= (-?\d+);", result["problem"])
            k = int(re.search(r"\((-?\d+)\)\.$", result["problem"]).group(1))
            if k in (int(m.group(1)), int(m.group(2))):
                boundary += 1
        self.assertGreater(boundary, 10)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(200):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"piecewise_evaluation", "piecewise_shipping",
                               "piecewise_billing", "piecewise_tax"})

    def test_billing_under_and_over_included(self):
        kinds = set()
        gen = PiecewiseEvaluationGenerator("billing")
        for _ in range(100):
            result = gen.generate()
            kinds.add("over" if any(s.startswith(f"S{DELIM}")
                                    for s in result["steps"]) else "under")
        self.assertEqual(kinds, {"over", "under"})

    def test_tax_single_and_two_bracket(self):
        kinds = set()
        gen = PiecewiseEvaluationGenerator("tax")
        for _ in range(100):
            result = gen.generate()
            mults = sum(1 for s in result["steps"]
                        if s.startswith(f"M{DELIM}"))
            kinds.add(mults)
        self.assertEqual(kinds, {1, 2})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            PiecewiseEvaluationGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
