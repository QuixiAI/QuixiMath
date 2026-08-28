"""Problem-text-only oracles for :class:`MethodDiscriminationGenerator`."""
import itertools
import math
import random
import re
import unittest
from fractions import Fraction

from generators.method_discrimination_generator import (
    APPLIED,
    FRAMES,
    MODIFIERS,
    VARIANTS,
    MethodDiscriminationGenerator,
)
from helpers import DELIM


def number(token):
    return Fraction(token.replace("$", ""))


def exact_text(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    scaled, places = value, 0
    while scaled.denominator != 1 and places < 12:
        scaled *= 10
        places += 1
    if scaled.denominator != 1:
        return f"{value.numerator}/{value.denominator}"
    digits = str(abs(scaled.numerator)).rjust(places + 1, "0")
    rendered = (digits[:-places] + "." + digits[-places:]).rstrip("0").rstrip(".")
    return ("-" if value < 0 else "") + rendered


def money_text(value):
    cents = Fraction(value) * 100
    if cents.denominator != 1:
        raise AssertionError(f"not exact cents: {value}")
    return f"${cents.numerator // 100}.{cents.numerator % 100:02d}"


def clean(problem):
    return re.sub(r"^A shelf nearby holds \d+ blank cards\. ", "", problem)


def solve(problem):
    """Infer both structures from cues and recompute both numeric facts."""
    text = clean(problem)

    match = re.search(r"Task A selects (\d+) of (\d+) books", text, re.I)
    if match:
        r, n = map(int, match.groups())
        choose = len(list(itertools.combinations(range(n), r)))
        arrange = len(list(itertools.permutations(range(n), r)))
        model = f"A=C({n},{r}); B=P({n},{r})"
        answer = f"A: combination, {choose}; B: permutation, {arrange}"
        return "combination_vs_permutation", answer, model

    match = re.search(r"bag contains (\d+) red tokens among (\d+) tokens", text, re.I)
    if match:
        red, total = map(int, match.groups())
        first = Fraction(red, total) ** 2
        second = Fraction(red, total) * Fraction(red - 1, total - 1)
        model = f"A=({red}/{total})^2; B=({red}/{total})*({red - 1}/{total - 1})"
        answer = (f"A: independent, {exact_text(first)}; B: dependent, "
                  f"{exact_text(second)}")
        return "independent_vs_dependent", answer, model

    match = re.search(r"rectangle is (\d+) cm long and (\d+) cm wide", text, re.I)
    if match:
        length, width = map(int, match.groups())
        perimeter, area = 2 * length + 2 * width, length * width
        model = f"A=2({length}+{width}); B={length}*{width}"
        answer = f"A: perimeter, {perimeter} cm; B: area, {area} cm²"
        return "area_vs_perimeter", answer, model

    match = re.search(r"data list ([0-9, ]+)\. Task A", text, re.I)
    if match:
        values = list(map(int, re.findall(r"\d+", match.group(1))))
        mean = Fraction(sum(values), len(values))
        median = sorted(values)[len(values) // 2]
        data = ", ".join(map(str, values))
        model = f"A=({'+'.join(map(str, values))})/5; B=middle({data})"
        answer = f"A: mean, {exact_text(mean)}; B: median, {median}"
        return "mean_vs_median", answer, model

    match = re.search(
        r"accounts each start with (\$\d+\.\d{2})\. Account A adds "
        r"(\$\d+\.\d{2}).*?Account B grows by (\d+)%.*?after (\d+) years",
        text, re.I)
    if match:
        start, addition = number(match.group(1)), number(match.group(2))
        rate, years = int(match.group(3)), int(match.group(4))
        linear = start + addition * years
        exponential = start * Fraction(100 + rate, 100) ** years
        model = f"A={start}+{addition}*{years}; B={start}*(1+{rate}/100)^{years}"
        answer = (f"A: linear, {money_text(linear)}; B: exponential, "
                  f"{money_text(exponential)}")
        return "linear_vs_exponential", answer, model

    match = re.search(
        r"Task A gives input-output records (.+?)\. Task B uses the same inputs "
        r"but records (.+?)\.", text, re.I)
    if match:
        rows_a = [(int(x), int(y)) for x, y in re.findall(r"(\d+) to (\d+)", match.group(1))]
        rows_b = [(int(x), int(y)) for x, y in re.findall(r"(\d+) to (\d+)", match.group(2))]
        rate = Fraction(rows_a[0][1], rows_a[0][0])
        self_fixed = rows_b[0][1] - rate * rows_b[0][0]
        query = int(re.search(r"at input (\d+)", text, re.I).group(1))
        first, second = rate * query, self_fixed + rate * query
        model = f"A:y={rate}x; B:y={self_fixed}+{rate}x"
        answer = (f"A: proportional, y={exact_text(first)}; B: not proportional, "
                  f"y={exact_text(second)} at x={query}")
        return "proportional_vs_not", answer, model

    match = re.search(
        r"machines start at (\d+) units and run for (\d+) rounds\. Machine A "
        r"adds (\d+) units each round\. Machine B makes its current value "
        r"(\d+) times", text, re.I)
    if match:
        start, rounds, change_a, change_b = map(int, match.groups())
        if change_a != change_b:
            raise AssertionError("paired tasks do not share the change number")
        additive = start + change_a * rounds
        multiplicative = start * change_b ** rounds
        model = f"A={start}+{change_a}*{rounds}; B={start}*{change_b}^{rounds}"
        answer = (f"A: additive, {additive} units; B: multiplicative, "
                  f"{multiplicative} units")
        return "additive_vs_multiplicative", answer, model

    match = re.search(
        r"right triangle with perpendicular sides (\d+) m and (\d+) m.*?small "
        r"triangle with sides \1 m and \2 m;.*?first side (\d+) m", text, re.I)
    if match:
        first, second, scaled_first = map(int, match.groups())
        hypotenuse = math.isqrt(first * first + second * second)
        scale = Fraction(scaled_first, first)
        scaled_second = scale * second
        model = (f"A:c^2={first}^2+{second}^2; "
                 f"B:{first}/{second}={scaled_first}/x")
        answer = (f"A: Pythagoras, {hypotenuse} m; B: similar triangles, "
                  f"{exact_text(scaled_second)} m")
        return "pythagoras_vs_similar", answer, model
    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer, model = solve(problem)
    if modifier == "with_model":
        answer = f"{model}; {answer}"
    return variant, answer, model


class TestMethodDiscriminationGenerator(unittest.TestCase):
    def test_marker_contract_and_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(269)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(20):
                    result = MethodDiscriminationGenerator(variant, modifier).generate()
                    self.assertEqual(result["steps"][-1],
                                     f"Z{DELIM}{result['final_answer']}")
                    parsed_variant, answer, model = expected(result["problem"], modifier)
                    self.assertEqual(parsed_variant, variant)
                    self.assertEqual(result["final_answer"], answer,
                                     result["problem"])
                    if modifier == "with_model":
                        self.assertEqual(result["steps"][0].split(DELIM)[1], model)
                    seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})

    def test_all_five_renderings_preserve_every_pair(self):
        facts = {
            "combination_vs_permutation": (
                "Task A selects 3 of 5 books for a trip, where changing their "
                "order does not create a new selection. Task B places 3 of the "
                "same 5 books in a row, where a different order does create a new result."),
            "independent_vs_dependent": (
                "A bag contains 4 red tokens among 8 tokens. Task A draws a token, "
                "returns it, mixes, and draws again. Task B draws twice from the "
                "same bag but does not return the first token."),
            "area_vs_perimeter": (
                "The same rectangle is 6 cm long and 4 cm wide. Task A asks for "
                "ribbon around its boundary. Task B asks for paper covering its entire face."),
            "mean_vs_median": (
                "Both tasks use the data list 2, 3, 4, 5, 11. Task A asks for the "
                "equal-share value if the total were spread across all five entries. "
                "Task B asks for the middle entry after ordering."),
            "linear_vs_exponential": (
                "Two accounts each start with $100.00. Account A adds $10.00 at "
                "the end of every year. Account B grows by 10% of its current "
                "balance each year. Compare them after 2 years."),
            "proportional_vs_not": (
                "Task A gives input-output records 1 to 3; 2 to 6; 4 to 12. "
                "Task B uses the same inputs but records 1 to 5; 2 to 8; 4 to 14."),
            "additive_vs_multiplicative": (
                "Two machines start at 5 units and run for 3 rounds. Machine A "
                "adds 2 units each round. Machine B makes its current value 2 "
                "times as large each round."),
            "pythagoras_vs_similar": (
                "Task A has a right triangle with perpendicular sides 3 m and 4 m "
                "and asks for the side across from the right angle. Task B has a "
                "small triangle with sides 3 m and 4 m; a same-shape larger triangle "
                "has the corresponding first side 6 m and asks for its corresponding second side."),
        }
        questions = {
            "combination_vs_permutation": "Name the structure of each task and give its number of outcomes.",
            "independent_vs_dependent": "Classify how the two draws relate in each task and find the chance of two red draws.",
            "area_vs_perimeter": "Name the quantity needed in each task and compute it.",
            "mean_vs_median": "Name the summary used by each task and give its value.",
            "linear_vs_exponential": "Name each growth pattern and compute both balances.",
            "proportional_vs_not": "Which record keeps one output-to-input ratio, and what does each record give at input 5?",
            "additive_vs_multiplicative": "Name each update pattern and compute both final values.",
            "pythagoras_vs_similar": "Name the relationship used in each task and compute both missing sides.",
        }
        self.assertEqual(len(FRAMES), 5)
        for variant in VARIANTS:
            for index, frame in enumerate(FRAMES):
                problem = frame.format(facts=facts[variant], question=questions[variant],
                                       place="the science room", name="Ada")
                with self.subTest(variant=variant, rendering=index):
                    self.assertEqual(solve(problem)[0], variant)

    def test_arithmetic_steps(self):
        random.seed(270)
        for _ in range(1000):
            result = MethodDiscriminationGenerator().generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(number(fields[1]) + number(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "M":
                    self.assertEqual(number(fields[1]) * number(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "D":
                    self.assertEqual(number(fields[1]) / number(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "E":
                    self.assertEqual(number(fields[1]) ** int(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "ROOT":
                    self.assertEqual(number(fields[2]) ** 2,
                                     number(fields[1]), raw)

    def test_modifier_shapes_labels_and_invalid_inputs(self):
        label_pairs = {
            "combination_vs_permutation": ("combination", "permutation"),
            "independent_vs_dependent": ("independent", "dependent"),
            "area_vs_perimeter": ("perimeter", "area"),
            "mean_vs_median": ("mean", "median"),
            "linear_vs_exponential": ("linear", "exponential"),
            "proportional_vs_not": ("proportional", "not proportional"),
            "additive_vs_multiplicative": ("additive", "multiplicative"),
            "pythagoras_vs_similar": ("Pythagoras", "similar triangles"),
        }
        random.seed(271)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = MethodDiscriminationGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                for label in label_pairs[variant]:
                    self.assertIn(label, result["final_answer"])
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            MethodDiscriminationGenerator("bogus")
        with self.assertRaises(ValueError):
            MethodDiscriminationGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(272)
        banned = ("1x", "-1x", "^1", "+ 0", "--", "the the", "e+")
        for _ in range(500):
            result = MethodDiscriminationGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            joined = " ".join((result["problem"], result["final_answer"],
                               *result["steps"]))
            for fragment in banned:
                self.assertNotIn(fragment, joined.lower())
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
