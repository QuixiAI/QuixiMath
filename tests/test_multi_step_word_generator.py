"""Problem-only template inversion for MultiStepWordGenerator."""
import random
import re
import string
import unittest
from fractions import Fraction

from generators.multi_step_word_generator import (
    APPLIED,
    MODIFIERS,
    PROMPTS,
    MultiStepWordGenerator,
)
from helpers import DELIM


FIELD_PATTERNS = {
    "name": r"[A-Za-z]+",
    "groups": r"\d+", "each": r"\d+", "remove": r"\d+",
    "extra": r"\d+", "r1": r"\d+", "r2": r"\d+", "r3": r"\d+",
    "b1": r"\d+", "b2": r"\d+", "b3": r"\d+",
    "price": r"\$\d+\.\d{2}", "paid": r"\$\d+\.\d{2}",
    "start": r"\d{1,2}:\d{2}", "end": r"\d{1,2}:\d{2}",
}


def compile_template(template):
    pieces = []
    seen = set()
    for literal, field, _, _ in string.Formatter().parse(template):
        pieces.append(re.escape(literal))
        if field is None:
            continue
        if field in seen:
            pieces.append(f"(?P={field})")
        else:
            pieces.append(f"(?P<{field}>{FIELD_PATTERNS[field]})")
            seen.add(field)
    return re.compile("".join(pieces) + r"\Z")


PARSERS = {
    variant: tuple(compile_template(template) for template in templates)
    for variant, templates in PROMPTS.items()
}


def strip_distractor(problem):
    return re.sub(r"^A nearby room has \d+ chairs\. ", "", problem)


def invert(problem):
    core = strip_distractor(problem)
    for variant, parsers in PARSERS.items():
        for index, parser in enumerate(parsers):
            match = parser.fullmatch(core)
            if match:
                return variant, index, match.groupdict()
    raise AssertionError(f"no template matched: {problem}")


def cash(text):
    return Fraction(text.removeprefix("$"))


def expected(problem, modifier):
    variant, _, fields = invert(problem)
    if variant in ("two_step_buy", "groups_then_remove"):
        value = int(fields["groups"]) * int(fields["each"]) - int(fields["remove"])
        unit = "pencils" if variant == "two_step_buy" else "books"
        answer = f"{value} {unit}"
        model = f"x = {fields['groups']} * {fields['each']} - {fields['remove']}"
    elif variant == "change_from_bill":
        value = cash(fields["paid"]) - int(fields["groups"]) * cash(fields["price"])
        answer = f"${value.numerator // value.denominator}.{(value * 100).numerator % 100:02d}"
        model = f"x = {cash(fields['paid'])} - {fields['groups']} * {cash(fields['price'])}"
    elif variant == "time_elapsed":
        sh, sm = map(int, fields["start"].split(":"))
        eh, em = map(int, fields["end"].split(":"))
        value = (eh * 60 + em) - (sh * 60 + sm)
        answer = f"{value} minutes"
        model = f"x = ({eh} * 60 + {em}) - ({sh} * 60 + {sm})"
    elif variant == "compare_totals":
        red = sum(int(fields[key]) for key in ("r1", "r2", "r3"))
        blue = sum(int(fields[key]) for key in ("b1", "b2", "b3"))
        value = red - blue
        answer = f"Red by {value} points"
        model = (f"Red = {fields['r1']} + {fields['r2']} + {fields['r3']}; "
                 f"Blue = {fields['b1']} + {fields['b2']} + {fields['b3']}")
    else:
        value = (int(fields["groups"]) * int(fields["each"])
                 + int(fields["extra"]) - int(fields["remove"]))
        answer = f"{value} cans"
        model = (f"x = {fields['groups']} * {fields['each']} + "
                 f"{fields['extra']} - {fields['remove']}")
    if modifier == "with_model":
        return variant, f"{model}; x = {answer}"
    return variant, answer


class TestMultiStepWordGenerator(unittest.TestCase):
    def test_applied_marker_and_contract(self):
        self.assertIs(APPLIED, True)
        result = MultiStepWordGenerator().generate()
        self.assertEqual(set(result),
                         {"problem_id", "operation", "problem", "steps",
                          "final_answer"})
        self.assertEqual(result["steps"][-1],
                         f"Z{DELIM}{result['final_answer']}")

    def test_problem_only_oracle(self):
        random.seed(901)
        seen = set()
        for _ in range(1200):
            result = MultiStepWordGenerator().generate()
            # Modifier names can contain underscores, so resolve by suffix.
            modifier = next(m for m in MODIFIERS
                            if result["operation"].endswith("_" + m))
            variant = result["operation"][:-len(modifier)-1].removeprefix(
                "applied_multi_step_word_"
            )
            parsed_variant, answer = expected(result["problem"], modifier)
            self.assertEqual(parsed_variant, variant)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in PROMPTS for m in MODIFIERS})

    def test_all_five_renderings_are_invertible(self):
        sample = dict(name="Ada", groups=4, each=6, remove=7, extra=5,
                      price="$2.50", paid="$20.00", start="9:15", end="10:40",
                      r1=20, r2=18, r3=17, b1=15, b2=14, b3=13)
        for variant, templates in PROMPTS.items():
            self.assertEqual(len(templates), 5)
            for index, template in enumerate(templates):
                problem = template.format(**sample)
                with self.subTest(variant=variant, index=index):
                    parsed_variant, parsed_index, _ = invert(problem)
                    self.assertEqual((parsed_variant, parsed_index),
                                     (variant, index))

    def test_arithmetic_steps(self):
        for _ in range(600):
            result = MultiStepWordGenerator().generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw)

    def test_modifiers_have_required_shape(self):
        for variant in MultiStepWordGenerator.VARIANTS:
            for modifier in MODIFIERS:
                result = MultiStepWordGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["final_answer"],
                                 expected(result["problem"], modifier)[1])
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                    self.assertEqual(codes.count("SELECT_RELEVANT"), 1)
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")

    def test_invalid_variant_and_modifier(self):
        with self.assertRaises(ValueError):
            MultiStepWordGenerator("bogus")
        with self.assertRaises(ValueError):
            MultiStepWordGenerator(modifier="bogus")

    def test_pipe_and_render_safety(self):
        for _ in range(500):
            result = MultiStepWordGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            rendered = " ".join([result["problem"], *result["steps"]])
            self.assertNotRegex(rendered, r"\b1x\b|\b-1x\b|\^1\b|--")
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
