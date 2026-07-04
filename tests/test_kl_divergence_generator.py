import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.kl_divergence_generator import KLDivergenceGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"For distributions P=\[([^]]+)\] and Q=\[([^]]+)\], compute "
    r"D_KL\((P|Q) to (P|Q)\) in bits\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def list_text(values):
    return "[" + ",".join(fraction_text(value) for value in values) + "]"


def bit_unit(value):
    return "bit" if Fraction(value) == 1 else "bits"


def log2_power(value):
    value = Fraction(value)
    exponent = 0
    while value > 1:
        value /= 2
        exponent += 1
    while value < 1:
        value *= 2
        exponent -= 1
    if value != 1:
        raise AssertionError(f"not a power of two: {value}")
    return exponent


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    if not match:
        raise AssertionError(problem)
    p = [Fraction(piece) for piece in match.group(1).split(",")]
    q = [Fraction(piece) for piece in match.group(2).split(",")]
    source_name = match.group(3)
    target_name = match.group(4)
    return p, q, source_name, target_name


def expected_flow(example):
    p, q, source_name, target_name = parse_problem(example["problem"])
    source = p if source_name == "P" else q
    target = q if target_name == "Q" else p
    steps = [
        make_step("KL_SETUP", f"P={list_text(p)}", f"Q={list_text(q)}",
                  f"direction={source_name} to {target_name}"),
        make_step("KL_FORMULA",
                  "D=sum source_i*log2(source_i/target_i)"),
    ]
    running = Fraction(0)
    for idx, (source_i, target_i) in enumerate(zip(source, target)):
        ratio = source_i / target_i
        log_ratio = log2_power(ratio)
        term = source_i * log_ratio
        steps.append(make_step("D", fraction_text(source_i),
                               fraction_text(target_i),
                               fraction_text(ratio)))
        steps.append(make_step("LOG2_RATIO", f"i={idx}",
                               f"ratio={fraction_text(ratio)}",
                               f"log={log_ratio}"))
        steps.append(make_step("M", fraction_text(source_i), log_ratio,
                               fraction_text(term)))
        new_running = running + term
        steps.append(make_step("A", fraction_text(running),
                               fraction_text(term),
                               fraction_text(new_running)))
        running = new_running
    answer = (
        f"D_KL({source_name} to {target_name})="
        f"{fraction_text(running)} {bit_unit(running)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestKLDivergenceGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = KLDivergenceGenerator()

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
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "LOG2_RATIO":
                    ratio = Fraction(fields[2].replace("ratio=", ""))
                    self.assertEqual(log2_power(ratio),
                                     int(fields[3].replace("log=", "")),
                                     raw_step)

    def test_variants_are_available(self):
        for variant in KLDivergenceGenerator.VARIANTS:
            result = KLDivergenceGenerator(variant).generate()
            self.assertEqual(result["operation"], f"kl_divergence_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            KLDivergenceGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
