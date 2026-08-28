"""Choose exact optima from small, fully stated practical search spaces.

Variants: ``max_area_fixed_fence``, ``best_of_three_plans_table``,
``min_cost_two_suppliers``, ``knapsack_small``, ``max_revenue``, and
``min_material_box``. Five context frames and all four applied modifiers are
supported. Ties are excluded by construction. Op-codes: ``SELECT_RELEVANT``,
``ESTIMATE``, ``ESTIMATE_CHECK``, ``MODEL_EQ``, ``REWRITE``, ``AREA``,
``OPTION``, ``DECIDE``, ``SUPPLIER_ALLOCATE``, ``KNAPSACK_OPTION``, ``REVENUE``,
``BOX_SURFACE``, ``TRY``, ``ACCEPT``, ``A``, ``S``, ``M``, ``D``, ``E``,
``CHECK``, and ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import CONTEXTS, NAMES, estimate_first, money, select_relevant_step, unit
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("max_area_fixed_fence", "best_of_three_plans_table",
            "min_cost_two_suppliers", "knapsack_small", "max_revenue",
            "min_material_box")
FRAMES = (
    "At {place}, {name} must choose the best feasible result. {facts} {question}",
    "{question} A planning note for {name} at {place} states: {facts}",
    "For {name}'s decision at {place}: {facts} {question}",
    "A report from {place}, reviewed by {name}, gives these constraints: {facts} {question}",
    "Consider the choice {name} is making at {place}. {facts} {question}",
)
PLACES = tuple(setting for key in ("business", "shop", "garden", "workshop")
               for setting in CONTEXTS[key].settings)


def _render(facts, question):
    return random.choice(FRAMES).format(facts=facts, question=question,
                                        place=random.choice(PLACES),
                                        name=random.choice(NAMES))


class OptimizationInContextGenerator(ProblemGenerator):
    """Generate six bounded optimization stories without method cues."""

    VARIANTS, MODIFIERS = VARIANTS, MODIFIERS

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant, self.modifier = variant, modifier

    @staticmethod
    def _max_area_fixed_fence():
        side = random.randint(5, 40)
        fence, half, area = 4 * side, 2 * side, side ** 2
        neighbor = (side - 1) * (side + 1)
        facts = f"A rectangular pen must use exactly {fence} m of fencing."
        question = "What whole-number dimensions give the largest area, and what is that area?"
        model = f"A = w({half} − w)"
        steps = [step("D", fence, 2, half),
                 step("MODEL_EQ", model, "half the fence is width plus length"),
                 step("REWRITE", f"A = −w² + {half}w"),
                 step("D", half, 2, side),
                 step("AREA", f"{side} × {side}", area),
                 step("TRY", f"w = {side - 1}", neighbor),
                 step("TRY", f"w = {side + 1}", neighbor),
                 step("ACCEPT", f"w = {side}", area),
                 step("CHECK", f"neighbor area {neighbor}", f"{neighbor} < {area}")]
        answer = f"{side} m by {side} m; {area} m²"
        used = [f"fence {fence} m", "whole-number dimensions"]
        return facts, question, steps, answer, Fraction(area), model, used, lambda v: unit(v, "m²")

    @staticmethod
    def _best_of_three_plans_table():
        costs = random.sample(range(250, 951), 3)
        best_index = min(range(3), key=costs.__getitem__)
        labels = "ABC"
        facts = (f"Three complete project plans have quoted costs — plan A: {money(costs[0])}; "
                 f"plan B: {money(costs[1])}; plan C: {money(costs[2])}.")
        question = "Which plan costs the least?"
        model = "choose the smallest quoted total"
        steps = [step("OPTION", label, money(cost)) for label, cost in zip(labels, costs)]
        ordered = sorted(costs)
        steps += [step("DECIDE", labels[best_index],
                       f"{money(ordered[0])} < {money(ordered[1])} < {money(ordered[2])}"),
                  step("CHECK", "all three complete plans compared", labels[best_index])]
        answer = f"plan {labels[best_index]}; {money(costs[best_index])}"
        used = [f"plan costs {money(costs[0])}, {money(costs[1])}, {money(costs[2])}"]
        return facts, question, steps, answer, Fraction(costs[best_index]), model, used, money

    @staticmethod
    def _min_cost_two_suppliers():
        demand = random.randint(30, 120)
        cap_a = random.randint(10, demand - 10)
        cap_b = random.randint(demand - cap_a, demand + 20)
        cost_a, cost_b = random.sample(range(2, 16), 2)
        if cost_a < cost_b:
            amount_a = min(cap_a, demand)
            amount_b = demand - amount_a
        else:
            amount_b = min(cap_b, demand)
            amount_a = demand - amount_b
        total_cost = cost_a * amount_a + cost_b * amount_b
        facts = (f"A project needs exactly {demand} units. Supplier A charges {money(cost_a)} "
                 f"per unit and can provide at most {cap_a}; supplier B charges {money(cost_b)} "
                 f"per unit and can provide at most {cap_b}.")
        question = "How many units should come from each supplier for the lowest cost?"
        model = f"minimize C = {cost_a}a + {cost_b}b; a + b = {demand}"
        steps = [step("MODEL_EQ", model, "demand and capacities"),
                 step("SUPPLIER_ALLOCATE", "supplier A", amount_a, f"capacity {cap_a}"),
                 step("SUPPLIER_ALLOCATE", "supplier B", amount_b, f"capacity {cap_b}"),
                 step("M", cost_a, amount_a, cost_a * amount_a),
                 step("M", cost_b, amount_b, cost_b * amount_b),
                 step("A", cost_a * amount_a, cost_b * amount_b, total_cost),
                 step("A", amount_a, amount_b, demand),
                 step("CHECK", "cheaper supplier used to capacity when needed", total_cost)]
        answer = f"supplier A {amount_a}; supplier B {amount_b}; cost {money(total_cost)}"
        used = [f"demand {demand}", f"A {money(cost_a)}, cap {cap_a}", f"B {money(cost_b)}, cap {cap_b}"]
        return facts, question, steps, answer, Fraction(total_cost), model, used, money

    @staticmethod
    def _knapsack_small():
        labels = "ABCD"
        while True:
            weights = random.sample(range(2, 14), 4)
            values = random.sample(range(8, 61), 4)
            capacity = random.randint(8, 22)
            feasible = []
            for mask in range(1, 16):
                weight = sum(weights[i] for i in range(4) if mask & (1 << i))
                value = sum(values[i] for i in range(4) if mask & (1 << i))
                if weight <= capacity:
                    feasible.append((value, -weight, mask))
            if feasible:
                top_value = max(item[0] for item in feasible)
                winners = [item for item in feasible if item[0] == top_value]
                if len(winners) == 1:
                    _, neg_weight, best_mask = winners[0]
                    break
        chosen = [labels[i] for i in range(4) if best_mask & (1 << i)]
        best_weight = -neg_weight
        facts = ("A pack can hold at most " + str(capacity) + " kg. Four indivisible items "
                 "are available — " + "; ".join(
                     f"item {labels[i]}: {weights[i]} kg, value {values[i]} points"
                     for i in range(4)) + ".")
        question = "Which items give the greatest total value without exceeding the limit?"
        model = f"maximize total points with weight ≤ {capacity} kg"
        steps = [step("MODEL_EQ", model, "all subsets of four items")]
        for mask in range(1, 16):
            subset = "".join(labels[i] for i in range(4) if mask & (1 << i))
            weight = sum(weights[i] for i in range(4) if mask & (1 << i))
            value = sum(values[i] for i in range(4) if mask & (1 << i))
            status = "feasible" if weight <= capacity else "over limit"
            steps.append(step("KNAPSACK_OPTION", subset, weight, value, status))
        steps += [step("DECIDE", "+".join(chosen), f"value {top_value}"),
                  step("CHECK", f"weight {best_weight}", f"{best_weight} ≤ {capacity}")]
        answer = f"items {'+'.join(chosen)}; value {top_value}; weight {best_weight} kg"
        used = [f"capacity {capacity} kg"] + [f"{labels[i]} {weights[i]} kg value {values[i]}" for i in range(4)]
        return facts, question, steps, answer, Fraction(top_value), model, used, str

    @staticmethod
    def _max_revenue():
        slope = random.randint(2, 6)
        price = random.randint(5, 35)
        intercept = 2 * slope * price
        quantity, revenue = intercept - slope * price, price * (intercept - slope * price)
        left = (price - 1) * (intercept - slope * (price - 1))
        right = (price + 1) * (intercept - slope * (price + 1))
        facts = (f"At a whole-dollar price p, demand is {intercept} − {slope}p units. "
                 "Revenue is price times demand.")
        question = "Which price gives the greatest revenue, and what is that revenue?"
        model = f"R = p({intercept} − {slope}p)"
        steps = [step("REVENUE", model), step("REWRITE", f"R = −{slope}p² + {intercept}p"),
                 step("M", 2, -slope, -2 * slope), step("D", -intercept, -2 * slope, price),
                 step("M", slope, price, slope * price), step("S", intercept, slope * price, quantity),
                 step("M", price, quantity, revenue), step("TRY", f"p = {price - 1}", left),
                 step("TRY", f"p = {price + 1}", right), step("ACCEPT", f"p = {price}", revenue),
                 step("CHECK", "neighbor revenues", f"{left}, {right} < {revenue}")]
        answer = f"price {money(price)}; revenue {money(revenue)}"
        used = [f"demand {intercept} − {slope}p", "whole-dollar price", "revenue price times demand"]
        return facts, question, steps, answer, Fraction(revenue), model, used, money

    @staticmethod
    def _min_material_box():
        side = random.randint(3, 16)
        volume = side ** 3
        candidates = []
        for base in range(1, volume + 1):
            if volume % (base * base) == 0:
                height = volume // (base * base)
                surface = 2 * base * base + 4 * base * height
                candidates.append((surface, base, height))
        surface, base, height = min(candidates)
        facts = (f"A closed box with a square base must hold {volume} cm³. Its base side "
                 "and height must be positive whole centimeters.")
        question = "Which dimensions use the least material, and what surface area is needed?"
        model = f"S = 2x² + 4xh; x²h = {volume}"
        steps = [step("MODEL_EQ", model, "closed square-base box")]
        for candidate_surface, candidate_base, candidate_height in sorted(candidates)[:8]:
            steps.append(step("BOX_SURFACE", f"{candidate_base}×{candidate_base}×{candidate_height}",
                              candidate_surface))
        steps += [step("ACCEPT", f"x = {base}, h = {height}", surface),
                  step("E", base, 2, base ** 2), step("M", base ** 2, height, volume),
                  step("CHECK", "required volume", unit(volume, "cm³"))]
        answer = f"{base} cm by {base} cm by {height} cm; {surface} cm²"
        used = [f"volume {volume} cm³", "whole-centimeter square base and height"]
        return facts, question, steps, answer, Fraction(surface), model, used, lambda v: unit(v, "cm²")

    @classmethod
    def _case(cls, variant):
        return getattr(cls, f"_{variant}")()

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        modifier = self.modifier or random.choice(self.MODIFIERS)
        facts, question, steps, answer, value, model, used, renderer = self._case(variant)
        problem = _render(facts, question)
        if modifier == "distractor":
            occupied = {int(token) for token in re.findall(r"\d+", problem)}
            extra = random.choice([value for value in range(601, 1001) if value not in occupied])
            problem = f"A separate ledger mentions {extra} old invoices. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} old invoices"))
        elif modifier == "estimate_first":
            steps = estimate_first(steps + [step("Z", answer)], value,
                                   "predict the best feasible scale",
                                   render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "objective and constraints"))
            answer = f"{model}; {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"applied_optimization_context_{variant}_{modifier}",
                "problem": problem, "steps": steps, "final_answer": answer}
