"""Problem-text-only brute-force oracles for SystemsWordGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.systems_word_generator import (
    APPLIED, FRAMES, MODIFIERS, VARIANTS, SystemsWordGenerator,
)
from helpers import DELIM


def number(token):
    return Fraction(token.replace("$", "").replace("%", "").rstrip("."))


def money(value):
    cents = int(Fraction(value) * 100)
    return f"${cents // 100}.{cents % 100:02d}"


def clean(problem):
    return re.sub(r"^An unrelated inventory lists \d+ shipping labels\. ", "", problem)


def unique_pair(pairs, problem):
    pairs = list(pairs)
    if len(pairs) != 1:
        raise AssertionError(f"expected one solution, got {pairs}: {problem}")
    return pairs[0]


def solve(problem):
    text = clean(problem)

    match = re.search(
        r"theater sold (\d+) tickets for \$(\d+)\. Adult tickets cost \$(\d+) "
        r"and child tickets cost \$(\d+)", text, re.I)
    if match:
        total, revenue, adult_price, child_price = map(int, match.groups())
        adults, children = unique_pair(
            ((a, total - a) for a in range(total + 1)
             if adult_price * a + child_price * (total - a) == revenue), text)
        model = f"a + c = {total}; {adult_price}a + {child_price}c = {revenue}"
        return "tickets", f"adults {adults}; children {children}", model

    match = re.search(
        r"order contains (\d+) items and costs \$(\d+)\. Each notebook costs "
        r"\$(\d+), and each pen costs \$(\d+)", text, re.I)
    if match:
        total, cost, notebook_price, pen_price = map(int, match.groups())
        notebooks, pens = unique_pair(
            ((n, total - n) for n in range(total + 1)
             if notebook_price * n + pen_price * (total - n) == cost), text)
        model = f"n + p = {total}; {notebook_price}n + {pen_price}p = {cost}"
        return "two_item_purchase", f"notebooks {notebooks}; pens {pens}", model

    match = re.search(
        r"total of \$(\d+) is split between accounts paying (\d+)% and (\d+)% "
        r"simple annual interest\. After one year, the interest is \$(\d+)", text, re.I)
    if match:
        total, high_rate, low_rate, interest = map(int, match.groups())
        high_amount, low_amount = unique_pair(
            ((h, total - h) for h in range(0, total + 1, 100)
             if high_rate * h + low_rate * (total - h) == interest * 100), text)
        combined = interest * 100
        model = f"h + l = {total}; {high_rate}h + {low_rate}l = {combined}"
        answer = (f"{high_rate}% account {money(high_amount)}; {low_rate}% "
                  f"account {money(low_amount)}")
        return "investment_two_rates", answer, model

    match = re.search(
        r"solutions that are (\d+)% and (\d+)% concentrated\. The final "
        r"(\d+) L blend is ([0-9/]+)% concentrated", text, re.I)
    if match:
        high_pct, low_pct, total = map(int, match.groups()[:3])
        target = number(match.group(4))
        high_volume, low_volume = unique_pair(
            ((h, total - h) for h in range(total + 1)
             if high_pct * h + low_pct * (total - h) == target * total), text)
        combined = int(target * total)
        model = f"h + l = {total}; {high_pct}h + {low_pct}l = {combined}"
        answer = (f"{high_pct}% solution {high_volume} L; {low_pct}% solution "
                  f"{low_volume} L")
        return "mixture_as_system", answer, model

    match = re.search(
        r"rectangle has perimeter (\d+) m\. Its length is (\d+) m greater "
        r"than its width", text, re.I)
    if match:
        perimeter, difference = map(int, match.groups())
        length, width = unique_pair(
            ((length, width) for length in range(1, perimeter)
             for width in range(1, perimeter)
             if 2 * (length + width) == perimeter and length - width == difference), text)
        half = perimeter // 2
        model = f"L + W = {half}; L − W = {difference}"
        return "perimeter_and_relation", f"length {length} m; width {width} m", model

    match = re.search(
        r"order A: (\d+) markers? and (\d+) folders? cost \$(\d+); order B: "
        r"(\d+) markers? and (\d+) folders? cost \$(\d+)", text, re.I)
    if match:
        a1, b1, total1, a2, b2, total2 = map(int, match.groups())
        marker, folder = unique_pair(
            ((m, f) for m in range(1, 51) for f in range(1, 51)
             if a1 * m + b1 * f == total1 and a2 * m + b2 * f == total2), text)
        model = f"{a1}m + {b1}f = {total1}; {a2}m + {b2}f = {total2}"
        return "from_table", f"marker {money(marker)}; folder {money(folder)}", model

    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer, model = solve(problem)
    return variant, (f"{model}; {answer}" if modifier == "with_model" else answer), model


class TestSystemsWordGenerator(unittest.TestCase):
    def test_marker_contract_and_500_sample_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(330)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(24):
                    result = SystemsWordGenerator(variant, modifier).generate()
                    self.assertEqual(result["steps"][-1],
                                     f"Z{DELIM}{result['final_answer']}")
                    parsed, answer, model = expected(result["problem"], modifier)
                    self.assertEqual(parsed, variant)
                    self.assertEqual(result["final_answer"], answer, result["problem"])
                    if modifier == "with_model":
                        self.assertEqual(result["steps"][0].split(DELIM)[1], model)
                    seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})

    def test_all_five_renderings_invert_every_variant(self):
        examples = {
            "tickets": ("A theater sold 200 tickets for $1390. Adult tickets cost $8 "
                        "and child tickets cost $5.",
                        "How many adult tickets and child tickets were sold?"),
            "two_item_purchase": ("A supply order contains 20 items and costs $80. "
                                  "Each notebook costs $6, and each pen costs $2.",
                                  "How many notebooks and pens are in the order?"),
            "investment_two_rates": ("A total of $5000 is split between accounts "
                                     "paying 8% and 4% simple annual interest. After "
                                     "one year, the interest is $280.",
                                     "How much was placed in each account?"),
            "mixture_as_system": ("A blend uses solutions that are 60% and 20% "
                                  "concentrated. The final 10 L blend is 40% concentrated.",
                                  "How many liters of each solution were used?"),
            "perimeter_and_relation": ("A rectangle has perimeter 44 m. Its length "
                                       "is 4 m greater than its width.",
                                       "What are the rectangle's length and width?"),
            "from_table": ("Two supply orders are listed — order A: 2 markers and 3 "
                           "folders cost $19; order B: 4 markers and 1 folders cost $23.",
                           "What is the price of one marker and one folder?"),
        }
        for variant, (facts, question) in examples.items():
            for frame in FRAMES:
                problem = frame.format(place="the school store", name="Ari",
                                       facts=facts, question=question)
                self.assertEqual(solve(problem)[0], variant, problem)

    def test_arithmetic_inside_emitted_steps(self):
        random.seed(331)
        for _ in range(900):
            result = SystemsWordGenerator().generate()
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
        random.seed(332)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = SystemsWordGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["operation"], f"applied_systems_word_{variant}_{modifier}")
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            SystemsWordGenerator("bogus")
        with self.assertRaises(ValueError):
            SystemsWordGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(333)
        banned = ("1x", "-1x", "^1", "+ 0", "--", "the the", "e+")
        for _ in range(700):
            result = SystemsWordGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            joined = " ".join((result["problem"], result["final_answer"], *result["steps"]))
            for fragment in banned:
                self.assertNotIn(fragment, joined.lower())
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
