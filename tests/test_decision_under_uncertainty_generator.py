"""Problem-text-only brute-force oracles for DecisionUnderUncertaintyGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.decision_under_uncertainty_generator import (
    APPLIED, FRAMES, MODIFIERS, VARIANTS, DecisionUnderUncertaintyGenerator,
)
from helpers import DELIM

MODELS = {
    "expected_cost_two_plans": "expected(B) = base + probability × fee",
    "insurance_premium_vs_expected_loss": "expected loss = probability × loss",
    "fair_price": "fair price = p × payout1 + (1 − p) × payout2",
    "minimax_vs_expected": "worst case = smallest possible payout; expected = probability-weighted average",
    "risk_of_ruin_simple": "P(ruin) = 1 − (1 − p)^rounds",
    "wait_or_buy": "expected(wait) = p × new price + (1 − p) × current price",
}


def dec(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    scaled, places = value, 0
    while scaled.denominator != 1 and places < 12:
        scaled *= 10
        places += 1
    if scaled.denominator != 1:
        raise AssertionError(f"does not terminate: {value}")
    digits = str(abs(scaled.numerator)).rjust(places + 1, "0")
    text = (digits[:-places] + "." + digits[-places:]).rstrip("0").rstrip(".")
    return ("-" if value < 0 else "") + text


def money(value):
    cents = Fraction(value) * 100
    if cents.denominator != 1:
        raise AssertionError(f"not exact cents: {value}")
    cents = int(cents)
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}${cents // 100}.{cents % 100:02d}"


def frac_percent(fr):
    pct_value = Fraction(fr) * 100
    whole, remainder = divmod(pct_value.numerator, pct_value.denominator)
    remainder = Fraction(remainder, pct_value.denominator)
    if remainder == 0:
        return f"{whole}%"
    try:
        return dec(pct_value) + "%"
    except AssertionError:
        return f"{whole} {remainder.numerator}/{remainder.denominator}%"


def clean(problem):
    return re.sub(r"^An unrelated memo lists \d+ archived files\. ", "", problem)


def solve(problem):
    text = clean(problem)

    match = re.search(
        r"Plan A costs \$(\d+) flat\. Plan B costs \$(\d+) plus a \$(\d+) "
        r"repair fee that is needed with probability (\d+(?:\.\d+)?)", text)
    if match:
        flat, base, fee = int(match.group(1)), int(match.group(2)), int(match.group(3))
        prob = Fraction(match.group(4))
        cost_b = base + fee * prob
        winner, w, l = ("A", flat, cost_b) if flat < cost_b else ("B", cost_b, flat)
        return "expected_cost_two_plans", f"plan {winner}; ${dec(w)} vs ${dec(l)}"

    match = re.search(
        r"An insurance premium is \$(\d+)\. There is a (\d+)% chance of a "
        r"\$(\d+) loss", text)
    if match:
        premium, pct, loss = map(int, match.groups())
        expected_loss = pct * loss // 100
        diff = premium - expected_loss
        verb = "exceeds it by" if diff > 0 else "is below it by"
        return ("insurance_premium_vs_expected_loss",
                f"expected loss ${expected_loss}; premium {verb} ${abs(diff)}")

    match = re.search(
        r"A game pays \$(\d+) with probability (\d+(?:\.\d+)?) and \$(\d+) otherwise", text)
    if match:
        x, prob_str, y = match.group(1), match.group(2), match.group(3)
        x, y, prob = int(x), int(y), Fraction(prob_str)
        fair = prob * x + (1 - prob) * y
        return "fair_price", money(fair)

    match = re.search(
        r"Option A guarantees \$(\d+)\. Option B pays \$(\d+) with "
        r"probability (\d+(?:\.\d+)?) and \$0 otherwise", text)
    if match:
        guaranteed, high = int(match.group(1)), int(match.group(2))
        prob = Fraction(match.group(3))
        expected_b = high * prob
        ev_winner = "A" if guaranteed > expected_b else "B"
        hi, lo = (guaranteed, expected_b) if guaranteed > expected_b else (expected_b, guaranteed)
        return ("minimax_vs_expected",
                f"worst-case: A; expected value: {ev_winner} (${dec(hi)} vs ${dec(lo)})")

    match = re.search(
        r"On each of (\d+) independent rounds, there is a (\d+(?:\.\d+)?)% chance of ruin", text)
    if match:
        n = int(match.group(1))
        p = Fraction(match.group(2)) / 100
        survive = (1 - p) ** n
        ruin = 1 - survive
        return "risk_of_ruin_simple", frac_percent(ruin)

    match = re.search(
        r"A price is \$(\d+) now\. There is a (\d+(?:\.\d+)?) probability it "
        r"changes to \$(\d+) next week", text)
    if match:
        price_now, new_price = int(match.group(1)), int(match.group(3))
        prob = Fraction(match.group(2))
        expected_wait = prob * new_price + (1 - prob) * price_now
        winner = "buy now" if price_now < expected_wait else "wait"
        w, l = (price_now, expected_wait) if price_now < expected_wait else (expected_wait, price_now)
        return "wait_or_buy", f"{winner}; ${dec(w)} vs ${dec(l)}"

    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer = solve(problem)
    model = MODELS[variant]
    return variant, (f"{model}; {answer}" if modifier == "with_model" else answer), model


class TestDecisionUnderUncertaintyGenerator(unittest.TestCase):
    def test_marker_contract_and_full_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(400)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(24):
                    result = DecisionUnderUncertaintyGenerator(variant, modifier).generate()
                    self.assertEqual(result["steps"][-1], f"Z{DELIM}{result['final_answer']}")
                    parsed, answer, model = expected(result["problem"], modifier)
                    self.assertEqual(parsed, variant, result["problem"])
                    self.assertEqual(result["final_answer"], answer, result["problem"])
                    if modifier == "with_model":
                        self.assertEqual(result["steps"][0].split(DELIM)[1], model)
                    seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})

    def test_plans_worked_example(self):
        self.assertEqual(
            solve("Plan A costs $100 flat. Plan B costs $50 plus a $200 "
                  "repair fee that is needed with probability 0.3. Which "
                  "has the lower expected cost?"),
            ("expected_cost_two_plans", "plan A; $100 vs $110"))
        self.assertEqual(
            solve("An insurance premium is $120. There is a 2% chance of "
                  "a $5000 loss. How does the premium compare to the "
                  "expected loss?"),
            ("insurance_premium_vs_expected_loss",
             "expected loss $100; premium exceeds it by $20"))

    def test_all_five_renderings_invert_every_variant(self):
        examples = {
            "expected_cost_two_plans": (
                "Plan A costs $100 flat. Plan B costs $50 plus a $200 "
                "repair fee that is needed with probability 0.3.",
                "Which has the lower expected cost?"),
            "insurance_premium_vs_expected_loss": (
                "An insurance premium is $120. There is a 2% chance of a "
                "$5000 loss.",
                "How does the premium compare to the expected loss?"),
            "fair_price": (
                "A game pays $100 with probability 0.5 and $20 otherwise.",
                "What is the fair price to play?"),
            "minimax_vs_expected": (
                "Option A guarantees $50. Option B pays $300 with "
                "probability 0.5 and $0 otherwise.",
                "Which option does the worst-case rule choose, and which "
                "option is better once each outcome's probability is "
                "accounted for?"),
            "risk_of_ruin_simple": (
                "On each of 3 independent rounds, there is a 20% chance "
                "of ruin.",
                "What is the probability of ruin over all 3 rounds combined?"),
            "wait_or_buy": (
                "A price is $200 now. There is a 0.5 probability it "
                "changes to $100 next week; otherwise it stays at $200.",
                "Is it better to buy now or wait, based on expected cost?"),
        }
        for variant, (facts, question) in examples.items():
            for frame in FRAMES:
                problem = frame.format(place="the market stand", name="Ari",
                                       facts=facts, question=question)
                self.assertEqual(solve(problem)[0], variant, problem)

    def test_ties_are_excluded(self):
        random.seed(401)
        for variant in ("expected_cost_two_plans", "minimax_vs_expected",
                        "wait_or_buy"):
            for _ in range(200):
                result = DecisionUnderUncertaintyGenerator(variant).generate()
                self.assertNotIn(" vs $0 vs", result["final_answer"])
                left, right = re.search(r"\$([\d.]+) vs \$([\d.]+)",
                                        result["final_answer"]).groups()
                self.assertNotEqual(left, right, result["final_answer"])

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(402)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = DecisionUnderUncertaintyGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["operation"],
                                 f"applied_decision_under_uncertainty_{variant}_{modifier}")
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            DecisionUnderUncertaintyGenerator("bogus")
        with self.assertRaises(ValueError):
            DecisionUnderUncertaintyGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(403)
        banned = ("1x", "-1x", "^1", "--", "the the", "e+")
        for _ in range(700):
            result = DecisionUnderUncertaintyGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            joined = " ".join((result["problem"], result["final_answer"], *result["steps"]))
            for fragment in banned:
                self.assertNotIn(fragment, joined.lower())
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)

    def test_determinism_under_seed(self):
        random.seed(23)
        gen = DecisionUnderUncertaintyGenerator()
        first = [gen.generate()["problem"] for _ in range(30)]
        random.seed(23)
        second = [gen.generate()["problem"] for _ in range(30)]
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
