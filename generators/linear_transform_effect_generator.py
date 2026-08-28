"""Track how linear transformations change statistical summaries.

Variants: ``shift``, ``scale``, ``affine``, ``unit_conversion``, ``reverse``,
and ``which_change``. Every numeric transformation states ``y = k·x + c``
or supplies the equivalent unit conversion. Steps explicitly apply the
location rule ``k·location + c`` and spread rule ``abs(k)·spread``. The
``which_change`` variant includes both shifts and reflections, with min/max
roles reversed when ``k < 0``. Random summaries, data sets, contexts,
settings, parameters, conversion systems, and four phrasings give unbounded
capacity.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from stats_common import CONTEXTS, num_txt


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
QUERIES = {
    "shift": (
        "Find the transformed mean and standard deviation.",
        "How do the data's mean and standard deviation change?",
        "Apply the shift rule to report the new mean and sd.",
        "Calculate both summary values after every observation is shifted.",
    ),
    "scale": (
        "Find the scaled mean and standard deviation.",
        "Use the scale factor to calculate the new mean and sd.",
        "Report both summary values after the multiplication.",
        "How does this scaling change the mean and standard deviation?",
    ),
    "affine": (
        "Find the affine-transformed mean and standard deviation.",
        "Apply the affine rule to calculate the new mean and sd.",
        "Report both summary values under the stated transformation.",
        "How do the mean and standard deviation change after this mapping?",
    ),
    "unit_conversion": (
        "Find the converted mean and standard deviation, with units.",
        "Convert both summary values to the requested unit.",
        "Use the supplied conversion to report the new mean and sd.",
        "Calculate both summaries on the converted measurement scale.",
    ),
    "reverse": (
        "Find k and c.",
        "Recover both parameters of the increasing transformation.",
        "Use the two pairs of summaries to solve for k and c.",
        "Determine the positive scale factor and the shift.",
    ),
    "which_change": (
        "Which listed statistic values change, and which remain unchanged?",
        "Classify the seven summaries as changed or unchanged.",
        "Report which location and spread statistics keep their values.",
        "Compare the original and transformed summary values by name.",
    ),
}


def _signed_term(value):
    value = Fraction(value)
    sign = "+" if value >= 0 else "−"
    return sign, num_txt(abs(value))


def _transform_text(k, c, x="x", y="y"):
    coefficient = num_txt(abs(Fraction(k)))
    first = f"{coefficient}·{x}"
    if k < 0:
        first = "−" + first
    if c:
        sign, amount = _signed_term(c)
        first += f" {sign} {amount}"
    return f"{y} = {first}"


def _site():
    return f"{random.choice(LOCATIONS)} during the {random.choice(SETTINGS)}"


def _linear_value_steps(label, old, k, c):
    old = Fraction(old)
    k = Fraction(k)
    c = Fraction(c)
    product = k * old
    new = product + c
    sign, amount = _signed_term(c)
    substitution = f"{num_txt(k)}·{num_txt(old)}"
    if c:
        substitution += f" {sign} {amount}"
    steps = [step("LINEAR_EFFECT", label, "k·value + c", substitution),
             step("M", num_txt(k), num_txt(old), num_txt(product))]
    if c > 0:
        steps.append(step("A", num_txt(product), num_txt(c), num_txt(new)))
    elif c < 0:
        steps.append(step("S", num_txt(product), num_txt(-c), num_txt(new)))
    return steps, new


def _spread_steps(label, old, k):
    old = Fraction(old)
    factor = abs(Fraction(k))
    new = factor * old
    return [step("LINEAR_EFFECT", label, "abs(k)·spread",
                 f"{num_txt(factor)}·{num_txt(old)}"),
            step("M", num_txt(factor), num_txt(old), num_txt(new))], new


def _summary_problem(k, c):
    ctx = random.choice(CONTEXTS)
    mean = random.randint(ctx.lo, ctx.hi)
    sd = random.randint(1, max(1, min(12, (ctx.hi - ctx.lo) // 4)))
    transform = _transform_text(k, c)
    prefix = (f"At the {_site()}, original {ctx.label} have "
              f"mean {mean} and standard deviation {sd}. Every value is "
              f"transformed by {transform}.")
    mean_steps, new_mean = _linear_value_steps("mean", mean, k, c)
    sd_steps, new_sd = _spread_steps("sd", sd, k)
    answer = f"mean {num_txt(new_mean)}; sd {num_txt(new_sd)}"
    steps = [step("STAT_SETUP", f"linear transform of {ctx.label}",
                  f"k={num_txt(k)}, c={num_txt(c)}"),
             *mean_steps, *sd_steps,
             step("CHECK", "transformed summaries", answer)]
    return prefix, steps, answer


def _median(values):
    ordered = sorted(Fraction(value) for value in values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def _iqr_five(values):
    ordered = sorted(Fraction(value) for value in values)
    q1 = (ordered[0] + ordered[1]) / 2
    q3 = (ordered[3] + ordered[4]) / 2
    return q3 - q1


class LinearTransformEffectGenerator(ProblemGenerator):
    """Generate exact effects of ``y = kx + c`` on summary statistics."""

    VARIANTS = ("shift", "scale", "affine", "unit_conversion", "reverse",
                "which_change")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _unit_conversion():
        if random.choice((True, False)):
            mean = random.choice(tuple(range(-10, 41, 5)))
            sd = random.choice((5, 10, 15, 20))
            k, c = Fraction(9, 5), 32
            old_unit, new_unit = "°C", "°F"
            conversion = "Fahrenheit = 1.8·Celsius + 32"
        else:
            mean = random.choice(tuple(range(20, 201, 5)))
            sd = random.choice(tuple(value for value in range(5, 51, 5)
                                     if value <= mean // 3))
            k, c = Fraction(2, 5), 0
            old_unit, new_unit = "cm", "in"
            conversion = "inches = 0.4·centimeters"
        prefix = (f"At the {_site()}, measurements have mean {mean} "
                  f"{old_unit} and standard "
                  f"deviation {sd} {old_unit}. Convert every value by "
                  f"{conversion}. The supplied scale factor is "
                  f"{num_txt(k)}.")
        mean_steps, new_mean = _linear_value_steps("mean", mean, k, c)
        sd_steps, new_sd = _spread_steps("sd", sd, k)
        answer = (f"mean {num_txt(new_mean)} {new_unit}; sd "
                  f"{num_txt(new_sd)} {new_unit}")
        steps = [step("STAT_SETUP", "unit conversion",
                      f"{old_unit} to {new_unit}"),
                 step("CONV_FACTOR", old_unit, num_txt(k)),
                 *mean_steps, *sd_steps,
                 step("CHECK", "converted summaries", answer)]
        return prefix, steps, answer

    @staticmethod
    def _reverse():
        old_mean = random.randint(5, 50)
        old_sd = random.randint(2, 12)
        k = random.randint(2, 6)
        c = random.choice([value for value in range(-25, 26) if value])
        new_mean = k * old_mean + c
        new_sd = k * old_sd
        prefix = (f"At the {_site()}, an increasing transformation is "
                  f"written y = k·x + c "
                  f"with k > 0. The original "
                  f"mean is {old_mean} and sd is {old_sd}; the transformed "
                  f"mean is {new_mean} and sd is {new_sd}.")
        answer = f"k = {k}; c = {c}"
        product = k * old_mean
        steps = [
            step("STAT_SETUP", "reverse increasing transform", "k > 0"),
            step("LINEAR_EFFECT", "sd", "new sd = k·old sd",
                 f"{new_sd} = k·{old_sd}"),
            step("D", new_sd, old_sd, k),
            step("LINEAR_EFFECT", "mean", "new mean = k·old mean + c",
                 f"{new_mean} = {k}·{old_mean} + c"),
            step("M", k, old_mean, product),
            step("S", new_mean, product, c),
            step("CHECK", "substitute", f"mean {new_mean}, sd {new_sd}",
                 answer),
        ]
        return prefix, steps, answer

    @staticmethod
    def _which_change():
        ordered = sorted(random.sample(range(random.randint(0, 30),
                                             random.randint(55, 90)), 5))
        values = ordered[:]
        random.shuffle(values)
        old_mean = Fraction(sum(values), len(values))
        old_median = _median(values)
        old_min, old_max = min(values), max(values)
        old_iqr = _iqr_five(values)
        old_range = old_max - old_min
        k = random.choice((-1, 1))
        while True:
            c = random.choice([value for value in range(-30, 31) if value])
            transformed = [k * value + c for value in values]
            locations = (_median(transformed), min(transformed),
                         max(transformed), Fraction(sum(transformed), 5))
            if all(new != old for new, old in zip(
                    locations, (old_median, old_min, old_max, old_mean))):
                break
        transform = _transform_text(k, c)
        prefix = (f"At the {_site()}, data are: "
                  f"{', '.join(map(str, values))}. Every value is "
                  f"transformed by {transform}. Consider mean, median, min, "
                  f"max, sd, IQR, and range. Use median-exclusive halves "
                  f"for IQR.")
        new_mean = Fraction(sum(transformed), 5)
        new_median = _median(transformed)
        new_min, new_max = min(transformed), max(transformed)
        new_iqr = _iqr_five(transformed)
        new_range = new_max - new_min
        steps = [step("STAT_SETUP", "compare transformed summaries",
                      f"k={k}, c={c}"),
                 step("SORT", ",".join(map(str, ordered))),
                 step("RULE", "linear summaries",
                      "locations use k·value+c; spreads use abs(k)·spread")]
        for label, old, source in (
                ("mean", old_mean, old_mean),
                ("median", old_median, old_median),
                ("min", old_min, old_max if k < 0 else old_min),
                ("max", old_max, old_min if k < 0 else old_max)):
            value_steps, new = _linear_value_steps(label, source, k, c)
            steps.extend(value_steps)
            expected = {"mean": new_mean, "median": new_median,
                        "min": new_min, "max": new_max}[label]
            assert new == expected
            steps.append(step("CHANGE_ROW", label,
                              f"{num_txt(old)} to {num_txt(new)}", "changed"))
        for label, old, new in (("IQR", old_iqr, new_iqr),
                                ("range", old_range, new_range)):
            spread_steps, calculated = _spread_steps(label, old, k)
            assert calculated == new
            steps.extend(spread_steps)
            steps.append(step("CHANGE_ROW", label,
                              f"{num_txt(old)} to {num_txt(new)}",
                              "unchanged"))
        steps.extend([
            step("LINEAR_EFFECT", "sd", "abs(k)·sd", "abs(k)=1"),
            step("CHANGE_ROW", "sd", "factor 1", "unchanged"),
        ])
        answer = ("mean, median, min, max change; sd, IQR, range unchanged")
        steps.append(step("CHECK", "change classification", answer))
        return prefix, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "shift":
            c = random.choice([value for value in range(-25, 26) if value])
            prefix, steps, answer = _summary_problem(1, c)
        elif variant == "scale":
            prefix, steps, answer = _summary_problem(
                random.choice((-4, -3, -2, 2, 3, 4)), 0)
        elif variant == "affine":
            prefix, steps, answer = _summary_problem(
                random.choice((-4, -3, -2, 2, 3, 4)),
                random.choice([value for value in range(-25, 26) if value]))
        elif variant == "unit_conversion":
            prefix, steps, answer = self._unit_conversion()
        elif variant == "reverse":
            prefix, steps, answer = self._reverse()
        else:
            prefix, steps, answer = self._which_change()
        problem = f"{prefix}\n{random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_linear_transform_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
