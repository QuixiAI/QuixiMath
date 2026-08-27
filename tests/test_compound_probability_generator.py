import math
import os
import random
import re
import sys
import unittest
from fractions import Fraction

current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.compound_probability_generator import (
    CompoundProbabilityIndependentGenerator,
    CompoundProbabilityDependentGenerator,
)
from helpers import DELIM


# --- oracle machinery (independent of the generator) -----------------------

COLORS = ["red", "blue", "green", "yellow", "purple", "orange",
          "white", "black", "silver", "gold"]
COLOR_ALT = "|".join(COLORS)
ROSTER_RE = re.compile(rf"(\d+) ({COLOR_ALT})\b")
SEQ_RE = re.compile(rf"\b({COLOR_ALT}), then ({COLOR_ALT})"
                    rf"(?:, then ({COLOR_ALT}))?")
NUMBERED_RE = re.compile(r"numbered 1 to (\d+)")
NUMBERED_D_RE = re.compile(r"(\d+) (?:tickets|balls|tiles|chips|cards"
                           r"|tokens|discs|counters)")
PROP_RE = re.compile(r"all (even|odd|multiples of \d+|greater than \d+|"
                     r"less than \d+)")
CARD_D_RE = re.compile(r"(\d+) cards")
CARD_TARGET_RE = re.compile(r"(?:all of them are|are all|every one of them "
                            r"is|all \d+ are) ([a-z ]+)[?.]")

RANKS = ["ace", "two", "three", "four", "five", "six", "seven", "eight",
         "nine", "ten", "jack", "queen", "king"]
SUITS = ["hearts", "diamonds", "clubs", "spades"]
DECK = [(rank, suit) for rank in RANKS for suit in SUITS]


def card_matches(target):
    """Predicate over (rank, suit) built from the target words alone."""
    target = target.strip()
    for article in ("a ", "an ", "the "):
        if target.startswith(article):
            target = target[len(article):]
    if target.endswith("es") and target[:-2] in RANKS:
        target = target[:-2]
    elif target.endswith("s") and target[:-1] in RANKS:
        target = target[:-1]
    if target in RANKS:
        return lambda card: card[0] == target
    if target in SUITS:
        return lambda card: card[1] == target
    if target + "s" in SUITS:
        return lambda card: card[1] == target + "s"
    if target in ("red card", "red cards"):
        return lambda card: card[1] in ("hearts", "diamonds")
    if target in ("black card", "black cards"):
        return lambda card: card[1] in ("clubs", "spades")
    if target in ("face card", "face cards"):
        return lambda card: card[0] in ("jack", "queen", "king")
    if target in ("number card", "number cards"):
        return lambda card: card[0] in RANKS[1:10]
    raise AssertionError(f"unknown card target: {target!r}")


def number_matches(prop):
    """Predicate over integers built from the property words alone."""
    if prop == "even":
        return lambda v: v % 2 == 0
    if prop == "odd":
        return lambda v: v % 2 == 1
    m = re.fullmatch(r"multiples of (\d+)", prop)
    if m:
        step_size = int(m.group(1))
        return lambda v: v % step_size == 0
    m = re.fullmatch(r"greater than (\d+)", prop)
    if m:
        cut = int(m.group(1))
        return lambda v: v > cut
    m = re.fullmatch(r"less than (\d+)", prop)
    if m:
        cut = int(m.group(1))
        return lambda v: v < cut
    raise AssertionError(f"unknown property: {prop!r}")


def oracle_probability(problem):
    """Recompute the answer from the problem text by counting outcomes."""
    if NUMBERED_RE.search(problem):
        n = int(NUMBERED_RE.search(problem).group(1))
        draws = int(NUMBERED_D_RE.search(problem).group(1))
        prop = PROP_RE.search(problem).group(1)
        favorable = sum(1 for v in range(1, n + 1)
                        if number_matches(prop)(v))
        return Fraction(math.comb(favorable, draws), math.comb(n, draws))
    if "deck" in problem:
        draws = int(CARD_D_RE.search(problem).group(1))
        target = CARD_TARGET_RE.search(problem).group(1)
        favorable = sum(1 for card in DECK if card_matches(target)(card))
        return Fraction(math.comb(favorable, draws), math.comb(52, draws))
    counts = {color: int(num) for num, color in ROSTER_RE.findall(problem)}
    total = sum(counts.values())
    seq = [c for c in SEQ_RE.search(problem).groups() if c]
    wanted = {}
    for color in seq:
        wanted[color] = wanted.get(color, 0) + 1
    numerator = 1
    for color, times in wanted.items():
        numerator *= math.perm(counts[color], times)
    return Fraction(numerator, math.perm(total, len(seq)))


def independent_oracle_probability(problem):
    """Parse the independent experiment and multiply exact atom weights."""
    coin = re.search(
        r"fair coin is flipped twice\. Target order: (heads|tails), then "
        r"(heads|tails)\.", problem)
    if coin:
        return Fraction(1, 4)
    dice = re.search(
        r"fair (\d+)-sided die and a fair (\d+)-sided die are rolled\. "
        r"Target faces: (\d+), then (\d+)\.", problem)
    if dice:
        sides1, sides2, target1, target2 = map(int, dice.groups())
        assert 1 <= target1 <= sides1 and 1 <= target2 <= sides2
        return Fraction(1, sides1 * sides2)
    mixed = re.search(
        r"fair coin and a fair (\d+)-sided die are used\. Target outcomes: "
        r"(heads|tails), then (\d+)\.", problem)
    if mixed:
        sides, _coin, target = mixed.groups()
        assert 1 <= int(target) <= int(sides)
        return Fraction(1, 2 * int(sides))
    roster = re.search(
        r"contains ((?:[a-z]+=[0-9]+(?:, )?)+) "
        r"(?:marbles|beads|tokens|balls|buttons|chips|cubes|tiles)\.",
        problem)
    target = re.search(r"Target order: ([a-z]+(?:, then [a-z]+)+)\.",
                       problem)
    assert roster and target, problem
    counts = {color: int(count)
              for color, count in re.findall(r"([a-z]+)=([0-9]+)",
                                             roster.group(1))}
    total = sum(counts.values())
    wanted = target.group(1).split(", then ")
    value = Fraction(1)
    for color in wanted:
        value *= Fraction(counts[color], total)
    return value


class TestCompoundProbabilityIndependentGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = CompoundProbabilityIndependentGenerator()

    def test_generate_output_format(self):
        result = self.generator.generate()
        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIn("operation", result)
        self.assertEqual(result["operation"], "compound_probability_independent")
        self.assertIn("problem", result)
        self.assertIn("steps", result)
        self.assertIn("final_answer", result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))

    def test_generate_consistency(self):
        for _ in range(20):
            result = self.generator.generate()
            has_setup = any(s.startswith(f"PROB_DESCRIBE{DELIM}") for s in result["steps"])
            has_independent = any(s.startswith(f"PROB_INDEPENDENT{DELIM}") for s in result["steps"])
            has_multiply = any(s.startswith(f"PROB_MULTIPLY{DELIM}") for s in result["steps"])

            self.assertTrue(has_setup, "Missing PROB_DESCRIBE step")
            self.assertTrue(has_independent, "Missing PROB_INDEPENDENT step")
            self.assertTrue(has_multiply, "Missing PROB_MULTIPLY step")

    def test_answer_is_fraction(self):
        for _ in range(10):
            result = self.generator.generate()
            # Answer should be in fraction form (contains /)
            self.assertIn("/", result["final_answer"])

    def test_oracle_from_problem_text(self):
        """A9: enumerate each printed experiment's independent atoms."""
        for _ in range(1600):
            result = self.generator.generate()
            expected = independent_oracle_probability(result["problem"])
            self.assertEqual(Fraction(result["final_answer"]), expected,
                             result["problem"])
            self.assertEqual(result["final_answer"], str(expected))
            self.assertEqual(result["steps"][-1],
                             f"Z{DELIM}{result['final_answer']}")

    def test_step_arithmetic(self):
        for _ in range(500):
            result = self.generator.generate()
            products = []
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "PROB_MULTIPLY":
                    first, second, product = map(Fraction, fields[1:4])
                    self.assertEqual(first * second, product, raw)
                    products.append(product)
            self.assertTrue(products)
            self.assertEqual(products[-1], Fraction(result["final_answer"]))

    def test_all_scenarios_and_phrasings_vary(self):
        scenarios = set()
        problems = set()
        for _ in range(800):
            problem = self.generator.generate()["problem"]
            problems.add(problem)
            if "flipped twice" in problem:
                scenarios.add("coins")
            elif "-sided die and a fair" in problem:
                scenarios.add("dice")
            elif "fair coin and a fair" in problem:
                scenarios.add("coin_die")
            elif "After every draw" in problem:
                scenarios.add("replacement")
        self.assertEqual(scenarios,
                         {"coins", "dice", "coin_die", "replacement"})
        self.assertGreater(len(problems), 760)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.generator.generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


class TestCompoundProbabilityDependentGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = CompoundProbabilityDependentGenerator()

    def test_generate_output_format(self):
        result = self.generator.generate()
        self.assertIsInstance(result, dict)
        self.assertIn("operation", result)
        self.assertEqual(result["operation"], "compound_probability_dependent")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_generate_consistency(self):
        for _ in range(20):
            result = self.generator.generate()
            has_setup = any(s.startswith(f"PROB_DESCRIBE{DELIM}") for s in result["steps"])
            has_dependent = any(s.startswith(f"PROB_DEPENDENT{DELIM}") for s in result["steps"])
            has_conditional = any(s.startswith(f"PROB_CONDITIONAL{DELIM}") for s in result["steps"])

            self.assertTrue(has_setup, "Missing PROB_DESCRIBE step")
            self.assertTrue(has_dependent, "Missing PROB_DEPENDENT step")
            self.assertTrue(has_conditional, "Missing PROB_CONDITIONAL step")

    def test_without_replacement_context(self):
        """Test that problems mention 'without replacement'."""
        for _ in range(50):
            result = self.generator.generate()
            self.assertIn("without replacement", result["problem"].lower())

    def test_oracle_counts_outcomes_from_problem_text(self):
        """A9: recount the sample space (permutations / combinations)."""
        for _ in range(1200):
            result = self.generator.generate()
            expected = oracle_probability(result["problem"])
            self.assertEqual(Fraction(result["final_answer"]), expected,
                             result["problem"])
            self.assertGreater(expected, 0)
            self.assertLess(expected, 1)

    def test_answer_is_in_lowest_terms(self):
        for _ in range(300):
            result = self.generator.generate()
            value = Fraction(result["final_answer"])
            self.assertEqual(result["final_answer"], str(value))

    def test_step_arithmetic(self):
        for _ in range(400):
            result = self.generator.generate()
            product = None
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "PROB_MULTIPLY":
                    a, b, c = (Fraction(f) for f in fields[1:4])
                    self.assertEqual(a * b, c, raw)
                    na, da = (int(x) for x in fields[1].split("/"))
                    nb, db = (int(x) for x in fields[2].split("/"))
                    self.assertEqual(fields[3], f"{na * nb}/{da * db}", raw)
                    product = c
                elif fields[0] == "PROB_SIMPLIFY":
                    self.assertEqual(Fraction(fields[1]), Fraction(fields[2]),
                                     raw)
                    self.assertEqual(fields[2], str(Fraction(fields[2])), raw)
                    product = Fraction(fields[2])
            self.assertEqual(product, Fraction(result["final_answer"]))

    def test_first_and_conditional_probabilities_match_counts(self):
        for _ in range(400):
            result = self.generator.generate()
            identify = next(s for s in result["steps"]
                            if s.startswith(f"PROB_IDENTIFY{DELIM}"))
            conds = [s for s in result["steps"]
                     if s.startswith(f"PROB_CONDITIONAL{DELIM}")]
            first = identify.split(DELIM)[2]
            _, den = (int(x) for x in first.split("/"))
            for offset, cond in enumerate(conds, start=1):
                cnum, cden = (int(x) for x in
                              cond.split(DELIM)[2].split("/"))
                self.assertEqual(cden, den - offset, cond)
                self.assertGreaterEqual(cnum, 1)

    def test_all_three_scenarios_appear(self):
        kinds = set()
        for _ in range(400):
            problem = self.generator.generate()["problem"]
            if "numbered 1 to" in problem:
                kinds.add("numbered")
            elif "deck" in problem:
                kinds.add("cards")
            else:
                kinds.add("bag")
        self.assertEqual(kinds, {"numbered", "cards", "bag"})

    def test_three_draw_problems_occur(self):
        found = False
        for _ in range(300):
            result = self.generator.generate()
            if len([s for s in result["steps"]
                    if s.startswith(f"PROB_CONDITIONAL{DELIM}")]) == 2:
                found = True
                break
        self.assertTrue(found)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.generator.generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)

    def test_problem_texts_vary(self):
        problems = {self.generator.generate()["problem"] for _ in range(400)}
        self.assertGreater(len(problems), 380)


if __name__ == "__main__":
    unittest.main()
