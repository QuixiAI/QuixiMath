"""Build and use probability generating functions with exact polynomials.

Variants: ``build``, ``extract_pmf``, ``mean_from_pgf``,
``variance_from_pgf``, ``sum_independent_product``, ``binomial_pgf``, and
``prob_even``. Op-codes: ``PGF_SETUP``, ``PGF_TERM``, ``PGF_DERIV``,
``POLY_MUL``, ``SUBST``, ``NCR``, ``E``, ``M``, ``A``, ``S``, ``D``,
``CHECK``, and ``Z``. Positive dyadic pmfs and small binomial laws keep all
coefficients exact; polynomials are rendered in descending powers with
fractional coefficients parenthesized.
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
P_BANK = (Fraction(1, 4), Fraction(1, 3), Fraction(2, 5), Fraction(1, 2),
          Fraction(3, 5), Fraction(2, 3), Fraction(3, 4))
QUERIES = {
    "build": (
        "Write the probability generating function G_X(s).",
        "Convert the pmf into its exact PGF polynomial.",
        "Build ΣP(X=k)s^k in descending powers.",
        "What is G_X(s)?",
        "Place each probability on its matching power of s.",
    ),
    "extract_pmf": (
        "Extract the requested probability from the PGF.",
        "Read the coefficient of the target power of s.",
        "Recover P(X=k) from the displayed polynomial.",
        "What pmf value corresponds to the requested exponent?",
        "Use the PGF coefficient rule.",
    ),
    "mean_from_pgf": (
        "Find E[X] from G'_X(1).",
        "Differentiate the PGF and substitute s=1.",
        "Compute the exact mean using the first PGF derivative.",
        "What is G'_X(1)?",
        "Use the derivative identity for expectation.",
    ),
    "variance_from_pgf": (
        "Find Var(X) from the first two PGF derivatives.",
        "Use G''(1)+G'(1)−G'(1)².",
        "Compute the exact variance from factorial moments.",
        "What variance follows from the displayed PGF?",
        "Differentiate twice, substitute one, and combine the moments.",
    ),
    "sum_independent_product": (
        "Find the PGF and pmf of S=X+Y.",
        "Multiply the independent PGFs and read the sum coefficients.",
        "Compute G_S(s)=G_X(s)G_Y(s).",
        "What distribution polynomial describes the sum?",
        "Use polynomial multiplication to convolve the two pmfs.",
    ),
    "binomial_pgf": (
        "Write the expanded binomial PGF and find its mean.",
        "Expand (1−p+ps)^n and evaluate G'(1).",
        "Build the PGF of the binomial count.",
        "What polynomial and expectation describe X?",
        "Use binomial coefficients for every PGF term.",
    ),
    "prob_even": (
        "Find P(X is even) using G(1) and G(−1).",
        "Apply the even-coefficient filter (G(1)+G(−1))/2.",
        "Compute the exact probability of an even value from the PGF.",
        "What mass lies on even exponents?",
        "Evaluate the polynomial at plus and minus one, then average.",
    ),
}


def _setting():
    return random.choice(VENUES), random.choice(CITIES), random.choice(NAMES)


def _weights(size):
    total = 2 ** random.randint(4, 8)
    cuts = sorted(random.sample(range(1, total), size - 1))
    counts = [cuts[0]]
    counts.extend(cuts[index] - cuts[index - 1]
                  for index in range(1, len(cuts)))
    counts.append(total - cuts[-1])
    return tuple(Fraction(count, total) for count in counts)


def _pmf(size=None):
    size = size or random.randint(3, 5)
    return {exponent: probability for exponent, probability in enumerate(_weights(size))}


def _pmf_text(label, pmf):
    return "; ".join(f"P({label}={k})={prob_txt(p)}" for k, p in pmf.items())


def _term_text(coefficient, exponent):
    coefficient = Fraction(coefficient)
    if exponent == 0:
        return prob_txt(coefficient)
    variable = "s" if exponent == 1 else f"s^{exponent}"
    if coefficient == 1:
        return variable
    return f"({prob_txt(coefficient)}){variable}"


def _poly_text(polynomial):
    terms = [_term_text(coefficient, exponent)
             for exponent, coefficient in sorted(polynomial.items(), reverse=True)
             if coefficient]
    return " + ".join(terms) if terms else "0"


def _derivative(polynomial):
    return {exponent - 1: exponent * coefficient
            for exponent, coefficient in polynomial.items() if exponent > 0}


def _evaluate(polynomial, value):
    return sum((coefficient * Fraction(value) ** exponent
                for exponent, coefficient in polynomial.items()), Fraction())


def _multiply(first, second):
    output = {}
    for first_exp, first_coeff in first.items():
        for second_exp, second_coeff in second.items():
            exponent = first_exp + second_exp
            output[exponent] = output.get(exponent, Fraction()) + first_coeff * second_coeff
    return output


def _sum_steps(steps, values):
    running = values[0]
    for value in values[1:]:
        steps.append(step("A", prob_txt(running), prob_txt(value),
                          prob_txt(running + value)))
        running += value
    return running


def _setup_steps(polynomial):
    steps = [step("PGF_SETUP", "G(s) = Σ P(X=k)·s^k")]
    for exponent, coefficient in sorted(polynomial.items(), reverse=True):
        steps.append(step("PGF_TERM", f"k={exponent}",
                          _term_text(coefficient, exponent)))
    return steps


def _answer_pmf(label, polynomial):
    return "; ".join(f"P({label}={k}) = {prob_txt(p)}"
                     for k, p in sorted(polynomial.items()))


class PGFGenerator(ProblemGenerator):
    """Generate exact finite probability-generating-function exercises."""

    VARIANTS = ("build", "extract_pmf", "mean_from_pgf",
                "variance_from_pgf", "sum_independent_product",
                "binomial_pgf", "prob_even")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _single(variant):
        polynomial = _pmf()
        venue, city, name = _setting()
        pmf_data = _pmf_text("X", polynomial)
        poly = _poly_text(polynomial)
        if variant == "extract_pmf":
            target = random.choice(tuple(polynomial))
            prefix = (f"At the {venue} in {city}, {name} is given "
                      f"G_X(s) = {poly}. Target: P(X={target}).")
            target_power = "1" if target == 0 else "s" if target == 1 else f"s^{target}"
            steps = [step("PGF_SETUP", f"G_X(s) = {poly}"),
                     step("PGF_TERM", f"coefficient of {target_power}",
                          prob_txt(polynomial[target])),
                     step("CHECK", "PGF coefficient equals pmf mass",
                          prob_txt(polynomial[target]))]
            answer = f"P(X={target}) = {prob_txt(polynomial[target])}"
            return prefix, steps, answer
        prefix = (f"At the {venue} in {city}, {name} has pmf: {pmf_data}. "
                  f"Thus G_X(s) = {poly}.")
        steps = _setup_steps(polynomial)
        if variant == "build":
            steps.append(step("CHECK", "G_X(1)", prob_txt(_evaluate(polynomial, 1))))
            return prefix, steps, f"G(s) = {poly}"
        first = _derivative(polynomial)
        first_at_one = _evaluate(first, 1)
        steps.extend([step("PGF_DERIV", "G'(s)", _poly_text(first)),
                      step("SUBST", "s", 1, prob_txt(first_at_one))])
        if variant == "mean_from_pgf":
            return prefix, steps, f"E[X] = {prob_txt(first_at_one)}"
        second = _derivative(first)
        second_at_one = _evaluate(second, 1)
        mean_square = first_at_one ** 2
        partial = second_at_one + first_at_one
        variance = partial - mean_square
        steps.extend([step("PGF_DERIV", "G''(s)", _poly_text(second)),
                      step("SUBST", "s", 1, prob_txt(second_at_one)),
                      step("E", prob_txt(first_at_one), 2, prob_txt(mean_square)),
                      step("A", prob_txt(second_at_one), prob_txt(first_at_one),
                           prob_txt(partial)),
                      step("S", prob_txt(partial), prob_txt(mean_square),
                           prob_txt(variance)),
                      step("CHECK", "definition variance", prob_txt(variance))])
        return prefix, steps, f"Var(X) = {prob_txt(variance)}"

    @staticmethod
    def _sum_product():
        first, second = _pmf(random.randint(2, 4)), _pmf(random.randint(2, 4))
        product = _multiply(first, second)
        venue, city, name = _setting()
        prefix = (f"At the {venue} in {city}, {name} has independent variables. "
                  f"X pmf: {_pmf_text('X', first)}. Y pmf: {_pmf_text('Y', second)}.")
        first_poly, second_poly, product_poly = (_poly_text(first), _poly_text(second),
                                                 _poly_text(product))
        steps = _setup_steps(first) + _setup_steps(second)
        steps.append(step("POLY_MUL", f"({first_poly})({second_poly})", product_poly))
        steps.append(step("CHECK", "G_S(1)", prob_txt(_evaluate(product, 1))))
        answer = f"G_S(s) = {product_poly}; {_answer_pmf('S', product)}"
        return prefix, steps, answer

    @staticmethod
    def _binomial():
        n, p = random.randint(2, 6), random.choice(P_BANK)
        q = 1 - p
        polynomial = {k: Fraction(math.comb(n, k)) * p ** k * q ** (n - k)
                      for k in range(n + 1)}
        venue, city, name = _setting()
        prefix = (f"At the {venue} in {city}, {name} has X~Binomial({n},"
                  f"{prob_txt(p)}).")
        steps = [step("PGF_SETUP", f"G_X(s) = ({prob_txt(q)} + {prob_txt(p)}s)^{n}")]
        for k, probability in polynomial.items():
            coefficient = math.comb(n, k)
            pk, qk = p ** k, q ** (n - k)
            partial = coefficient * pk
            steps.extend([step("NCR", f"C({n}, {k})", coefficient),
                          step("E", prob_txt(p), k, prob_txt(pk)),
                          step("E", prob_txt(q), n - k, prob_txt(qk)),
                          step("M", coefficient, prob_txt(pk), prob_txt(partial)),
                          step("M", prob_txt(partial), prob_txt(qk),
                               prob_txt(probability)),
                          step("PGF_TERM", f"k={k}",
                               _term_text(probability, k))])
        mean = n * p
        steps.extend([step("PGF_DERIV", "G'_X(1) = np"),
                      step("M", n, prob_txt(p), prob_txt(mean)),
                      step("CHECK", "expanded coefficients sum", 1)])
        answer = f"G(s) = {_poly_text(polynomial)}; E[X] = {prob_txt(mean)}"
        return prefix, steps, answer

    @staticmethod
    def _even():
        polynomial = _pmf()
        venue, city, name = _setting()
        prefix = (f"At the {venue} in {city}, {name} has pmf: "
                  f"{_pmf_text('X', polynomial)}. Thus G_X(s) = {_poly_text(polynomial)}.")
        steps = _setup_steps(polynomial)
        signed_terms = []
        for exponent, probability in polynomial.items():
            sign = Fraction(-1) ** exponent
            term = probability * sign
            steps.extend([step("E", -1, exponent, sign),
                          step("M", prob_txt(probability), sign, prob_txt(term))])
            signed_terms.append(term)
        g_negative = _sum_steps(steps, signed_terms)
        g_positive = _evaluate(polynomial, 1)
        summed = g_positive + g_negative
        value = summed / 2
        steps.extend([step("SUBST", "s", -1, prob_txt(g_negative)),
                      step("A", prob_txt(g_positive), prob_txt(g_negative),
                           prob_txt(summed)),
                      step("D", prob_txt(summed), 2, prob_txt(value)),
                      step("CHECK", "direct even coefficients", prob_txt(value))])
        return prefix, steps, prob_txt(value)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant in ("build", "extract_pmf", "mean_from_pgf",
                       "variance_from_pgf"):
            prefix, steps, answer = self._single(variant)
        elif variant == "sum_independent_product":
            prefix, steps, answer = self._sum_product()
        elif variant == "binomial_pgf":
            prefix, steps, answer = self._binomial()
        else:
            prefix, steps, answer = self._even()
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_pgf_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
