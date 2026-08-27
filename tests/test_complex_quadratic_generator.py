import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.complex_quadratic_generator import ComplexQuadraticGenerator
from helpers import DELIM


EQ_RE = re.compile(
    r"(\d*)([a-z])\^2"
    r"(?: ([+-]) (\d*)\2)?"
    r"(?: ([+-]) (\d+))?"
    r" = (-?\d+)"
)


def parse_eq(problem):
    """Recover (A, B, C, var, rhs) from any phrasing of the problem text.

    The displayed equation may carry a non-zero constant on the right, so the
    standard-form constant is C = displayed_constant - rhs.
    """
    m = EQ_RE.search(problem)
    assert m, problem
    lead = int(m.group(1) or 1)
    var = m.group(2)
    b = 0
    if m.group(3):
        b = int(m.group(4) or 1) * (1 if m.group(3) == "+" else -1)
    shown_c = 0
    if m.group(5):
        shown_c = int(m.group(6)) * (1 if m.group(5) == "+" else -1)
    rhs = int(m.group(7))
    return lead, b, shown_c - rhs, var, rhs


def parse_root(text):
    """'2 + 3i' / '3 - i√2' / 'i√5' / '-2i' -> (p, q, k) with root
    p + q·i·√k (k=1 for gaussian)."""
    m = re.fullmatch(r"(?:(-?\d+) ([+-]) )?(-?)(\d*)i(?:√(\d+))?", text)
    assert m, text
    p = int(m.group(1) or 0)
    mag = int(m.group(4) or 1)
    neg = (m.group(2) == "-") or (m.group(3) == "-")
    return p, -mag if neg else mag, int(m.group(5) or 1)


def parse_answer(answer, var):
    m = re.fullmatch(rf"{var} = (.+) or {var} = (.+)", answer)
    assert m, answer
    return m.groups()


def oracle_check(example):
    """Substitute both roots into A x^2 + Bx + C symbolically (exact)."""
    A, B, C, var, _ = parse_eq(example["problem"])
    for txt in parse_answer(example["final_answer"], var):
        p, q, k = parse_root(txt)
        # A(p + qi√k)^2 + B(p + qi√k) + C
        real = A * (p * p - q * q * k) + B * p + C
        imag_coef = 2 * A * p * q + B * q   # coefficient of i√k
        if real != 0 or imag_coef != 0:
            return False
    return True


class TestComplexQuadraticGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ComplexQuadraticGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "quadratic_complex_roots")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_roots_satisfy_equation(self):
        """A9 oracle: both roots substituted back give exactly zero."""
        for _ in range(1000):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_oracle_sum_and_product_of_roots(self):
        """Second independent route: Vieta's formulas on the parsed roots."""
        for _ in range(600):
            result = self.gen.generate()
            A, B, C, var, _ = parse_eq(result["problem"])
            hi, lo = parse_answer(result["final_answer"], var)
            p1, q1, k1 = parse_root(hi)
            p2, q2, k2 = parse_root(lo)
            self.assertEqual(k1, k2)
            # sum = -B/A, product = C/A (conjugates -> both real)
            self.assertEqual(A * (p1 + p2), -B, result["problem"])
            self.assertEqual(A * (p1 * p2 - q1 * q2 * k1), C,
                             result["problem"])

    def test_discriminant_is_negative_and_correct(self):
        for _ in range(400):
            result = self.gen.generate()
            A, B, C, _, _ = parse_eq(result["problem"])
            d = next(s for s in result["steps"]
                     if s.startswith(f"DISC{DELIM}"))
            fields = d.split(DELIM)
            wb = str(B) if B >= 0 else f"({B})"
            self.assertEqual(fields[1], f"{wb}^2 - 4({A})({C})", d)
            self.assertEqual(int(fields[2]), B * B - 4 * A * C, d)
            self.assertLess(int(fields[2]), 0)
            self.assertTrue(any(s.startswith(f"DISC_CLASSIFY{DELIM}")
                                for s in result["steps"]))

    def test_move_constant_step_arithmetic(self):
        seen_shift = seen_plain = False
        for _ in range(400):
            result = self.gen.generate()
            A, B, C, var, rhs = parse_eq(result["problem"])
            moves = [s for s in result["steps"] if s.startswith(f"S{DELIM}")]
            if rhs == 0:
                seen_plain = True
                self.assertEqual(moves, [], result["problem"])
                continue
            seen_shift = True
            self.assertEqual(len(moves), 1, result["problem"])
            shown, moved, remainder = moves[0].split(DELIM)[1:]
            self.assertEqual(int(shown) - int(moved), int(remainder),
                             moves[0])
            self.assertEqual(int(remainder), C, result["problem"])
            rewrite = next(s for s in result["steps"]
                           if s.startswith(f"REWRITE{DELIM}"))
            self.assertTrue(rewrite.endswith(" = 0"), rewrite)
        self.assertTrue(seen_shift and seen_plain)

    def test_sqrt_and_formula_steps(self):
        for _ in range(400):
            result = self.gen.generate()
            A, B, C, var, _ = parse_eq(result["problem"])
            disc = B * B - 4 * A * C
            sq = next(s for s in result["steps"]
                      if s.startswith(f"SQRT_NEG{DELIM}"))
            self.assertEqual(sq.split(DELIM)[1], f"√({disc})", sq)
            simp = [s for s in result["steps"]
                    if s.startswith(f"ROOT_SIMPLIFY{DELIM}")]
            radical = (simp[0].split(DELIM)[1] if simp
                       else sq.split(DELIM)[2])
            m = re.fullmatch(r"(\d*)i(?:√(\d+))?", radical)
            self.assertIsNotNone(m, radical)
            coef = int(m.group(1) or 1)
            inner = int(m.group(2) or 1)
            self.assertEqual(coef * coef * inner, -disc, radical)
            for code in ("Q1", "Q2"):
                q = next(s for s in result["steps"]
                         if s.startswith(f"{code}{DELIM}"))
                fields = q.split(DELIM)
                self.assertEqual(int(fields[1]), -B, q)
                self.assertEqual(fields[2], radical, q)
                self.assertEqual(int(fields[3]), 2 * A, q)

    def test_roots_are_conjugates(self):
        for _ in range(400):
            result = self.gen.generate()
            _, _, _, var, _ = parse_eq(result["problem"])
            hi, lo = parse_answer(result["final_answer"], var)
            p1, q1, k1 = parse_root(hi)
            p2, q2, k2 = parse_root(lo)
            self.assertEqual((p1, k1), (p2, k2))
            self.assertEqual(q1, -q2)
            self.assertGreater(q1, 0)  # + root listed first

    def test_radical_k_is_squarefree(self):
        gen = ComplexQuadraticGenerator("radical")
        for _ in range(300):
            result = gen.generate()
            m = re.search(r"√(\d+)", result["final_answer"])
            k = int(m.group(1))
            for f in range(2, int(math.isqrt(k)) + 1):
                self.assertNotEqual(k % (f * f), 0,
                                    result["final_answer"])

    def test_pure_imaginary_case_occurs(self):
        found = False
        for _ in range(800):
            result = self.gen.generate()
            _, B, _, var, _ = parse_eq(result["problem"])
            if B == 0:
                hi, lo = parse_answer(result["final_answer"], var)
                self.assertEqual(parse_root(hi)[0], 0, result["final_answer"])
                self.assertEqual(parse_root(lo)[0], 0, result["final_answer"])
                found = True
                break
        self.assertTrue(found)

    def test_variable_letters_and_phrasings_vary(self):
        variables = set()
        problems = set()
        for _ in range(500):
            result = self.gen.generate()
            variables.add(parse_eq(result["problem"])[3])
            problems.add(result["problem"])
        self.assertGreaterEqual(len(variables), 8)
        self.assertGreater(len(problems), 490)

    def test_leading_coefficient_varies(self):
        leads = {parse_eq(self.gen.generate()["problem"])[0]
                 for _ in range(300)}
        self.assertEqual(leads, {1, 2, 3})

    def test_pipe_safe(self):
        for _ in range(400):
            result = self.gen.generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            ComplexQuadraticGenerator("bogus")
        for variant in ("gaussian", "radical"):
            gen = ComplexQuadraticGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                has_radical = "√" in result["final_answer"]
                self.assertEqual(has_radical, variant == "radical",
                                 result["final_answer"])


if __name__ == "__main__":
    unittest.main()
