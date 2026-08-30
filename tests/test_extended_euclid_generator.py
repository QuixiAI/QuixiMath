import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.extended_euclid_generator import ExtendedEuclidGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Use the extended Euclidean algorithm to find gcd\((\d+), (\d+)\) "
    r"and coefficients x,y with \d+x \+ \d+y = gcd\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    return tuple(map(int, match.groups()))


def expected_flow(a, b):
    old_r, r = a, b
    old_x, x = 1, 0
    old_y, y = 0, 1
    steps = [
        make_step("EXT_GCD_SETUP", a, b),
        make_step("BACK_SUB_ROW", f"r={old_r}", f"x={old_x}", f"y={old_y}"),
        make_step("BACK_SUB_ROW", f"r={r}", f"x={x}", f"y={y}"),
    ]

    while r != 0:
        q = old_r // r
        product = q * r
        new_r = old_r - product
        steps.append(make_step("EUCLID_DIV", old_r, r, q, new_r))
        steps.append(make_step("M", q, r, product))
        steps.append(make_step("S", old_r, product, new_r))

        qx = q * x
        new_x = old_x - qx
        steps.append(make_step("M", q, x, qx))
        steps.append(make_step("S", old_x, qx, new_x))

        qy = q * y
        new_y = old_y - qy
        steps.append(make_step("M", q, y, qy))
        steps.append(make_step("S", old_y, qy, new_y))
        steps.append(make_step("BACK_SUB_ROW", f"r={new_r}",
                               f"x={new_x}", f"y={new_y}"))

        old_r, r = r, new_r
        old_x, x = x, new_x
        old_y, y = y, new_y

    ax = a * old_x
    by = b * old_y
    steps.extend([
        make_step("M", a, old_x, ax),
        make_step("M", b, old_y, by),
        make_step("A", ax, by, old_r),
        make_step("BEZOUT_CHECK", f"{a}*{old_x} + {b}*{old_y}", old_r),
        make_step("CHECK", "gcd is last nonzero remainder", old_r),
    ])
    answer = f"gcd = {old_r}; x = {old_x}; y = {old_y}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestExtendedEuclidGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        # Pin the legacy face: the default draw now mixes in the depth
        # strand's tiered variants (see the module docstring).
        self.gen = ExtendedEuclidGenerator("legacy")

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "extended_euclid")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            a, b = parse_problem(result["problem"])
            expected_steps, answer = expected_flow(a, b)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_bezout_identity_and_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            a, b = parse_problem(result["problem"])
            answer_match = re.fullmatch(
                r"gcd = (-?\d+); x = (-?\d+); y = (-?\d+)",
                result["final_answer"],
            )
            self.assertIsNotNone(answer_match)
            g, x, y = map(int, answer_match.groups())
            self.assertEqual(a * x + b * y, g)
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "EUCLID_DIV":
                    dividend, divisor, quotient, remainder = map(
                        int, fields[1:]
                    )
                    self.assertEqual(dividend, quotient * divisor + remainder)
                    self.assertGreaterEqual(remainder, 0)
                    self.assertLess(remainder, divisor)
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(int(fields[1]) - int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "A":
                    self.assertEqual(int(fields[1]) + int(fields[2]),
                                     int(fields[3]), raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


class TestDepthVariants(unittest.TestCase):
    """The d50 retrofit faces (plans/depth_plan.md Strand E)."""

    def setUp(self):
        random.seed(42)

    def test_bezout_chain_reaches_the_floor_and_identity_holds(self):
        from depth_common import TIER_FLOORS
        from tests.depth_oracle import chain_depth
        gen = ExtendedEuclidGenerator("bezout")
        for _ in range(25):
            result = gen.generate()
            self.assertEqual(result["operation"],
                             "extended_euclid_bezout_d50")
            self.assertGreaterEqual(chain_depth(result["steps"]),
                                    TIER_FLOORS["d50"])
            a, b = map(int, re.search(r"\((\d+), (\d+)\)",
                                      result["problem"]).groups())
            g, x, y = map(int, re.fullmatch(
                r"gcd = (\d+); x = (-?\d+); y = (-?\d+)",
                result["final_answer"]).groups())
            import math
            self.assertEqual(math.gcd(a, b), g)
            self.assertEqual(a * x + b * y, g)
            n = int(re.search(r"(\d+) (?:division )?steps",
                              result["problem"]).group(1))
            pairs = [s2 for s2 in result["steps"]
                     if s2.startswith(f"EUCLID_PAIR{DELIM}")]
            self.assertEqual(len(pairs), n)
            # every pair step applies its stated quotient exactly
            for raw in pairs:
                fields = raw.split(DELIM)
                r0, r1 = map(int, fields[1].strip("()").split(", "))
                q = int(fields[2].removeprefix("q="))
                n0, n1 = map(int, fields[3].strip("()").split(", "))
                self.assertEqual((n0, n1), (r1, r0 - q * r1), raw)
            self.assertLessEqual(a, 2 * 10 ** 16)

    def test_crt_chain_solves_every_congruence(self):
        gen = ExtendedEuclidGenerator("crt_chain")
        for _ in range(25):
            result = gen.generate()
            self.assertEqual(result["operation"],
                             "extended_euclid_crt_chain_d50")
            congruences = re.findall(r"x = (\d+) \(mod (\d+)\)",
                                     result["problem"])
            x, modulus = map(int, re.fullmatch(
                r"x = (\d+) \(mod (\d+)\)",
                result["final_answer"]).groups())
            product = 1
            for residue, m in congruences:
                self.assertEqual(x % int(m), int(residue))
                product *= int(m)
            self.assertEqual(product, modulus)
            self.assertLess(x, modulus)

    def test_default_wrapper_preserves_legacy_rng_advancement(self):
        for seed in range(30):
            random.seed(seed)
            ExtendedEuclidGenerator("legacy").generate()
            expected_state = random.getstate()
            random.seed(seed)
            ExtendedEuclidGenerator().generate()
            self.assertEqual(random.getstate(), expected_state)

    def test_default_wrapper_reaches_all_three_faces(self):
        random.seed(4)
        gen = ExtendedEuclidGenerator()
        seen = {gen.generate()["operation"] for _ in range(120)}
        self.assertEqual(seen, {"extended_euclid",
                                "extended_euclid_bezout_d50",
                                "extended_euclid_crt_chain_d50"})

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            ExtendedEuclidGenerator("bogus")
        with self.assertRaises(ValueError):
            ExtendedEuclidGenerator("bezout", tier="d100")
        with self.assertRaises(ValueError):
            ExtendedEuclidGenerator(tier="d50")


if __name__ == "__main__":
    unittest.main()
