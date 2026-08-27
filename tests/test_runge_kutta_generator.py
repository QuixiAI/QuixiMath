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


ODE_RE = re.compile(
    r"ODE \[d(?P<dep>[A-Za-z])/d(?P<indep>[A-Za-z]) = (?P<rhs>.*?); "
    r"(?P=dep)\((?P<x0>-?\d+(?:/\d+)?)\) = "
    r"(?P<y0>-?\d+(?:/\d+)?)\]"
)


def parse_f(expr, indep, dep):
    """Parse the printed affine RHS without importing generator helpers."""
    coefficients = {indep: 0, dep: 0}
    constant = 0
    for term in expr.replace(" - ", " + -").split(" + "):
        term = term.strip()
        if term.endswith(indep) or term.endswith(dep):
            variable = term[-1]
            raw = term[:-1]
            coefficient = {"": 1, "-": -1}.get(raw)
            if coefficient is None:
                coefficient = int(raw)
            coefficients[variable] += coefficient
        else:
            constant += int(term)
    return lambda x, y: (coefficients[indep] * x
                         + coefficients[dep] * y + constant)


def parse_problem(problem):
    match = ODE_RE.search(problem)
    assert match, problem
    method = re.search(r"\b(RK2 midpoint|RK4)\b", problem)
    step_size = re.search(r"\bh = (-?\d+(?:/\d+)?)", problem)
    assert method and step_size, problem
    dep = match.group("dep")
    targets = re.findall(rf"{dep}\((-?\d+(?:/\d+)?)\)", problem)
    assert len(targets) >= 2, problem
    return {
        "variant": "rk2" if method.group(1) == "RK2 midpoint" else "rk4",
        "h": Fraction(step_size.group(1)),
        "target": Fraction(targets[-1]),
        "x0": Fraction(match.group("x0")),
        "f": parse_f(match.group("rhs"), match.group("indep"), dep),
        "y0": Fraction(match.group("y0")),
    }


def rk_answer(parts):
    h = parts["h"]
    f = parts["f"]
    x0 = parts["x0"]
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
        for _ in range(1000):
            result = self.gen.generate()
            parts = parse_problem(result["problem"])
            self.assertEqual(parts["target"], parts["x0"] + parts["h"])
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

    def test_widened_axes_appear(self):
        starts = set()
        variables = set()
        constants = False
        problems = set()
        for _ in range(800):
            result = self.gen.generate()
            parts = parse_problem(result["problem"])
            starts.add(parts["x0"])
            match = ODE_RE.search(result["problem"])
            variables.add((match.group("indep"), match.group("dep")))
            rhs = match.group("rhs")
            constants |= bool(re.search(r"(?:^| [+-] )\d+$", rhs))
            problems.add(result["problem"])
        self.assertGreater(len(starts), 5)
        self.assertGreater(len(variables), 5)
        self.assertTrue(constants)
        self.assertGreater(len(problems), 790)


if __name__ == "__main__":
    unittest.main()
