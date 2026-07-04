import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.runge_kutta_generator import RungeKuttaGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Use (RK2 midpoint|RK4) with step size h = ([^ ]+) to approximate "
    r"y\(([^)]+)\) for dy/dx = (.+) with y\(0\) = ([^.]+)\."
)


def parse_f(expr):
    expr = re.sub(r"(?<![A-Za-z0-9])x", "1*x", expr)
    expr = re.sub(r"(?<![A-Za-z0-9])y", "1*y", expr)
    expr = re.sub(r"(-?\d+)([xy])", r"\1*\2", expr)
    return eval("lambda x, y: " + expr)


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "variant": "rk2" if match.group(1) == "RK2 midpoint" else "rk4",
        "h": Fraction(match.group(2)),
        "target": Fraction(match.group(3)),
        "f": parse_f(match.group(4)),
        "y0": Fraction(match.group(5)),
    }


def rk_answer(parts):
    h = parts["h"]
    f = parts["f"]
    x0 = Fraction(0)
    y0 = parts["y0"]
    if parts["variant"] == "rk2":
        k1 = f(x0, y0)
        k2 = f(x0 + h / 2, y0 + (h / 2) * k1)
        return y0 + h * k2
    k1 = f(x0, y0)
    k2 = f(x0 + h / 2, y0 + (h / 2) * k1)
    k3 = f(x0 + h / 2, y0 + (h / 2) * k2)
    k4 = f(x0 + h, y0 + h * k3)
    return y0 + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)


class TestRungeKuttaGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = RungeKuttaGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_recomputes_answer_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            parts = parse_problem(result["problem"])
            self.assertEqual(str(rk_answer(parts)), result["final_answer"],
                             result["problem"])

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_stage_counts(self):
        for variant, count in (("rk2", 2), ("rk4", 4)):
            result = RungeKuttaGenerator(variant).generate()
            stages = [s for s in result["steps"]
                      if s.startswith(f"RK_STAGE{DELIM}")]
            self.assertEqual(len(stages), count)

    def test_variants_are_available(self):
        for variant in RungeKuttaGenerator.VARIANTS:
            result = RungeKuttaGenerator(variant).generate()
            self.assertEqual(result["operation"], f"runge_kutta_{variant}")
            self.assertEqual(parse_problem(result["problem"])["variant"],
                             variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            RungeKuttaGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
