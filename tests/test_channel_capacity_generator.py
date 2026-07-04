import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.channel_capacity_generator import ChannelCapacityGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"A binary symmetric channel has crossover probability p=([^ ]+)\. "
    r"Use -log2\(p\)=([^ ]+) and -log2\(1-p\)=([^ ]+)\. (.+)"
)
BLOCK_RE = re.compile(
    r"For N=(\d+) channel uses, find maximum reliable bits N\*C\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def dec(value):
    value = Fraction(value)
    num, den = value.numerator, value.denominator
    p10 = 0
    while den % 2 == 0:
        den //= 2
        num *= 5
        p10 += 1
    while den % 5 == 0:
        den //= 5
        num *= 2
        p10 += 1
    assert den == 1, value
    if p10 == 0:
        return str(num)
    s = str(abs(num)).rjust(p10 + 1, "0")
    out = f"{s[:-p10]}.{s[-p10:]}".rstrip("0").rstrip(".")
    return ("-" if num < 0 else "") + out


def base_trace(p, info_p, info_q):
    q = 1 - p
    term_p = p * info_p
    term_q = q * info_q
    entropy = term_p + term_q
    capacity = 1 - entropy
    steps = [
        make_step("BSC_SETUP", f"p={fraction_text(p)}",
                  f"-log2(p)={dec(info_p)}",
                  f"-log2(1-p)={dec(info_q)}"),
        make_step("S", 1, fraction_text(p), fraction_text(q)),
        make_step("BSC_FORMULA",
                  "H_b=p*(-log2 p)+(1-p)*(-log2(1-p))"),
        make_step("M", fraction_text(p), dec(info_p), dec(term_p)),
        make_step("M", fraction_text(q), dec(info_q), dec(term_q)),
        make_step("A", dec(term_p), dec(term_q), dec(entropy)),
        make_step("BSC_FORMULA", "C=1-H_b"),
        make_step("S", 1, dec(entropy), dec(capacity)),
    ]
    return steps, entropy, capacity


def expected_flow(example):
    p_raw, info_p_raw, info_q_raw, task = (
        PROBLEM_RE.fullmatch(example["problem"]).groups()
    )
    p = Fraction(p_raw)
    info_p = Fraction(info_p_raw)
    info_q = Fraction(info_q_raw)
    steps, entropy, capacity = base_trace(p, info_p, info_q)
    if task == "Find H_b(p).":
        answer = f"H_b={dec(entropy)} bits"
    elif task == "Find capacity C=1-H_b(p).":
        answer = f"C={dec(capacity)} bits/use"
    else:
        n_uses = int(BLOCK_RE.fullmatch(task).group(1))
        max_bits = n_uses * capacity
        steps.append(make_step("BSC_FORMULA", "max_bits=N*C"))
        steps.append(make_step("M", n_uses, dec(capacity), dec(max_bits)))
        answer = f"max_bits={dec(max_bits)} bits"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestChannelCapacityGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = ChannelCapacityGenerator()

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
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in ChannelCapacityGenerator.VARIANTS:
            result = ChannelCapacityGenerator(variant).generate()
            self.assertEqual(result["operation"], f"channel_capacity_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ChannelCapacityGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
