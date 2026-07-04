import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.log_equation_generator import LogEquationGenerator
from helpers import DELIM


def parse_lin(txt):
    m = re.fullmatch(r"(\d*)x(?: ([+-]) (\d+))?", txt)
    assert m, txt
    a = int(m.group(1) or 1)
    c = int(m.group(3) or 0) * (1 if (m.group(2) or "+") == "+" else -1)
    return a, c


def oracle_answer(example):
    """Independently solves with domain filtering."""
    p = example["problem"]
    m = re.fullmatch(r"Solve: log_(\d+)\((.+)\) = (\d+)\.", p)
    if m and "log" not in m.group(2):
        b, arg, d = int(m.group(1)), m.group(2), int(m.group(3))
        a, c = parse_lin(arg)
        x = Fraction(b ** d - c, a)
        assert x.denominator == 1 and a * x + c > 0
        return f"x = {x.numerator}"
    m = re.fullmatch(r"Solve: log_(\d+)\(x\) \+ log_(\d+)\(x \+ (\d+)\) "
                     r"= (\d+)\.", p)
    if m:
        b, k, d = int(m.group(1)), int(m.group(3)), int(m.group(4))
        N = b ** d
        roots = [t for t in range(-200, 201) if t * t + k * t - N == 0]
        valid = [t for t in roots if t > 0 and t + k > 0]
        assert len(valid) == 1
        return f"x = {valid[0]}"
    m = re.fullmatch(r"Solve: log_(\d+)\((.+)\) = log_\1\((.+)\)\.", p)
    assert m, p
    a1, c1 = parse_lin(m.group(2))
    a2, c2 = parse_lin(m.group(3))
    x = Fraction(c2 - c1, a1 - a2)
    assert x.denominator == 1
    x = x.numerator
    if a1 * x + c1 > 0 and a2 * x + c2 > 0:
        return f"x = {x}"
    return "No solution"


class TestLogEquationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = LogEquationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: re-solve with domain filtering."""
        for _ in range(600):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_domain_note_always_present(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(any(s.startswith(f"DOMAIN_NOTE{DELIM}")
                                for s in result["steps"]), result["steps"])

    def test_product_rejects_negative_candidate(self):
        gen = LogEquationGenerator("product")
        for _ in range(200):
            result = gen.generate()
            rejects = [s for s in result["steps"]
                       if s.startswith(f"REJECT{DELIM}x = ")]
            log_rejects = [s for s in rejects if "extraneous" in s]
            self.assertEqual(len(log_rejects), 1, result["steps"])
            val = int(log_rejects[0].split(DELIM)[1].replace("x = ", ""))
            self.assertLess(val, 0)

    def test_no_solution_cases_occur_and_are_justified(self):
        gen = LogEquationGenerator("both_sides")
        outcomes = set()
        for _ in range(200):
            result = gen.generate()
            outcomes.add(result["final_answer"] == "No solution")
            if result["final_answer"] == "No solution":
                self.assertTrue(any(s.startswith(f"REJECT{DELIM}")
                                    for s in result["steps"]))
        self.assertEqual(outcomes, {True, False})

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "E":
                    self.assertEqual(int(f[1]) ** int(f[2]), int(f[3]), s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"log_eq_basic", "log_eq_product",
                               "log_eq_both_sides"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            LogEquationGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
