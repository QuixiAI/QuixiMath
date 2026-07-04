import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.minkowski_interval_generator import MinkowskiIntervalGenerator
from helpers import DELIM


INTERVAL_RE = re.compile(
    r"In c=1 units, an event separation has ct=(-?\d+) and x=(-?\d+)\. "
    r"Compute s2=ct\^2-x\^2 and classify the interval\."
)
RAPIDITY_RE = re.compile(
    r"Two collinear boosts have rapidities eta1=([^ ]+) and eta2=([^ ]+)\. "
    r"Compute the total rapidity\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def interval_class(s2):
    if s2 > 0:
        return "timelike"
    if s2 < 0:
        return "spacelike"
    return "lightlike"


def expected_interval(problem):
    ct, x = (int(value) for value in INTERVAL_RE.fullmatch(problem).groups())
    ct_sq = ct ** 2
    x_sq = x ** 2
    s2 = ct_sq - x_sq
    classification = interval_class(s2)
    steps = [
        make_step("MINKOWSKI_SETUP", "interval_classification",
                  f"ct={ct}", f"x={x}"),
        make_step("MINKOWSKI_FORMULA", "s2=ct^2-x^2"),
        make_step("E", ct, 2, ct_sq),
        make_step("E", x, 2, x_sq),
        make_step("S", ct_sq, x_sq, s2),
        make_step("INTERVAL_CLASS", f"s2={s2}", classification),
    ]
    answer = f"s2={s2}; class={classification}"
    return steps, answer


def expected_rapidity(problem):
    eta1_raw, eta2_raw = RAPIDITY_RE.fullmatch(problem).groups()
    eta1 = Fraction(eta1_raw)
    eta2 = Fraction(eta2_raw)
    total = eta1 + eta2
    steps = [
        make_step("MINKOWSKI_SETUP", "rapidity_addition",
                  f"eta1={fraction_text(eta1)}", f"eta2={fraction_text(eta2)}"),
        make_step("MINKOWSKI_FORMULA", "eta_total=eta1+eta2"),
        make_step("A", fraction_text(eta1), fraction_text(eta2),
                  fraction_text(total)),
        make_step("RAPIDITY_SUM", "collinear boosts", fraction_text(total)),
    ]
    answer = f"eta_total={fraction_text(total)}"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if INTERVAL_RE.fullmatch(problem):
        steps, answer = expected_interval(problem)
    else:
        steps, answer = expected_rapidity(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestMinkowskiIntervalGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = MinkowskiIntervalGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_all_interval_classes_occur(self):
        gen = MinkowskiIntervalGenerator("interval_classification")
        seen = set()
        for _ in range(800):
            result = gen.generate()
            seen.add(result["final_answer"].split("class=", 1)[1])
        self.assertEqual(seen, {"timelike", "spacelike", "lightlike"})

    def test_variants_are_available(self):
        for variant in MinkowskiIntervalGenerator.VARIANTS:
            result = MinkowskiIntervalGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"minkowski_interval_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            MinkowskiIntervalGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
