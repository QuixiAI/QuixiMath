import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.param_count_generator import ParamCountGenerator
from helpers import DELIM


TRANSFORMER_RE = re.compile(
    r"Count parameters for a transformer with vocab=([0-9]+), "
    r"d_model=([0-9]+), layers=([0-9]+), and MLP multiplier ([0-9]+)\. "
    r"Include embeddings, attention matrices, MLP matrices, and the "
    r"12\*d\^2\*L estimate\."
)
LORA_RE = re.compile(
    r"Count LoRA parameters for a dense layer with d_in=([0-9]+), "
    r"d_out=([0-9]+), and rank r=([0-9]+)\. Compare r\(d_in\+d_out\) "
    r"with full fine-tuning d_in\*d_out\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_transformer(problem):
    match = TRANSFORMER_RE.fullmatch(problem)
    vocab = int(match.group(1))
    d_model = int(match.group(2))
    layers = int(match.group(3))
    mlp_mult = int(match.group(4))
    d2 = d_model * d_model
    attention = 4 * d2
    mlp = 2 * mlp_mult * d2
    per_layer = attention + mlp
    stack = per_layer * layers
    embeddings = vocab * d_model
    total = stack + embeddings
    approx_per_layer = 12 * d2
    approx_stack = approx_per_layer * layers
    steps = [
        make_step("PARAM_SETUP", "type=transformer",
                  f"vocab={vocab},d={d_model},layers={layers}",
                  f"mlp_mult={mlp_mult}"),
        make_step("M", d_model, d_model, d2),
        make_step("M", 4, d2, attention),
        make_step("PARAM_PART", "attention_per_layer", attention),
        make_step("M", 2 * mlp_mult, d2, mlp),
        make_step("PARAM_PART", "mlp_per_layer", mlp),
        make_step("A", attention, mlp, per_layer),
        make_step("PARAM_PART", "per_layer", per_layer),
        make_step("M", per_layer, layers, stack),
        make_step("PARAM_PART", "layer_stack", stack),
        make_step("M", vocab, d_model, embeddings),
        make_step("PARAM_PART", "embeddings", embeddings),
        make_step("A", stack, embeddings, total),
        make_step("M", 12, d2, approx_per_layer),
        make_step("M", approx_per_layer, layers, approx_stack),
        make_step("APPROX", "12*d^2*L", approx_stack),
    ]
    answer = (
        f"embeddings={embeddings}; per_layer={per_layer}; "
        f"stack={stack}; total={total}; approx_stack={approx_stack}"
    )
    return steps, answer


def expected_lora(problem):
    match = LORA_RE.fullmatch(problem)
    d_in = int(match.group(1))
    d_out = int(match.group(2))
    rank = int(match.group(3))
    full = d_in * d_out
    dim_sum = d_in + d_out
    lora = rank * dim_sum
    ratio = Fraction(lora, full)
    steps = [
        make_step("PARAM_SETUP", "type=lora",
                  f"d_in={d_in},d_out={d_out},rank={rank}"),
        make_step("M", d_in, d_out, full),
        make_step("PARAM_PART", "full_matrix", full),
        make_step("A", d_in, d_out, dim_sum),
        make_step("M", rank, dim_sum, lora),
        make_step("LORA_COUNT", "r*(d_in+d_out)", lora),
        make_step("D", lora, full, fraction_text(ratio)),
        make_step("APPROX", "lora/full", fraction_text(ratio)),
    ]
    answer = f"full={full}; lora={lora}; ratio={fraction_text(ratio)}"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if TRANSFORMER_RE.fullmatch(problem):
        steps, answer = expected_transformer(problem)
    elif LORA_RE.fullmatch(problem):
        steps, answer = expected_lora(problem)
    else:
        raise AssertionError(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestParamCountGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = ParamCountGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["operation"].startswith("param_count_"))
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
        for variant in ParamCountGenerator.VARIANTS:
            result = ParamCountGenerator(variant).generate()
            self.assertEqual(result["operation"], f"param_count_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ParamCountGenerator("bogus")

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
