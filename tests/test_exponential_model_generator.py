"""Problem-text-only brute-force oracle for ExponentialModelGenerator."""
import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.exponential_model_generator import (
    APPLIED,
    MODIFIERS,
    ExponentialModelGenerator,
    dec,
    money,
)
from helpers import DELIM

GROWTH_WORDS = ("grows", "appreciates", "increases", "rises", "gains")
DECAY_WORDS = ("loses", "depreciates", "declines", "drops", "falls")

FORMULAS = {
    "growth": "A = P(1 + r)^t",
    "decay": "A = P(1 - r)^t",
    "half_life": "A = P · (1/2)^(t/h)",
    "continuous": "A = Pe^(rt)",
}


def clean(problem):
    return re.sub(r"^A nearby ledger lists \d+ unrelated entries\. ", "", problem)


def solve(problem):
    """A9 oracle: recompute every model exactly from the problem text.

    Parses whatever phrasing was chosen (after stripping any distractor
    lead-in), then rebuilds the plain (non ``with_model``) answer with exact
    Fraction arithmetic (repeated halving for half-life, a direct power for
    compound growth/decay). Returns ``(variant, answer, formula)``.
    """
    p = clean(problem)

    if "half-life" in p:
        h = int(re.search(r"half-life[^\d]*(\d+)", p).group(1))
        m_txt, unit = re.search(r"(\d+) (mg|kg|g)\b", p).groups()
        tu = re.search(r"\d+ (years|days|hours)", p).group(1)
        times = [int(v) for v in re.findall(rf"(\d+) {tu}\b", p)]
        elapsed = {v for v in times if v != h}
        assert len(elapsed) == 1, p
        t = elapsed.pop()
        assert t % h == 0, p
        remaining = int(m_txt)
        for _ in range(t // h):
            assert remaining % 2 == 0, p
            remaining //= 2
        return "half_life", f"{remaining} {unit}", FORMULAS["half_life"]

    P = int(re.search(r"\$(\d+)", p).group(1))
    r = int(re.search(r"(\d+)%", p).group(1))
    t = int(re.search(r"(\d+) years", p).group(1))

    if "continuously" in p:
        return ("continuous", f"{P}e^{dec(Fraction(r * t, 100))}",
                FORMULAS["continuous"])

    grew = any(w in p for w in GROWTH_WORDS)
    fell = any(w in p for w in DECAY_WORDS)
    assert grew != fell, p
    base = 1 + Fraction(r, 100) * (1 if grew else -1)
    variant = "growth" if grew else "decay"
    return variant, money(P * base ** t), FORMULAS[variant]


def expected(result):
    """``(variant, answer)`` expected for a live-generated record, honoring
    the ``with_model`` decoration read off its ``operation``."""
    variant, answer, formula = solve(result["problem"])
    if "with_model" in result["operation"]:
        answer = f"{formula}; {answer}"
    return variant, answer


class TestExponentialModelGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ExponentialModelGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_marker_and_oracle_over_every_variant_and_modifier(self):
        self.assertIs(APPLIED, True)
        random.seed(350)
        seen = set()
        for variant in ExponentialModelGenerator.VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(40):
                    result = ExponentialModelGenerator(variant, modifier).generate()
                    self.assertEqual(result["steps"][-1],
                                     f"Z{DELIM}{result['final_answer']}")
                    parsed_variant, answer = expected(result)
                    self.assertEqual(parsed_variant, variant, result["problem"])
                    self.assertEqual(answer, result["final_answer"], result["problem"])
                    seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in ExponentialModelGenerator.VARIANTS
                                for m in MODIFIERS})

    def test_oracle_answer_from_problem_text(self):
        for _ in range(600):
            result = self.gen.generate()
            variant, answer = expected(result)
            self.assertEqual(answer, result["final_answer"], result["problem"])

    def test_step_arithmetic_exact(self):
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] in ("A", "S", "M", "D", "E") and len(f) == 4:
                    x, y, z = (Fraction(v) for v in f[1:])
                    got = {"A": lambda: x + y, "S": lambda: x - y,
                           "M": lambda: x * y, "D": lambda: x / y,
                           "E": lambda: x ** int(f[2])}[f[0]]()
                    self.assertEqual(got, z, s)

    def test_half_life_halves_step_by_step(self):
        gen = ExponentialModelGenerator("half_life")
        for _ in range(200):
            result = gen.generate()
            divs = [s.split(DELIM) for s in result["steps"]
                    if s.startswith(f"D{DELIM}")]
            k = int(divs[0][3])  # first D is t/h
            self.assertEqual(len(divs) - 1, k, result["steps"])
            for d in divs[1:]:
                self.assertEqual(d[2], "2", d)

    def test_continuous_answers_stay_exact(self):
        gen = ExponentialModelGenerator("continuous", "plain")
        for _ in range(200):
            result = gen.generate()
            self.assertRegex(result["final_answer"], r"^\d+e\^[\d.]+$")
            self.assertNotIn("..", result["final_answer"])

    def test_money_answers_have_two_decimals(self):
        for v in ("growth", "decay"):
            gen = ExponentialModelGenerator(v, "plain")
            for _ in range(150):
                result = gen.generate()
                self.assertRegex(result["final_answer"], r"^\$\d+\.\d\d$")

    def test_half_life_answer_units(self):
        gen = ExponentialModelGenerator("half_life", "plain")
        units = set()
        for _ in range(300):
            result = gen.generate()
            self.assertRegex(result["final_answer"], r"^\d+ (mg|kg|g)$")
            units.add(result["final_answer"].split()[1])
        self.assertEqual(units, {"g", "mg", "kg"})

    def test_with_model_prepends_the_named_formula(self):
        for variant in ExponentialModelGenerator.VARIANTS:
            gen = ExponentialModelGenerator(variant, "with_model")
            for _ in range(60):
                result = gen.generate()
                self.assertTrue(
                    result["final_answer"].startswith(FORMULAS[variant] + "; "),
                    result["final_answer"])

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(352)
        for variant in ExponentialModelGenerator.VARIANTS:
            for modifier in MODIFIERS:
                result = ExponentialModelGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["operation"],
                                 f"applied_exponential_model_{variant}_{modifier}")
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
        with self.assertRaises(ValueError):
            ExponentialModelGenerator("bogus")
        with self.assertRaises(ValueError):
            ExponentialModelGenerator(modifier="bogus")

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(400):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {f"applied_exponential_model_{v}_{m}"
                               for v in ExponentialModelGenerator.VARIANTS
                               for m in MODIFIERS})

    def test_every_phrasing_is_parsed(self):
        """All phrasings must round-trip through the independent parser."""
        seen = set()
        for _ in range(1500):
            result = self.gen.generate()
            variant, answer = expected(result)
            self.assertEqual(answer, result["final_answer"], result["problem"])
            seen.add(clean(result["problem"]).split()[0])
        self.assertGreaterEqual(len(seen), 8)

    def test_every_variant_oracle(self):
        for variant in ExponentialModelGenerator.VARIANTS:
            gen = ExponentialModelGenerator(variant)
            for _ in range(300):
                result = gen.generate()
                parsed_variant, answer = expected(result)
                self.assertEqual(parsed_variant, variant)
                self.assertEqual(answer, result["final_answer"], result["problem"])

    def test_pipe_safety(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)), 5, s)

    def test_determinism_under_seed(self):
        random.seed(23)
        first = [self.gen.generate()["problem"] for _ in range(30)]
        random.seed(23)
        second = [self.gen.generate()["problem"] for _ in range(30)]
        self.assertEqual(first, second)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            ExponentialModelGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
