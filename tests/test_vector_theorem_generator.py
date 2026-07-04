import math
import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.vector_theorem_generator import VectorTheoremGenerator
from helpers import DELIM


def fmt_pi(coeff):
    if coeff == 1:
        return "pi"
    if coeff == -1:
        return "-pi"
    return f"{coeff}*pi"


def parse_term(term, var):
    if term == "0":
        return 0
    if term == var:
        return 1
    if term == f"-{var}":
        return -1
    coeff, got_var = term.split("*")
    assert got_var == var
    return int(coeff)


def oracle_answer(example):
    problem = example["problem"]
    if "Green's theorem" in problem:
        q_txt, width, height = re.fullmatch(
            r"Use Green's theorem to compute the counterclockwise "
            r"circulation of F=<0, (.+)> around the rectangle "
            r"0 <= x <= (\d+), 0 <= y <= (\d+)\.",
            problem,
        ).groups()
        value = parse_term(q_txt, "x") * int(width) * int(height)
        return f"circulation {value}"
    if "divergence theorem" in problem:
        p_txt, q_txt, r_txt, length, width, height = re.fullmatch(
            r"Use the divergence theorem to compute the outward flux "
            r"of F=<(.+), (.+), (.+)> through the box "
            r"0 <= x <= (\d+), 0 <= y <= (\d+), 0 <= z <= (\d+)\.",
            problem,
        ).groups()
        div = (parse_term(p_txt, "x") + parse_term(q_txt, "y") +
               parse_term(r_txt, "z"))
        value = div * int(length) * int(width) * int(height)
        return f"outward flux {value}"
    p_txt, radius_sq = re.fullmatch(
        r"Use Stokes' theorem to compute the counterclockwise circulation "
        r"of F=<(.+), 0, 0> around the circle x\^2 \+ y\^2 = "
        r"(\d+) in the plane z = 0\.",
        problem,
    ).groups()
    curl_z = -parse_term(p_txt, "y")
    radius = math.isqrt(int(radius_sq))
    return f"circulation {fmt_pi(curl_z * radius * radius)}"


def eval_pi_expr(expr):
    assert expr.endswith("*pi")
    expr = expr[:-3].replace("^", "**")
    expr = re.sub(r"\d+", lambda m: f"Fraction({m.group(0)})", expr)
    return eval(expr, {"__builtins__": {}, "Fraction": Fraction}, {})


def coeff_from_pi(text):
    if text == "pi":
        return Fraction(1)
    if text == "-pi":
        return Fraction(-1)
    return Fraction(text[:-3])


def eval_arith(expr):
    expr = expr.replace("^", "**")
    return Fraction(eval(expr, {"__builtins__": {}}, {}))


def check_step_arithmetic(example):
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        if parts[0] == "REGION_MEASURE" and "pi" not in parts[2]:
            if eval_arith(parts[2]) != Fraction(parts[3]):
                return False
        elif parts[0] == "FLUX_SUM":
            if eval_arith(parts[1]) != Fraction(parts[2]):
                return False
        elif parts[0] == "CIRCULATION_SUM":
            if "pi" in parts[1]:
                if eval_pi_expr(parts[1]) != coeff_from_pi(parts[2]):
                    return False
            elif eval_arith(parts[1]) != Fraction(parts[2]):
                return False
    return True


class TestVectorTheoremGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = VectorTheoremGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_variant_markers(self):
        markers = {
            "green_rectangle": "Green's theorem",
            "divergence_box": "divergence theorem",
            "stokes_disk": "Stokes' theorem",
        }
        for variant, phrase in markers.items():
            gen = VectorTheoremGenerator(variant)
            for _ in range(40):
                result = gen.generate()
                self.assertIn(phrase, result["problem"])

    def test_no_degenerate_rendering(self):
        bad = re.compile(r"(?<!\d)1\*|\+ 0|--")
        for _ in range(300):
            result = self.gen.generate()
            self.assertIsNone(bad.search(result["problem"]))
            self.assertIsNone(bad.search(result["final_answer"]))

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            VectorTheoremGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
