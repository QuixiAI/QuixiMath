import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.invariant_mass_generator import InvariantMassGenerator
from helpers import DELIM


PAIR = r"\(E,p\)=\((-?\d+),(-?\d+)\)"
INV_RE = re.compile(
    rf"Two decay products in one dimension have {PAIR} and {PAIR}\. "
    r"Compute the invariant mass "
    r"M=sqrt\(\(E1\+E2\)\^2-\(p1\+p2\)\^2\)\."
)
CM_RE = re.compile(
    rf"Two incoming particles in one dimension have {PAIR} and {PAIR}\. "
    r"Compute the center-of-mass energy "
    r"sqrt\(s\)=sqrt\(\(E1\+E2\)\^2-\(p1\+p2\)\^2\)\."
)
THRESHOLD_RE = re.compile(
    r"A beam particle of mass m_a=(\d+) hits a stationary target "
    r"of mass m_b=(\d+)\. The final particles have total rest mass "
    r"M_f=(\d+)\. Compute "
    r"E_thr=\(M_f\^2-m_a\^2-m_b\^2\)/\(2\*m_b\)\."
)
TWO_BODY_RE = re.compile(
    r"A parent of mass M=(\d+) decays into two equal daughters "
    r"m1=m2=(\d+)\. Compute the two-body momentum "
    r"p=sqrt\(\(M\^2-\(m1\+m2\)\^2\)\*"
    r"\(M\^2-\(m1-m2\)\^2\)\)/\(2\*M\)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def sqrt_int(value):
    root = int(value ** 0.5)
    assert root * root == value
    return root


def parse_problem(problem):
    match = INV_RE.fullmatch(problem)
    if match:
        return {
            "variant": "invariant_mass",
            "e1": int(match.group(1)),
            "p1": int(match.group(2)),
            "e2": int(match.group(3)),
            "p2": int(match.group(4)),
        }
    match = CM_RE.fullmatch(problem)
    if match:
        return {
            "variant": "cm_energy",
            "e1": int(match.group(1)),
            "p1": int(match.group(2)),
            "e2": int(match.group(3)),
            "p2": int(match.group(4)),
        }
    match = THRESHOLD_RE.fullmatch(problem)
    if match:
        return {
            "variant": "threshold",
            "m_a": int(match.group(1)),
            "m_b": int(match.group(2)),
            "final_mass": int(match.group(3)),
        }
    match = TWO_BODY_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "variant": "two_body_momentum",
        "parent": int(match.group(1)),
        "daughter": int(match.group(2)),
    }


def expected_mass_like(parts):
    e1 = parts["e1"]
    p1 = parts["p1"]
    e2 = parts["e2"]
    p2 = parts["p2"]
    total_e = e1 + e2
    total_p = p1 + p2
    e_sq = total_e ** 2
    p_sq = total_p ** 2
    mass_sq = e_sq - p_sq
    root = sqrt_int(mass_sq)
    target = "M" if parts["variant"] == "invariant_mass" else "sqrt(s)"
    formula = (
        "M=sqrt((E1+E2)^2-(p1+p2)^2)"
        if parts["variant"] == "invariant_mass"
        else "sqrt(s)=sqrt((E1+E2)^2-(p1+p2)^2)"
    )
    steps = [
        make_step("KIN_SETUP", parts["variant"],
                  f"(E1,p1)=({e1},{p1})", f"(E2,p2)=({e2},{p2})",
                  target),
        make_step("KIN_FORMULA", formula),
        make_step("A", e1, e2, total_e),
        make_step("A", p1, p2, total_p),
        make_step("E", total_e, 2, e_sq),
        make_step("E", total_p, 2, p_sq),
        make_step("S", e_sq, p_sq, mass_sq),
        make_step("ROOT", f"sqrt({mass_sq})", root),
    ]
    answer = f"{target} = {root}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_threshold(parts):
    m_a = parts["m_a"]
    m_b = parts["m_b"]
    final_mass = parts["final_mass"]
    final_sq = final_mass ** 2
    m_a_sq = m_a ** 2
    m_b_sq = m_b ** 2
    after_a = final_sq - m_a_sq
    numerator = after_a - m_b_sq
    denominator = 2 * m_b
    threshold = Fraction(numerator, denominator)
    steps = [
        make_step("KIN_SETUP", "threshold",
                  f"m_a={m_a},m_b={m_b}", f"M_f={final_mass}", "E_thr"),
        make_step("KIN_FORMULA",
                  "E_thr=(M_f^2-m_a^2-m_b^2)/(2*m_b)"),
        make_step("E", final_mass, 2, final_sq),
        make_step("E", m_a, 2, m_a_sq),
        make_step("E", m_b, 2, m_b_sq),
        make_step("S", final_sq, m_a_sq, after_a),
        make_step("S", after_a, m_b_sq, numerator),
        make_step("M", 2, m_b, denominator),
        make_step("D", numerator, denominator, fraction_text(threshold)),
    ]
    answer = f"E_thr = {fraction_text(threshold)}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_two_body(parts):
    parent = parts["parent"]
    m1 = parts["daughter"]
    m2 = parts["daughter"]
    mass_sum = m1 + m2
    mass_diff = m1 - m2
    parent_sq = parent ** 2
    sum_sq = mass_sum ** 2
    diff_sq = mass_diff ** 2
    left = parent_sq - sum_sq
    right = parent_sq - diff_sq
    radicand = left * right
    root = sqrt_int(radicand)
    denominator = 2 * parent
    momentum = Fraction(root, denominator)
    steps = [
        make_step("KIN_SETUP", "two_body_momentum",
                  f"M={parent}", f"m1={m1},m2={m2}", "p"),
        make_step(
            "KIN_FORMULA",
            "p=sqrt((M^2-(m1+m2)^2)*(M^2-(m1-m2)^2))/(2*M)",
        ),
        make_step("A", m1, m2, mass_sum),
        make_step("S", m1, m2, mass_diff),
        make_step("E", parent, 2, parent_sq),
        make_step("E", mass_sum, 2, sum_sq),
        make_step("E", mass_diff, 2, diff_sq),
        make_step("S", parent_sq, sum_sq, left),
        make_step("S", parent_sq, diff_sq, right),
        make_step("M", left, right, radicand),
        make_step("ROOT", f"sqrt({radicand})", root),
        make_step("M", 2, parent, denominator),
        make_step("D", root, denominator, fraction_text(momentum)),
    ]
    answer = f"p = {fraction_text(momentum)}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] in ("invariant_mass", "cm_energy"):
        return expected_mass_like(parts)
    if parts["variant"] == "threshold":
        return expected_threshold(parts)
    return expected_two_body(parts)


class TestInvariantMassGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = InvariantMassGenerator()

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
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(int(fields[1]) ** int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "ROOT":
                    inside = int(fields[1].removeprefix("sqrt(").rstrip(")"))
                    root = int(fields[2])
                    self.assertEqual(root * root, inside, raw_step)

    def test_variants_are_available(self):
        for variant in InvariantMassGenerator.VARIANTS:
            result = InvariantMassGenerator(variant).generate()
            self.assertEqual(result["operation"], f"invariant_mass_{variant}")
            self.assertEqual(parse_problem(result["problem"])["variant"],
                             variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            InvariantMassGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])

    def test_all_variants_seen_with_random_generator(self):
        seen = {self.gen.generate()["operation"] for _ in range(200)}
        self.assertEqual(
            seen,
            {"invariant_mass_invariant_mass", "invariant_mass_cm_energy",
             "invariant_mass_threshold",
             "invariant_mass_two_body_momentum"},
        )


if __name__ == "__main__":
    unittest.main()
