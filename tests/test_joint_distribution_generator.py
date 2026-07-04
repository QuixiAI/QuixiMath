import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.joint_distribution_generator import JointDistributionGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"For binary variables X,Y with P\(X=0,Y=0\)=([^,]+), "
    r"P\(X=0,Y=1\)=([^,]+), P\(X=1,Y=0\)=([^,]+), and "
    r"P\(X=1,Y=1\)=([^,]+), compute the marginals, "
    r"P\(Y=1 given X=1\), independence, covariance, and correlation\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    p00, p01, p10, p11 = (Fraction(match.group(i)) for i in range(1, 5))
    return p00, p01, p10, p11


def expected_flow(example):
    p00, p01, p10, p11 = parse_problem(example["problem"])
    px0 = p00 + p01
    px1 = p10 + p11
    py0 = p00 + p10
    py1 = p01 + p11
    conditional = p11 / px1
    product = px1 * py1
    independent = p11 == product
    covariance = p11 - product
    one_minus_px = 1 - px1
    var_x = px1 * one_minus_px
    one_minus_py = 1 - py1
    var_y = py1 * one_minus_py
    var_product = var_x * var_y
    std_product = var_x
    correlation = covariance / std_product
    steps = [
        make_step("JOINT_SETUP", "X,Y in {0,1}",
                  f"p00={fraction_text(p00)}, p01={fraction_text(p01)}",
                  f"p10={fraction_text(p10)}, p11={fraction_text(p11)}"),
        make_step("MARGINAL", "P(X=0)=p00+p01"),
        make_step("A", fraction_text(p00), fraction_text(p01),
                  fraction_text(px0)),
        make_step("MARGINAL", "P(X=1)=p10+p11"),
        make_step("A", fraction_text(p10), fraction_text(p11),
                  fraction_text(px1)),
        make_step("MARGINAL", "P(Y=0)=p00+p10"),
        make_step("A", fraction_text(p00), fraction_text(p10),
                  fraction_text(py0)),
        make_step("MARGINAL", "P(Y=1)=p01+p11"),
        make_step("A", fraction_text(p01), fraction_text(p11),
                  fraction_text(py1)),
        make_step("COND_FORMULA",
                  "P(Y=1 given X=1)=P(X=1,Y=1)/P(X=1)"),
        make_step("D", fraction_text(p11), fraction_text(px1),
                  fraction_text(conditional)),
        make_step("INDEP_FORMULA",
                  "independent iff P11=P(X=1)P(Y=1)"),
        make_step("M", fraction_text(px1), fraction_text(py1),
                  fraction_text(product)),
        make_step("INDEP_CHECK", f"P11={fraction_text(p11)}",
                  f"product={fraction_text(product)}",
                  "yes" if independent else "no"),
        make_step("EXPECTATION", f"E[X]={fraction_text(px1)}",
                  f"E[Y]={fraction_text(py1)}",
                  f"E[XY]={fraction_text(p11)}"),
        make_step("COV_FORMULA", "Cov=E[XY]-E[X]E[Y]"),
        make_step("S", fraction_text(p11), fraction_text(product),
                  fraction_text(covariance)),
        make_step("S", 1, fraction_text(px1), fraction_text(one_minus_px)),
        make_step("M", fraction_text(px1), fraction_text(one_minus_px),
                  fraction_text(var_x)),
        make_step("S", 1, fraction_text(py1), fraction_text(one_minus_py)),
        make_step("M", fraction_text(py1), fraction_text(one_minus_py),
                  fraction_text(var_y)),
        make_step("CORR_FORMULA", "rho=Cov/sqrt(VarX*VarY)"),
        make_step("M", fraction_text(var_x), fraction_text(var_y),
                  fraction_text(var_product)),
        make_step("ROOT", f"sqrt({fraction_text(var_product)})",
                  fraction_text(std_product)),
        make_step("D", fraction_text(covariance), fraction_text(std_product),
                  fraction_text(correlation)),
    ]
    answer = (
        f"P_X(0)={fraction_text(px0)}, P_X(1)={fraction_text(px1)}; "
        f"P_Y(0)={fraction_text(py0)}, P_Y(1)={fraction_text(py1)}; "
        f"P(Y=1 given X=1)={fraction_text(conditional)}; "
        f"independent={'yes' if independent else 'no'}; "
        f"covariance={fraction_text(covariance)}; "
        f"correlation={fraction_text(correlation)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestJointDistributionGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = JointDistributionGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "joint_distribution_binary")
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
                elif fields[0] == "ROOT":
                    radicand = Fraction(re.fullmatch(
                        r"sqrt\(([^)]+)\)", fields[1]
                    ).group(1))
                    self.assertEqual(Fraction(fields[2]) * Fraction(fields[2]),
                                     radicand, raw_step)

    def test_probability_table_is_valid(self):
        for _ in range(300):
            p00, p01, p10, p11 = parse_problem(self.gen.generate()["problem"])
            cells = (p00, p01, p10, p11)
            self.assertEqual(sum(cells, Fraction(0)), 1)
            for cell in cells:
                self.assertGreaterEqual(cell, 0)
                self.assertLessEqual(cell, 1)

    def test_enough_unique_tables_for_sampling(self):
        problems = {self.gen.generate()["problem"] for _ in range(500)}
        self.assertGreaterEqual(len(problems), 200)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
