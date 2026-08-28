"""Problem-text-only enumeration oracles for OptimizationInContextGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.optimization_in_context_generator import (
    APPLIED, FRAMES, MODIFIERS, VARIANTS, OptimizationInContextGenerator,
)
from helpers import DELIM


def number(token):
    return Fraction(token.replace("$", "").replace(",", "").rstrip("."))


def money(value):
    cents = int(Fraction(value) * 100)
    return f"${cents // 100}.{cents % 100:02d}"


def clean(problem):
    return re.sub(r"^A separate ledger mentions \d+ old invoices\. ", "", problem)


def unique_best(candidates, key, problem):
    optimum = min(key(item) for item in candidates)
    winners = [item for item in candidates if key(item) == optimum]
    if len(winners) != 1:
        raise AssertionError(f"optimum not unique: {winners}: {problem}")
    return winners[0]


def solve(problem):
    text = clean(problem)

    match = re.search(r"rectangular pen must use exactly (\d+) m of fencing", text, re.I)
    if match:
        fence = int(match.group(1))
        half = fence // 2
        candidates = [(width * (half - width), width, half - width)
                      for width in range(1, half) if width <= half - width]
        area, width, length = max(candidates)
        model = f"A = w({half} − w)"
        return "max_area_fixed_fence", f"{width} m by {length} m; {area} m²", model

    match = re.search(
        r"plan A: (\$[0-9.]+); plan B: (\$[0-9.]+); plan C: (\$[0-9.]+)", text, re.I)
    if match:
        costs = list(map(number, match.groups()))
        index = min(range(3), key=costs.__getitem__)
        return "best_of_three_plans_table", f"plan {'ABC'[index]}; {money(costs[index])}", "choose the smallest quoted total"

    match = re.search(
        r"needs exactly (\d+) units\. Supplier A charges (\$[0-9.]+) per unit "
        r"and can provide at most (\d+); supplier B charges (\$[0-9.]+) per unit "
        r"and can provide at most (\d+)", text, re.I)
    if match:
        demand = int(match.group(1))
        cost_a, cap_a = number(match.group(2)), int(match.group(3))
        cost_b, cap_b = number(match.group(4)), int(match.group(5))
        candidates = [(cost_a * a + cost_b * (demand - a), a, demand - a)
                      for a in range(demand + 1)
                      if a <= cap_a and demand - a <= cap_b]
        total, amount_a, amount_b = unique_best(candidates, lambda item: item[0], text)
        model = f"minimize C = {cost_a}a + {cost_b}b; a + b = {demand}"
        answer = f"supplier A {amount_a}; supplier B {amount_b}; cost {money(total)}"
        return "min_cost_two_suppliers", answer, model

    capacity_match = re.search(r"pack can hold at most (\d+) kg", text, re.I)
    items = re.findall(r"item ([A-D]): (\d+) kg, value (\d+) points", text, re.I)
    if capacity_match and len(items) == 4:
        capacity = int(capacity_match.group(1))
        weights = [int(item[1]) for item in items]
        values = [int(item[2]) for item in items]
        candidates = []
        for mask in range(1, 16):
            weight = sum(weights[i] for i in range(4) if mask & (1 << i))
            value = sum(values[i] for i in range(4) if mask & (1 << i))
            if weight <= capacity:
                candidates.append((-value, weight, mask))
        neg_value, weight, mask = unique_best(candidates, lambda item: item[0], text)
        chosen = "+".join("ABCD"[i] for i in range(4) if mask & (1 << i))
        model = f"maximize total points with weight ≤ {capacity} kg"
        return "knapsack_small", f"items {chosen}; value {-neg_value}; weight {weight} kg", model

    match = re.search(
        r"whole-dollar price p, demand is (\d+) − (\d+)p units", text, re.I)
    if match:
        intercept, slope = map(int, match.groups())
        candidates = [(p * (intercept - slope * p), p)
                      for p in range(intercept // slope + 1)]
        revenue, price = max(candidates)
        model = f"R = p({intercept} − {slope}p)"
        return "max_revenue", f"price {money(price)}; revenue {money(revenue)}", model

    match = re.search(
        r"closed box with a square base must hold (\d+) cm³", text, re.I)
    if match:
        volume = int(match.group(1))
        candidates = []
        for base in range(1, volume + 1):
            if volume % (base * base) == 0:
                height = volume // (base * base)
                surface = 2 * base * base + 4 * base * height
                candidates.append((surface, base, height))
        surface, base, height = unique_best(candidates, lambda item: item[0], text)
        model = f"S = 2x² + 4xh; x²h = {volume}"
        answer = f"{base} cm by {base} cm by {height} cm; {surface} cm²"
        return "min_material_box", answer, model

    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer, model = solve(problem)
    return variant, (f"{model}; {answer}" if modifier == "with_model" else answer), model


class TestOptimizationInContextGenerator(unittest.TestCase):
    def test_marker_contract_and_500_sample_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(360)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(24):
                    result = OptimizationInContextGenerator(variant, modifier).generate()
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
            "max_area_fixed_fence": ("A rectangular pen must use exactly 40 m of fencing.",
                                     "What whole-number dimensions give the largest area, and what is that area?"),
            "best_of_three_plans_table": ("Three complete project plans have quoted costs — "
                                          "plan A: $420.00; plan B: $455.00; plan C: $430.00.",
                                          "Which plan costs the least?"),
            "min_cost_two_suppliers": ("A project needs exactly 50 units. Supplier A charges "
                                       "$4.00 per unit and can provide at most 30; supplier B "
                                       "charges $7.00 per unit and can provide at most 30.",
                                       "How many units should come from each supplier for the lowest cost?"),
            "knapsack_small": ("A pack can hold at most 7 kg. Four indivisible items are "
                               "available — item A: 2 kg, value 8 points; item B: 3 kg, value "
                               "10 points; item C: 4 kg, value 15 points; item D: 6 kg, value 18 points.",
                               "Which items give the greatest total value without exceeding the limit?"),
            "max_revenue": ("At a whole-dollar price p, demand is 40 − 2p units. Revenue "
                            "is price times demand.",
                            "Which price gives the greatest revenue, and what is that revenue?"),
            "min_material_box": ("A closed box with a square base must hold 125 cm³. Its base "
                                 "side and height must be positive whole centimeters.",
                                 "Which dimensions use the least material, and what surface area is needed?"),
        }
        for variant, (facts, question) in examples.items():
            for frame in FRAMES:
                problem = frame.format(place="the workshop", name="Ari",
                                       facts=facts, question=question)
                self.assertEqual(solve(problem)[0], variant, problem)

    def test_arithmetic_and_complete_knapsack_enumeration(self):
        random.seed(361)
        for _ in range(900):
            result = OptimizationInContextGenerator().generate()
            if "_knapsack_small_" in result["operation"]:
                options = [s for s in result["steps"] if s.startswith(f"KNAPSACK_OPTION{DELIM}")]
                self.assertEqual(len(options), 15)
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
                elif fields[0] == "E":
                    self.assertEqual(number(fields[1]) ** int(fields[2]), number(fields[3]), raw)
                elif fields[0] == "AREA":
                    left, right = fields[1].split(" × ")
                    self.assertEqual(number(left) * number(right), number(fields[2]), raw)

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(362)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = OptimizationInContextGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["operation"], f"applied_optimization_context_{variant}_{modifier}")
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            OptimizationInContextGenerator("bogus")
        with self.assertRaises(ValueError):
            OptimizationInContextGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(363)
        banned = ("1x", "-1x", "^1", "+ 0", "--", "the the", "e+")
        for _ in range(700):
            result = OptimizationInContextGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            joined = " ".join((result["problem"], result["final_answer"], *result["steps"]))
            for fragment in banned:
                self.assertNotIn(fragment, joined.lower())
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
