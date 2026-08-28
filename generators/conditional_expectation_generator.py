"""Compute conditional moments and verify tower identities exactly.

Variants: ``from_table``, ``tower_check``, ``two_stage_experiment``,
``conditional_variance``, ``random_sum_mean``, ``random_sum_variance``, and
``total_variance_check``. Op-codes: ``JOINT_ROW``, ``MARGINAL``,
``COND_FORMULA``, ``COND_EXP``, ``COND_VAR``, ``TOWER``, ``TOTAL_VARIANCE``,
``M``, ``A``, ``S``, ``D``, ``E``, ``CHECK``, and ``Z``. Positive dyadic
tables and small Bernoulli product spaces make every result exact and fully
enumerable by the independent oracle.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt


PROBABILITY = True
VENUES = ("amber study", "birch survey", "cedar trial", "delta project",
          "ember lab", "forest audit", "granite program", "harbor test",
          "indigo review", "jade pilot", "kestrel study", "lunar trial",
          "maple project", "nova lab", "onyx survey", "pearl audit",
          "quartz program", "river test", "solar review", "topaz pilot",
          "umber study", "violet trial", "willow project", "zephyr lab")
CITIES = ("Albany", "Boston", "Cedarville", "Dover", "Erie", "Fresno",
          "Galveston", "Hartford", "Ithaca", "Juneau", "Kingston", "Lowell",
          "Madison", "Norfolk", "Olympia", "Portland", "Quincy", "Raleigh",
          "Salem", "Trenton", "Utica", "Ventura", "Wichita", "Yonkers")
NAMES = ("Aiko", "Ben", "Chidi", "Daria", "Elena", "Farah", "Gita", "Hugo",
         "Imani", "Jae", "Kira", "Luca", "Mina", "Noah", "Omar", "Priya",
         "Quinn", "Ravi", "Sofia", "Tariq", "Uma", "Vera", "Wen", "Zola")
P_BANK = (Fraction(1, 4), Fraction(1, 3), Fraction(2, 5), Fraction(1, 2),
          Fraction(3, 5), Fraction(2, 3), Fraction(3, 4))
QUERIES = {
    "from_table": (
        "Find the requested conditional expectation.",
        "Renormalize the stated Y-slice and compute its mean.",
        "Use the joint table to determine E[X given Y].",
        "What is the exact conditional mean for the target Y value?",
        "Divide the slice's weighted X sum by its marginal probability.",
    ),
    "tower_check": (
        "Find both conditional means and verify the tower property.",
        "Compute E[E[X given Y]] and compare it with direct E[X].",
        "Use both Y-slices to reconstruct the overall expectation.",
        "What conditional means make the tower identity hold?",
        "Renormalize each slice, then average those conditional expectations.",
    ),
    "two_stage_experiment": (
        "Find the expected number of heads.",
        "Condition on the die result and apply the tower property.",
        "Average the conditional head count over every die face.",
        "What is E[H] in this two-stage experiment?",
        "Use E[H given N=n] before averaging over N.",
    ),
    "conditional_variance": (
        "Find the conditional mean and variance for the target Y value.",
        "Renormalize the slice and compute its first two central moments.",
        "Use the joint table to determine Var(X given Y).",
        "What are E[X given Y] and Var(X given Y) for this slice?",
        "Compute the weighted squared deviations inside the conditioned row.",
    ),
    "random_sum_mean": (
        "Find E[S] for the random sum.",
        "Use E[S] = E[N]E[B].",
        "Condition on N and average the Bernoulli-sum means.",
        "What is the exact expected random-sum total?",
        "Apply the random-sum mean identity to the printed pmf.",
    ),
    "random_sum_variance": (
        "Find Var(S) for the random sum.",
        "Use E[N]Var(B) + Var(N)(E[B])².",
        "Combine count uncertainty with Bernoulli increment uncertainty.",
        "What is the exact variance of the random sum?",
        "Apply the random-sum variance identity to the printed pmf.",
    ),
    "total_variance_check": (
        "Verify the law of total variance from the joint table.",
        "Compute both terms in Var(X)=E[Var(X given Y)]+Var(E[X given Y]).",
        "Use the two Y-slices to reconstruct the unconditional variance.",
        "What are the within-slice and between-slice variance terms?",
        "Check that the conditional variance decomposition equals Var(X).",
    ),
}


def _setting():
    return random.choice(VENUES), random.choice(CITIES), random.choice(NAMES)


def _dyadic_weights(count):
    total = 2 ** random.randint(4, 8)
    cuts = sorted(random.sample(range(1, total), count - 1))
    amounts = [cuts[0]]
    amounts.extend(cuts[index] - cuts[index - 1]
                   for index in range(1, len(cuts)))
    amounts.append(total - cuts[-1])
    return tuple(Fraction(amount, total) for amount in amounts)


def _joint_data():
    x_values = tuple(sorted(random.sample(range(-6, 10), 2)))
    weights = _dyadic_weights(4)
    rows = [(x, y, weights[2 * y + index])
            for y in (0, 1) for index, x in enumerate(x_values)]
    return x_values, rows


def _joint_text(rows):
    return "; ".join(f"P(X={x},Y={y})={prob_txt(p)}" for x, y, p in rows)


def _sum_steps(steps, values):
    running = values[0]
    for value in values[1:]:
        steps.append(step("A", prob_txt(running), prob_txt(value),
                          prob_txt(running + value)))
        running += value
    return running


def _conditional(rows, y_value):
    selected = [(x, p) for x, y, p in rows if y == y_value]
    marginal = sum((p for _, p in selected), Fraction())
    numerator = sum((x * p for x, p in selected), Fraction())
    mean = numerator / marginal
    variance_numerator = sum(((Fraction(x) - mean) ** 2 * p
                              for x, p in selected), Fraction())
    return marginal, numerator, mean, variance_numerator / marginal


def _conditional_steps(rows, y_value, include_variance=False):
    selected = [(x, p) for x, y, p in rows if y == y_value]
    steps = []
    probabilities = [p for _, p in selected]
    marginal = _sum_steps(steps, probabilities)
    steps.append(step("MARGINAL", f"P(Y={y_value})",
                      " + ".join(prob_txt(p) for p in probabilities),
                      prob_txt(marginal)))
    products = []
    for x, probability in selected:
        term = x * probability
        steps.append(step("M", x, prob_txt(probability), prob_txt(term)))
        products.append(term)
    numerator = _sum_steps(steps, products)
    mean = numerator / marginal
    steps.extend([step("COND_FORMULA", "E[X given Y=y] = Σ xP(x,y)/P(Y=y)"),
                  step("D", prob_txt(numerator), prob_txt(marginal), prob_txt(mean)),
                  step("COND_EXP", f"E[X given Y={y_value}]", prob_txt(mean))])
    variance = None
    if include_variance:
        terms = []
        for x, probability in selected:
            difference = Fraction(x) - mean
            square = difference ** 2
            weighted = square * probability
            steps.extend([step("S", x, prob_txt(mean), prob_txt(difference)),
                          step("E", prob_txt(difference), 2, prob_txt(square)),
                          step("M", prob_txt(square), prob_txt(probability),
                               prob_txt(weighted))])
            terms.append(weighted)
        numerator_var = _sum_steps(steps, terms)
        variance = numerator_var / marginal
        steps.extend([step("D", prob_txt(numerator_var), prob_txt(marginal),
                           prob_txt(variance)),
                      step("COND_VAR", f"Var(X given Y={y_value})",
                           prob_txt(variance))])
    return steps, marginal, mean, variance


def _n_distribution():
    weights = _dyadic_weights(4)
    return tuple((n, weights[n]) for n in range(4))


def _n_text(rows):
    return "; ".join(f"P(N={n})={prob_txt(p)}" for n, p in rows)


def _n_moments_steps(rows):
    steps = []
    mean_terms, second_terms = [], []
    for n, probability in rows:
        mean_term = n * probability
        second_term = n * n * probability
        steps.extend([step("M", n, prob_txt(probability), prob_txt(mean_term)),
                      step("M", n * n, prob_txt(probability),
                           prob_txt(second_term))])
        mean_terms.append(mean_term)
        second_terms.append(second_term)
    mean = _sum_steps(steps, mean_terms)
    second = _sum_steps(steps, second_terms)
    mean_square = mean ** 2
    variance = second - mean_square
    steps.extend([step("E", prob_txt(mean), 2, prob_txt(mean_square)),
                  step("S", prob_txt(second), prob_txt(mean_square),
                       prob_txt(variance))])
    return steps, mean, variance


class ConditionalExpectationGenerator(ProblemGenerator):
    """Generate exact conditional-expectation and variance decompositions."""

    VARIANTS = ("from_table", "tower_check", "two_stage_experiment",
                "conditional_variance", "random_sum_mean",
                "random_sum_variance", "total_variance_check")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _table_variant(variant):
        _, rows = _joint_data()
        venue, city, name = _setting()
        target_y = random.choice((0, 1))
        prefix = f"At the {venue} in {city}, {name} has joint pmf: {_joint_text(rows)}."
        steps = [step("JOINT_ROW", f"x={x}, y={y}", prob_txt(p))
                 for x, y, p in rows]
        if variant == "from_table":
            extra, _, mean, _ = _conditional_steps(rows, target_y)
            steps.extend(extra)
            prefix += f" Target: E[X given Y={target_y}]."
            answer = f"E[X given Y={target_y}] = {prob_txt(mean)}"
        elif variant == "conditional_variance":
            extra, _, mean, variance = _conditional_steps(rows, target_y, True)
            steps.extend(extra)
            prefix += f" Target: conditional moments given Y={target_y}."
            answer = (f"E[X given Y={target_y}] = {prob_txt(mean)}; "
                      f"Var(X given Y={target_y}) = {prob_txt(variance)}")
        else:
            first_steps, p0, mean0, var0 = _conditional_steps(
                rows, 0, variant == "total_variance_check")
            second_steps, p1, mean1, var1 = _conditional_steps(
                rows, 1, variant == "total_variance_check")
            steps.extend(first_steps + second_steps)
            direct_mean = sum((x * p for x, _, p in rows), Fraction())
            weighted0, weighted1 = p0 * mean0, p1 * mean1
            tower_mean = weighted0 + weighted1
            steps.extend([step("M", prob_txt(p0), prob_txt(mean0), prob_txt(weighted0)),
                          step("M", prob_txt(p1), prob_txt(mean1), prob_txt(weighted1)),
                          step("A", prob_txt(weighted0), prob_txt(weighted1),
                               prob_txt(tower_mean)),
                          step("TOWER", "E[X] = Σ P(Y=y)E[X given Y=y]",
                               prob_txt(tower_mean)),
                          step("CHECK", "direct E[X]", prob_txt(direct_mean))])
            if variant == "tower_check":
                prefix += " Target: conditional means and tower check."
                answer = (f"E[X given Y=0] = {prob_txt(mean0)}; "
                          f"E[X given Y=1] = {prob_txt(mean1)}; "
                          f"E[X] = {prob_txt(tower_mean)}")
            else:
                overall_second = sum((x * x * p for x, _, p in rows), Fraction())
                overall_var = overall_second - direct_mean ** 2
                within0, within1 = p0 * var0, p1 * var1
                within = within0 + within1
                between0 = p0 * (mean0 - direct_mean) ** 2
                between1 = p1 * (mean1 - direct_mean) ** 2
                between = between0 + between1
                steps.extend([
                    step("M", prob_txt(p0), prob_txt(var0), prob_txt(within0)),
                    step("M", prob_txt(p1), prob_txt(var1), prob_txt(within1)),
                    step("A", prob_txt(within0), prob_txt(within1), prob_txt(within)),
                    step("M", prob_txt(p0), prob_txt((mean0 - direct_mean) ** 2),
                         prob_txt(between0)),
                    step("M", prob_txt(p1), prob_txt((mean1 - direct_mean) ** 2),
                         prob_txt(between1)),
                    step("A", prob_txt(between0), prob_txt(between1),
                         prob_txt(between)),
                    step("A", prob_txt(within), prob_txt(between),
                         prob_txt(within + between)),
                    step("TOTAL_VARIANCE",
                         "Var(X) = E[Var(X given Y)] + Var(E[X given Y])",
                         prob_txt(overall_var)),
                    step("CHECK", "direct variance equals decomposition",
                         prob_txt(overall_var), prob_txt(within + between)),
                ])
                prefix += " Target: total variance decomposition."
                answer = (f"Var(X) = {prob_txt(overall_var)}; "
                          f"E[Var(X given Y)] = {prob_txt(within)}; "
                          f"Var(E[X given Y]) = {prob_txt(between)}")
        return prefix, steps, answer

    @staticmethod
    def _two_stage():
        faces = random.randint(4, 8)
        venue, city, name = _setting()
        prefix = (f"At the {venue} in {city}, {name} rolls a fair {faces}-sided "
                  "die to get N, then flips N fair coins. Let H count heads.")
        steps = [step("TOWER", "E[H] = Σ P(N=n)E[H given N=n]")]
        terms = []
        for n in range(1, faces + 1):
            conditional = Fraction(n, 2)
            term = Fraction(1, faces) * conditional
            steps.extend([step("COND_EXP", f"E[H given N={n}]",
                               f"{n} × 1/2", prob_txt(conditional)),
                          step("M", prob_txt(Fraction(1, faces)),
                               prob_txt(conditional), prob_txt(term))])
            terms.append(term)
        value = _sum_steps(steps, terms)
        steps.append(step("CHECK", "E[N]/2", prob_txt(value)))
        return prefix, steps, f"E[H] = {prob_txt(value)}"

    @staticmethod
    def _random_sum(variance_variant):
        rows = _n_distribution()
        p = random.choice(P_BANK)
        venue, city, name = _setting()
        prefix = (f"At the {venue} in {city}, {name} has count pmf: {_n_text(rows)}. "
                  f"Given N=n, S is the sum of n independent Bernoulli({prob_txt(p)}) "
                  "increments, independent of N.")
        steps, mean_n, variance_n = _n_moments_steps(rows)
        q = 1 - p
        mean_increment, var_increment = p, p * q
        if not variance_variant:
            value = mean_n * mean_increment
            steps.extend([step("TOWER", "E[S] = E[N]E[B]"),
                          step("M", prob_txt(mean_n), prob_txt(mean_increment),
                               prob_txt(value)),
                          step("CHECK", "conditional mean E[S given N]=Np",
                               prob_txt(value))])
            answer = f"E[S] = {prob_txt(value)}"
        else:
            first = mean_n * var_increment
            mean_square = mean_increment ** 2
            second = variance_n * mean_square
            value = first + second
            steps.extend([step("S", 1, prob_txt(p), prob_txt(q)),
                          step("M", prob_txt(p), prob_txt(q),
                               prob_txt(var_increment)),
                          step("E", prob_txt(mean_increment), 2,
                               prob_txt(mean_square)),
                          step("M", prob_txt(mean_n), prob_txt(var_increment),
                               prob_txt(first)),
                          step("M", prob_txt(variance_n), prob_txt(mean_square),
                               prob_txt(second)),
                          step("A", prob_txt(first), prob_txt(second),
                               prob_txt(value)),
                          step("TOTAL_VARIANCE",
                               "Var(S) = E[N]Var(B) + Var(N)(E[B])²",
                               prob_txt(value))])
            answer = f"Var(S) = {prob_txt(value)}"
        return prefix, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant in ("from_table", "tower_check", "conditional_variance",
                       "total_variance_check"):
            prefix, steps, answer = self._table_variant(variant)
        elif variant == "two_stage_experiment":
            prefix, steps, answer = self._two_stage()
        elif variant == "random_sum_mean":
            prefix, steps, answer = self._random_sum(False)
        else:
            prefix, steps, answer = self._random_sum(True)
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_conditional_expectation_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
