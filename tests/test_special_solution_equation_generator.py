import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.special_solution_equation_generator import (
    SpecialSolutionEquationGenerator,
)
from helpers import DELIM

PROBLEM_RE = re.compile(
    r"Solve for x: (\d+)\((?:(\d+))?x \+ (\d+)\) \+ (?:(\d+))?x"
    r"(?: ([+-]) (\d+))? = (?:(\d+))?x(?: ([+-]) (\d+))?$")


def parse_problem(problem):
    """Returns (m, p, mp, q): both sides as integer m·x + c pairs."""
    m0 = PROBLEM_RE.match(problem)
    assert m0, f"Unparseable: {problem}"
    f = int(m0.group(1))
    g = int(m0.group(2) or 1)
    h = int(m0.group(3))
    j = int(m0.group(4) or 1)
    k = int(m0.group(6) or 0) * (-1 if m0.group(5) == "-" else 1)
    mp = int(m0.group(7) or 1)
    q = int(m0.group(9) or 0) * (-1 if m0.group(8) == "-" else 1)
    return f * g + j, f * h + k, mp, q


def oracle_answer(example):
    m, p, mp, q = parse_problem(example["problem"])
    if m == mp:
        return "All real numbers" if p == q else "No solution"
    x = Fraction(q - p, m - mp)
    assert x.denominator == 1, "solution not integer"
    return str(int(x))


class TestSpecialSolutionEquationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = SpecialSolutionEquationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_all_outcomes_reachable(self):
        seen = {self.gen.generate()["operation"] for _ in range(80)}
        self.assertEqual(seen, {"linear_eq_unique", "linear_eq_identity",
                                "linear_eq_contradiction"})

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: expand and classify from the problem text alone."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_classification_matches_operation(self):
        for _ in range(200):
            result = self.gen.generate()
            expected = {"All real numbers": "linear_eq_identity",
                        "No solution": "linear_eq_contradiction"}.get(
                            result["final_answer"], "linear_eq_unique")
            self.assertEqual(result["operation"], expected)

    def test_step_arithmetic(self):
        """DIST, COMB_X, COMB_CONST, CHECK, CHECK_POINT independently true."""
        point_re = re.compile(r"(-?\d+)·\(?(-?\d+)\)? ([+-]) (\d+) = (-?\d+)")
        for _ in range(400):
            result = self.gen.generate()
            m, p, mp, q = parse_problem(result["problem"])
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "COMB_X":
                    self.assertEqual(int(f[1][:-1]) + int(f[2][:-1]),
                                     int(f[3][:-1]), s)
                elif f[0] == "COMB_CONST":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)
                elif f[0] in ("CHECK", "CHECK_POINT"):
                    vals = []
                    for work in f[2:4]:
                        w = point_re.fullmatch(work)
                        self.assertIsNotNone(w, s)
                        coef, x, sgn, c, val = (int(w.group(1)), int(w.group(2)),
                                                w.group(3), int(w.group(4)),
                                                int(w.group(5)))
                        c = c if sgn == "+" else -c
                        self.assertEqual(coef * x + c, val, s)
                        vals.append(val)
                    if f[0] == "CHECK":
                        self.assertEqual(vals[0], vals[1], s)
                elif f[0] == "SPECIAL_SOLUTION":
                    lhs_c, rhs_c = (int(v) for v in f[1].split(" = "))
                    self.assertEqual(lhs_c, p, s)
                    self.assertEqual(rhs_c, q, s)
                    if "identity" in f[2]:
                        self.assertEqual(lhs_c, rhs_c, s)
                    else:
                        self.assertNotEqual(lhs_c, rhs_c, s)

    def test_contradiction_check_point_disagrees(self):
        gen = SpecialSolutionEquationGenerator("contradiction")
        for _ in range(50):
            result = gen.generate()
            cp = next(s for s in result["steps"]
                      if s.startswith(f"CHECK_POINT{DELIM}"))
            f = cp.split(DELIM)
            lhs_val = int(f[2].rsplit("= ", 1)[1])
            rhs_val = int(f[3].rsplit("= ", 1)[1])
            self.assertNotEqual(lhs_val, rhs_val, cp)

    def test_fixed_outcome_constructor(self):
        for outcome, op in (("unique", "linear_eq_unique"),
                            ("identity", "linear_eq_identity"),
                            ("contradiction", "linear_eq_contradiction")):
            gen = SpecialSolutionEquationGenerator(outcome)
            for _ in range(10):
                self.assertEqual(gen.generate()["operation"], op)
        with self.assertRaises(ValueError):
            SpecialSolutionEquationGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
