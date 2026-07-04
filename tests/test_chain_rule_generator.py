import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.chain_rule_generator import ChainRuleGenerator
from helpers import DELIM


def to_py(expr):
    """Math text -> evaluable Python (x is the free variable)."""
    s = expr.replace("^", "**")
    for _ in range(3):
        s = re.sub(r"(\d)x", r"\1*x", s)
        s = re.sub(r"(\d)\(", r"\1*(", s)
        s = re.sub(r"\)\(", ")*(", s)
        s = re.sub(r"\)x", ")*x", s)
        s = re.sub(r"x\(", "x*(", s)
    return s


def numeric_check(example):
    """Claimed derivative vs a central secant of the original."""
    m = re.fullmatch(r"Differentiate y = (.+)\.", example["problem"])
    body = to_py(m.group(1))
    ans = to_py(example["final_answer"].replace("y' = ", ""))
    for x in (0.37, 1.21, -0.83):
        h = 1e-6
        f_hi = eval(body, {"x": x + h})
        f_lo = eval(body, {"x": x - h})
        secant = (f_hi - f_lo) / (2 * h)
        claimed = eval(ans, {"x": x})
        scale = max(1.0, abs(claimed))
        if abs(secant - claimed) / scale > 1e-3:
            return False
    return True


class TestChainRuleGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ChainRuleGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_numeric_secant(self):
        """A9 oracle: central-difference agreement at three points."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertTrue(numeric_check(result),
                            (result["problem"], result["final_answer"]))

    def test_every_layer_substituted(self):
        gen = ChainRuleGenerator("nested")
        for _ in range(100):
            result = gen.generate()
            subs = [s for s in result["steps"]
                    if s.startswith(f"SUBST{DELIM}")]
            self.assertEqual(len(subs), 2)
            self.assertEqual(subs[0].split(DELIM)[1], "u")
            self.assertEqual(subs[1].split(DELIM)[1], "v")

    def test_constants_multiplied(self):
        for v in ("linear_power", "nested"):
            gen = ChainRuleGenerator(v)
            for _ in range(100):
                result = gen.generate()
                for s in result["steps"]:
                    f = s.split(DELIM)
                    if f[0] == "M":
                        self.assertEqual(int(f[1]) * int(f[2]),
                                         int(f[3]), s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            ChainRuleGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
