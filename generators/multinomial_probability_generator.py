"""Compute exact probabilities and moments for three-category trials.

Variants: ``exact_counts``, ``marginal_is_binomial``, ``mean_cov``,
``sequence_vs_counts``, and ``bag_with_replacement``. Op-codes:
``MULTI_SETUP``, ``MULTI_FORMULA``, ``BINOMIAL_MARGINAL``,
``MOMENT_FORMULA``, ``SEQUENCE_FORMULA``, ``FACT``, ``NCR``, ``POW``,
``A``, ``S``, ``M``, ``D``, ``CHECK``, and ``Z``. Every trial has three
exhaustive outcomes and n is at most 6, so the matching tests can enumerate
the entire weighted sequence space independently.
"""
import math
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
CATEGORY_BANK = (
    ("amber", "blue", "coral"), ("circle", "square", "triangle"),
    ("cedar", "maple", "pine"), ("north", "central", "south"),
    ("basic", "standard", "premium"), ("small", "medium", "large"),
    ("type I", "type II", "type III"), ("alpha", "beta", "gamma"),
)
PROBABILITY_BANK = (
    (Fraction(1, 6), Fraction(1, 6), Fraction(2, 3)),
    (Fraction(1, 4), Fraction(1, 4), Fraction(1, 2)),
    (Fraction(1, 5), Fraction(2, 5), Fraction(2, 5)),
    (Fraction(1, 3), Fraction(1, 3), Fraction(1, 3)),
    (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)),
    (Fraction(1, 5), Fraction(1, 5), Fraction(3, 5)),
    (Fraction(1, 4), Fraction(1, 2), Fraction(1, 4)),
    (Fraction(2, 5), Fraction(1, 5), Fraction(2, 5)),
    (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)),
    (Fraction(2, 3), Fraction(1, 6), Fraction(1, 6)),
)
BAG_BANK = ((1, 1, 2), (1, 2, 2), (1, 2, 3), (1, 3, 2),
            (2, 1, 3), (2, 2, 1), (2, 2, 3), (2, 3, 1),
            (3, 1, 2), (3, 2, 2), (3, 2, 3), (3, 3, 2))
QUERIES = {
    "exact_counts": (
        "Find this exact multinomial probability.",
        "Use the multinomial count formula.",
        "Count all orderings with the stated category totals.",
        "What is the probability of this count vector?",
        "Evaluate the exact joint count probability.",
    ),
    "marginal_is_binomial": (
        "Identify the marginal law of X_A and find the target probability.",
        "Collapse outcomes B and C, then compute the binomial probability.",
        "Find the marginal distribution and requested point mass of X_A.",
        "Treat A versus not-A as a two-outcome trial.",
        "State the binomial marginal and evaluate its target probability.",
    ),
    "mean_cov": (
        "Find E[X_A], Var(X_A), and Cov(X_A,X_B).",
        "Compute the first marginal mean, variance, and cross-covariance.",
        "Use multinomial moment identities for X_A and X_B.",
        "Report the requested mean, variance, and covariance exactly.",
        "Quantify the center, spread, and dependence of these two counts.",
    ),
    "sequence_vs_counts": (
        "Compare the probability of the specified order with all matching orders.",
        "Find both the ordered-sequence probability and the count-vector probability.",
        "Evaluate one exact ordering, then include every permutation of its counts.",
        "How likely is that sequence, and how likely are those totals in any order?",
        "Compute the ordered and unordered-count probabilities exactly.",
    ),
    "bag_with_replacement": (
        "Find this exact count probability.",
        "Use a multinomial model for the replacement draws.",
        "Count every draw order having the stated color totals.",
        "What is the probability of this color-count vector?",
        "Evaluate the replacement-sampling probability exactly.",
    ),
}


def _setting():
    return random.choice(VENUES), random.choice(CITIES), random.choice(NAMES)


def _positive_counts(n):
    first, second = sorted(random.sample(range(1, n), 2))
    return first, second - first, n - second


def _power(base, exponent):
    value = base ** exponent
    return step("POW", f"base {prob_txt(base)}, exponent {exponent}",
                prob_txt(value)), value


def _tokens(count, label):
    return f"{count} {label} token" + ("" if count == 1 else "s")


def _count_steps(n, counts, probabilities):
    a, b, c = counts
    numerator = math.factorial(n)
    factorials = tuple(math.factorial(value) for value in counts)
    first_denominator = factorials[0] * factorials[1]
    denominator = first_denominator * factorials[2]
    coefficient = numerator // denominator
    steps = [
        step("MULTI_FORMULA", "n!/(a!b!c!) times p_A^a p_B^b p_C^c",
             f"{n}!/({a}!{b}!{c}!)"),
        step("FACT", n, numerator),
        step("FACT", a, factorials[0]),
        step("FACT", b, factorials[1]),
        step("FACT", c, factorials[2]),
        step("M", factorials[0], factorials[1], first_denominator),
        step("M", first_denominator, factorials[2], denominator),
        step("D", numerator, denominator, coefficient),
    ]
    powers = []
    for probability, exponent in zip(probabilities, counts):
        raw, value = _power(probability, exponent)
        steps.append(raw)
        powers.append(value)
    first_product = powers[0] * powers[1]
    sequence_probability = first_product * powers[2]
    total = coefficient * sequence_probability
    steps.extend([
        step("M", prob_txt(powers[0]), prob_txt(powers[1]),
             prob_txt(first_product)),
        step("M", prob_txt(first_product), prob_txt(powers[2]),
             prob_txt(sequence_probability)),
        step("M", coefficient, prob_txt(sequence_probability), prob_txt(total)),
        step("CHECK", "a+b+c", f"{a}+{b}+{c}", n),
    ])
    return steps, sequence_probability, total


def _generic_prefix(n, probabilities, labels, target):
    venue, city, name = _setting()
    pa, pb, pc = probabilities
    la, lb, lc = labels
    return (f"At the {venue} in {city}, {name} runs {n} independent trials. "
            f"Each trial has exactly three outcomes: A ({la}) with probability "
            f"p_A={prob_txt(pa)}, B ({lb}) with probability p_B={prob_txt(pb)}, "
            f"and C ({lc}) with probability p_C={prob_txt(pc)}. Let X_A, X_B, "
            f"and X_C be their counts. {target}")


class MultinomialProbabilityGenerator(ProblemGenerator):
    """Generate exact three-category multinomial exercises."""

    VARIANTS = ("exact_counts", "marginal_is_binomial", "mean_cov",
                "sequence_vs_counts", "bag_with_replacement")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _exact_counts():
        n = random.randint(3, 6)
        counts = _positive_counts(n)
        probabilities = random.choice(PROBABILITY_BANK)
        labels = random.choice(CATEGORY_BANK)
        a, b, c = counts
        target = f"Target: P(X_A={a}, X_B={b}, X_C={c})."
        problem = _generic_prefix(n, probabilities, labels, target)
        steps = [step("MULTI_SETUP", f"X_A={a}, X_B={b}, X_C={c}",
                      f"total {n}")]
        extra, _, answer = _count_steps(n, counts, probabilities)
        steps.extend(extra)
        return problem, steps, prob_txt(answer)

    @staticmethod
    def _marginal():
        n = random.randint(3, 6)
        k = random.randint(1, n - 1)
        probabilities = random.choice(PROBABILITY_BANK)
        labels = random.choice(CATEGORY_BANK)
        p = probabilities[0]
        q = 1 - p
        target = f"Target: the marginal law of X_A and P(X_A={k})."
        problem = _generic_prefix(n, probabilities, labels, target)
        coefficient = math.comb(n, k)
        p_step, p_power = _power(p, k)
        q_step, q_power = _power(q, n - k)
        first = coefficient * p_power
        value = first * q_power
        steps = [
            step("MULTI_SETUP", f"n={n}, p_A={prob_txt(p)}", f"X_A={k}"),
            step("BINOMIAL_MARGINAL", "X_A ~ Binomial(n,p_A)",
                 "B and C combine as not-A"),
            step("S", 1, prob_txt(p), prob_txt(q)),
            step("NCR", f"C({n}, {k})", coefficient),
            p_step, q_step,
            step("M", coefficient, prob_txt(p_power), prob_txt(first)),
            step("M", prob_txt(first), prob_txt(q_power), prob_txt(value)),
            step("CHECK", "p_A+(p_B+p_C)",
                 f"{prob_txt(p)}+{prob_txt(q)}", 1),
        ]
        answer = (f"X_A ~ Binomial({n}, {prob_txt(p)}); "
                  f"P(X_A={k}) = {prob_txt(value)}")
        return problem, steps, answer

    @staticmethod
    def _mean_cov():
        n = random.randint(3, 6)
        probabilities = random.choice(PROBABILITY_BANK)
        labels = random.choice(CATEGORY_BANK)
        pa, pb, _ = probabilities
        mean = n * pa
        q = 1 - pa
        variance = mean * q
        positive_cov = mean * pb
        covariance = -positive_cov
        target = "Target: moments for X_A and the pair (X_A,X_B)."
        problem = _generic_prefix(n, probabilities, labels, target)
        steps = [
            step("MULTI_SETUP", f"n={n}, p_A={prob_txt(pa)}, p_B={prob_txt(pb)}",
                 "moments"),
            step("MOMENT_FORMULA", "E[X_A]=np_A; Var(X_A)=np_A(1-p_A)",
                 "Cov(X_A,X_B)=-np_Ap_B"),
            step("M", n, prob_txt(pa), prob_txt(mean)),
            step("S", 1, prob_txt(pa), prob_txt(q)),
            step("M", prob_txt(mean), prob_txt(q), prob_txt(variance)),
            step("M", prob_txt(mean), prob_txt(pb), prob_txt(positive_cov)),
            step("M", prob_txt(positive_cov), -1, prob_txt(covariance)),
            step("CHECK", "covariance sign", "distinct counts compete", "nonpositive"),
        ]
        answer = (f"E[X_A] = {prob_txt(mean)}; Var(X_A) = {prob_txt(variance)}; "
                  f"Cov(X_A,X_B) = {prob_txt(covariance)}")
        return problem, steps, answer

    @staticmethod
    def _sequence_vs_counts():
        n = random.randint(3, 6)
        probabilities = random.choice(PROBABILITY_BANK)
        labels = random.choice(CATEGORY_BANK)
        sequence = [random.choice("ABC") for _ in range(n)]
        counts = tuple(sequence.count(symbol) for symbol in "ABC")
        a, b, c = counts
        sequence_text = ",".join(sequence)
        target = (f"Specified sequence: {sequence_text}. Matching count target: "
                  f"(X_A,X_B,X_C)=({a},{b},{c}).")
        problem = _generic_prefix(n, probabilities, labels, target)
        steps = [
            step("MULTI_SETUP", f"sequence {sequence_text}",
                 f"counts ({a},{b},{c})"),
            step("SEQUENCE_FORMULA", "multiply probabilities in the stated order",
                 "equal symbols may be grouped as powers"),
        ]
        extra, sequence_probability, count_probability = _count_steps(
            n, counts, probabilities)
        steps.extend(extra)
        coefficient = math.factorial(n)
        for count in counts:
            coefficient //= math.factorial(count)
        steps.append(step("CHECK", "matching orders", coefficient,
                          "count probability = orders times sequence probability"))
        answer = (f"specified sequence = {prob_txt(sequence_probability)}; "
                  f"matching counts = {prob_txt(count_probability)}")
        return problem, steps, answer

    @staticmethod
    def _bag():
        venue, city, name = _setting()
        labels = random.choice(CATEGORY_BANK)
        bag_counts = random.choice(BAG_BANK)
        total_tokens = sum(bag_counts)
        probabilities = tuple(Fraction(value, total_tokens) for value in bag_counts)
        n = random.randint(3, 6)
        counts = _positive_counts(n)
        la, lb, lc = labels
        ba, bb, bc = bag_counts
        a, b, c = counts
        problem = (f"At the {venue} in {city}, a bag contains {_tokens(ba, la)}, "
                   f"{_tokens(bb, lb)}, and {_tokens(bc, lc)}. {name} makes {n} "
                   f"draws with replacement, mixing before each draw. Let X_A "
                   f"count {la}, X_B count {lb}, and X_C count {lc}. Target: "
                   f"P(X_A={a}, X_B={b}, X_C={c}).")
        steps = [
            step("MULTI_SETUP", f"bag counts {ba},{bb},{bc}; total {total_tokens}",
                 f"draw counts {a},{b},{c}; total {n}"),
            step("D", ba, total_tokens, prob_txt(probabilities[0])),
            step("D", bb, total_tokens, prob_txt(probabilities[1])),
            step("D", bc, total_tokens, prob_txt(probabilities[2])),
        ]
        extra, _, answer = _count_steps(n, counts, probabilities)
        steps.extend(extra)
        return problem, steps, prob_txt(answer)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "exact_counts":
            problem, steps, answer = self._exact_counts()
        elif variant == "marginal_is_binomial":
            problem, steps, answer = self._marginal()
        elif variant == "mean_cov":
            problem, steps, answer = self._mean_cov()
        elif variant == "sequence_vs_counts":
            problem, steps, answer = self._sequence_vs_counts()
        else:
            problem, steps, answer = self._bag()
        problem = f"{problem} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_multinomial_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
