"""Problem-text-only oracles for :class:`MixtureGenerator`."""
import random
import re
import unittest
from fractions import Fraction

from generators.mixture_generator import (
    APPLIED,
    FRAMES,
    MODIFIERS,
    VARIANTS,
    MixtureGenerator,
)
from helpers import DELIM


def number(token):
    """Parse displayed integers, decimals, or reduced fractions exactly."""
    return Fraction(token.replace("$", ""))


def exact_text(value):
    """Independent exact renderer using long division, not project helpers."""
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    scaled = value
    places = 0
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
        raise AssertionError(f"not an exact cent amount: {value}")
    return f"${cents.numerator // 100}.{cents.numerator % 100:02d}"


def clean(problem):
    return re.sub(r"^A shelf nearby holds \d+ empty bottles\. ", "", problem)


def solve(problem):
    """Invert the story and solve from its displayed quantities only."""
    text = clean(problem)

    match = re.search(
        r"(\d+) (L|kg) of a (\d+)% (salt|copper) (solution|alloy) is "
        r"combined with (\d+) \2 of a (\d+)% \4 \5", text, re.I)
    if match:
        first, unit_name, low, substance, noun, second, high = match.groups()
        first, low, second, high = map(int, (first, low, second, high))
        # Count one percent as one unit per hundred units of mixture. This
        # integer-weight route is independent of the generator's decimals.
        percent = Fraction(first * low + second * high, first + second)
        variant = "alloy" if noun.lower() == "alloy" else "two_solutions"
        model = (f"x = ({first}*{low}/100 + {second}*{high}/100) / "
                 f"({first}+{second}) * 100")
        return variant, f"{exact_text(percent)}%", model

    match = re.search(
        r"tank holds (\d+) L of a (\d+)% acid solution\. Pure acid is "
        r"added until the concentration is (\d+)%", text, re.I)
    if match:
        volume, start, target = map(int, match.groups())
        added = Fraction(volume * (target - start), 100 - target)
        model = f"({start}/100*{volume} + x)/({volume}+x) = {target}/100"
        return "add_pure", f"{exact_text(added)} L", model

    match = re.search(
        r"container has (\d+) L of a (\d+)% cleaner\. Water is added until "
        r"the cleaner is (\d+)%", text, re.I)
    if match:
        volume, start, target = map(int, match.groups())
        added = Fraction(volume * (start - target), target)
        model = f"({start}/100*{volume})/({volume}+x) = {target}/100"
        return "add_water", f"{exact_text(added)} L", model

    match = re.search(
        r"coffee blend uses (\d+) kg costing (\$\d+\.\d{2}) per kg and "
        r"(\d+) kg costing (\$\d+\.\d{2}) per kg", text, re.I)
    if match:
        first, price1, second, price2 = match.groups()
        first, second = int(first), int(second)
        price1, price2 = number(price1), number(price2)
        price = Fraction(first * price1 + second * price2, first + second)
        model = (f"x = ({first}*{price1} + {second}*{price2})/"
                 f"({first}+{second})")
        return "price_blend", f"{money_text(price)} per kg", model

    match = re.search(
        r"vat contains (\d+) L of a (\d+)% dye solution\. A (\d+)% solution "
        r"is added to make a (\d+)% mixture", text, re.I)
    if match:
        volume, low, high, target = map(int, match.groups())
        added = Fraction(volume * (target - low), high - target)
        model = (f"({low}/100*{volume} + {high}/100*x)/({volume}+x) = "
                 f"{target}/100")
        return ("target_concentration_unknown_amount",
                f"{exact_text(added)} L", model)
    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer, model = solve(problem)
    if modifier == "with_model":
        answer = f"{model}; x = {answer}"
    return variant, answer


class TestMixtureGenerator(unittest.TestCase):
    def test_marker_contract_and_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(229)
        seen = set()
        for _ in range(1200):
            result = MixtureGenerator().generate()
            self.assertEqual(result["steps"][-1],
                             f"Z{DELIM}{result['final_answer']}")
            modifier = next(m for m in MODIFIERS
                            if result["operation"].endswith("_" + m))
            variant = result["operation"][:-len(modifier)-1].removeprefix(
                "applied_mixture_")
            parsed_variant, answer = expected(result["problem"], modifier)
            self.assertEqual(parsed_variant, variant)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})

    def test_all_five_renderings_preserve_every_template(self):
        cases = (
            ("3 L of a 20% salt solution is combined with 7 L of a 40% salt "
             "solution.", "What percent salt is in the combined solution?",
             "two_solutions"),
            ("A tank holds 10 L of a 20% acid solution. Pure acid is added "
             "until the concentration is 60%.",
             "How many litres of pure acid are added?", "add_pure"),
            ("A container has 10 L of a 60% cleaner. Water is added until the "
             "cleaner is 20%.", "How many litres of water are added?",
             "add_water"),
            ("A coffee blend uses 3 kg costing $2.00 per kg and 7 kg costing "
             "$4.00 per kg.", "What does the combined blend cost per kg?",
             "price_blend"),
            ("3 kg of a 20% copper alloy is combined with 7 kg of a 40% copper "
             "alloy.", "What percent copper is in the combined alloy?", "alloy"),
            ("A vat contains 10 L of a 20% dye solution. A 60% solution is "
             "added to make a 40% mixture.",
             "How many litres of the 60% solution are added?",
             "target_concentration_unknown_amount"),
        )
        self.assertEqual(len(FRAMES), 5)
        for facts, question, variant in cases:
            for index, frame in enumerate(FRAMES):
                problem = frame.format(
                    facts=facts, facts_lc=facts[:1].lower() + facts[1:],
                    question=question, place="the school lab", record="A17")
                with self.subTest(variant=variant, rendering=index):
                    self.assertEqual(solve(problem)[0], variant)

    def test_arithmetic_steps(self):
        random.seed(230)
        for _ in range(700):
            result = MixtureGenerator().generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(number(fields[1]) + number(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "S":
                    self.assertEqual(number(fields[1]) - number(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "M":
                    self.assertEqual(number(fields[1]) * number(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "D":
                    self.assertEqual(number(fields[1]) / number(fields[2]),
                                     number(fields[3]), raw)

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(231)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = MixtureGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["final_answer"],
                                 expected(result["problem"], modifier)[1])
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            MixtureGenerator("bogus")
        with self.assertRaises(ValueError):
            MixtureGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(232)
        banned = ("1x", "-1x", "^1", "+ 0", "--")
        for _ in range(500):
            result = MixtureGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            joined = " ".join((result["problem"], result["final_answer"],
                               *result["steps"]))
            self.assertNotIn("the the", joined.lower())
            for fragment in banned:
                self.assertNotIn(fragment, joined)
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
