"""Problem-text-only oracles for :class:`PercentChainGenerator`."""
import random
import re
import unittest
from fractions import Fraction

from generators.percent_chain_generator import (
    APPLIED,
    FRAMES,
    MODIFIERS,
    VARIANTS,
    PercentChainGenerator,
)
from helpers import DELIM


def number(token):
    return Fraction(token.replace("$", "").replace("%", ""))


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


def percent_text(value):
    return f"{exact_text(value)}%"


def clean(problem):
    return re.sub(r"^A display nearby holds \d+ postcards\. ", "", problem)


def solve(problem):
    text = clean(problem)

    match = re.search(
        r"jacket starts at (\$\d+\.\d{2})\. Its price rises by (\d+)%, then "
        r"the marked price is reduced by (\d+)%", text, re.I)
    if match:
        base, increase, decrease = number(match.group(1)), int(match.group(2)), int(match.group(3))
        final = base * Fraction(100 + increase, 100) * Fraction(100 - decrease, 100)
        net = (final - base) / base * 100
        model = f"x = {exact_text(base)}*(1+{increase}/100)*(1-{decrease}/100)"
        return "markup_then_discount", f"{money_text(final)}; net change {percent_text(net)}", model, net

    match = re.search(
        r"meal costs (\$\d+\.\d{2}) before (\d+)% tax\. A (\d+)% tip is "
        r"then calculated from the taxed subtotal", text, re.I)
    if match:
        base, tax, tip = number(match.group(1)), int(match.group(2)), int(match.group(3))
        taxed = base * Fraction(100 + tax, 100)
        gratuity = taxed * Fraction(tip, 100)
        final = taxed + gratuity
        model = f"x = {exact_text(base)}*(1+{tax}/100)*(1+{tip}/100)"
        answer = (f"subtotal {money_text(taxed)}; tip {money_text(gratuity)}; "
                  f"total {money_text(final)}")
        return "tax_then_tip", answer, model, None

    match = re.search(
        r"monthly cost is (\$\d+\.\d{2})\. It increases by (\d+)% .*? "
        r"decreases by (\d+)%", text, re.I)
    if match:
        base, increase, decrease = number(match.group(1)), int(match.group(2)), int(match.group(3))
        final = base * Fraction(100 + increase, 100) * Fraction(100 - decrease, 100)
        net = (final - base) / base * 100
        model = f"x = {exact_text(base)}*(1+{increase}/100)*(1-{decrease}/100)"
        return "successive_changes_net", f"{money_text(final)}; net change {percent_text(net)}", model, net

    match = re.search(
        r"sale price is (\$\d+\.\d{2}) after a (\d+)% discount", text, re.I)
    if match:
        shown, rate = number(match.group(1)), int(match.group(2))
        base = shown / Fraction(100 - rate, 100)
        model = f"x*(1-{rate}/100) = {exact_text(shown)}"
        return "reverse_from_sale_price", money_text(base), model, None

    match = re.search(
        r"purchase totals (\$\d+\.\d{2}) after (\d+)% tax", text, re.I)
    if match:
        shown, rate = number(match.group(1)), int(match.group(2))
        base = shown / Fraction(100 + rate, 100)
        model = f"x*(1+{rate}/100) = {exact_text(shown)}"
        return "reverse_from_total_with_tax", money_text(base), model, None

    match = re.search(
        r"survey, (\d+)% of all respondents choose option A\. Of those "
        r"respondents, (\d+)% also choose option B", text, re.I)
    if match:
        first, second = map(int, match.groups())
        result = Fraction(first * second, 100)
        model = f"x = {first}/100*{second}/100*100"
        return "percent_of_percent", percent_text(result), model, None
    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer, model, net = solve(problem)
    if modifier == "with_model":
        answer = f"{model}; x = {answer}"
    return variant, answer, net


class TestPercentChainGenerator(unittest.TestCase):
    def test_marker_contract_and_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(241)
        seen = set()
        net_signs = {"markup_then_discount": set(),
                     "successive_changes_net": set()}
        for _ in range(1200):
            result = PercentChainGenerator().generate()
            self.assertEqual(result["steps"][-1],
                             f"Z{DELIM}{result['final_answer']}")
            modifier = next(m for m in MODIFIERS
                            if result["operation"].endswith("_" + m))
            variant = result["operation"][:-len(modifier)-1].removeprefix(
                "applied_percent_chain_")
            parsed_variant, answer, net = expected(result["problem"], modifier)
            self.assertEqual(parsed_variant, variant)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            seen.add((variant, modifier))
            if net is not None:
                net_signs[variant].add((net > 0) - (net < 0))
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})
        for signs in net_signs.values():
            self.assertTrue({-1, 1}.issubset(signs))

    def test_all_five_renderings_preserve_every_template(self):
        cases = (
            ("A jacket starts at $80.00. Its price rises by 25%, then the "
             "marked price is reduced by 20%.",
             "What is the final price and the net percent change from the start?",
             "markup_then_discount"),
            ("A meal costs $50.00 before 10% tax. A 20% tip is then calculated "
             "from the taxed subtotal.",
             "What are the taxed subtotal, the tip, and the final total?",
             "tax_then_tip"),
            ("A monthly cost is $100.00. It increases by 20% one month and "
             "decreases by 10% the next month.",
             "What is the new cost and the net percent change from the original?",
             "successive_changes_net"),
            ("A sale price is $60.00 after a 25% discount from the original price.",
             "What was the original price?", "reverse_from_sale_price"),
            ("A purchase totals $110.00 after 10% tax is added to its pre-tax price.",
             "What was the pre-tax price?", "reverse_from_total_with_tax"),
            ("In a survey, 40% of all respondents choose option A. Of those "
             "respondents, 25% also choose option B.",
             "What percent of all respondents choose both A and B?",
             "percent_of_percent"),
        )
        self.assertEqual(len(FRAMES), 5)
        for facts, question, variant in cases:
            for index, frame in enumerate(FRAMES):
                problem = frame.format(
                    facts=facts, facts_lc=facts[:1].lower() + facts[1:],
                    question=question, place="the corner shop", record="A17")
                with self.subTest(variant=variant, rendering=index):
                    self.assertEqual(solve(problem)[0], variant)

    def test_arithmetic_steps(self):
        random.seed(242)
        for _ in range(700):
            result = PercentChainGenerator().generate()
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
        random.seed(243)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = PercentChainGenerator(variant, modifier).generate()
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
            PercentChainGenerator("bogus")
        with self.assertRaises(ValueError):
            PercentChainGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(244)
        banned = ("1x", "-1x", "^1", "+ 0", "--", "the the", "e+")
        for _ in range(500):
            result = PercentChainGenerator().generate()
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
