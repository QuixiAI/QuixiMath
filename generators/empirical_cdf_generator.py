"""Exact empirical-CDF and one-sample KS calculations from small samples.

Variants: ``ecdf_value``, ``ecdf_table``, ``ecdf_quantile``, ``jump_size``,
and ``ks_distance_uniform``. Samples have n = 4..8, table answers use unique
sorted support points, quantiles use the smallest-x rule, and KS enumerates
both the before-jump and at-jump gaps against supplied ``F0(x)=x/b``.
Op-codes: ``ECDF_SETUP``, ``ECDF_ROW``, ``KS_ROW``, ``SORT``, ``COUNT``,
``RULE``, ``D``, ``CHECK``, and ``Z``.
"""
import random
from collections import Counter
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import exact, prob_txt
from stats_common import text_list


STATISTICS = True
UNIFORM_BOUNDS = (10, 20, 50)
QUANTILES = (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4),
             Fraction(4, 5))
VENUES = (
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
    "ecdf_value": (
        "Evaluate the empirical CDF at the stated x.",
        "Find the fraction of observations less than or equal to x.",
        "Compute F̂(x) from the raw sample.",
        "Report the ECDF value at the requested point.",
    ),
    "ecdf_table": (
        "Build the ECDF table at every unique sample value.",
        "Report the cumulative fractions as a text list.",
        "Compute F̂ at each jump point.",
        "List the empirical CDF's support-value rows.",
    ),
    "ecdf_quantile": (
        "Find the empirical quantile under the stated smallest-x rule.",
        "Locate the first x whose ECDF reaches the target probability.",
        "Invert F̂ at the supplied p.",
        "Report the requested empirical quantile.",
    ),
    "jump_size": (
        "Find the ECDF jump size at the stated sample value.",
        "Divide that value's multiplicity by n.",
        "Compute the height of the requested empirical-CDF jump.",
        "Report the mass attached to the stated x.",
    ),
    "ks_distance_uniform": (
        "Find the one-sample KS distance D and its smallest maximizing x.",
        "Check every before-jump and at-jump gap against F0.",
        "Compute the maximum vertical ECDF-to-uniform distance.",
        "Report D and the first jump point attaining it.",
    ),
}


def _site():
    code = f"sample {random.choice('ABCDEFGH')}{random.randint(10, 99)}"
    return (f"{random.choice(LOCATIONS)} during the "
            f"{random.choice(VENUES)} ({code})")


def _sample(bound=None):
    n = random.randint(4, 8)
    high = (bound - 1) if bound is not None else random.randint(9, 30)
    values = [random.randint(1, high) for _ in range(n)]
    return values


def _rows(values):
    counts = Counter(values)
    cumulative = 0
    rows = []
    for value in sorted(counts):
        cumulative += counts[value]
        rows.append((value, Fraction(cumulative, len(values))))
    return rows


def _base_steps(values):
    ordered = sorted(values)
    return [step("ECDF_SETUP", f"n = {len(values)}", "F̂(x) = count(X ≤ x)/n"),
            step("SORT", ", ".join(map(str, values)),
                 ", ".join(map(str, ordered)))]


class EmpiricalCDFGenerator(ProblemGenerator):
    """Generate ECDF values, tables, inverse rows, jumps, and KS distances.

    Variants are ``ecdf_value``, ``ecdf_table``, ``ecdf_quantile``,
    ``jump_size``, and ``ks_distance_uniform``. Exactness and bounds are in
    the module docstring; op-codes are ``ECDF_SETUP``, ``ECDF_ROW``,
    ``KS_ROW``, ``SORT``, ``COUNT``, ``RULE``, ``D``, ``CHECK``, and ``Z``.
    """

    VARIANTS = tuple(QUERIES)

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _result(variant, problem, steps, answer):
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_empirical_cdf_{variant}",
                "problem": problem, "steps": steps,
                "final_answer": answer}

    def _ordinary(self, variant):
        values = _sample()
        rows = _rows(values)
        sample_text = ", ".join(map(str, values))
        steps = _base_steps(values)
        detail = ""
        if variant == "ecdf_value":
            target = random.randint(0, max(values) + 2)
            count = sum(value <= target for value in values)
            answer = prob_txt(Fraction(count, len(values)))
            steps.extend([
                step("COUNT", f"values ≤ {target}", count),
                step("ECDF_ROW", target, answer),
            ])
            detail = f" Evaluate at x = {target}."
        elif variant == "ecdf_table":
            for value, cdf in rows:
                steps.append(step("ECDF_ROW", value, prob_txt(cdf)))
            answer = text_list((value, prob_txt(cdf)) for value, cdf in rows)
        elif variant == "ecdf_quantile":
            target = random.choice(QUANTILES)
            answer_value = next(value for value, cdf in rows if cdf >= target)
            steps.append(step("RULE", "empirical quantile",
                              "smallest x with F̂(x) ≥ p"))
            for value, cdf in rows:
                steps.append(step("ECDF_ROW", value, prob_txt(cdf)))
            steps.append(step("CHECK", "first row reaching p",
                              f"F̂({answer_value}) ≥ {prob_txt(target)}",
                              answer_value))
            answer = str(answer_value)
            detail = f" Use p = {prob_txt(target)}."
        else:
            target = random.choice(sorted(set(values)))
            multiplicity = values.count(target)
            jump = Fraction(multiplicity, len(values))
            answer = prob_txt(jump)
            steps.extend([
                step("COUNT", f"sample values equal {target}", multiplicity),
                step("D", multiplicity, len(values), answer),
                step("ECDF_ROW", f"jump at {target}", answer),
            ])
            detail = f" Find the jump at x = {target}."
        problem = (f"At the {_site()}, the sample is {sample_text}.{detail}\n"
                   f"{random.choice(QUERIES[variant])}")
        return self._result(variant, problem, steps, answer)

    def _ks(self):
        bound = random.choice(UNIFORM_BOUNDS)
        values = _sample(bound)
        rows = _rows(values)
        steps = _base_steps(values)
        steps.append(step("RULE", "KS tie break",
                          "evaluate before and at each jump; smallest x wins ties"))
        previous = Fraction(0)
        candidates = []
        for value, cdf in rows:
            model = Fraction(value, bound)
            before_gap = abs(previous - model)
            at_gap = abs(cdf - model)
            steps.extend([
                step("ECDF_ROW", value, prob_txt(cdf)),
                step("KS_ROW", f"x = {value}, before",
                     f"abs({prob_txt(previous)} − {exact(model)})",
                     exact(before_gap)),
                step("KS_ROW", f"x = {value}, at",
                     f"abs({prob_txt(cdf)} − {exact(model)})",
                     exact(at_gap)),
            ])
            candidates.extend(((before_gap, value), (at_gap, value)))
            previous = cdf
        distance = max(gap for gap, _ in candidates)
        location = min(value for gap, value in candidates if gap == distance)
        steps.append(step("CHECK", "max gap", exact(distance),
                          f"at x = {location}"))
        sample_text = ", ".join(map(str, values))
        problem = (f"At the {_site()}, the sample is {sample_text}. Compare "
                   f"its ECDF with the supplied uniform CDF F0(x) = x/{bound} "
                   f"on [0, {bound}]. Evaluate both the before-jump and "
                   f"at-jump gaps; if gaps tie, choose the smallest x.\n"
                   f"{random.choice(QUERIES['ks_distance_uniform'])}")
        answer = f"D = {exact(distance)} at x = {location}"
        return self._result("ks_distance_uniform", problem, steps, answer)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "ks_distance_uniform":
            return self._ks()
        return self._ordinary(variant)
