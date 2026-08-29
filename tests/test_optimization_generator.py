import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.optimization_generator import MODIFIERS, OptimizationGenerator
from helpers import DELIM

MODELS = {
    "barn_fence": "A = x(P − 2x); max at x = P/4",
    "box": "V = x(W − 2x)²; max at x = W/6",
    "product": "P = x·y² with x + y = S; max at y = 2S/3",
}


def clean(problem):
    return re.sub(r"^An unrelated note mentions \d+ unrelated items\. ", "", problem)


def oracle_check(example):
    """Recompute the optimum and confirm it beats nearby values."""
    p = clean(example["problem"])
    answer = example["final_answer"]
    variant = None
    for name, model in MODELS.items():
        if answer.startswith(model + "; "):
            answer = answer[len(model) + 2:]
            variant = name
            break

    m = re.fullmatch(r"A farmer has (\d+) m of fence.*", p)
    if m:
        P = int(m.group(1))
        x = P // 4

        def A(t):
            return t * (P - 2 * t)
        want = (f"x = {x} m, long side = {P - 2 * x} m; maximum "
                f"area {A(x)} m²")
        return (variant in (None, "barn_fence") and answer == want and
                A(x) > A(x - 1) and A(x) > A(x + 1))
    m = re.fullmatch(r"An open-top box is made from a (\d+) by \1 "
                     r"sheet.*", p)
    if m:
        W = int(m.group(1))
        x = W // 6

        def V(t):
            return t * (W - 2 * t) ** 2
        want = f"x = {x}; maximum volume {V(x)}"
        return (variant in (None, "box") and answer == want and
                V(x) >= V(x - 0.1) and V(x) >= V(x + 0.1))
    m = re.fullmatch(r"Two positive numbers x and y satisfy "
                     r"x \+ y = (\d+)\. Maximize x·y²\.", p)
    assert m, p
    S = int(m.group(1))
    y = 2 * S // 3
    x = S - y

    def Pfn(t):
        return (S - t) * t * t
    want = f"x = {x}, y = {y}; maximum product {Pfn(y)}"
    return (variant in (None, "product") and answer == want and
            Pfn(y) >= Pfn(y - 0.1) and Pfn(y) >= Pfn(y + 0.1))


class TestOptimizationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = OptimizationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_optimum_verified(self):
        """A9 oracle: the reported optimum beats its neighbors."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_degenerate_roots_rejected(self):
        for v in ("box", "product"):
            gen = OptimizationGenerator(v)
            for _ in range(100):
                result = gen.generate()
                self.assertTrue(any(s.startswith(f"REJECT{DELIM}")
                                    for s in result["steps"]),
                                result["steps"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "S":
                    self.assertEqual(int(f[1]) - int(f[2]), int(f[3]), s)
                elif f[0] == "E":
                    self.assertEqual(int(f[1]) ** int(f[2]), int(f[3]), s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(400):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {f"optimization_{v}_{m}"
                               for v in OptimizationGenerator.VARIANTS
                               for m in MODIFIERS})

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(50)
        for variant in OptimizationGenerator.VARIANTS:
            for modifier in MODIFIERS:
                result = OptimizationGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["operation"], f"optimization_{variant}_{modifier}")
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
                    self.assertTrue(result["final_answer"].startswith(MODELS[variant] + "; "))
        with self.assertRaises(ValueError):
            OptimizationGenerator("bogus")
        with self.assertRaises(ValueError):
            OptimizationGenerator(modifier="bogus")

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            OptimizationGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
