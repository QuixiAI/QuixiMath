"""Compute and select midrange, trimmed, harmonic, and geometric means.

Variants: ``midrange``, ``trimmed_mean``, ``harmonic_mean``,
``geometric_mean_data``, and ``which_mean``. Op-codes: ``STAT_SETUP``,
``RULE``, ``SORT``, ``TRIM``, ``RECIP_ROW``, ``L``, ``C``, ``A``, ``M``,
``D``, ``ROOT``, ``CHECK``, and ``Z``. Trimmed interiors
are symmetric around an exact target, harmonic data come from reciprocal
LCM families, and geometric products are perfect powers. Random contexts,
scales, data order, settings, scenario parameters, and four phrasings give
unbounded capacity.
"""
import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from stats_common import CONTEXTS, num_txt, running_sum_steps


STATISTICS = True
SETTINGS = (
    "amber study", "birch survey", "cedar trial", "delta project",
    "ember lab", "forest audit", "granite program", "harbor test",
    "indigo review", "jade pilot", "kestrel study", "lunar trial",
)
SAMPLE_NAMES = (
    "Aster", "Beryl", "Cobalt", "Dahlia", "Elm", "Flint", "Garnet",
    "Helix", "Iris", "Juniper", "Kite", "Lotus", "Maple", "Nova",
    "Opal", "Pine", "Quartz", "Reed", "Sable", "Thistle",
)
HARMONIC_FAMILIES = (
    (2, 3, 6), (3, 4, 6, 12), (4, 5, 20), (6, 8, 12, 24),
    (5, 10, 20, 20), (3, 6, 9, 18),
)
RATE_PAIRS = ((30, 60), (40, 60), (45, 90), (24, 40), (36, 60),
              (48, 80), (50, 75), (60, 100))
QUERIES = {
    "midrange": (
        "Find the midrange of the data.",
        "Average the minimum and maximum to obtain the midrange.",
        "What exact midpoint lies between the two extreme values?",
        "Use the endpoints of the data set to calculate its midrange.",
    ),
    "trimmed_mean": (
        "Find the trimmed mean under the stated rule.",
        "Remove the required values at both ends, then average those kept.",
        "What exact mean remains after the symmetric trim?",
        "Apply the trimming percentage and compute the new average.",
    ),
    "harmonic_mean": (
        "Find the exact harmonic mean of the data.",
        "Average the reciprocals, then take the reciprocal.",
        "Use the harmonic-mean formula on all listed values.",
        "Compute n divided by the sum of the reciprocals.",
    ),
    "geometric_mean_data": (
        "Find the exact geometric mean of the data.",
        "Multiply all values and take the appropriate root.",
        "What common multiplicative center do these values have?",
        "Use the perfect-power product to compute the geometric mean.",
    ),
    "which_mean": (
        "Choose the appropriate mean and calculate its exact value.",
        "Name the correct mean for this situation and compute it.",
        "Should harmonic or geometric mean be used, and what is the result?",
        "Report both the mean type and its numerical value.",
    ),
}


def _harmonic_steps(values, setup="harmonic data"):
    steps = [step("STAT_SETUP", setup, f"n={len(values)}")]
    reciprocals = [Fraction(1, value) for value in values]
    for value, reciprocal in zip(values, reciprocals):
        steps.append(step("RECIP_ROW", value, str(reciprocal)))
    common = math.lcm(*values)
    steps.append(step("L", ",".join(map(str, values)), common))
    for value in values:
        steps.append(step("C", f"1/{value}",
                          f"{common // value}/{common}"))
    reciprocal_sum = reciprocals[0]
    for reciprocal in reciprocals[1:]:
        steps.append(step("A", str(reciprocal_sum), str(reciprocal),
                          str(reciprocal_sum + reciprocal)))
        reciprocal_sum += reciprocal
    mean = Fraction(len(values), 1) / reciprocal_sum
    steps.extend([step("D", len(values), num_txt(reciprocal_sum),
                       num_txt(mean)),
                  step("CHECK", "harmonic mean",
                       f"{len(values)}/({num_txt(reciprocal_sum)})",
                       num_txt(mean))])
    return steps, mean


def _product_steps(values):
    products = []
    running = Fraction(values[0])
    for value in values[1:]:
        product = running * value
        products.append(step("M", num_txt(running), num_txt(value),
                             num_txt(product)))
        running = product
    return products, running


class AlternativeMeansGenerator(ProblemGenerator):
    """Generate exact alternative-mean calculations and method choices."""

    VARIANTS = ("midrange", "trimmed_mean", "harmonic_mean",
                "geometric_mean_data", "which_mean")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _midrange():
        ctx = random.choice(CONTEXTS)
        size = random.randint(5, 10)
        values = [random.randint(ctx.lo, ctx.hi) for _ in range(size)]
        while min(values) == max(values):
            values = [random.randint(ctx.lo, ctx.hi) for _ in range(size)]
        random.shuffle(values)
        low, high = min(values), max(values)
        answer = Fraction(low + high, 2)
        prefix = (f"At the {random.choice(SETTINGS)}, {ctx.label} are: "
                  f"{', '.join(map(str, values))}.")
        steps = [
            step("STAT_SETUP", ctx.label, f"n={size}"),
            step("SORT", ",".join(map(str, sorted(values)))),
            step("A", low, high, low + high),
            step("D", low + high, 2, num_txt(answer)),
            step("CHECK", "extremes", f"min {low}, max {high}",
                 num_txt(answer)),
        ]
        return prefix, steps, num_txt(answer)

    @staticmethod
    def _trimmed_mean():
        size = random.choice((10, 20))
        percent = random.choice((10, 20))
        drop = size * percent // 100
        kept = size - 2 * drop
        center = random.randint(20, 80)
        deviations = []
        for _ in range(kept // 2):
            delta = random.randint(1, 12)
            deviations.extend((-delta, delta))
        inner = sorted(center + delta for delta in deviations)
        lows = [inner[0] - random.randint(2, 12) for _ in range(drop)]
        highs = [inner[-1] + random.randint(2, 12) for _ in range(drop)]
        values = lows + inner + highs
        random.shuffle(values)
        rule = f"remove the lowest {percent}% and the highest {percent}%"
        prefix = (f"At the {random.choice(SETTINGS)}, sample "
                  f"{random.choice(SAMPLE_NAMES)} has data values: "
                  f"{', '.join(map(str, values))}. Trim rule: {rule}.")
        steps = [
            step("STAT_SETUP", "trimmed data", f"n={size}"),
            step("RULE", f"trim {percent}% of {size}",
                 f"drop {drop} low, {drop} high"),
            step("SORT", ",".join(map(str, sorted(values)))),
            step("TRIM", f"low {','.join(map(str, sorted(lows)))}; high "
                 f"{','.join(map(str, sorted(highs)))}", f"{kept} kept"),
        ]
        additions, total = running_sum_steps(inner)
        steps.extend(additions)
        steps.extend([step("D", total, kept, center),
                      step("CHECK", "trimmed center", f"{total}/{kept}",
                           center)])
        return prefix, steps, str(center)

    @staticmethod
    def _harmonic_mean():
        factor = random.randint(1, 60)
        values = [factor * value for value in random.choice(HARMONIC_FAMILIES)]
        random.shuffle(values)
        prefix = (f"At the {random.choice(SETTINGS)}, sample "
                  f"{random.choice(SAMPLE_NAMES)} has positive data values: "
                  f"{', '.join(map(str, values))}.")
        steps, mean = _harmonic_steps(values)
        return prefix, steps, num_txt(mean)

    @staticmethod
    def _geometric_mean():
        size = random.choice((3, 4))
        divisor = random.choice((2, 3, 4))
        center = divisor * random.randint(2, 40)
        if size == 3:
            values = [center // divisor, center, center * divisor]
        else:
            values = [center // divisor, center, center,
                      center * divisor]
        random.shuffle(values)
        prefix = (f"At the {random.choice(SETTINGS)}, sample "
                  f"{random.choice(SAMPLE_NAMES)} has positive data values: "
                  f"{', '.join(map(str, values))}.")
        steps = [step("STAT_SETUP", "geometric data", f"n={size}")]
        products, product = _product_steps(values)
        steps.extend(products)
        radical = "∛" if size == 3 else "∜"
        steps.extend([step("ROOT", f"{radical}{product}", center),
                      step("CHECK", "perfect power",
                           f"{center}^{size}", product)])
        return prefix, steps, str(center)

    @staticmethod
    def _which_mean():
        if random.choice((True, False)):
            first, second = random.choice(RATE_PAIRS)
            scale = random.randint(1, 8)
            speeds = [first * scale, second * scale]
            prefix = (f"During the {random.choice(SETTINGS)}, a test vehicle "
                      f"on route {random.choice(SAMPLE_NAMES)} travels equal "
                      f"distances at {speeds[0]} mph and {speeds[1]} mph.")
            steps = [step("RULE", "equal-distance rates", "use harmonic mean")]
            harmonic_steps, mean = _harmonic_steps(speeds, "equal-distance rates")
            steps.extend(harmonic_steps)
            answer = f"harmonic; {num_txt(mean)} mph"
        else:
            center = Fraction(random.randint(8, 20), 10)
            ratio = random.choice((2, 4, 5, 8, 10))
            factors = [center / ratio, center * ratio]
            prefix = (f"During the {random.choice(SETTINGS)}, portfolio "
                      f"{random.choice(SAMPLE_NAMES)} has multiplicative "
                      f"growth factors "
                      f"{num_txt(factors[0])} and {num_txt(factors[1])} over "
                      f"equal periods.")
            steps = [
                step("STAT_SETUP", "equal-period growth", "2 factors"),
                step("RULE", "multiplicative growth", "use geometric mean"),
                step("M", num_txt(factors[0]), num_txt(factors[1]),
                     num_txt(center * center)),
                step("ROOT", f"√{num_txt(center * center)}", num_txt(center)),
                step("CHECK", "growth factor", f"{num_txt(center)}^2",
                     num_txt(center * center)),
            ]
            answer = f"geometric; factor {num_txt(center)}"
        return prefix, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        methods = {
            "midrange": self._midrange,
            "trimmed_mean": self._trimmed_mean,
            "harmonic_mean": self._harmonic_mean,
            "geometric_mean_data": self._geometric_mean,
            "which_mean": self._which_mean,
        }
        prefix, steps, answer = methods[variant]()
        problem = f"{prefix}\n{random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_alternative_means_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
