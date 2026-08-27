import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec
# Shared with the probability strand (plans/probability_plan.md §4); re-exported
# here because the tests import it from this module.
from prob_common import exact

# Upper-tail χ² critical values (α = 0.05) by degrees of freedom,
# supplied in the problem text (Principle 5).
CRIT_BY_DF = {
    1: "3.841", 2: "5.991", 3: "7.815", 4: "9.488",
    5: "11.070", 6: "12.592",
}
# Expected counts per category for the uniform goodness-of-fit case;
# each divides a power of 10 so every χ² term is an exact decimal.
GOF_EXPECTED = [5, 10, 20, 25, 50, 100]

CATEGORY_BANKS = [
    ["red", "blue", "green", "yellow", "purple", "orange", "white"],
    ["north", "south", "east", "west", "central", "coastal", "inland"],
    ["apple", "banana", "cherry", "grape", "mango", "pear", "plum"],
    ["bus", "car", "bike", "walk", "train", "tram", "ferry"],
    ["bronze", "silver", "gold", "black", "white", "copper", "blue"],
    ["A", "B", "C", "D", "E", "F", "G"],
]

TABLE_LABELS = [
    ("treatment", "control", "improved", "not improved"),
    ("morning", "evening", "yes", "no"),
    ("urban", "rural", "supports", "opposes"),
    ("online", "in person", "passed", "did not pass"),
    ("new design", "old design", "clicked", "did not click"),
    ("group A", "group B", "selected", "not selected"),
    ("before noon", "after noon", "on time", "late"),
    ("method one", "method two", "success", "failure"),
]

NAMES = [
    "Aisha", "Ben", "Cleo", "Diego", "Emi", "Farah", "Grace", "Hugo",
    "Imani", "Jonas", "Kavya", "Liam", "Maya", "Noah", "Omar", "Priya",
    "Quinn", "Rosa", "Samir", "Tara", "Uma", "Vera", "Wes", "Ximena",
]
SETTINGS = [
    "statistics class", "the survey lab", "study hall", "the library",
    "a research workshop", "the school office", "a quality-control meeting",
    "the learning center", "a classroom review", "an online lesson",
    "the community center", "a data-analysis seminar",
]
PROBLEM_TEMPLATES = [
    "At {place}, {name} analyzes this study. {data} {ask}",
    "{name} is working in {place}. {data} {ask}",
    "During {place}, {name} receives the following summary: {data} {ask}",
    "A worksheet for {name} at {place} gives this information. {data} {ask}",
    "For a report in {place}, {name} must analyze these data. {data} {ask}",
    "{name} checks a result during {place}. {data} {ask}",
]


def sq_txt(d):
    """(d)^2 rendered with parentheses around a negative base."""
    return f"({d})^2 = {d * d}" if d < 0 else f"{d}^2 = {d * d}"


class ChiSquareGenerator(ProblemGenerator):
    """
    Chi-square tests worked cell by cell: a goodness-of-fit test
    against a uniform model, and a 2×2 test of independence with an
    expected-count table. Data are built so every expected count and
    every χ² contribution is exact; the critical value is supplied in
    the problem (Principle 5).

    Variants:
    - gof_stat:       the χ² statistic for goodness of fit
    - gof_decision:   χ², then reject / fail to reject
    - independence_stat:     the χ² statistic for a 2×2 table
    - independence_decision: χ², then reject / fail to reject

    Op-codes used:
    - CHI_SETUP: observed/expected (or the table) and the goal
    - CHI_FORMULA: the χ² definition
    - EXP_CELL: one expected count = (row·col)/N
    - CHI_TERM: one contribution (O-E, (O-E)², (O-E)²/E)
    - A (established): running sum of the contributions
    - CHECK (established): χ² vs the critical value
    - Z: the statistic, or "reject H0" / "fail to reject H0"
    """

    VARIANTS = ["gof_stat", "gof_decision", "independence_stat",
                "independence_decision"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _decision_step(chi, crit):
        reject = chi > crit
        rel = ">" if reject else "≤"
        comparison = f"{exact(chi)} {rel} {dec(crit)}"
        head = "reject H0" if reject else "fail to reject H0"
        # composite verdict: the bare label would be a gradable coin flip
        verdict = f"{head} ({comparison})"
        return step("CHECK", "χ² vs critical value", comparison, head), verdict

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant.startswith("gof"):
            return self._generate_gof(variant)
        return self._generate_independence(variant)

    @staticmethod
    def _phrase(data, ask):
        return random.choice(PROBLEM_TEMPLATES).format(
            name=random.choice(NAMES), place=random.choice(SETTINGS),
            data=data, ask=ask)

    @staticmethod
    def _sum_terms(steps, terms):
        running = terms[0]
        for term in terms[1:]:
            steps.append(step("A", exact(running), exact(term),
                              exact(running + term)))
            running += term

    def _finish(self, variant, problem, steps, chi, crit):
        if variant.endswith("decision"):
            decision, answer = self._decision_step(chi, crit)
            steps.append(decision)
        else:
            answer = exact(chi)
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(), operation=f"chi_square_{variant}",
            problem=problem, steps=steps, final_answer=answer)

    def _generate_gof(self, variant):
        k = random.randint(3, 7)
        expected = random.choice(GOF_EXPECTED)
        df = k - 1
        crit = Fraction(CRIT_BY_DF[df])
        limit = min(8, expected - 1)
        while True:
            deviations = [random.randint(-limit, limit) for _ in range(k - 1)]
            deviations.append(-sum(deviations))
            observed = [expected + d for d in deviations]
            if (all(value > 0 for value in observed)
                    and abs(deviations[-1]) <= limit
                    and any(deviations)):
                break
        labels = random.sample(random.choice(CATEGORY_BANKS), k)
        labelled = ", ".join(f"{label}={count}"
                             for label, count in zip(labels, observed))
        data = ("Goodness-of-fit data [observed counts by category: "
                f"{labelled}; each expected count is {expected}; critical "
                f"value of {dec(crit)} (df = {df})].")
        ask = ("Find the χ² test statistic."
               if variant == "gof_stat"
               else "State the conclusion: reject H0 or fail to reject H0.")
        problem = self._phrase(data, ask)
        steps = [
            step("CHI_SETUP", f"observed: {', '.join(map(str, observed))}; "
                 f"expected: {expected} each",
                 f"goodness of fit; df = {df}, critical value = {dec(crit)}"),
            step("CHI_FORMULA", "χ² = Σ (O - E)^2/E"),
        ]
        terms = []
        for value, difference in zip(observed, deviations):
            term = Fraction(difference * difference, expected)
            terms.append(term)
            steps.append(step("CHI_TERM",
                              f"{value} - {expected} = {difference}",
                              sq_txt(difference),
                              f"{difference * difference}/{expected} = "
                              f"{exact(term)}"))
        self._sum_terms(steps, terms)
        chi = sum(terms, Fraction(0))
        return self._finish(variant, problem, steps, chi, crit)

    def _generate_independence(self, variant):
        crit = Fraction(CRIT_BY_DF[1])
        total = random.choice([100, 200, 300, 400])
        row_tenths = random.randint(2, 8)
        col_tenths = random.randint(2, 8)
        row1 = total * row_tenths // 10
        row2 = total - row1
        col1 = total * col_tenths // 10
        col2 = total - col1
        expected = [Fraction(row1 * col1, total),
                    Fraction(row1 * col2, total),
                    Fraction(row2 * col1, total),
                    Fraction(row2 * col2, total)]
        limit = min(12, *(int(value) - 1 for value in expected))
        delta = random.choice([d for d in range(-limit, limit + 1)
                               if d != 0])
        observed = [int(expected[0]) + delta, int(expected[1]) - delta,
                    int(expected[2]) - delta, int(expected[3]) + delta]
        r1, r2, c1, c2 = random.choice(TABLE_LABELS)
        data = (f"Independence table data [rows {r1}, {r2}; columns {c1}, "
                f"{c2}; counts: {observed[0]}, {observed[1]}; "
                f"{observed[2]}, {observed[3]}; N = {total}; critical value "
                f"of {dec(crit)} (df = 1)].")
        ask = ("Find the χ² test statistic."
               if variant == "independence_stat"
               else "State the conclusion: reject H0 or fail to reject H0.")
        problem = self._phrase(data, ask)
        margins = [(row1, col1), (row1, col2),
                   (row2, col1), (row2, col2)]
        steps = [
            step("CHI_SETUP",
                 f"row 1: {observed[0]}, {observed[1]}; row 2: "
                 f"{observed[2]}, {observed[3]}; N = {total}",
                 f"independence; df = 1, critical value = {dec(crit)}"),
            step("CHI_FORMULA", "E = (row·col)/N; χ² = Σ (O - E)^2/E"),
        ]
        for value, (row, column) in zip(expected, margins):
            steps.append(step("EXP_CELL", f"({row}·{column})/{total}",
                              exact(value)))
        terms = []
        for observed_value, expected_value in zip(observed, expected):
            difference = observed_value - expected_value
            term = Fraction(difference * difference) / expected_value
            terms.append(term)
            difference = int(difference)
            steps.append(step("CHI_TERM",
                              f"{observed_value} - {exact(expected_value)} = "
                              f"{difference}", sq_txt(difference),
                              f"{difference * difference}/"
                              f"{exact(expected_value)} = {exact(term)}"))
        self._sum_terms(steps, terms)
        chi = sum(terms, Fraction(0))
        return self._finish(variant, problem, steps, chi, crit)
