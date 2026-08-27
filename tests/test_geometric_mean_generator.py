import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.geometric_mean_generator import GeometricMeanGenerator
from helpers import DELIM

UNIT_RE = re.compile(
    r"\b(units|centimeters|millimeters|meters|inches|feet|yards"
    r"|cm|mm|ft|yd)\b")
NUM_RE = re.compile(r"\d+")


def rad(n):
    """Independent √n simplifier: prime factorization, not the generator's."""
    factors = {}
    m, d = n, 2
    while d * d <= m:
        while m % d == 0:
            factors[d] = factors.get(d, 0) + 1
            m //= d
        d += 1
    if m > 1:
        factors[m] = factors.get(m, 0) + 1
    outside, inside = 1, 1
    for prime, exp in factors.items():
        outside *= prime ** (exp // 2)
        if exp % 2:
            inside *= prime
    if inside == 1:
        return str(outside)
    return f"√{inside}" if outside == 1 else f"{outside}√{inside}"


def rad_squared(text):
    """Square of a rendered radical: '3√2' -> 18, '6' -> 36."""
    m = re.fullmatch(r"(\d+)?(?:√(\d+))?", text)
    assert m, text
    outside = int(m.group(1) or 1)
    inside = int(m.group(2) or 1)
    return outside * outside * inside


def classify(text):
    """Which relation the sentence asks for — from the goal wording alone."""
    if re.search(r"\bx\b", text):
        return "proportional"
    if re.search(r"\bc\b", text):
        return "hypotenuse"
    if "leg" in text:
        return "leg"
    if re.search(r"\bq\b", text):
        return "find_segment"
    if re.search(r"\bh\b", text):
        return "altitude"
    raise AssertionError(text)


def oracle_answer(example):
    """A9: rebuild the answer from the problem text by an independent route."""
    text = example["problem"]
    kind = classify(text)
    nums = [int(n) for n in NUM_RE.findall(text)]
    units = set(UNIT_RE.findall(text))
    if kind == "proportional":
        a, b = nums[0], nums[1]
        if units:
            assert len(units) == 1, text
            return f"x = {rad(a * b)} {units.pop()}"
        return "x = " + rad(a * b)
    assert len(units) == 1, text
    unit = units.pop()
    first, second = nums[0], nums[1]
    if kind == "altitude":
        return f"h = {rad(first * second)} {unit}"
    if kind == "leg":
        return f"leg = {rad(first * (first + second))} {unit}"
    if kind == "find_segment":
        assert (first * first) % second == 0, text
        return f"q = {first * first // second} {unit}"
    assert (first * first) % second == 0, text
    return f"c = {first * first // second} {unit}"


PHRASE_MARKERS = {
    "geometric_mean_altitude": [
        "splits it into segments of length",
        "meets the hypotenuse",
        "cuts it into a piece",
        "lands on",
        "is laying out a right-triangular",
    ],
    "geometric_mean_leg": [
        "Find the leg adjacent to the segment of length p.",
        "the one that meets segment",
        "beside one leg",
        "measures a right-triangular",
        "whose projection on the hypotenuse is",
    ],
    "geometric_mean_find_segment": [
        "splits the hypotenuse into two",
        "to the hypotenuse measures",
        "How long is the other piece q?",
        "draws the altitude of a right-triangular",
        "Determine q, the length of",
    ],
    "geometric_mean_hypotenuse": [
        "its projection on the hypotenuse is",
        "find the hypotenuse c, the length of",
        "cuts off a piece of",
        "checks a right-triangular",
        "it projects onto the hypotenuse is",
    ],
    "geometric_mean_proportional": [
        "Find the geometric mean x of",
        "Solve the proportion",
        "What positive number x satisfies",
        "needs the mean proportional x between",
        "form a geometric sequence",
        "mean proportional between them",
        "needs a brace whose length x",
        "that is the geometric mean of those two segments",
    ],
}


class TestGeometricMeanGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = GeometricMeanGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: reapply the relations independently."""
        for _ in range(2000):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_relation_holds_by_squaring(self):
        """Second route: square the reported length and check the product."""
        for _ in range(800):
            result = self.gen.generate()
            text = result["problem"]
            kind = classify(text)
            nums = [int(n) for n in NUM_RE.findall(text)]
            value = result["final_answer"].split(" = ", 1)[1].split(" ")[0]
            if kind == "altitude":
                self.assertEqual(rad_squared(value), nums[0] * nums[1], text)
            elif kind == "leg":
                self.assertEqual(rad_squared(value),
                                 nums[0] * (nums[0] + nums[1]), text)
            elif kind == "proportional":
                self.assertEqual(rad_squared(value), nums[0] * nums[1], text)
            elif kind == "find_segment":
                self.assertEqual(int(value) * nums[1], nums[0] * nums[0], text)
            else:
                self.assertEqual(int(value) * nums[1], nums[0] * nums[0], text)

    def test_radicals_are_fully_simplified(self):
        for _ in range(600):
            result = self.gen.generate()
            m = re.search(r"(?:(\d+))?√(\d+)", result["final_answer"])
            if m:
                inside = int(m.group(2))
                for f in range(2, int(math.isqrt(inside)) + 1):
                    self.assertNotEqual(inside % (f * f), 0,
                                        result["final_answer"])

    def test_step_arithmetic(self):
        for _ in range(600):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)
                elif f[0] == "E":
                    self.assertEqual(int(f[1]) ** int(f[2]), int(f[3]), s)
                elif f[0] == "D":
                    self.assertEqual(int(f[1]), int(f[2]) * int(f[3]), s)

    def test_check_steps_agree(self):
        seen = 0
        for _ in range(600):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] != "CHECK":
                    continue
                seen += 1
                self.assertIn(f[1], ("substitute", "cross_products"), s)
                lhs = int(f[2].rsplit("= ", 1)[1])
                rhs = int(f[3].rsplit("= ", 1)[1])
                self.assertEqual(lhs, rhs, s)
        self.assertGreater(seen, 100)

    def test_root_simplify_step_matches_answer(self):
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                if s.startswith("ROOT_SIMPLIFY" + DELIM):
                    body = s.split(DELIM)[1]
                    if body.endswith("has no perfect-square factor"):
                        inside = int(body.split()[0][1:])
                        self.assertEqual(rad(inside), f"√{inside}", s)
                        self.assertIn(f"√{inside}", result["final_answer"], s)
                        continue
                    left, right = body.split(" = ")
                    self.assertEqual(rad(int(left[1:])), right, s)
                    self.assertIn(right, result["final_answer"], s)

    def test_pipe_safety_and_render_sanity(self):
        for _ in range(400):
            result = self.gen.generate()
            self.assertNotIn(DELIM, result["problem"])
            for s in result["steps"]:
                fields = s.split(DELIM)
                self.assertLessEqual(len(fields), 5, s)
                for field in fields[1:]:
                    self.assertNotIn(DELIM, field)
            self.assertNotIn("  ", result["problem"])
            self.assertNotIn(" .", result["problem"])
            self.assertNotIn("--", result["final_answer"])

    def test_integer_and_radical_answers_occur(self):
        kinds = set()
        for _ in range(300):
            kinds.add("√" in self.gen.generate()["final_answer"])
        self.assertEqual(kinds, {True, False})

    def test_units_echo_the_problem(self):
        for _ in range(300):
            result = self.gen.generate()
            units = set(UNIT_RE.findall(result["problem"]))
            if units:
                self.assertTrue(
                    result["final_answer"].endswith(" " + units.pop()),
                    result["final_answer"])
            else:
                self.assertFalse(UNIT_RE.search(result["final_answer"]),
                                 result["final_answer"])

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(300):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, set(PHRASE_MARKERS))

    def test_every_phrasing_appears(self):
        pending = {op: set(markers) for op, markers in PHRASE_MARKERS.items()}
        for _ in range(4000):
            result = self.gen.generate()
            op = result["operation"]
            text = result["problem"]
            hits = [m for m in PHRASE_MARKERS[op] if m in text]
            self.assertEqual(len(hits), 1, text)
            pending[op].discard(hits[0])
        for op, missing in pending.items():
            self.assertFalse(missing, f"{op}: {missing}")

    def test_problem_space_is_wide(self):
        texts = set()
        for _ in range(1500):
            texts.add(self.gen.generate()["problem"])
        self.assertGreater(len(texts), 1450)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            GeometricMeanGenerator("bogus")
        for variant in GeometricMeanGenerator.VARIANTS:
            gen = GeometricMeanGenerator(variant)
            for _ in range(30):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"geometric_mean_{variant}")
                self.assertEqual(oracle_answer(result),
                                 result["final_answer"])


if __name__ == "__main__":
    unittest.main()
