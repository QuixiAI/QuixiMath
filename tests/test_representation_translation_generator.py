"""Problem-text-only oracles for RepresentationTranslationGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.representation_translation_generator import (
    APPLIED, FRAMES, MODIFIERS, VARIANTS, RepresentationTranslationGenerator,
)
from helpers import DELIM


def number(token):
    return Fraction(token.rstrip("."))


def clean(problem):
    return re.sub(r"^An unrelated file lists \d+ blank labels\. ", "", problem)


def solve(problem):
    text = clean(problem)

    match = re.search(
        r"tank begins with (\d+) liters and receives (\d+) liters each minute",
        text, re.I)
    if match:
        initial, rate = map(int, match.groups())
        equation = f"y = {rate}x + {initial}"
        return "words_to_equation", equation, equation

    match = re.search(
        r"relationship y = (\d+)x \+ (\d+) uses x for hours worked and y for "
        r"total dollars earned", text, re.I)
    if match:
        rate, initial = map(int, match.groups())
        equation = f"y = {rate}x + {initial}"
        return "equation_to_words", f"starts with ${initial}; earns ${rate} per hour", equation

    table = re.search(
        r"table lists \(0, (\d+)\), \(1, (\d+)\), \(2, (\d+)\), \(3, (\d+)\)",
        text, re.I)
    if table:
        values = list(map(int, table.groups()))
        differences = [values[i] - values[i - 1] for i in range(1, 4)]
        if len(set(differences)) == 1:
            difference = differences[0]
            equation = f"y = {difference}x + {values[0]}"
            answer = f"linear; common difference {difference}; {equation}"
            return "table_to_equation_linear", answer, equation
        ratios = [Fraction(values[i], values[i - 1]) for i in range(1, 4)]
        if len(set(ratios)) != 1:
            raise AssertionError(f"neither constant differences nor ratios: {values}")
        ratio = ratios[0]
        equation = f"y = {values[0]}·{ratio}^x"
        answer = f"exponential; common ratio {ratio}; {equation}"
        return "table_to_equation_exponential", answer, equation

    equation_table = re.search(r"The relationship is y = (\d+)x \+ (\d+)", text, re.I)
    x_values = re.search(r"y-values for x = ([\d, ]+)", text, re.I)
    if equation_table and x_values:
        rate, initial = map(int, equation_table.groups())
        xs = [int(token.strip()) for token in x_values.group(1).split(",")]
        equation = f"y = {rate}x + {initial}"
        answer = "; ".join(f"x={x} → y={rate * x + initial}" for x in xs)
        return "equation_to_table", answer, equation

    match = re.search(
        r"line crosses the vertical axis at (\d+)\. Moving 1 unit right moves "
        r"(\d+) units up", text, re.I)
    if match:
        intercept, slope = map(int, match.groups())
        equation = f"y = {slope}x + {intercept}"
        return "graph_features_to_equation", equation, equation

    match = re.search(
        r"plumber's total charge C dollars for h hours is C = (\d+) \+ (\d+)h",
        text, re.I)
    if match:
        fixed, rate = map(int, match.groups())
        equation = f"C = {fixed} + {rate}h"
        return "intercept_meaning", f"{fixed}; the fixed call-out fee", equation

    story = re.search(
        r"service charges \$(\d+) before work begins and \$(\d+) for each hour",
        text, re.I)
    options = dict(re.findall(r"([ABC]): (y = \d+x [−+] \d+)", text))
    if story and len(options) == 3:
        initial, rate = map(int, story.groups())
        equation = f"y = {rate}x + {initial}"
        labels = [label for label, option in options.items() if option == equation]
        if len(labels) != 1:
            raise AssertionError(f"matching option not unique: {options}")
        return "which_representation_matches", f"option {labels[0]}; {equation}", equation

    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer, model = solve(problem)
    return variant, (f"{model}; {answer}" if modifier == "with_model" else answer), model


class TestRepresentationTranslationGenerator(unittest.TestCase):
    def test_marker_contract_and_500_sample_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(380)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(16):
                    result = RepresentationTranslationGenerator(variant, modifier).generate()
                    self.assertEqual(result["steps"][-1], f"Z{DELIM}{result['final_answer']}")
                    parsed, answer, model = expected(result["problem"], modifier)
                    self.assertEqual(parsed, variant)
                    self.assertEqual(result["final_answer"], answer, result["problem"])
                    if modifier == "with_model":
                        self.assertEqual(result["steps"][0].split(DELIM)[1], model)
                    seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})

    def test_all_five_renderings_invert_every_variant(self):
        examples = {
            "words_to_equation": ("A tank begins with 40 liters and receives 5 liters "
                                  "each minute. Let x be elapsed minutes and y be liters in the tank.",
                                  "Write the relationship between x and y."),
            "equation_to_words": ("The relationship y = 12x + 30 uses x for hours "
                                  "worked and y for total dollars earned.",
                                  "Describe what the two numbers mean."),
            "table_to_equation_linear": ("A table lists (0, 40), (1, 65), (2, 90), "
                                         "(3, 115).", "Is the relationship linear or "
                                         "exponential, and what relationship gives y from x?"),
            "table_to_equation_exponential": ("A table lists (0, 3), (1, 6), (2, 12), "
                                              "(3, 24).", "Is the relationship linear or "
                                              "exponential, and what relationship gives y from x?"),
            "equation_to_table": ("The relationship is y = 4x + 7.",
                                  "Give the y-values for x = 0, 1, 2, 3."),
            "graph_features_to_equation": ("A line crosses the vertical axis at 6. "
                                           "Moving 1 unit right moves 3 units up.",
                                           "Write y in terms of x for this line."),
            "intercept_meaning": ("A plumber's total charge C dollars for h hours is "
                                  "C = 40 + 25h.", "What does 40 mean in this situation?"),
            "which_representation_matches": ("A service charges $30 before work begins "
                                             "and $12 for each hour. Choices — A: y = 30x + 12; "
                                             "B: y = 12x + 30; C: y = 12x − 30.",
                                             "Which choice matches the service cost?"),
        }
        for variant, (facts, question) in examples.items():
            for frame in FRAMES:
                problem = frame.format(place="the classroom", name="Ari",
                                       facts=facts, question=question)
                self.assertEqual(solve(problem)[0], variant, problem)

    def test_arithmetic_inside_emitted_steps(self):
        random.seed(381)
        for _ in range(900):
            result = RepresentationTranslationGenerator().generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(number(fields[1]) + number(fields[2]), number(fields[3]), raw)
                elif fields[0] == "S":
                    self.assertEqual(number(fields[1]) - number(fields[2]), number(fields[3]), raw)
                elif fields[0] == "M":
                    self.assertEqual(number(fields[1]) * number(fields[2]), number(fields[3]), raw)
                elif fields[0] == "D":
                    self.assertEqual(number(fields[1]) / number(fields[2]), number(fields[3]), raw)

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(382)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = RepresentationTranslationGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["operation"], f"applied_representation_translation_{variant}_{modifier}")
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            RepresentationTranslationGenerator("bogus")
        with self.assertRaises(ValueError):
            RepresentationTranslationGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(383)
        banned = ("^1", "+ 0", "--", "the the", "e+")
        for _ in range(700):
            result = RepresentationTranslationGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            joined = " ".join((result["problem"], result["final_answer"], *result["steps"]))
            for fragment in banned:
                self.assertNotIn(fragment, joined.lower())
            self.assertIsNone(re.search(r"(?<!\d)-?1x\b", joined.lower()))
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
