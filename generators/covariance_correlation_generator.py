"""Compute covariance and correlation by exact hand procedures.

Variants: ``sample_covariance``, ``population_covariance``,
``r_from_summaries``, ``r_from_z_products``, ``covariance_sign``, and
``r_properties``. Raw paired data use integer zero-sum deviation patterns;
z-score rows use exact standardized vectors whose squared sum is ``n - 1``;
summary variants avoid radicals by supplying covariance and standard
deviations. Random patterns, pairings, scales, centers, sites, parameters,
and four phrasings give unbounded capacity.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from stats_common import num_txt, patterns, running_sum_steps


STATISTICS = True
SETTINGS = (
    "amber study", "birch survey", "cedar trial", "delta project",
    "ember lab", "forest audit", "granite program", "harbor test",
    "indigo review", "jade pilot", "kestrel study", "lunar trial",
)
LOCATIONS = (
    "north campus", "south campus", "east annex", "west annex",
    "river center", "lake center", "hill school", "valley school",
    "maple office", "oak office", "pine clinic", "cedar clinic",
)
R_VALUES = tuple(Fraction(value, 10)
                 for value in (-9, -8, -6, -5, -4, -2, 2, 4, 5, 6, 8, 9))
QUERIES = {
    "sample_covariance": (
        "Find the exact sample covariance.",
        "Use divisor n - 1 to calculate the covariance of the paired data.",
        "Build the deviation-product sum and report the sample covariance.",
        "What sample covariance do these observations produce?",
    ),
    "population_covariance": (
        "Find the exact population covariance.",
        "Use divisor n to calculate the covariance of the paired data.",
        "Build the deviation-product sum and report the population covariance.",
        "What population covariance do these observations produce?",
    ),
    "r_from_summaries": (
        "Use the supplied summaries to find r.",
        "Divide covariance by the product of the two standard deviations.",
        "Calculate the exact correlation coefficient from the summary values.",
        "What value of r corresponds to these covariance summaries?",
    ),
    "r_from_z_products": (
        "Use the supplied z-score products to find sample r.",
        "Add the paired z products and divide by n - 1.",
        "Calculate the exact correlation from these standardized rows.",
        "What sample correlation do the listed z-score pairs produce?",
    ),
    "covariance_sign": (
        "Find the sample covariance and interpret its sign.",
        "Report both the covariance direction and its exact value.",
        "Calculate the sample covariance, then label it positive or negative.",
        "What sign does the paired-data covariance have, and what is it?",
    ),
    "r_properties": (
        "State what happens to r and give its resulting value.",
        "Does this positive-scale unit conversion change the correlation?",
        "Apply the correlation invariance rule to report the new r.",
        "Give a composite unchanged-or-changed verdict with the coefficient.",
    ),
}


def _site():
    return f"{random.choice(LOCATIONS)} during the {random.choice(SETTINGS)}"


def _raw_data(require_nonzero=False):
    while True:
        n = random.randint(4, 8)
        dx = list(random.choice(patterns(n, max_abs=5)))
        dy = list(random.choice(patterns(n, max_abs=5)))
        x_scale = random.randint(1, 4)
        y_scale = random.randint(1, 4)
        dx = [value * x_scale for value in dx]
        dy = [value * y_scale for value in dy]
        random.shuffle(dx)
        random.shuffle(dy)
        product_sum = sum(a * b for a, b in zip(dx, dy))
        if product_sum or not require_nonzero:
            break
    x_mean = random.randint(30, 100)
    y_mean = random.randint(40, 140)
    xs = [x_mean + value for value in dx]
    ys = [y_mean + value for value in dy]
    pairs = list(zip(xs, ys))
    random.shuffle(pairs)
    xs, ys = map(list, zip(*pairs))
    return xs, ys


def _raw_prefix(xs, ys):
    return (f"At the {_site()}, paired data are listed in matching order.\n"
            f"x values: {', '.join(map(str, xs))}.\n"
            f"y values: {', '.join(map(str, ys))}.")


def _covariance_steps(xs, ys, sample):
    n = len(xs)
    x_total, y_total = sum(xs), sum(ys)
    x_mean, y_mean = Fraction(x_total, n), Fraction(y_total, n)
    steps = [
        step("STAT_SETUP", "sample covariance" if sample else
             "population covariance", f"n={n}"),
        step("SUM", "x: " + " + ".join(map(str, xs)), x_total),
        step("MEAN_DIV", x_total, n, num_txt(x_mean)),
        step("SUM", "y: " + " + ".join(map(str, ys)), y_total),
        step("MEAN_DIV", y_total, n, num_txt(y_mean)),
    ]
    products = []
    for x, y in zip(xs, ys):
        dx, dy = Fraction(x) - x_mean, Fraction(y) - y_mean
        product = dx * dy
        products.append(product)
        steps.append(step("REG_ROW", f"x-x̄={num_txt(dx)}",
                          f"y-ȳ={num_txt(dy)}",
                          f"product={num_txt(product)}"))
    additions, product_sum = running_sum_steps(products)
    steps.extend(additions)
    steps.append(step("SUM", "deviation products", num_txt(product_sum)))
    divisor = n - 1 if sample else n
    if sample:
        steps.append(step("EVAL", "n - 1", divisor))
    covariance = product_sum / divisor
    steps.extend([step("D", num_txt(product_sum), divisor,
                       num_txt(covariance)),
                  step("CHECK", "covariance divisor",
                       "n - 1" if sample else "n", num_txt(covariance))])
    return steps, covariance


class CovarianceCorrelationGenerator(ProblemGenerator):
    """Generate exact covariance and standalone correlation exercises."""

    VARIANTS = ("sample_covariance", "population_covariance",
                "r_from_summaries", "r_from_z_products", "covariance_sign",
                "r_properties")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _raw(sample, sign=False):
        xs, ys = _raw_data(require_nonzero=sign)
        prefix = _raw_prefix(xs, ys)
        steps, covariance = _covariance_steps(xs, ys, sample)
        if sign:
            label = "positive" if covariance > 0 else "negative"
            answer = f"{label}; cov = {num_txt(covariance)}"
            steps.append(step("SIGN", num_txt(covariance), label))
            steps.append(step("CHECK", "covariance interpretation", answer))
        else:
            answer = num_txt(covariance)
        return prefix, steps, answer

    @staticmethod
    def _from_summaries():
        sx = random.randint(2, 12)
        sy = random.randint(2, 12)
        r = random.choice(R_VALUES)
        covariance = r * sx * sy
        prefix = (f"At the {_site()}, supplied sample summaries are: "
                  f"covariance = {num_txt(covariance)}; sx = {sx}; sy = "
                  f"{sy}. Use r = covariance/(sx·sy).")
        denominator = sx * sy
        steps = [
            step("STAT_SETUP", "r from sample summaries", f"sx={sx}, sy={sy}"),
            step("CORR_FORMULA", "r = covariance/(sx·sy)"),
            step("M", sx, sy, denominator),
            step("D", num_txt(covariance), denominator, num_txt(r)),
            step("CHECK", "abs(r) ≤ 1", f"abs(r)={num_txt(abs(r))}"),
        ]
        return prefix, steps, num_txt(r)

    @staticmethod
    def _from_z_products():
        zx = [-1, -1, 0, 1, 1]
        zy = zx[:]
        random.shuffle(zx)
        random.shuffle(zy)
        pairs = list(zip(zx, zy))
        random.shuffle(pairs)
        products = [a * b for a, b in pairs]
        total = sum(products)
        r = Fraction(total, len(pairs) - 1)
        prefix = (f"At the {_site()}, paired sample z-scores are: "
                  f"{', '.join(f'({a}, {b})' for a, b in pairs)}. "
                  f"Use r = Σ(zx·zy)/(n - 1).")
        steps = [step("STAT_SETUP", "correlation from z products", "n=5")]
        for (a, b), product in zip(pairs, products):
            steps.append(step("ZPROD_ROW", a, b, product))
        additions, checked_total = running_sum_steps(products)
        steps.extend(additions)
        assert checked_total == total
        steps.extend([step("SUM", "z products", total),
                      step("EVAL", "n - 1", 4),
                      step("D", total, 4, num_txt(r)),
                      step("CHECK", "abs(r) ≤ 1",
                           f"abs(r)={num_txt(abs(r))}")])
        return prefix, steps, num_txt(r)

    @staticmethod
    def _properties():
        r = random.choice(R_VALUES)
        k, c, conversion = random.choice((
            (Fraction(9, 5), 32,
             "y′ = 1.8·y + 32 (Celsius to Fahrenheit)"),
            (Fraction(2, 5), 0, "y′ = 0.4·y (centimeters to inches)"),
            (100, 0, "y′ = 100·y (meters to centimeters)"),
            (Fraction(5, 9), Fraction(-160, 9),
             "y′ = 5/9·y − 160/9 (Fahrenheit to Celsius)"),
        ))
        prefix = (f"At the {_site()}, the correlation between x and y is "
                  f"r = {num_txt(r)}. Replace y by {conversion}. This is a "
                  f"positive-scale unit conversion with k = {num_txt(k)}.")
        answer = f"unchanged; r = {num_txt(r)}"
        steps = [
            step("STAT_SETUP", "correlation under unit conversion",
                 f"k={num_txt(k)}, c={num_txt(c)}"),
            step("CORR_PROPERTY", "positive rescaling and shifts",
                 "correlation unchanged"),
            step("CHECK", "k > 0", num_txt(k)),
            step("CHECK", "transformed correlation", answer),
        ]
        return prefix, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "sample_covariance":
            prefix, steps, answer = self._raw(sample=True)
        elif variant == "population_covariance":
            prefix, steps, answer = self._raw(sample=False)
        elif variant == "covariance_sign":
            prefix, steps, answer = self._raw(sample=True, sign=True)
        elif variant == "r_from_summaries":
            prefix, steps, answer = self._from_summaries()
        elif variant == "r_from_z_products":
            prefix, steps, answer = self._from_z_products()
        else:
            prefix, steps, answer = self._properties()
        problem = f"{prefix}\n{random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_covariance_correlation_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
