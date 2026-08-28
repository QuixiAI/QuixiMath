"""Build distributions of sums, weighted sums, maxima, and minima.

Variants: ``convolution_pmf``, ``single_value``, ``weighted_dice_sum``,
``max_of_two``, ``min_of_two``, ``sum_binomial_rule``, and
``sum_poisson_rule``. Op-codes: ``CONV_WINDOW``, ``CONV_SUM``, ``CDF_ROW``,
``DIST_RULE``, ``NCR``, ``POW``, ``M``, ``A``, ``S``, ``CHECK``, and ``Z``.
Finite variants use small exact dyadic pmfs or product spaces; Poisson closure
is reported symbolically through its exact rate, so no unstated exponential
lookup is required.
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
    "convolution_pmf": (
        "Find the complete pmf of S = X + Y.",
        "Convolve the two independent pmfs.",
        "Compute every probability in the distribution of the sum.",
        "What is the exact sum distribution?",
        "Slide the convolution window across all possible totals.",
    ),
    "single_value": (
        "Find the requested probability for S = X + Y.",
        "Use one convolution window at the target sum.",
        "Add all independent pair masses that produce the target.",
        "What is the exact point probability of the sum?",
        "Compute P(S=s) from the two printed pmfs.",
    ),
    "weighted_dice_sum": (
        "Find the requested weighted-dice probability.",
        "Enumerate the fair die pairs that satisfy the linear total.",
        "Compute the exact probability of the target weighted sum.",
        "What fraction of die pairs gives this value?",
        "Count solutions to aX+bY=t in the dice product space.",
    ),
    "max_of_two": (
        "Find the complete pmf of M = max(X,Y).",
        "Multiply the two cdfs and then difference successive values.",
        "Compute the distribution of the maximum.",
        "What is the exact max pmf?",
        "Use P(M≤k)=F_X(k)F_Y(k).",
    ),
    "min_of_two": (
        "Find the complete pmf of M = min(X,Y).",
        "Multiply the two survival functions and difference them.",
        "Compute the distribution of the minimum.",
        "What is the exact min pmf?",
        "Use P(M≥k)=P(X≥k)P(Y≥k).",
    ),
    "sum_binomial_rule": (
        "Identify the sum law and find the requested point probability.",
        "Use closure of independent binomials with a common p.",
        "Combine the trial counts, then evaluate the target mass.",
        "What binomial distribution describes S, and what is P(S=k)?",
        "Apply the binomial sum rule before computing the probability.",
    ),
    "sum_poisson_rule": (
        "Identify the distribution, mean, and variance of the sum.",
        "Use closure of independent Poisson variables under addition.",
        "Add the exact rates for the summed count.",
        "What Poisson law describes S?",
        "Report the sum rate and its matching mean and variance.",
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


def _pmf(size):
    return {value: probability for value, probability in enumerate(_weights(size))}


def _pmf_text(label, pmf):
    return "; ".join(f"P({label}={value})={prob_txt(probability)}"
                     for value, probability in pmf.items())


def _answer_pmf(label, pmf):
    return "; ".join(f"P({label}={value}) = {prob_txt(probability)}"
                     for value, probability in sorted(pmf.items()))


def _sum_steps(steps, values):
    running = values[0]
    for value in values[1:]:
        steps.append(step("A", prob_txt(running), prob_txt(value),
                          prob_txt(running + value)))
        running += value
    return running


def _convolution(x_pmf, y_pmf):
    output = {}
    for x, px in x_pmf.items():
        for y, py in y_pmf.items():
            output[x + y] = output.get(x + y, Fraction()) + px * py
    return output


def _convolution_steps(x_pmf, y_pmf, totals):
    steps = []
    values = {}
    for total in totals:
        terms = []
        descriptions = []
        for x, px in x_pmf.items():
            y = total - x
            if y not in y_pmf:
                continue
            term = px * y_pmf[y]
            steps.append(step("M", prob_txt(px), prob_txt(y_pmf[y]),
                              prob_txt(term)))
            terms.append(term)
            descriptions.append(f"{prob_txt(px)}·{prob_txt(y_pmf[y])}")
        value = _sum_steps(steps, terms)
        steps.extend([step("CONV_WINDOW", f"s={total}",
                           " + ".join(descriptions)),
                      step("CONV_SUM", f"s={total}", prob_txt(value))])
        values[total] = value
    return steps, values


class DistributionOfSumGenerator(ProblemGenerator):
    """Generate exact convolution and independent-distribution closure tasks."""

    VARIANTS = ("convolution_pmf", "single_value", "weighted_dice_sum",
                "max_of_two", "min_of_two", "sum_binomial_rule",
                "sum_poisson_rule")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _convolution_variant(single):
        x_pmf, y_pmf = _pmf(random.randint(2, 4)), _pmf(random.randint(2, 4))
        venue, city, name = _setting()
        prefix = (f"At the {venue} in {city}, {name} has independent variables. "
                  f"X pmf: {_pmf_text('X', x_pmf)}. Y pmf: {_pmf_text('Y', y_pmf)}.")
        all_values = _convolution(x_pmf, y_pmf)
        if single:
            target = random.choice(tuple(all_values))
            prefix += f" Target: P(S={target}) for S=X+Y."
            steps, values = _convolution_steps(x_pmf, y_pmf, (target,))
            answer = prob_txt(values[target])
        else:
            prefix += " Target: pmf of S=X+Y."
            steps, values = _convolution_steps(x_pmf, y_pmf, sorted(all_values))
            answer = _answer_pmf("S", values)
        total_steps = []
        total = _sum_steps(total_steps, list(values.values())) if not single else None
        if not single:
            steps.extend(total_steps)
            steps.append(step("CHECK", "Σ P(S=s)", prob_txt(total)))
        return prefix, steps, answer

    @staticmethod
    def _weighted_dice():
        sides_x, sides_y = random.randint(4, 6), random.randint(4, 6)
        a, b = random.randint(2, 4), random.randint(2, 4)
        pairs = [(x, y) for x in range(1, sides_x + 1)
                 for y in range(1, sides_y + 1)]
        target = a * random.randint(1, sides_x) + b * random.randint(1, sides_y)
        favorable = [(x, y) for x, y in pairs if a * x + b * y == target]
        probability = Fraction(len(favorable), len(pairs))
        venue, city, name = _setting()
        prefix = (f"At the {venue} in {city}, {name} rolls independent fair "
                  f"{sides_x}- and {sides_y}-sided dice X and Y. Let W={a}X+{b}Y. "
                  f"Target: P(W={target}).")
        steps = [step("DIST_RULE", "enumerate independent die pairs",
                      f"{sides_x} × {sides_y} outcomes"),
                 step("M", sides_x, sides_y, len(pairs)),
                 step("CHECK", f"{a}x+{b}y={target}",
                      ", ".join(f"({x},{y})" for x, y in favorable),
                      len(favorable)),
                 step("D", len(favorable), len(pairs), prob_txt(probability))]
        return prefix, steps, prob_txt(probability)

    @staticmethod
    def _extreme(maximum):
        x_pmf, y_pmf = _pmf(3), _pmf(3)
        venue, city, name = _setting()
        symbol = "max" if maximum else "min"
        prefix = (f"At the {venue} in {city}, {name} has independent variables. "
                  f"X pmf: {_pmf_text('X', x_pmf)}. Y pmf: {_pmf_text('Y', y_pmf)}. "
                  f"Target: pmf of M={symbol}(X,Y).")
        steps = [step("DIST_RULE",
                      "F_M(k)=F_X(k)F_Y(k)" if maximum else
                      "P(M≥k)=P(X≥k)P(Y≥k)")]
        output = {}
        if maximum:
            previous = Fraction()
            for k in range(3):
                fx = sum((p for value, p in x_pmf.items() if value <= k), Fraction())
                fy = sum((p for value, p in y_pmf.items() if value <= k), Fraction())
                cdf = fx * fy
                value = cdf - previous
                steps.extend([step("M", prob_txt(fx), prob_txt(fy), prob_txt(cdf)),
                              step("CDF_ROW", f"F_M({k})", prob_txt(cdf)),
                              step("S", prob_txt(cdf), prob_txt(previous),
                                   prob_txt(value)),
                              step("CONV_SUM", f"M={k}", prob_txt(value))])
                output[k], previous = value, cdf
        else:
            next_survival = Fraction()
            for k in reversed(range(3)):
                sx = sum((p for value, p in x_pmf.items() if value >= k), Fraction())
                sy = sum((p for value, p in y_pmf.items() if value >= k), Fraction())
                survival = sx * sy
                value = survival - next_survival
                steps.extend([step("M", prob_txt(sx), prob_txt(sy),
                                   prob_txt(survival)),
                              step("CDF_ROW", f"P(M≥{k})", prob_txt(survival)),
                              step("S", prob_txt(survival), prob_txt(next_survival),
                                   prob_txt(value)),
                              step("CONV_SUM", f"M={k}", prob_txt(value))])
                output[k], next_survival = value, survival
        steps.append(step("CHECK", "Σ P(M=k)",
                          prob_txt(sum(output.values(), Fraction()))))
        return prefix, steps, _answer_pmf("M", output)

    @staticmethod
    def _binomial():
        n1, n2 = random.randint(2, 4), random.randint(2, 4)
        p = random.choice(P_BANK)
        total = n1 + n2
        k = random.choice([value for value in range(total + 1)
                           if value not in (1, total - 1)])
        coefficient = math.comb(total, k)
        pk, qk = p ** k, (1 - p) ** (total - k)
        partial, probability = coefficient * pk, coefficient * pk * qk
        venue, city, name = _setting()
        prefix = (f"At the {venue} in {city}, {name} has independent "
                  f"X~Binomial({n1},{prob_txt(p)}) and "
                  f"Y~Binomial({n2},{prob_txt(p)}). Let S=X+Y. Target: P(S={k}).")
        steps = [step("DIST_RULE", "independent binomials with common p",
                      f"S~Binomial({total},{prob_txt(p)})"),
                 step("NCR", f"C({total}, {k})", coefficient),
                 step("POW", f"({prob_txt(p)})^{k}", prob_txt(pk)),
                 step("POW", f"({prob_txt(1 - p)})^{total - k}", prob_txt(qk)),
                 step("M", coefficient, prob_txt(pk), prob_txt(partial)),
                 step("M", prob_txt(partial), prob_txt(qk), prob_txt(probability))]
        answer = f"Binomial({total}, {prob_txt(p)}); P(S={k}) = {prob_txt(probability)}"
        return prefix, steps, answer

    @staticmethod
    def _poisson():
        lambda1, lambda2 = random.randint(1, 20), random.randint(1, 20)
        total = lambda1 + lambda2
        venue, city, name = _setting()
        prefix = (f"At the {venue} in {city}, {name} has independent "
                  f"X~Poisson({lambda1}) and Y~Poisson({lambda2}). Let S=X+Y.")
        steps = [step("DIST_RULE", "independent Poisson sum",
                      "rates add"),
                 step("A", lambda1, lambda2, total),
                 step("CHECK", "Poisson mean equals variance", total, total)]
        answer = f"Poisson({total}); mean {total}; variance {total}"
        return prefix, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "convolution_pmf":
            prefix, steps, answer = self._convolution_variant(False)
        elif variant == "single_value":
            prefix, steps, answer = self._convolution_variant(True)
        elif variant == "weighted_dice_sum":
            prefix, steps, answer = self._weighted_dice()
        elif variant == "max_of_two":
            prefix, steps, answer = self._extreme(True)
        elif variant == "min_of_two":
            prefix, steps, answer = self._extreme(False)
        elif variant == "sum_binomial_rule":
            prefix, steps, answer = self._binomial()
        else:
            prefix, steps, answer = self._poisson()
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_distribution_sum_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
