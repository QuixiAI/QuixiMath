"""Exact goodness-of-fit, contingency-table, and homogeneity procedures."""
import hashlib
import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec
# Shared with the probability strand (plans/probability_plan.md §4); re-exported
# here because the tests import it from this module.
from prob_common import exact
from stats_common import text_list

# Upper-tail χ² critical values (α = 0.05) by degrees of freedom,
# supplied in the problem text (Principle 5).
CRIT_BY_DF = {
    1: "3.841", 2: "5.991", 3: "7.815", 4: "9.488",
    5: "11.070", 6: "12.592",
}
CRIT_BY_ALPHA = {
    "0.10": {
        1: "2.706", 2: "4.605", 3: "6.251", 4: "7.779",
        5: "9.236", 6: "10.645",
    },
    "0.05": CRIT_BY_DF,
    "0.01": {
        1: "6.635", 2: "9.210", 3: "11.345", 4: "13.277",
        5: "15.086", 6: "16.812",
    },
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

NONUNIFORM_MODELS = (
    (Fraction(1, 2), Fraction(3, 10), Fraction(1, 5)),
    (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)),
    (Fraction(2, 5), Fraction(3, 10), Fraction(1, 5), Fraction(1, 10)),
    (Fraction(2, 5), Fraction(1, 5), Fraction(1, 5),
     Fraction(1, 10), Fraction(1, 10)),
    (Fraction(1, 4), Fraction(1, 4), Fraction(1, 5),
     Fraction(1, 5), Fraction(1, 10)),
)
MODEL_TOTALS = (20, 40, 50, 100, 200)
SHAPES = ((2, 3), (3, 2), (3, 3))
MARGIN_BANK = {
    2: ((20, 80), (30, 70), (40, 60), (50, 50)),
    3: ((10, 40, 50), (20, 30, 50), (20, 40, 40), (30, 30, 40)),
}
ROW_LABEL_BANK = (
    ("program A", "program B", "program C"),
    ("north site", "central site", "south site"),
    ("morning", "afternoon", "evening"),
    ("population 1", "population 2", "population 3"),
)
COL_LABEL_BANK = (
    ("low", "medium", "high"),
    ("yes", "no", "undecided"),
    ("category A", "category B", "category C"),
    ("first", "second", "third"),
)
LEGACY_VARIANTS = ("gof_stat", "gof_decision", "independence_stat",
                   "independence_decision")
EXTENSION_VARIANTS = ("gof_nonuniform", "expected_table", "rxc_stat",
                      "rxc_decision", "homogeneity", "df_from_shape")
STATISTICS = True


def sq_txt(d):
    """(d)^2 rendered with parentheses around a negative base."""
    return f"({d})^2 = {d * d}" if d < 0 else f"{d}^2 = {d * d}"


class ChiSquareGenerator(ProblemGenerator):
    """
    Chi-square procedures worked cell by cell: uniform and nonuniform
    goodness of fit, 2×2 and r×c independence, expected-count tables,
    homogeneity, and degrees of freedom from shape. Integer margins and
    zero-sum perturbations make every expected count and χ² contribution
    exact; each required critical value is supplied in the problem.

    Variants:
    - gof_stat:       the χ² statistic for goodness of fit
    - gof_decision:   χ², then reject / fail to reject
    - independence_stat:     the χ² statistic for a 2×2 table
    - independence_decision: χ², then reject / fail to reject
    - gof_nonuniform: goodness of fit to supplied nonuniform proportions
    - expected_table: compute every expected count of an r×c table
    - rxc_stat / rxc_decision: 2×3, 3×2, or 3×3 independence tests
    - homogeneity: compare category distributions across populations
    - df_from_shape: compute contingency-table degrees of freedom

    Op-codes used:
    - CHI_SETUP: observed/expected (or the table) and the goal
    - CHI_FORMULA: the χ² definition
    - CHI_DF: (rows - 1)(columns - 1) and its value
    - EXP_CELL: one labeled expected count = (row·col)/N
    - CHI_TERM: one contribution (O-E, (O-E)², (O-E)²/E)
    - M / A (established): expected-count products and running sums
    - CHECK (established): χ² vs the critical value
    - Z: statistic, expected table, df composite, or checkable verdict
    """

    VARIANTS = [*LEGACY_VARIANTS, *EXTENSION_VARIANTS]

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
        if self.variant is not None:
            return self._generate_variant(self.variant)

        # Preserve the exact post-call RNG state of the four-variant legacy
        # generator while expanding its output distribution deterministically.
        legacy_variant = random.choice(LEGACY_VARIANTS)
        legacy = self._generate_variant(legacy_variant)
        post_legacy_state = random.getstate()
        digest = hashlib.sha256(
            legacy["problem"].encode("utf-8")
            + repr(post_legacy_state).encode("ascii")
        ).digest()
        random.seed(int.from_bytes(digest[1:9], "big"))
        try:
            return self._generate_variant(
                self.VARIANTS[digest[0] % len(self.VARIANTS)])
        finally:
            random.setstate(post_legacy_state)

    def _generate_variant(self, variant):
        if variant.startswith("gof"):
            if variant == "gof_nonuniform":
                return self._generate_gof_nonuniform()
            return self._generate_gof(variant)
        if variant.startswith("independence"):
            return self._generate_independence(variant)
        if variant == "df_from_shape":
            return self._generate_df_from_shape()
        return self._generate_matrix_variant(variant)

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

    @staticmethod
    def _critical(df):
        alpha = random.choice(tuple(CRIT_BY_ALPHA))
        text = CRIT_BY_ALPHA[alpha][df]
        return alpha, text, Fraction(text)

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

    def _generate_gof_nonuniform(self):
        model = random.choice(NONUNIFORM_MODELS)
        compatible_totals = [
            total for total in MODEL_TOTALS
            if all((total * probability).denominator == 1
                   for probability in model)
        ]
        total = random.choice(compatible_totals)
        expected = [int(total * probability) for probability in model]
        first, second = random.sample(range(len(model)), 2)
        limit = min(8, expected[first] - 1, expected[second] - 1)
        delta = random.choice([value for value in range(-limit, limit + 1)
                               if value])
        deviations = [0] * len(model)
        deviations[first], deviations[second] = delta, -delta
        observed = [value + change
                    for value, change in zip(expected, deviations)]
        labels = random.sample(random.choice(CATEGORY_BANKS), len(model))
        model_text = ", ".join(
            f"{label}={exact(probability)}"
            for label, probability in zip(labels, model)
        )
        observed_text = ", ".join(
            f"{label}={count}" for label, count in zip(labels, observed)
        )
        df = len(model) - 1
        alpha, crit_text, crit = self._critical(df)
        data = (f"Nonuniform goodness-of-fit data [model proportions: "
                f"{model_text}; observed counts: {observed_text}; N = {total}; "
                f"χ² critical value of {crit_text} (df = {df}, "
                f"α = {alpha})].")
        problem = self._phrase(data, "Find the χ² test statistic.")
        steps = [
            step("CHI_SETUP", f"model: {model_text}; observed: {observed_text}",
                 f"N = {total}, df = {df}, α = {alpha}, critical = {crit_text}"),
            step("CHI_FORMULA", "E = N·p; χ² = Σ (O - E)^2/E"),
        ]
        for probability, value in zip(model, expected):
            steps.append(step("M", total, exact(probability), value))
        terms = []
        for label, obs, exp, difference in zip(
                labels, observed, expected, deviations):
            term = Fraction(difference * difference, exp)
            terms.append(term)
            steps.append(step(
                "CHI_TERM", f"{label}: {obs} - {exp} = {difference}",
                sq_txt(difference),
                f"{difference * difference}/{exp} = {exact(term)}"))
        self._sum_terms(steps, terms)
        return self._finish("gof_nonuniform", problem, steps,
                            sum(terms, Fraction(0)), crit)

    @staticmethod
    def _matrix_case():
        rows, columns = random.choice(SHAPES)
        row_totals = list(random.choice(MARGIN_BANK[rows]))
        column_totals = list(random.choice(MARGIN_BANK[columns]))
        random.shuffle(row_totals)
        random.shuffle(column_totals)
        expected = [[row * column // 100 for column in column_totals]
                    for row in row_totals]
        while True:
            r1, r2 = random.sample(range(rows), 2)
            c1, c2 = random.sample(range(columns), 2)
            limit = min(12, expected[r1][c1] - 1,
                        expected[r1][c2] - 1,
                        expected[r2][c1] - 1,
                        expected[r2][c2] - 1)
            if limit >= 1:
                break
        delta = random.choice([value for value in range(-limit, limit + 1)
                               if value])
        observed = [row[:] for row in expected]
        observed[r1][c1] += delta
        observed[r1][c2] -= delta
        observed[r2][c1] -= delta
        observed[r2][c2] += delta
        return rows, columns, row_totals, column_totals, expected, observed

    @staticmethod
    def _matrix_text(matrix):
        return " / ".join(", ".join(map(str, row)) for row in matrix)

    def _matrix_problem(self, variant, rows, columns, observed, df,
                        alpha, crit_text):
        row_labels = random.sample(random.choice(ROW_LABEL_BANK), rows)
        column_labels = random.sample(random.choice(COL_LABEL_BANK), columns)
        if variant == "homogeneity":
            lead = "Homogeneity data for populations using the same categories"
            ask = ("Test whether the populations have the same category "
                   "distribution; report χ², df, and the conclusion.")
        else:
            lead = "Contingency data"
            ask = {
                "expected_table": "Find the expected-count table.",
                "rxc_stat": "Find the χ² test statistic.",
                "rxc_decision": ("State the conclusion: reject H0 or fail "
                                  "to reject H0."),
            }[variant]
        data = (f"{lead} [shape {rows}x{columns}; row labels: "
                f"{', '.join(row_labels)}; column labels: "
                f"{', '.join(column_labels)}; counts by row: "
                f"{self._matrix_text(observed)}; N = 100; χ² critical "
                f"value of {crit_text} (df = {df}, α = {alpha})].")
        return self._phrase(data, ask)

    @staticmethod
    def _matrix_base_steps(kind, rows, columns, observed, row_totals,
                           column_totals, expected, df, alpha, crit_text):
        steps = [
            step("CHI_SETUP", f"observed rows: {ChiSquareGenerator._matrix_text(observed)}",
                 f"{kind}; shape {rows}x{columns}; df = {df}; α = {alpha}; "
                 f"critical = {crit_text}"),
            step("CHI_DF", f"df = ({rows} - 1)({columns} - 1)", df),
            step("CHI_FORMULA", "E = (row·column)/N; χ² = Σ (O - E)^2/E"),
        ]
        for i in range(rows):
            for j in range(columns):
                steps.append(step(
                    "EXP_CELL", f"r{i + 1}c{j + 1}",
                    f"({row_totals[i]}·{column_totals[j]})/100",
                    expected[i][j]))
        return steps

    def _generate_matrix_variant(self, variant):
        (rows, columns, row_totals, column_totals,
         expected, observed) = self._matrix_case()
        df = (rows - 1) * (columns - 1)
        alpha, crit_text, crit = self._critical(df)
        kind = "homogeneity" if variant == "homogeneity" else "independence"
        problem = self._matrix_problem(
            variant, rows, columns, observed, df, alpha, crit_text)
        steps = self._matrix_base_steps(
            kind, rows, columns, observed, row_totals, column_totals,
            expected, df, alpha, crit_text)
        if variant == "expected_table":
            answer = text_list(
                (f"r{i + 1}c{j + 1}", expected[i][j])
                for i in range(rows) for j in range(columns)
            )
            steps.append(step("Z", answer))
            return dict(problem_id=jid(), operation="chi_square_expected_table",
                        problem=problem, steps=steps, final_answer=answer)

        terms = []
        for i in range(rows):
            for j in range(columns):
                difference = observed[i][j] - expected[i][j]
                term = Fraction(difference * difference, expected[i][j])
                terms.append(term)
                steps.append(step(
                    "CHI_TERM",
                    f"r{i + 1}c{j + 1}: {observed[i][j]} - "
                    f"{expected[i][j]} = {difference}",
                    sq_txt(difference),
                    f"{difference * difference}/{expected[i][j]} = "
                    f"{exact(term)}"))
        self._sum_terms(steps, terms)
        chi = sum(terms, Fraction(0))
        if variant == "homogeneity":
            decision, verdict = self._decision_step(chi, crit)
            steps.append(decision)
            answer = f"χ² = {exact(chi)}; df = {df}; {verdict}"
            steps.append(step("Z", answer))
            return dict(problem_id=jid(), operation="chi_square_homogeneity",
                        problem=problem, steps=steps, final_answer=answer)
        return self._finish(variant, problem, steps, chi, crit)

    def _generate_df_from_shape(self):
        rows, columns = random.choice(SHAPES)
        df = (rows - 1) * (columns - 1)
        alpha, crit_text, _ = self._critical(df)
        data = (f"A contingency table has shape {rows}x{columns}. Its χ² "
                f"critical value of {crit_text} is supplied for df = {df} "
                f"and α = {alpha}.")
        problem = self._phrase(
            data, "Compute the degrees of freedom from the table shape.")
        steps = [
            step("CHI_SETUP", f"shape {rows}x{columns}",
                 f"critical = {crit_text}, α = {alpha}"),
            step("CHI_DF", f"df = ({rows} - 1)({columns} - 1)", df),
            step("M", rows - 1, columns - 1, df),
        ]
        answer = f"df = {df}; ({rows} - 1)({columns} - 1)"
        steps.append(step("Z", answer))
        return dict(problem_id=jid(), operation="chi_square_df_from_shape",
                    problem=problem, steps=steps, final_answer=answer)
