"""Describe scatterplots by explicit quadrant counts or residuals.

Variants: ``direction``, ``stronger_of_two``, ``identify_outlier``, and
``no_association``. Direction uses the stated mean-line rule: points whose
nonzero x and y deviations share a sign agree, a strict majority of agrees
is positive, a strict majority of disagrees is negative, and an exact half
is classified as no association. Outliers use the unique largest absolute
residual from a supplied line. Random point patterns, scales, centers,
residual patterns, sites, and four phrasings give unbounded capacity.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from stats_common import num_txt


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
QUADRANT_RULE = (
    "using x̄ and ȳ, ignore mean-line ties; a strict majority whose "
    "deviations share a sign means positive, a strict majority with "
    "opposite signs means negative, and exactly half agreeing means no "
    "association"
)
QUERIES = {
    "direction": (
        "Use the stated quadrant-count rule to describe the direction.",
        "Count sign agreements and classify this scatterplot's direction.",
        "Is the association positive or negative under the supplied rule?",
        "Report the direction together with the count that proves it.",
    ),
    "stronger_of_two": (
        "Which set has the stronger positive association by agreement fraction?",
        "Compare the two exact agreement fractions and name the stronger set.",
        "Use quadrant counts to decide which positive pattern is stronger.",
        "Report the winning set and the exact agreement-count comparison.",
    ),
    "identify_outlier": (
        "Identify the point with the largest absolute residual.",
        "Compute every residual and report the unique residual outlier.",
        "Which point lies farthest vertically from the supplied line?",
        "Find the largest absolute error and give its signed residual.",
    ),
    "no_association": (
        "Use the stated rule to verify that this has no association.",
        "Count the agreements and justify the no-association classification.",
        "Show why the quadrant-count result is exactly balanced.",
        "Report the classification and its exact half-agreeing witness.",
    ),
}


def _site():
    return f"{random.choice(LOCATIONS)} during the {random.choice(SETTINGS)}"


def _base_deviations(n):
    if n == 6:
        return [-3, -2, -1, 1, 2, 3]
    if n == 8:
        return [-4, -3, -2, -1, 1, 2, 3, 4]
    raise ValueError("scatter size must be 6 or 8")


def _points_with_agreements(n, target):
    base = _base_deviations(n)
    while True:
        y_deviations = base[:]
        random.shuffle(y_deviations)
        agreements = sum(dx * dy > 0
                         for dx, dy in zip(base, y_deviations))
        if agreements == target:
            break
    x_scale = random.randint(1, 5)
    y_scale = random.randint(1, 8)
    x_center = random.randint(25, 100)
    y_center = random.randint(40, 160)
    points = [(x_center + x_scale * dx,
               y_center + y_scale * dy)
              for dx, dy in zip(base, y_deviations)]
    random.shuffle(points)
    return points


def _points_text(points):
    return ", ".join(f"({x}, {y})" for x, y in points)


def _sign(value):
    return "+" if value > 0 else "−"


def _quadrant_steps(points, label=None):
    n = len(points)
    x_total = sum(x for x, _ in points)
    y_total = sum(y for _, y in points)
    x_mean = Fraction(x_total, n)
    y_mean = Fraction(y_total, n)
    tag = f"{label} " if label else ""
    steps = [
        step("SUM", f"{tag}x: " + " + ".join(str(x) for x, _ in points),
             x_total),
        step("MEAN_DIV", x_total, n, num_txt(x_mean)),
        step("SUM", f"{tag}y: " + " + ".join(str(y) for _, y in points),
             y_total),
        step("MEAN_DIV", y_total, n, num_txt(y_mean)),
    ]
    agreements = 0
    for x, y in points:
        dx = Fraction(x) - x_mean
        dy = Fraction(y) - y_mean
        assert dx and dy
        agrees = dx * dy > 0
        agreements += agrees
        steps.append(step("QUADRANT_ROW", f"{tag}({x}, {y})".strip(),
                          f"{_sign(dx)},{_sign(dy)}",
                          "agree" if agrees else "disagree"))
    steps.extend([
        step("COUNT", f"{tag}agree".strip(), f"{agreements}/{n}"),
        step("COUNT", f"{tag}disagree".strip(), f"{n - agreements}/{n}"),
    ])
    return steps, agreements


def _line_text(intercept, slope):
    magnitude = "x" if abs(slope) == 1 else f"{abs(slope)}x"
    sign = "+" if slope > 0 else "−"
    return f"ŷ = {intercept} {sign} {magnitude}"


class ScatterPlotDescribeGenerator(ProblemGenerator):
    """Generate exact rule-based scatterplot descriptions."""

    VARIANTS = ("direction", "stronger_of_two", "identify_outlier",
                "no_association")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _direction(no_association=False):
        if no_association:
            n, target = 8, 4
        else:
            n = random.choice((6, 8))
            if random.choice((True, False)):
                target = random.choice((n, n - 2))
            else:
                target = random.choice((0, 2))
        points = _points_with_agreements(n, target)
        prefix = (f"At the {_site()}, points are: {_points_text(points)}. "
                  f"Quadrant-count rule: {QUADRANT_RULE}.")
        steps = [step("STAT_SETUP", "scatter direction", f"n={n}"),
                 step("RULE", "direction", QUADRANT_RULE)]
        rows, agreements = _quadrant_steps(points)
        steps.extend(rows)
        if agreements > n / 2:
            answer = f"positive; {agreements} of {n} points agree in sign"
        elif agreements < n / 2:
            disagrees = n - agreements
            answer = f"negative; {disagrees} of {n} points disagree in sign"
        else:
            answer = (f"no association; {agreements} of {n} points agree "
                      f"in sign")
        steps.append(step("CHECK", "quadrant majority", answer))
        return prefix, steps, answer

    @staticmethod
    def _stronger():
        n = random.choice((6, 8))
        strong_count, weak_count = n, n - 2
        strong = _points_with_agreements(n, strong_count)
        weak = _points_with_agreements(n, weak_count)
        if random.choice((True, False)):
            sets = {"A": strong, "B": weak}
        else:
            sets = {"A": weak, "B": strong}
        prefix = (f"At the {_site()}, set A points are: "
                  f"{_points_text(sets['A'])}.\nSet B points are: "
                  f"{_points_text(sets['B'])}.\nQuadrant-count rule: "
                  f"{QUADRANT_RULE}.")
        steps = [step("STAT_SETUP", "compare scatter agreement fractions",
                      f"nA={n}, nB={n}"),
                 step("RULE", "direction", QUADRANT_RULE)]
        counts = {}
        for label in ("A", "B"):
            rows, counts[label] = _quadrant_steps(sets[label], label)
            steps.extend(rows)
            steps.append(step("D", counts[label], n,
                              num_txt(Fraction(counts[label], n))))
        winner = "A" if counts["A"] > counts["B"] else "B"
        loser = "B" if winner == "A" else "A"
        answer = (f"{winner}; agreement {counts[winner]}/{n} > "
                  f"{counts[loser]}/{n}")
        steps.extend([
            step("COMPARE", "agreement fractions",
                 f"A={counts['A']}/{n}", f"B={counts['B']}/{n}"),
            step("CHECK", "stronger positive association", answer),
        ])
        return prefix, steps, answer

    @staticmethod
    def _outlier():
        n = random.choice((6, 7, 8))
        intercept = random.randint(40, 80)
        slope = random.choice((-4, -3, -2, -1, 1, 2, 3, 4))
        residuals = [random.randint(-2, 2) for _ in range(n)]
        target = random.randrange(n)
        residuals[target] = random.choice((-1, 1)) * random.randint(7, 12)
        points = [(x, intercept + slope * x + residuals[x - 1])
                  for x in range(1, n + 1)]
        random.shuffle(points)
        line = _line_text(intercept, slope)
        prefix = (f"At the {_site()}, points are: {_points_text(points)}. "
                  f"Supplied line: {line}. Residual = observed y − predicted "
                  f"ŷ.")
        steps = [step("STAT_SETUP", "residual outlier", f"line {line}"),
                 step("RULE", "outlier", "unique largest abs(residual)")]
        computed = []
        for x, y in points:
            product = slope * x
            prediction = intercept + product
            residual = y - prediction
            steps.append(step("M", slope, x, product))
            if product >= 0:
                steps.append(step("A", intercept, product, prediction))
            else:
                steps.append(step("S", intercept, -product, prediction))
            steps.extend([
                step("S", y, prediction, residual),
                step("ABS", residual, abs(residual)),
                step("RESID_ROW", f"({x}, {y})", f"ŷ={prediction}",
                     f"residual={residual}"),
            ])
            computed.append((abs(residual), x, y, residual))
        _, x, y, residual = max(computed)
        answer = f"({x}, {y}); residual {residual}"
        steps.extend([step("MAX_ABS", f"point ({x}, {y})", abs(residual)),
                      step("CHECK", "unique residual outlier", answer)])
        return prefix, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "direction":
            prefix, steps, answer = self._direction()
        elif variant == "stronger_of_two":
            prefix, steps, answer = self._stronger()
        elif variant == "identify_outlier":
            prefix, steps, answer = self._outlier()
        else:
            prefix, steps, answer = self._direction(no_association=True)
        problem = f"{prefix}\n{random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_scatter_describe_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
