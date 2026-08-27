import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.geometric_sequence_generator import (
    GeometricSequenceGenerator,
)
from helpers import DELIM

SEQ_RE = re.compile(r"((?:-?\d+|__)(?:, (?:-?\d+|__))+), \.\.\.")
INT_RE = re.compile(r"-?\d+")

OPENING_MARKERS = [
    "The geometric",
    "begins",
    "on the board",
    "Consider the geometric",
    "is a fixed multiple",
    "with n starting at 1",
    "extends the geometric pattern",
    "form a geometric",
]

GOAL_MARKERS = {
    "geometric_sequence_nth_term": [
        "Find term ",
        "What is the ",
        "Find the ",
        "Determine the value of term ",
        "Which number appears as term ",
    ],
    "geometric_sequence_partial_sum": [
        "Find the sum of the first",
        "What is the total",
        "Add up the first",
        "Compute the sum S_",
        "Determine the sum of terms 1 through",
    ],
    "geometric_sequence_infinite_sum": [
        "sum of the infinite series",
        "What value does the infinite sum approach",
        "Compute the total of all the terms",
        "Evaluate the infinite sum",
        "Find the limit of its partial sums",
    ],
    "geometric_sequence_missing_term": [
        "Find the missing term",
        "What number belongs in the blank",
        "Determine the term hidden by the blank",
        "Supply the missing value",
        "Which number completes the sequence",
    ],
}


def read_problem(text):
    """Splits the sentence into shown terms and the goal clause."""
    m = SEQ_RE.search(text)
    assert m, text
    items = m.group(1).split(", ")
    return items, text[m.end():]


def ratio_of(vals):
    """Common ratio from the first visible adjacent pair."""
    for i in range(len(vals) - 1):
        if vals[i] is not None and vals[i + 1] is not None and vals[i] != 0:
            return vals[i + 1] / vals[i]
    raise AssertionError(vals)


def oracle_answer(example):
    """A9: recompute from the listed terms alone, without the closed forms."""
    text = example["problem"]
    items, goal = read_problem(text)
    vals = [None if x == "__" else Fraction(int(x)) for x in items]
    r = ratio_of(vals)

    if "__" in items:
        j = items.index("__")
        if j > 0 and vals[j - 1] is not None:
            vals[j] = vals[j - 1] * r
        else:
            vals[j] = vals[j + 1] / r
    for i in range(len(vals) - 1):
        assert vals[i + 1] == vals[i] * r, text
    if "__" in items:
        return str(vals[items.index("__")])

    a = vals[0]
    if ("infinite" in goal or "all the terms" in goal
            or "limit" in goal):
        assert abs(r) < 1, text
        total = a / (1 - r)
        # independent identity: S = a + r·S
        assert total == a + r * total, text
        return str(total)

    n = int(INT_RE.findall(goal)[-1])
    if "sum" in goal or "total" in goal or "Add up" in goal:
        # direct summation, not the closed form
        running, term = Fraction(0), a
        for _ in range(n):
            running += term
            term *= r
        return str(running)
    value = a
    for _ in range(n - 1):
        value *= r
    return str(value)


class TestGeometricSequenceGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = GeometricSequenceGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: recompute every variant with exact fractions."""
        for _ in range(2000):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_setup_step_lists_the_shown_terms(self):
        for _ in range(400):
            result = self.gen.generate()
            setup = result["steps"][0].split(DELIM)
            self.assertEqual(setup[0], "SEQ_SETUP")
            items, _ = read_problem(result["problem"])
            self.assertEqual(setup[1], ", ".join(items) + ", ...")

    def test_ratio_computed_and_verified(self):
        for _ in range(400):
            result = self.gen.generate()
            cr = next(s for s in result["steps"]
                      if s.startswith(f"COMMON_RATIO{DELIM}"))
            f = cr.split(DELIM)
            num, den = f[1].split("/", 1)
            self.assertEqual(Fraction(int(num), int(den.strip("()"))),
                             Fraction(f[2]), cr)
            items, _ = read_problem(result["problem"])
            vals = [None if x == "__" else Fraction(int(x)) for x in items]
            self.assertEqual(Fraction(f[2]), ratio_of(vals), cr)

    def test_check_steps_agree(self):
        seen = 0
        for _ in range(600):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] != "CHECK":
                    continue
                seen += 1
                self.assertEqual(f[1], "ratio", s)
                work, value = f[2].rsplit(" = ", 1)
                self.assertEqual(Fraction(value), Fraction(f[3]), s)
                num, den = work.split("/", 1)
                self.assertEqual(
                    Fraction(int(num), int(den.strip("()"))),
                    Fraction(value), s)
        self.assertGreater(seen, 300)

    def test_step_arithmetic_exact(self):
        for _ in range(600):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] in ("S", "M", "D") and len(f) == 4:
                    x, y, z = (Fraction(v) for v in f[1:])
                    got = {"S": lambda: x - y, "M": lambda: x * y,
                           "D": lambda: x / y}[f[0]]()
                    self.assertEqual(got, z, s)
                elif f[0] == "E":
                    base = Fraction(f[1].strip("()"))
                    self.assertEqual(base ** int(f[2]), Fraction(f[3]), s)

    def test_infinite_sum_states_convergence(self):
        gen = GeometricSequenceGenerator("infinite_sum")
        for _ in range(300):
            result = gen.generate()
            conv = next(s for s in result["steps"]
                        if s.startswith(f"CONVERGE_CHECK{DELIM}"))
            m = re.fullmatch(r"abs\(r\) = ([\d/]+) < 1",
                             conv.split(DELIM)[1])
            self.assertIsNotNone(m, conv)
            self.assertLess(Fraction(m.group(1)), 1, conv)

    def test_no_pipe_inside_step_fields(self):
        """The delimiter must never appear inside a field's math text."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertNotIn(DELIM, result["problem"])
            for s in result["steps"]:
                op = s.split(DELIM)[0]
                self.assertTrue(op.isupper() and op.replace("_", "").isalpha(),
                                s)
                self.assertLessEqual(len(s.split(DELIM)), 5, s)
            self.assertNotIn("  ", result["problem"])
            self.assertNotIn("--", result["final_answer"])

    def test_partial_sum_integer_ratio_gives_integer_answer(self):
        gen = GeometricSequenceGenerator("partial_sum")
        integer_ratio_seen = 0
        for _ in range(400):
            result = gen.generate()
            items, _ = read_problem(result["problem"])
            vals = [Fraction(int(x)) for x in items]
            if ratio_of(vals).denominator == 1:
                integer_ratio_seen += 1
                self.assertNotIn("/", result["final_answer"],
                                 result["problem"])
        self.assertGreater(integer_ratio_seen, 100)

    def test_shown_terms_are_integers_and_geometric(self):
        for _ in range(500):
            result = self.gen.generate()
            items, _ = read_problem(result["problem"])
            self.assertIn(len(items), (3, 4, 5), result["problem"])
            for item in items:
                if item != "__":
                    int(item)  # raises on anything non-integer

    def test_fraction_answers_occur_for_nth_term(self):
        gen = GeometricSequenceGenerator("nth_term")
        kinds = set()
        for _ in range(300):
            kinds.add("/" in gen.generate()["final_answer"])
        self.assertEqual(kinds, {True, False})

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(300):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, set(GOAL_MARKERS))

    def test_every_opening_and_goal_appears(self):
        openings = set()
        goals = {op: set() for op in GOAL_MARKERS}
        for _ in range(4000):
            result = self.gen.generate()
            text = result["problem"]
            hits = [m for m in OPENING_MARKERS if m in text]
            self.assertEqual(len(hits), 1, text)
            openings.add(hits[0])
            _, goal = read_problem(text)
            ghits = [m for m in GOAL_MARKERS[result["operation"]]
                     if m in goal]
            self.assertGreaterEqual(len(ghits), 1, text)
            goals[result["operation"]].add(ghits[0])
        self.assertEqual(openings, set(OPENING_MARKERS))
        for op, markers in GOAL_MARKERS.items():
            self.assertEqual(goals[op], set(markers), op)

    def test_problem_space_is_wide(self):
        texts = set()
        for _ in range(1500):
            texts.add(self.gen.generate()["problem"])
        self.assertGreater(len(texts), 1450)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            GeometricSequenceGenerator("bogus")
        for variant in GeometricSequenceGenerator.VARIANTS:
            gen = GeometricSequenceGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"geometric_sequence_{variant}")
                self.assertEqual(oracle_answer(result),
                                 result["final_answer"])


if __name__ == "__main__":
    unittest.main()
