"""Compute exact probability bounds from standard inequalities.

Variants: ``markov``, ``chebyshev``, ``chebyshev_within``,
``chebyshev_find_k``, ``boole_union_bound``, ``bonferroni_lower``,
``lln_bound``, ``lln_sample_size``, and ``compare_exact``. Op-codes:
``INEQ_FORMULA``, ``INEQ_BOUND``, ``PMF_ROW``, ``CEIL``, ``E``, ``M``,
``A``, ``S``, ``D``, ``CHECK``, and ``Z``. Variances, radii, tolerances,
and confidence levels are constructed backward so all bounds are exact and
hand-computable; settings and five phrasings provide a large problem space.
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
EPSILONS = (Fraction(1, 5), Fraction(1, 4), Fraction(1, 3),
            Fraction(2, 5), Fraction(1, 2), Fraction(3, 4))
DELTAS = (Fraction(1, 20), Fraction(1, 10), Fraction(1, 8),
          Fraction(1, 5), Fraction(1, 4))
QUERIES = {
    "markov": (
        "Find Markov's upper bound for the displayed tail.",
        "Divide the nonnegative variable's mean by the threshold.",
        "Apply Markov's inequality exactly.",
        "What upper bound follows from E[X]?",
        "Use P(X≥a)≤E[X]/a.",
    ),
    "chebyshev": (
        "Find Chebyshev's upper bound for the displayed deviation event.",
        "Divide the variance by the squared radius.",
        "Apply Chebyshev's inequality exactly.",
        "What upper bound follows for this two-sided tail?",
        "Use P(abs(X−μ)≥c)≤Var(X)/c².",
    ),
    "chebyshev_within": (
        "Find the guaranteed probability of being within the stated radius.",
        "Complement Chebyshev's two-sided tail bound.",
        "Give the exact lower bound for the central interval.",
        "What probability is guaranteed within k standard deviations?",
        "Use P(abs(X−μ)<kσ)≥1−1/k².",
    ),
    "chebyshev_find_k": (
        "Find the smallest stated k that gives the target guarantee.",
        "Solve 1−1/k² for the displayed central probability.",
        "Determine the standard-deviation multiplier from Chebyshev's rule.",
        "What k produces this exact guaranteed coverage?",
        "Invert the within-k lower bound.",
    ),
    "boole_union_bound": (
        "Find Boole's upper bound for the union.",
        "Add the stated event probabilities.",
        "Apply the union bound exactly.",
        "What upper bound is guaranteed for at least one event?",
        "Use P(union A_i)≤ΣP(A_i).",
    ),
    "bonferroni_lower": (
        "Find the Bonferroni lower bound for the intersection.",
        "Add P(A) and P(B), then subtract one.",
        "Apply the two-event lower bound exactly.",
        "What minimum overlap is forced by these marginals?",
        "Use P(A∩B)≥P(A)+P(B)−1.",
    ),
    "lln_bound": (
        "Find the Chebyshev-form LLN upper bound.",
        "Use Var(X)/(nε²) for the sample-mean deviation.",
        "Compute the exact finite-sample law-of-large-numbers bound.",
        "What upper bound applies to the sample-mean error?",
        "Square the tolerance and divide the variance by nε².",
    ),
    "lln_sample_size": (
        "Find the smallest integer sample size meeting the target bound.",
        "Solve Var(X)/(nε²)≤δ and round up.",
        "Compute the required LLN sample size.",
        "What minimum n guarantees the displayed Chebyshev bound?",
        "Invert the variance-tolerance-confidence expression and take its ceiling.",
    ),
    "compare_exact": (
        "Compare Markov's bound with the exact tail probability.",
        "Use the printed pmf to evaluate the bound and the true tail.",
        "Compute both the theorem bound and exact probability.",
        "How loose is Markov's inequality for this finite distribution?",
        "Report the bound beside the enumerated tail mass.",
    ),
}


def _setting():
    return random.choice(VENUES), random.choice(CITIES), random.choice(NAMES)


def _ceil_fraction(value):
    value = Fraction(value)
    return -(-value.numerator // value.denominator)


def _prefix(text):
    venue, city, name = _setting()
    return f"At the {venue} in {city}, {name} studies {text}"


class ProbabilityInequalityGenerator(ProblemGenerator):
    """Generate exact probability-inequality and LLN-bound exercises."""

    VARIANTS = ("markov", "chebyshev", "chebyshev_within",
                "chebyshev_find_k", "boole_union_bound",
                "bonferroni_lower", "lln_bound", "lln_sample_size",
                "compare_exact")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _markov():
        mean = random.randint(1, 30)
        threshold = random.randint(mean, mean * 8)
        value = Fraction(mean, threshold)
        prefix = _prefix(f"a nonnegative X with E[X]={mean}. Target: P(X≥{threshold}).")
        steps = [step("INEQ_FORMULA", "Markov", "P(X≥a)≤E[X]/a"),
                 step("D", mean, threshold, prob_txt(value)),
                 step("INEQ_BOUND", f"P(X≥{threshold})", f"≤ {prob_txt(value)}")]
        return prefix, steps, prob_txt(value)

    @staticmethod
    def _chebyshev(within=False):
        mean = random.randint(-100, 100)
        sigma = random.randint(1, 20)
        variance = sigma * sigma
        k = random.randint(2, 8)
        radius = sigma * k
        tail = Fraction(1, k * k)
        if within:
            value = 1 - tail
            prefix = _prefix(
                f"X with mean μ={mean} and variance {variance}. Target: "
                f"P(abs(X−{mean})<{radius}).")
            steps = [step("INEQ_FORMULA", "Chebyshev within",
                          "P(abs(X−μ)<kσ)≥1−1/k²"),
                     step("E", k, 2, k * k),
                     step("D", 1, k * k, prob_txt(tail)),
                     step("S", 1, prob_txt(tail), prob_txt(value)),
                     step("INEQ_BOUND", f"P(abs(X−{mean})<{radius})",
                          f"≥ {prob_txt(value)}")]
        else:
            radius_square = radius * radius
            value = Fraction(variance, radius_square)
            prefix = _prefix(
                f"X with mean μ={mean} and variance {variance}. Target: "
                f"P(abs(X−{mean})≥{radius}).")
            steps = [step("INEQ_FORMULA", "Chebyshev",
                          "P(abs(X−μ)≥c)≤Var(X)/c²"),
                     step("E", radius, 2, radius_square),
                     step("D", variance, radius_square, prob_txt(value)),
                     step("INEQ_BOUND", f"P(abs(X−{mean})≥{radius})",
                          f"≤ {prob_txt(value)}")]
        return prefix, steps, prob_txt(value)

    @staticmethod
    def _find_k():
        k = random.randint(2, 12)
        square = k * k
        tail = Fraction(1, square)
        coverage = 1 - tail
        prefix = _prefix(
            f"Chebyshev's within-k rule. Target guarantee: "
            f"P(abs(X−μ)<kσ)≥{prob_txt(coverage)}.")
        steps = [step("INEQ_FORMULA", "within-k", "coverage ≥ 1−1/k²"),
                 step("S", 1, prob_txt(coverage), prob_txt(tail)),
                 step("D", 1, prob_txt(tail), square),
                 step("CHECK", f"k²={square}", f"k={k}")]
        return prefix, steps, f"k = {k}"

    @staticmethod
    def _boole():
        count = random.randint(2, 6)
        denominator = random.randint(count + 1, 40)
        raw = [random.randint(1, denominator // count) for _ in range(count)]
        while sum(raw) > denominator:
            raw[random.randrange(count)] = 1
        probabilities = tuple(Fraction(value, denominator) for value in raw)
        data = ", ".join(f"P(A{i + 1})={prob_txt(value)}"
                         for i, value in enumerate(probabilities))
        prefix = _prefix(f"events with {data}. Target: P(union of all A_i).")
        steps = [step("INEQ_FORMULA", "Boole union bound",
                      "P(union A_i)≤ΣP(A_i)")]
        running = probabilities[0]
        for probability in probabilities[1:]:
            steps.append(step("A", prob_txt(running), prob_txt(probability),
                              prob_txt(running + probability)))
            running += probability
        steps.append(step("INEQ_BOUND", "P(union A_i)", f"≤ {prob_txt(running)}"))
        return prefix, steps, prob_txt(running)

    @staticmethod
    def _bonferroni():
        denominator = random.randint(4, 30)
        a = random.randint(denominator // 2 + 1, denominator - 1)
        b = random.randint(denominator - a + 1, denominator - 1)
        pa, pb = Fraction(a, denominator), Fraction(b, denominator)
        summed = pa + pb
        value = summed - 1
        prefix = _prefix(
            f"events with P(A)={prob_txt(pa)} and P(B)={prob_txt(pb)}. "
            "Target: P(A∩B).")
        steps = [step("INEQ_FORMULA", "Bonferroni lower bound",
                      "P(A∩B)≥P(A)+P(B)−1"),
                 step("A", prob_txt(pa), prob_txt(pb), prob_txt(summed)),
                 step("S", prob_txt(summed), 1, prob_txt(value)),
                 step("INEQ_BOUND", "P(A∩B)", f"≥ {prob_txt(value)}")]
        return prefix, steps, prob_txt(value)

    @staticmethod
    def _lln(sample_size=False):
        variance = random.randint(1, 25)
        epsilon = random.choice(EPSILONS)
        epsilon_square = epsilon ** 2
        if sample_size:
            delta = random.choice(DELTAS)
            denominator_factor = delta * epsilon_square
            raw = Fraction(variance, 1) / denominator_factor
            n = _ceil_fraction(raw)
            prefix = _prefix(
                f"iid variables with variance {variance}. For tolerance "
                f"ε={prob_txt(epsilon)}, require P(abs(Xbar−μ)≥ε)≤{prob_txt(delta)}.")
            steps = [step("INEQ_FORMULA", "LLN via Chebyshev",
                          "n≥Var(X)/(δ ε²)"),
                     step("E", prob_txt(epsilon), 2, prob_txt(epsilon_square)),
                     step("M", prob_txt(delta), prob_txt(epsilon_square),
                          prob_txt(denominator_factor)),
                     step("D", variance, prob_txt(denominator_factor),
                          prob_txt(raw)),
                     step("CEIL", prob_txt(raw), n),
                     step("CHECK", "smallest integer n", n)]
            return prefix, steps, f"n = {n}"
        minimum = _ceil_fraction(Fraction(variance, 1) / epsilon_square)
        n = random.randint(minimum, minimum + 200)
        denominator = n * epsilon_square
        value = Fraction(variance, 1) / denominator
        prefix = _prefix(
            f"iid variables with variance {variance} and sample size n={n}. "
            f"For tolerance ε={prob_txt(epsilon)}. "
            f"Target: P(abs(Xbar−μ)≥{prob_txt(epsilon)}).")
        steps = [step("INEQ_FORMULA", "LLN via Chebyshev",
                      "P(abs(Xbar−μ)≥ε)≤Var(X)/(nε²)"),
                 step("E", prob_txt(epsilon), 2, prob_txt(epsilon_square)),
                 step("M", n, prob_txt(epsilon_square), prob_txt(denominator)),
                 step("D", variance, prob_txt(denominator), prob_txt(value)),
                 step("INEQ_BOUND", "sample-mean deviation", f"≤ {prob_txt(value)}")]
        return prefix, steps, prob_txt(value)

    @staticmethod
    def _compare():
        while True:
            scale = random.randint(2, 12)
            support = (0, scale, 2 * scale, 3 * scale)
            weights = []
            total = 2 ** random.randint(4, 8)
            cuts = sorted(random.sample(range(1, total), 3))
            counts = (cuts[0], cuts[1] - cuts[0], cuts[2] - cuts[1],
                      total - cuts[2])
            weights = tuple(Fraction(count, total) for count in counts)
            mean = sum((x * p for x, p in zip(support, weights)), Fraction())
            thresholds = [value for value in support[1:] if value >= mean]
            if thresholds:
                threshold = random.choice(thresholds)
                break
        bound = mean / threshold
        exact_tail = sum((p for x, p in zip(support, weights) if x >= threshold),
                         Fraction())
        data = "; ".join(f"P(X={x})={prob_txt(p)}"
                         for x, p in zip(support, weights))
        prefix = _prefix(f"nonnegative X with pmf: {data}. Target: P(X≥{threshold}).")
        steps = [step("PMF_ROW", x, prob_txt(p)) for x, p in zip(support, weights)]
        mean_terms = []
        for x, probability in zip(support, weights):
            term = x * probability
            steps.append(step("M", x, prob_txt(probability), prob_txt(term)))
            mean_terms.append(term)
        running = mean_terms[0]
        for term in mean_terms[1:]:
            steps.append(step("A", prob_txt(running), prob_txt(term),
                              prob_txt(running + term)))
            running += term
        steps.extend([step("INEQ_FORMULA", "Markov", "bound=E[X]/a"),
                      step("D", prob_txt(mean), threshold, prob_txt(bound)),
                      step("CHECK", "exact tail from pmf", prob_txt(exact_tail)),
                      step("INEQ_BOUND", f"P(X≥{threshold})",
                           f"exact {prob_txt(exact_tail)} ≤ bound {prob_txt(bound)}")])
        return prefix, steps, f"bound {prob_txt(bound)}; exact {prob_txt(exact_tail)}"

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "markov":
            prefix, steps, answer = self._markov()
        elif variant == "chebyshev":
            prefix, steps, answer = self._chebyshev(False)
        elif variant == "chebyshev_within":
            prefix, steps, answer = self._chebyshev(True)
        elif variant == "chebyshev_find_k":
            prefix, steps, answer = self._find_k()
        elif variant == "boole_union_bound":
            prefix, steps, answer = self._boole()
        elif variant == "bonferroni_lower":
            prefix, steps, answer = self._bonferroni()
        elif variant == "lln_bound":
            prefix, steps, answer = self._lln(False)
        elif variant == "lln_sample_size":
            prefix, steps, answer = self._lln(True)
        else:
            prefix, steps, answer = self._compare()
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_inequality_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
