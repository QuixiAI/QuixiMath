"""Generate exact weighted-mean calculations in five common forms.

Variants: ``weights``, ``percent_weights``, ``frequency_table_mean``,
``price_per_unit``, and ``missing_weight``. Op-codes: ``STAT_SETUP``,
``PERCENT_TO_DEC``, ``WEIGHT_ROW``, ``A``, ``M``, ``S``, ``D``, ``SETUP``,
``CHECK``, and ``Z``. Ordinary, frequency, and price data are constructed
backward from an exact target; percent weights sum to one exactly; missing
weights are positive integers recovered from a linear equation. Random
weights, values, contexts, settings, component labels, and four phrasings
give unbounded capacity.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import dec, money
from stats_common import CONTEXTS, num_txt, running_sum_steps


STATISTICS = True
SETTINGS = (
    "amber study", "birch survey", "cedar trial", "delta project",
    "ember lab", "forest audit", "granite program", "harbor test",
    "indigo review", "jade pilot", "kestrel study", "lunar trial",
)
WEIGHT_BANK = (2, 3, 4, 5, 6, 8, 10, 12, 15, 20)
PERCENT_BANK = (
    (20, 30, 50), (10, 20, 30, 40), (25, 25, 50), (15, 25, 60),
    (40, 35, 25), (10, 15, 25, 50), (5, 15, 30, 50), (20, 20, 20, 40),
)
COMPONENT_BANK = (
    ("homework", "quizzes", "exam", "project"),
    ("labs", "reports", "presentation", "final"),
    ("practice", "skills test", "meet", "championship"),
    ("design", "build", "testing", "demonstration"),
    ("research", "draft", "revision", "publication"),
)
QUERIES = {
    "weights": (
        "Find the exact weighted mean.",
        "Multiply each value by its weight and compute the weighted average.",
        "What mean results when the stated weights are applied?",
        "Use all value-weight pairs to determine the weighted mean.",
    ),
    "percent_weights": (
        "Find the weighted mean score.",
        "Convert the percentages to decimals and compute the weighted average.",
        "What overall score do these percentage weights produce?",
        "Use the component percentages to calculate the exact weighted mean.",
    ),
    "frequency_table_mean": (
        "Find the mean represented by the frequency table.",
        "Treat each frequency as a weight and compute the exact mean.",
        "What is the weighted average of the tabulated values?",
        "Multiply each value by its frequency, then find the data mean.",
    ),
    "price_per_unit": (
        "Find the average price per kg of the blend.",
        "Use amount as the weight and compute the mixture's unit price.",
        "What exact price per kg does the combined blend cost?",
        "Divide the total blend cost by its total mass.",
    ),
    "missing_weight": (
        "Find the positive integer weight w.",
        "What value of w makes the weighted mean equal the target?",
        "Solve for the missing weight in the weighted-average equation.",
        "Determine the integer weight required to obtain the stated mean.",
    ),
}


def _backward_integer_data(n, low, high, weight_bank=WEIGHT_BANK):
    """Return integer values/weights with an integer weighted mean."""
    span = max(2, (high - low) // 4)
    while True:
        target = random.randint(low + span, high - span)
        weights = [random.choice(weight_bank) for _ in range(n)]
        values = [random.randint(target - span, target + span)
                  for _ in range(n - 1)]
        numerator = target * sum(weights) - sum(
            value * weight for value, weight in zip(values, weights))
        if numerator % weights[-1]:
            continue
        final = numerator // weights[-1]
        if low <= final <= high and len(set(values + [final])) > 1:
            return values + [final], weights, target


def _weighted_steps(values, weights, setup):
    steps = [step("STAT_SETUP", setup, f"entries={len(values)}")]
    products = []
    for value, weight in zip(values, weights):
        product = Fraction(value) * Fraction(weight)
        products.append(product)
        steps.append(step("WEIGHT_ROW", num_txt(value), num_txt(weight),
                          num_txt(product)))
    product_steps, weighted_total = running_sum_steps(products)
    weight_steps, weight_total = running_sum_steps(weights)
    steps.extend(product_steps + weight_steps)
    mean = weighted_total / weight_total
    steps.extend([step("D", num_txt(weighted_total), num_txt(weight_total),
                       num_txt(mean)),
                  step("CHECK", "weighted mean",
                       f"{num_txt(weighted_total)}/{num_txt(weight_total)}",
                       num_txt(mean))])
    return steps, mean


class WeightedMeanGenerator(ProblemGenerator):
    """Generate exact weighted-mean and missing-weight exercises."""

    VARIANTS = ("weights", "percent_weights", "frequency_table_mean",
                "price_per_unit", "missing_weight")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _weights():
        ctx = random.choice(CONTEXTS)
        values, weights, target = _backward_integer_data(
            random.randint(3, 5), ctx.lo, ctx.hi)
        entries = "; ".join(f"({value}, {weight})"
                            for value, weight in zip(values, weights))
        prefix = (f"At the {random.choice(SETTINGS)}, weighted {ctx.label} "
                  f"are listed as (value, weight): {entries}.")
        steps, mean = _weighted_steps(values, weights,
                                      f"weighted {ctx.label}")
        assert mean == target
        return prefix, steps, num_txt(mean)

    @staticmethod
    def _percent_weights():
        percents = random.choice(PERCENT_BANK)
        labels = random.choice(COMPONENT_BANK)[:len(percents)]
        scores = [random.randint(50, 100) for _ in percents]
        entries = "; ".join(
            f"{label}={score} at {percent}%"
            for label, score, percent in zip(labels, scores, percents)
        )
        prefix = f"Weighted components: {entries}."
        weights = [Fraction(percent, 100) for percent in percents]
        steps = [step("STAT_SETUP", "percentage-weighted scores",
                      f"components={len(scores)}")]
        for percent, weight in zip(percents, weights):
            steps.append(step("PERCENT_TO_DEC", f"{percent}%", dec(weight)))
        products = []
        for score, weight in zip(scores, weights):
            product = score * weight
            products.append(product)
            steps.append(step("WEIGHT_ROW", score, dec(weight),
                              num_txt(product)))
        additions, mean = running_sum_steps(products)
        steps.extend(additions)
        steps.append(step("CHECK", "percent weights sum", "100%", 1))
        return prefix, steps, num_txt(mean)

    @staticmethod
    def _frequency_table():
        n = random.randint(3, 5)
        while True:
            values, frequencies, target = _backward_integer_data(
                n, 2, 60, weight_bank=(1, 2, 3, 4, 5, 6, 8))
            if len(set(values)) == n:
                break
        pairs = sorted(zip(values, frequencies))
        values = [value for value, _ in pairs]
        frequencies = [frequency for _, frequency in pairs]
        table = "; ".join(f"{value}: {frequency}"
                          for value, frequency in pairs)
        prefix = f"Frequency table (value: frequency): {table}."
        steps, mean = _weighted_steps(values, frequencies, "frequency table")
        assert mean == target
        return prefix, steps, num_txt(mean)

    @staticmethod
    def _price_per_unit():
        cents, amounts, target_cents = _backward_integer_data(
            random.randint(3, 5), 100, 1200,
            weight_bank=(1, 2, 3, 4, 5, 6, 8, 10))
        prices = [Fraction(value, 100) for value in cents]
        entries = "; ".join(
            f"({money(price)} per kg, {amount} kg)"
            for price, amount in zip(prices, amounts)
        )
        prefix = f"Blend entries (unit price, amount): {entries}."
        steps, mean = _weighted_steps(prices, amounts, "price mixture")
        assert mean == Fraction(target_cents, 100)
        return prefix, steps, f"{money(mean)} per kg"

    @staticmethod
    def _missing_weight():
        while True:
            target = random.randint(25, 80)
            missing_value = target + random.randint(3, 18)
            wanted = random.randint(2, 12)
            known_weights = [random.randint(1, 8), random.randint(1, 8)]
            first_value = random.randint(max(1, target - 25), target - 2)
            numerator = (target * (sum(known_weights) + wanted)
                         - missing_value * wanted
                         - first_value * known_weights[0])
            if numerator % known_weights[1]:
                continue
            second_value = numerator // known_weights[1]
            if 1 <= second_value < target and second_value != first_value:
                break
        entries = (f"({first_value}, {known_weights[0]}); "
                   f"({second_value}, {known_weights[1]})")
        prefix = (f"Known entries (value, weight): {entries}. Missing entry: "
                  f"value {missing_value} with weight w. Target weighted "
                  f"mean: {target}.")
        products = [first_value * known_weights[0],
                    second_value * known_weights[1]]
        steps = [step("STAT_SETUP", "missing weighted entry", f"target={target}")]
        for value, weight, product in zip(
                (first_value, second_value), known_weights, products):
            steps.append(step("WEIGHT_ROW", value, weight, product))
        product_steps, known_total = running_sum_steps(products)
        weight_steps, known_weight = running_sum_steps(known_weights)
        steps.extend(product_steps + weight_steps)
        steps.append(step(
            "SETUP", "weighted mean",
            f"({known_total} + {missing_value}w)/({known_weight} + w) = {target}"))
        target_known = target * known_weight
        right_side = target_known - known_total
        coefficient = missing_value - target
        steps.extend([
            step("M", target, known_weight, target_known),
            step("S", target_known, known_total, right_side),
            step("S", missing_value, target, coefficient),
            step("D", right_side, coefficient, wanted),
            step("CHECK", "substitute",
                 f"({known_total} + {missing_value}·{wanted})/"
                 f"({known_weight} + {wanted})", target),
        ])
        return prefix, steps, str(wanted)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "weights":
            prefix, steps, answer = self._weights()
        elif variant == "percent_weights":
            prefix, steps, answer = self._percent_weights()
        elif variant == "frequency_table_mean":
            prefix, steps, answer = self._frequency_table()
        elif variant == "price_per_unit":
            prefix, steps, answer = self._price_per_unit()
        else:
            prefix, steps, answer = self._missing_weight()
        problem = f"{prefix}\n{random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_weighted_mean_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
