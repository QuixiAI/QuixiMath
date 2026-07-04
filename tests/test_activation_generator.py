import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.activation_generator import ActivationGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"For the two-layer scalar model y=w2\*a\(w1\*x\+b1\)\+b2 with "
    r"x=([-0-9]+), w1=([-0-9]+), b1=([-0-9]+), w2=([-0-9]+), "
    r"b2=([-0-9]+), use (ReLU|sigmoid|GELU) activation"
    r"(?: with provided exp\(-z\)=1| with provided GELU\(0\)=0 and "
    r"GELU'\(0\)=1/2)?\. Compute activation value, activation derivative, "
    r"y, and dy/dx\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def variant_key(name):
    return {"ReLU": "relu", "sigmoid": "sigmoid", "GELU": "gelu"}[name]


def expected_flow(example):
    match = PROBLEM_RE.fullmatch(example["problem"])
    if not match:
        raise AssertionError(example["problem"])
    x = int(match.group(1))
    w1 = int(match.group(2))
    b1 = int(match.group(3))
    w2 = int(match.group(4))
    b2 = int(match.group(5))
    variant = variant_key(match.group(6))
    z_linear = w1 * x
    z = z_linear + b1
    steps = [
        make_step("ACT_SETUP", f"activation={variant}", f"x={x}",
                  f"w1={w1},b1={b1},w2={w2},b2={b2}"),
        make_step("M", w1, x, z_linear),
        make_step("A", z_linear, b1, z),
    ]
    if variant == "relu":
        activation = Fraction(max(0, z))
        derivative = Fraction(1 if z > 0 else 0)
    elif variant == "sigmoid":
        exp_value = Fraction(1)
        denom = 1 + exp_value
        activation = Fraction(1, denom)
        one_minus = 1 - activation
        derivative = activation * one_minus
        steps.extend([
            make_step("EXP_VALUE", "exp(-z)", fraction_text(exp_value)),
            make_step("A", 1, fraction_text(exp_value), denom),
            make_step("D", 1, denom, fraction_text(activation)),
            make_step("S", 1, fraction_text(activation),
                      fraction_text(one_minus)),
            make_step("M", fraction_text(activation),
                      fraction_text(one_minus), fraction_text(derivative)),
        ])
    else:
        activation = Fraction(0)
        derivative = Fraction(1, 2)
    steps.extend([
        make_step("ACT_VALUE", variant, z, fraction_text(activation)),
        make_step("ACT_DERIV", variant, z, fraction_text(derivative)),
    ])
    hidden = w2 * activation
    output = hidden + b2
    derivative_partial = w2 * derivative
    chain = derivative_partial * w1
    steps.extend([
        make_step("M", w2, fraction_text(activation), fraction_text(hidden)),
        make_step("A", fraction_text(hidden), b2, fraction_text(output)),
        make_step("MODEL_OUTPUT", fraction_text(output)),
        make_step("M", w2, fraction_text(derivative),
                  fraction_text(derivative_partial)),
        make_step("M", fraction_text(derivative_partial), w1,
                  fraction_text(chain)),
        make_step("CHAIN_DERIV", "dy/dx", fraction_text(chain)),
    ])
    answer = (
        f"z={z}; a={fraction_text(activation)}; "
        f"a_prime={fraction_text(derivative)}; "
        f"y={fraction_text(output)}; dy_dx={fraction_text(chain)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestActivationGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = ActivationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["operation"].startswith("activation_chain_"))
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

    def test_variants_are_available(self):
        for variant in ActivationGenerator.VARIANTS:
            result = ActivationGenerator(variant).generate()
            self.assertEqual(result["operation"], f"activation_chain_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ActivationGenerator("bogus")

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

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
