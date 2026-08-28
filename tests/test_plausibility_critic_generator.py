"""Problem-text-only oracles for :class:`PlausibilityCriticGenerator`."""
import random
import re
import unittest
from fractions import Fraction

from generators.plausibility_critic_generator import (
    APPLIED,
    CASE_FAMILIES,
    FRAMES,
    MODIFIERS,
    VARIANTS,
    PlausibilityCriticGenerator,
)
from helpers import DELIM


def number(token):
    return Fraction(token.replace("$", "").replace("%", "").rstrip("."))


def exact_text(value):
    """Independent exact renderer: terminating decimal, else a fraction."""
    value = Fraction(value)
    denominator = value.denominator
    while denominator % 2 == 0:
        denominator //= 2
    while denominator % 5 == 0:
        denominator //= 5
    if denominator != 1:
        return (str(value.numerator) if value.denominator == 1
                else f"{value.numerator}/{value.denominator}")
    places = 0
    scaled = value
    while scaled.denominator != 1:
        scaled *= 10
        places += 1
    if places == 0:
        return str(scaled.numerator)
    sign = "-" if scaled < 0 else ""
    digits = str(abs(scaled.numerator)).rjust(places + 1, "0")
    rendered = (digits[:-places] + "." + digits[-places:]).rstrip("0").rstrip(".")
    return sign + rendered


def money_text(value):
    cents = Fraction(value) * 100
    if cents.denominator != 1:
        raise AssertionError(f"not exact cents: {value}")
    return f"${cents.numerator // 100}.{cents.numerator % 100:02d}"


def quantity(value, name):
    text = exact_text(value)
    if name in ("km/h", "m²"):
        return f"{text} {name}"
    return f"{text} {name if Fraction(value) == 1 else name + 's'}"


def clean(problem):
    return re.sub(r"^A nearby notice lists \d+ storage lockers\. ", "", problem)


def solve(problem):
    """Recompute the correct quantity and verdict from the story alone."""
    text = clean(problem)

    match = re.search(
        r"van covers ([0-9./]+) km in ([0-9./]+) hours?.*?"
        r"speed over the trip is ([0-9./]+) km/h", text, re.I)
    if match:
        distance, elapsed, claim = map(number, match.groups())
        correct_value = distance / elapsed
        correct = quantity(correct_value, "km/h")
        claim_correct = claim == correct_value
        model = (f"v = {exact_text(distance)}/{exact_text(elapsed)} = "
                 f"{correct}")
        return "magnitude", claim_correct, correct, model, correct_value

    match = re.search(
        r"floor is (\d+) m long and (\d+) m wide.*?covered is "
        r"(\d+) (m²|m)\.", text, re.I)
    if match:
        length, width, claim_value = map(int, match.groups()[:3])
        claim_unit = match.group(4)
        correct_value = Fraction(length * width)
        correct = quantity(correct_value, "m²")
        claim_correct = claim_value == correct_value and claim_unit == "m²"
        model = f"q = {length}*{width} = {correct}"
        return "units", claim_correct, correct, model, correct_value

    match = re.search(
        r"item is marked (\$[0-9.]+) and then reduced by (\d+)%.*?"
        r"new price is (\$[0-9.]+)", text, re.I)
    if match:
        marked, percent, claim = match.groups()
        price = number(marked)
        rate = Fraction(int(percent), 100)
        correct_value = price * (1 - rate)
        correct = money_text(correct_value)
        claim_correct = number(claim) == correct_value
        model = (f"s = {exact_text(price)}*(1 - {percent}/100) = "
                 f"{correct}")
        return "direction", claim_correct, correct, model, correct_value

    match = re.search(
        r"box holds (\d+) blue beads among (\d+) beads in all.*?"
        r"chance of blue is ([0-9./]+)", text, re.I)
    if match:
        blue, total = map(int, match.groups()[:2])
        claim = number(match.group(3))
        correct_value = Fraction(blue, total)
        correct = exact_text(correct_value)
        claim_correct = claim == correct_value
        model = f"p = {blue}/{total} = {correct}"
        return "bounds", claim_correct, correct, model, correct_value

    match = re.search(
        r"crew of (\d+) identical workers.*?in (\d+) hours\. A crew of "
        r"(\d+) workers.*?take ([0-9./]+) hours?\.", text, re.I)
    if match:
        workers, old_time, new_workers = map(int, match.groups()[:3])
        claim = number(match.group(4))
        correct_value = Fraction(workers * old_time, new_workers)
        correct = quantity(correct_value, "hour")
        claim_correct = claim == correct_value
        model = (f"t = {workers}*{old_time}/{new_workers} = "
                 f"{correct}")
        return "monotonicity", claim_correct, correct, model, correct_value

    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    family, claim_correct, correct, model, value = solve(problem)
    verdict = "plausible" if claim_correct else "implausible"
    answer = f"{verdict}; correct {correct}"
    if modifier == "with_model":
        answer = f"{model}; {answer}"
    return family, claim_correct, answer, model, value


class TestPlausibilityCriticGenerator(unittest.TestCase):
    def test_marker_contract_and_500_sample_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(273)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(24):
                    result = PlausibilityCriticGenerator(
                        variant, modifier).generate()
                    self.assertEqual(result["steps"][-1],
                                     f"Z{DELIM}{result['final_answer']}")
                    family, correct_claim, answer, model, _ = expected(
                        result["problem"], modifier)
                    if variant != "control_plausible":
                        self.assertEqual(family, variant)
                    else:
                        self.assertTrue(correct_claim)
                    self.assertEqual(result["final_answer"], answer,
                                     result["problem"])
                    if modifier == "with_model":
                        self.assertEqual(result["steps"][0].split(DELIM)[1],
                                         model)
                    seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})

    def test_all_five_renderings_invert_every_case_family(self):
        examples = {
            "magnitude": (
                "A van covers 120 km in 1.5 hours. Kai says its speed over the "
                "trip is 180 km/h."),
            "units": (
                "A rectangular floor is 4 m long and 6 m wide. Kai says the "
                "amount of floor covered is 24 m."),
            "direction": (
                "An item is marked $80.00 and then reduced by 25% of that marked "
                "price. Kai says the new price is $100.00."),
            "bounds": (
                "A box holds 7 blue beads among 20 beads in all. One bead will "
                "be chosen without looking. Kai says the chance of blue is 27/20."),
            "monotonicity": (
                "A crew of 4 identical workers completes a fixed job in 6 hours. "
                "A crew of 8 workers at the same steady pace is assigned the same "
                "job. Kai says it will take 12 hours."),
        }
        question = "Is that claim consistent with the recorded quantities?"
        self.assertEqual(len(FRAMES), 5)
        for family, facts in examples.items():
            for index, frame in enumerate(FRAMES):
                problem = frame.format(facts=facts, question=question,
                                       place="the field station", name="Ada")
                with self.subTest(family=family, rendering=index):
                    self.assertEqual(solve(problem)[0], family)

    def test_each_substantive_variant_reaches_both_verdicts(self):
        random.seed(274)
        for variant in CASE_FAMILIES:
            verdicts = set()
            for _ in range(240):
                result = PlausibilityCriticGenerator(variant, "plain").generate()
                verdicts.add(result["final_answer"].split(";", 1)[0])
            self.assertEqual(verdicts, {"plausible", "implausible"}, variant)

        for _ in range(240):
            result = PlausibilityCriticGenerator(
                "control_plausible", "plain").generate()
            self.assertTrue(result["final_answer"].startswith("plausible;"))

    def test_arithmetic_and_bound_steps(self):
        random.seed(275)
        for _ in range(1200):
            result = PlausibilityCriticGenerator().generate()
            family, claim_correct, _, _, _ = expected(
                result["problem"],
                next(m for m in MODIFIERS if result["operation"].endswith(m)))
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "M":
                    self.assertEqual(number(fields[1]) * number(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "D":
                    self.assertEqual(number(fields[1]) / number(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "S":
                    self.assertEqual(number(fields[1]) - number(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "PERCENT_TO_DEC":
                    self.assertEqual(number(fields[1]) / 100,
                                     number(fields[2]), raw)
                elif fields[0] == "BOUND" and family == "bounds":
                    claim = number(fields[2])
                    self.assertEqual(claim <= 1, claim_correct, raw)

    def test_modifier_shapes_operation_and_invalid_inputs(self):
        random.seed(276)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = PlausibilityCriticGenerator(
                    variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(
                    result["operation"],
                    f"applied_plausibility_critic_{variant}_{modifier}")
                self.assertIn("correct ", result["final_answer"])
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            PlausibilityCriticGenerator("bogus")
        with self.assertRaises(ValueError):
            PlausibilityCriticGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(277)
        banned = ("1x", "-1x", "^1", "+ 0", "--", "the the", "e+")
        for _ in range(600):
            result = PlausibilityCriticGenerator().generate()
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
