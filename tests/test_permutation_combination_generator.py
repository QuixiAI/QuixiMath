import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.permutation_combination_generator import (
    MODIFIERS,
    PermutationCombinationGenerator,
)
from helpers import DELIM


def oracle_check(example):
    """A9 oracle: recompute the count from the problem text."""
    p = example["problem"]
    ans = int(re.search(r"(\d+)$", example["final_answer"]).group(1))
    m = re.search(r"Evaluate (\d+)!", p)
    if m:
        return ans == math.factorial(int(m.group(1)))
    m = re.search(r"Compute P\((\d+), (\d+)\)", p)
    if m:
        return ans == math.perm(int(m.group(1)), int(m.group(2)))
    m = re.search(r"Compute C\((\d+), (\d+)\)", p)
    if m:
        return ans == math.comb(int(m.group(1)), int(m.group(2)))
    m = re.search(r"(\d+) people be seated .* group of (\d+)", p)
    if m:
        return ans == math.perm(int(m.group(2)), int(m.group(1)))
    m = re.search(r"committee of (\d+) be chosen from a group of (\d+)",
                  p)
    return ans == math.comb(int(m.group(2)), int(m.group(1)))


class TestPermutationCombinationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = PermutationCombinationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        """A9 oracle: math.factorial / perm / comb agree with each answer."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_running_products_are_correct(self):
        """Every multiplication and final combination division is exact."""
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                if s.startswith(f"M{DELIM}"):
                    _, a, b, c = s.split(DELIM)
                    self.assertEqual(int(a) * int(b), int(c), s)
                elif s.startswith(f"D{DELIM}"):
                    _, a, b, c = s.split(DELIM)
                    self.assertEqual(int(a) // int(b), int(c), s)
                    self.assertEqual(int(a) % int(b), 0, s)

    def test_word_identifies_order(self):
        gen = PermutationCombinationGenerator("word")
        kinds = set()
        for _ in range(200):
            result = gen.generate()
            ident = next(s for s in result["steps"]
                         if s.startswith(f"IDENTIFY{DELIM}"))
            kinds.add(ident.split(DELIM)[2])
        self.assertEqual(kinds, {"use P(n, r)", "use C(n, r)"})

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(600):
            ops.add(self.gen.generate()["operation"])
        expected = {"permutation_combination_factorial",
                   "permutation_combination_permutation",
                   "permutation_combination_combination"}
        expected |= {f"permutation_combination_word_{m}" for m in MODIFIERS}
        self.assertEqual(ops, expected)

    def test_word_modifier_shapes_and_invalid_inputs(self):
        random.seed(55)
        for modifier in MODIFIERS:
            result = PermutationCombinationGenerator("word", modifier).generate()
            codes = [raw.split(DELIM)[0] for raw in result["steps"]]
            self.assertEqual(result["operation"], f"permutation_combination_word_{modifier}")
            if modifier == "distractor":
                self.assertEqual(codes[0], "SELECT_RELEVANT")
            elif modifier == "estimate_first":
                self.assertEqual(codes[0], "ESTIMATE")
                self.assertEqual(codes[-2], "ESTIMATE_CHECK")
            elif modifier == "with_model":
                self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            PermutationCombinationGenerator(modifier="bogus")

    def test_non_word_variants_have_no_modifier_suffix(self):
        for variant in ("factorial", "permutation", "combination"):
            result = PermutationCombinationGenerator(variant).generate()
            self.assertEqual(result["operation"], f"permutation_combination_{variant}")

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            PermutationCombinationGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
