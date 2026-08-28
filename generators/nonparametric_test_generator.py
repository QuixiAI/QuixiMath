"""Exact hand-sized sign, permutation, bootstrap, and rank-sum procedures.

Variants: ``sign_test_pvalue``, ``sign_test_two_sided``,
``sign_test_decision``, ``permutation_pvalue``,
``bootstrap_percentile_ci``, and ``rank_sum_stat``. Sign tests keep n ≤ 12,
permutations enumerate all 6 or 20 labeled splits, bootstrap intervals state
the nearest-rank rule, and rank-sum samples exclude ties. Op-codes:
``SIGN_ROW``, ``COUNT``, ``BINOM_FORMULA``, ``NCR``, ``POW``, ``PERM_ROW``,
``RULE``, ``SORT``, ``CEIL``, ``PERCENTILE_PICK``, ``RANK_ROW``, ``A``,
``M``, ``CHECK``, and ``Z``.
"""
import itertools
import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import exact, prob_txt
from stats_common import nearest_rank_position


STATISTICS = True
ALPHAS = (Fraction(1, 10), Fraction(1, 20), Fraction(1, 100))
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
    "sign_test_pvalue": (
        "Find the one-sided sign-test p-value.",
        "Compute P(X ≥ the observed plus count).",
        "Use the exact Binomial(n, 1/2) upper tail.",
        "Report the reduced one-tail probability.",
    ),
    "sign_test_two_sided": (
        "Find the exact two-sided sign-test p-value.",
        "Double the smaller exact sign tail.",
        "Compute the two-tail probability from the more extreme sign count.",
        "Report the reduced two-sided p-value.",
    ),
    "sign_test_decision": (
        "Find the one-sided p-value and make the decision at the stated α.",
        "Compare the exact sign-test tail with α.",
        "Give the checkable sign-test conclusion.",
        "Decide whether the plus-sign excess is significant.",
    ),
    "permutation_pvalue": (
        "Enumerate every split and find the one-sided permutation p-value.",
        "Count reallocations whose mean difference is at least observed.",
        "Compute the exact randomization-test tail.",
        "Report the extreme-split fraction.",
    ),
    "bootstrap_percentile_ci": (
        "Use nearest ranks to find the supplied bootstrap percentile interval.",
        "Sort the 20 statistics and select the stated percentile endpoints.",
        "Apply the supplied nearest-rank rule to form the interval.",
        "Report the bootstrap percentile confidence interval.",
    ),
    "rank_sum_stat": (
        "Find the Wilcoxon rank sum W for group A.",
        "Rank the pooled tie-free observations and add A's ranks.",
        "Compute the requested rank-sum statistic.",
        "Report W for the first sample.",
    ),
}


def _site():
    code = f"case {random.choice('ABCDEFGH')}{random.randint(10, 99)}"
    return (f"{random.choice(LOCATIONS)} during the "
            f"{random.choice(VENUES)} ({code})")


def _result(variant, problem, steps, answer):
    steps.append(step("Z", answer))
    return {"problem_id": jid(),
            "operation": f"statistics_nonparametric_test_{variant}",
            "problem": problem, "steps": steps,
            "final_answer": answer}


def _sign_data(two_sided=False):
    n = random.randint(6, 12)
    minimum = n // 2 + 1
    plus = random.randint(minimum, n)
    differences = ([random.randint(1, 9) for _ in range(plus)]
                   + [-random.randint(1, 9) for _ in range(n - plus)])
    random.shuffle(differences)
    pairs = []
    for difference in differences:
        before = random.randint(20, 100)
        pairs.append((before, before + difference))
    return pairs, differences, plus


def _upper_tail(n, k):
    return sum((Fraction(math.comb(n, value), 2 ** n)
                for value in range(k, n + 1)), Fraction(0))


def _sign_steps(pairs, differences, plus, two_sided=False):
    n = len(pairs)
    extreme = max(plus, n - plus) if two_sided else plus
    terms = [(value, math.comb(n, value)) for value in range(extreme, n + 1)]
    formula = " + ".join(
        f"C({n},{value})/2^{n}" for value, _ in terms)
    steps = []
    for index, difference in enumerate(differences, 1):
        sign = "+" if difference > 0 else "-"
        steps.append(step("SIGN_ROW", f"pair {index}",
                          f"{difference:+d}", sign))
    steps.extend([
        step("COUNT", "plus signs", plus),
        step("BINOM_FORMULA", f"P(X ≥ {extreme}) = {formula}"),
    ])
    denominator = 2 ** n
    for value, coefficient in terms:
        steps.append(step("NCR", f"C({n},{value})", coefficient))
    steps.append(step("POW", f"(1/2)^{n}", f"1/{denominator}"))
    running = Fraction(terms[0][1], denominator)
    for _, coefficient in terms[1:]:
        term = Fraction(coefficient, denominator)
        steps.append(step("A", prob_txt(running), prob_txt(term),
                          prob_txt(running + term)))
        running += term
    if two_sided:
        doubled = 2 * running
        steps.append(step("M", 2, prob_txt(running), prob_txt(doubled)))
        running = doubled
    return steps, running


class NonparametricTestGenerator(ProblemGenerator):
    """Generate six exact nonparametric procedures from supplied raw data.

    Variants cover sign tests, permutation p-values, a supplied bootstrap
    percentile interval, and Wilcoxon W. Op-codes are ``SIGN_ROW``,
    ``COUNT``, ``BINOM_FORMULA``, ``NCR``, ``POW``, ``PERM_ROW``, ``RULE``,
    ``SORT``, ``CEIL``, ``PERCENTILE_PICK``, ``RANK_ROW``, ``A``, ``M``,
    ``CHECK``, and ``Z``. The module docstring records all exactness bounds.
    """

    VARIANTS = tuple(QUERIES)

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _sign(self, variant):
        two_sided = variant == "sign_test_two_sided"
        pairs, differences, plus = _sign_data(two_sided)
        steps, pvalue = _sign_steps(pairs, differences, plus, two_sided)
        alpha_clause = ""
        if variant == "sign_test_decision":
            alpha = random.choice(ALPHAS)
            reject = pvalue < alpha
            relation = "<" if reject else "≥"
            label = "reject H0" if reject else "fail to reject H0"
            alpha_clause = f" Use α = {exact(alpha)}."
            decimal = exact(pvalue)
            steps.extend([
                step("CHECK", "fraction as decimal",
                     f"{prob_txt(pvalue)} = {decimal}"),
                step("CHECK", "p vs α",
                     f"{prob_txt(pvalue)} {relation} {exact(alpha)}", label),
            ])
            answer = (f"{label} ({prob_txt(pvalue)} {relation} "
                      f"{exact(alpha)})")
        else:
            answer = prob_txt(pvalue)
        pair_text = "; ".join(f"({before}, {after})" for before, after in pairs)
        problem = (f"At the {_site()}, before/after pairs are {pair_text}. "
                   f"Under H0 each nonzero difference is + with probability "
                   f"1/2.{alpha_clause}\n{random.choice(QUERIES[variant])}")
        return _result(variant, problem, steps, answer)

    def _permutation(self):
        size = random.choice((2, 3))
        values = sorted(random.sample(range(2, 40), 2 * size))
        chosen = tuple(sorted(random.sample(range(2 * size), size)))
        group_a = tuple(values[index] for index in chosen)
        group_b = tuple(values[index] for index in range(2 * size)
                        if index not in chosen)
        if Fraction(sum(group_a), size) < Fraction(sum(group_b), size):
            group_a, group_b = group_b, group_a
        observed = Fraction(sum(group_a) - sum(group_b), size)
        rows = []
        extreme = 0
        indices = range(2 * size)
        for combination in itertools.combinations(indices, size):
            left = tuple(values[index] for index in combination)
            right = tuple(values[index] for index in indices
                          if index not in combination)
            left_mean, right_mean = (Fraction(sum(left), size),
                                     Fraction(sum(right), size))
            difference = left_mean - right_mean
            if difference >= observed:
                extreme += 1
            rows.append(step(
                "PERM_ROW", f"{{{', '.join(map(str, left))}}} vs "
                f"{{{', '.join(map(str, right))}}}",
                f"{exact(left_mean)} − {exact(right_mean)} = "
                f"{exact(difference)}"))
        total = len(rows)
        pvalue = Fraction(extreme, total)
        steps = [step("RULE", "permutation tail",
                      "count mean differences ≥ observed"), *rows,
                 step("COUNT", f"diff ≥ {exact(observed)}",
                      f"{extreme} of {total}")]
        problem = (f"At the {_site()}, a one-sided permutation test has "
                   f"group A = {', '.join(map(str, group_a))} and group B = "
                   f"{', '.join(map(str, group_b))}. The statistic is "
                   f"mean(A) − mean(B).\n"
                   f"{random.choice(QUERIES['permutation_pvalue'])}")
        return _result("permutation_pvalue", problem, steps, prob_txt(pvalue))

    def _bootstrap(self):
        center = random.randint(10, 100)
        statistics = [Fraction(center * 2 + random.randint(-16, 16), 2)
                      for _ in range(20)]
        low_pct, high_pct = random.choice(((5, 95), (10, 90), (25, 75)))
        ordered = sorted(statistics)
        low_pos = nearest_rank_position(20, low_pct)
        high_pos = nearest_rank_position(20, high_pct)
        lower, upper = ordered[low_pos - 1], ordered[high_pos - 1]
        stats_text = ", ".join(exact(value) for value in statistics)
        sorted_text = ", ".join(exact(value) for value in ordered)
        rule = "position = ceil(percent·20/100) in the sorted list"
        steps = [
            step("RULE", "nearest rank", rule),
            step("SORT", stats_text, sorted_text),
            step("CEIL", f"{low_pct}·20/100", low_pos),
            step("PERCENTILE_PICK", f"position {low_pos}", exact(lower)),
            step("CEIL", f"{high_pct}·20/100", high_pos),
            step("PERCENTILE_PICK", f"position {high_pos}", exact(upper)),
        ]
        problem = (f"At the {_site()}, 20 supplied bootstrap statistics are "
                   f"{stats_text}. Form the {low_pct}th-to-{high_pct}th "
                   f"percentile interval. Nearest-rank rule: {rule}.\n"
                   f"{random.choice(QUERIES['bootstrap_percentile_ci'])}")
        return _result("bootstrap_percentile_ci", problem, steps,
                       f"({exact(lower)}, {exact(upper)})")

    def _rank_sum(self):
        n1, n2 = random.choice(((3, 3), (3, 4), (4, 4)))
        pooled = random.sample(range(2, 60), n1 + n2)
        group_a = pooled[:n1]
        group_b = pooled[n1:]
        ordered = sorted(pooled)
        ranks = {value: rank for rank, value in enumerate(ordered, 1)}
        steps = [step("SORT", ", ".join(map(str, pooled)),
                      ", ".join(map(str, ordered)))]
        for value in ordered:
            group = "A" if value in group_a else "B"
            steps.append(step("RANK_ROW", value, ranks[value], group))
        a_ranks = [ranks[value] for value in group_a]
        running = a_ranks[0]
        for value in a_ranks[1:]:
            steps.append(step("A", running, value, running + value))
            running += value
        problem = (f"At the {_site()}, tie-free samples are group A = "
                   f"{', '.join(map(str, group_a))} and group B = "
                   f"{', '.join(map(str, group_b))}.\n"
                   f"{random.choice(QUERIES['rank_sum_stat'])}")
        return _result("rank_sum_stat", problem, steps, str(running))

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant.startswith("sign_test"):
            return self._sign(variant)
        if variant == "permutation_pvalue":
            return self._permutation()
        if variant == "bootstrap_percentile_ci":
            return self._bootstrap()
        return self._rank_sum()
