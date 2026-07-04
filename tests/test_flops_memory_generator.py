import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.flops_memory_generator import FLOPsMemoryGenerator
from helpers import DELIM


MATMUL_RE = re.compile(
    r"Compute FLOPs for an MLP forward pass X\(mxd\) @ W1\(dxh\) then "
    r"H\(mxh\) @ W2\(hxo\), using 2mnk per matmul, with "
    r"m=([0-9]+), d=([0-9]+), h=([0-9]+), o=([0-9]+)\."
)
KV_RE = re.compile(
    r"Compute KV-cache memory bytes for L=([0-9]+), h=([0-9]+), "
    r"d_k=([0-9]+), seq=([0-9]+), precision_bytes=([0-9]+) using "
    r"2\*L\*h\*d_k\*seq\*precision_bytes\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_matmul(problem):
    match = MATMUL_RE.fullmatch(problem)
    m = int(match.group(1))
    d = int(match.group(2))
    hidden = int(match.group(3))
    out = int(match.group(4))
    md = m * d
    first_half = md * hidden
    flops1 = 2 * first_half
    mh = m * hidden
    second_half = mh * out
    flops2 = 2 * second_half
    total = flops1 + flops2
    steps = [
        make_step("FLOPS_SETUP", "rule=2mnk",
                  f"m={m},d={d},h={hidden},o={out}"),
        make_step("M", m, d, md),
        make_step("M", md, hidden, first_half),
        make_step("M", 2, first_half, flops1),
        make_step("MATMUL_FLOPS", "XW1", flops1),
        make_step("M", m, hidden, mh),
        make_step("M", mh, out, second_half),
        make_step("M", 2, second_half, flops2),
        make_step("MATMUL_FLOPS", "HW2", flops2),
        make_step("A", flops1, flops2, total),
    ]
    answer = f"flops1={flops1}; flops2={flops2}; total_flops={total}"
    return steps, answer


def expected_kv(problem):
    match = KV_RE.fullmatch(problem)
    layers = int(match.group(1))
    heads = int(match.group(2))
    d_k = int(match.group(3))
    seq = int(match.group(4))
    precision = int(match.group(5))
    lh = layers * heads
    lhd = lh * d_k
    lhd_seq = lhd * seq
    kv_values = 2 * lhd_seq
    bytes_total = kv_values * precision
    mib = Fraction(bytes_total, 1024 * 1024)
    steps = [
        make_step("MEMORY_SETUP", "kv_cache",
                  f"L={layers},h={heads},d_k={d_k}",
                  f"seq={seq},precision_bytes={precision}"),
        make_step("M", layers, heads, lh),
        make_step("M", lh, d_k, lhd),
        make_step("M", lhd, seq, lhd_seq),
        make_step("M", 2, lhd_seq, kv_values),
        make_step("KV_CACHE", "values", kv_values),
        make_step("M", kv_values, precision, bytes_total),
        make_step("KV_CACHE", "bytes", bytes_total),
        make_step("D", bytes_total, 1024 * 1024, fraction_text(mib)),
        make_step("MEMORY_UNIT", "MiB", fraction_text(mib)),
    ]
    answer = f"bytes={bytes_total}; MiB={fraction_text(mib)}"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if MATMUL_RE.fullmatch(problem):
        steps, answer = expected_matmul(problem)
    elif KV_RE.fullmatch(problem):
        steps, answer = expected_kv(problem)
    else:
        raise AssertionError(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestFLOPsMemoryGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = FLOPsMemoryGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["operation"].startswith("flops_memory_"))
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
        for variant in FLOPsMemoryGenerator.VARIANTS:
            result = FLOPsMemoryGenerator(variant).generate()
            self.assertEqual(result["operation"], f"flops_memory_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            FLOPsMemoryGenerator("bogus")

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
