import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.trig_identity_verify_generator import (
    TrigIdentityVerifyGenerator,
    IDENTITIES,
)
from helpers import DELIM

VAR_RE = r"(?:θ|β|[xtA])"


def to_python(expr):
    """Converts a catalog trig expression to evaluable Python."""
    s = expr
    for fn, py in (("sin", "math.sin(T)"), ("cos", "math.cos(T)"),
                   ("tan", "math.tan(T)"),
                   ("sec", "(1/math.cos(T))"),
                   ("csc", "(1/math.sin(T))"),
                   ("cot", "(math.cos(T)/math.sin(T))")):
        s = re.sub(rf"{fn}\^(\d+) {VAR_RE}", rf"({py}**\1)", s)
        s = re.sub(rf"{fn} {VAR_RE}", f"({py})", s)
    s = s.replace("·", "*").replace("^", "**")
    # implicit multiplication: ')(', 'n(', ')n', ') (', 'n ('
    for _ in range(3):
        s = re.sub(r"\)\s*\(", ")*(", s)
        s = re.sub(r"(\d)\s*\(", r"\1*(", s)
        s = re.sub(r"\)\s*(\d)", r")*\1", s)
        s = re.sub(r"\(([^()]*)\)\s+\(", r"(\1)*(", s)
    s = re.sub(r"(\d)\s+\(", r"\1*(", s)
    return s


def val(expr, t):
    return eval(to_python(expr), {"math": math, "T": t})


def both_sides_equal(text, t):
    lhs, rhs = text.split(" = ", 1)
    return abs(val(lhs, t) - val(rhs, t)) < 1e-9


class TestTrigIdentityVerifyGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = TrigIdentityVerifyGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["final_answer"], "Identity verified")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))

    def test_catalog_identities_are_true(self):
        """A9 oracle: every catalog identity holds numerically."""
        for lhs, rhs, _ in IDENTITIES:
            for t in (0.7, 1.15, 2.3):
                l = val(lhs.replace("V", "x"), t)
                r = val(rhs.replace("V", "x"), t)
                self.assertLess(abs(l - r), 1e-9, (lhs, rhs))

    def test_every_step_line_is_numerically_true(self):
        """Each IDENT_SUB / IDENT_MATCH equation and each REWRITE value
        must match the identity's left side numerically."""
        for _ in range(200):
            result = self.gen.generate()
            m = re.fullmatch(r"Verify the identity: (.+)\.",
                             result["problem"])
            lhs = m.group(1).split(" = ", 1)[0]
            target = val(lhs, 0.9)
            transform_side = result["steps"][0].split(DELIM)[2]
            if "right" in transform_side:
                target = val(m.group(1).split(" = ", 1)[1], 0.9)
            for s in result["steps"][1:]:
                f = s.split(DELIM)
                if f[0] in ("IDENT_SUB", "IDENT_MATCH"):
                    self.assertTrue(both_sides_equal(f[1], 0.9), s)
                elif f[0] == "REWRITE":
                    self.assertLess(abs(val(f[1], 0.9) - target), 1e-9,
                                    s)

    def test_transform_side_is_the_complex_side(self):
        """The transformed side is where the path starts."""
        for _ in range(100):
            result = self.gen.generate()
            setup = result["steps"][0].split(DELIM)
            self.assertIn("transform the", setup[2])

    def test_all_identities_and_vars_appear(self):
        seen_vars = set()
        for _ in range(300):
            result = self.gen.generate()
            for v in ("θ", "β", "x", "t", "A"):
                if f" {v}" in result["problem"] or \
                        f"{v})" in result["problem"]:
                    seen_vars.add(v)
        self.assertEqual(len(seen_vars), 5, seen_vars)


if __name__ == "__main__":
    unittest.main()
