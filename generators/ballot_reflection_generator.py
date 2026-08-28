"""Compute ballot and simple-walk probabilities by reflection.

Variants: ``ballot_probability``, ``paths_touching_level``, ``first_return``,
``max_at_least``, ``stay_nonnegative``, and ``dyck_probability``. Op-codes:
``BALLOT_FORMULA``, ``REFLECT``, ``ENDPOINT_COUNT``, ``CATALAN_FORMULA``,
``NCR``, ``POW``, ``A``, ``S``, ``D``, ``CHECK``, and ``Z``. Ballot order
counts stay below 3,000 and walks use at most 14 steps, enabling exhaustive
oracles over every admissible ordering or plus/minus path.
"""
import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt


PROBABILITY = True
BALLOT_BANK = tuple((a, b) for a in range(3, 13) for b in range(1, a)
                    if math.comb(a + b, b) <= 3000)
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
QUERIES = {
    "ballot_probability": (
        "Find the probability that A is strictly ahead throughout.",
        "Use the strict Bertrand ballot formula.",
        "Compute the exact all-prefix lead probability.",
        "What fraction of count orders keep A ahead after every ballot?",
        "Evaluate the strict ballot probability.",
    ),
    "paths_touching_level": (
        "Find the probability that the walk touches the stated lower level.",
        "Reflect the initial segment through the first boundary hit.",
        "Count paths ending at the target that visit the lower barrier.",
        "Compute this exact boundary-touching probability.",
        "Use the reflection bijection for the constrained endpoint paths.",
    ),
    "first_return": (
        "Find the probability of a first return at the stated time.",
        "Count paths that avoid zero until their final step.",
        "Compute the exact first-return mass.",
        "Use the central-binomial first-return formula.",
        "Evaluate the chance of returning to zero for the first time then.",
    ),
    "max_at_least": (
        "Find the probability that the running maximum reaches the level.",
        "Use reflection to count paths that hit the upper barrier.",
        "Compute P(max S_t at least a) exactly.",
        "Count endpoints at and beyond the reflected threshold.",
        "Evaluate this maximum-crossing probability.",
    ),
    "stay_nonnegative": (
        "Find the probability that every partial sum is nonnegative.",
        "Use reflection to subtract paths that cross below zero.",
        "Compute the exact nonnegative-walk probability.",
        "Count paths that never visit -1.",
        "Evaluate this meander probability.",
    ),
    "dyck_probability": (
        "Find the probability of a nonnegative return path.",
        "Use the Catalan count for Dyck paths.",
        "Compute the chance of staying nonnegative and ending at zero.",
        "Evaluate the exact Dyck-path probability.",
        "Divide the Catalan path count by all symmetric paths.",
    ),
}


def _context():
    return (f"At the {random.choice(VENUES)} in {random.choice(CITIES)}, "
            f"{random.choice(NAMES)} studies a reflection-principle problem.")


def _power_two(exponent):
    value = 2 ** exponent
    return step("POW", f"base 2, exponent {exponent}", value), value


def _sum_counts(steps, counts):
    running = counts[0]
    for count in counts[1:]:
        steps.append(step("A", running, count, running + count))
        running += count
    return running


class BallotReflectionGenerator(ProblemGenerator):
    """Generate exact ballot, reflection, first-return, and Catalan exercises."""

    VARIANTS = ("ballot_probability", "paths_touching_level", "first_return",
                "max_at_least", "stay_nonnegative", "dyck_probability")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _ballot():
        a, b = random.choice(BALLOT_BANK)
        difference = a - b
        total = a + b
        probability = Fraction(difference, total)
        problem = (f"{_context()} Candidate A has a={a} votes and candidate B "
                   f"has b={b} votes. All ballot-count orders are equally likely. "
                   f"Target: P(A is strictly ahead after every counted ballot).")
        steps = [
            step("BALLOT_FORMULA", "strict lead probability=(a-b)/(a+b)"),
            step("S", a, b, difference),
            step("A", a, b, total),
            step("D", difference, total, prob_txt(probability)),
            step("CHECK", "a>b", f"{a}>{b}"),
        ]
        return problem, steps, prob_txt(probability)

    @staticmethod
    def _touching():
        choices = []
        for n in range(4, 15):
            for depth in (1, 2, 3):
                for endpoint in range(-n, n + 1, 2):
                    reflected_magnitude = endpoint + 2 * depth
                    reflected_down = (n - reflected_magnitude) // 2
                    if (endpoint > -depth and (n - reflected_magnitude) % 2 == 0
                            and 0 <= reflected_down <= n):
                        choices.append((n, endpoint, depth, reflected_down))
        n, endpoint, depth, reflected_down = random.choice(choices)
        favorable = math.comb(n, reflected_down)
        total = 2 ** n
        probability = Fraction(favorable, total)
        reflected_endpoint = -(endpoint + 2 * depth)
        problem = (f"{_context()} A simple symmetric walk starts at 0 and takes "
                   f"n={n} steps. Target: the probability that it ends at "
                   f"S_n={endpoint} and touches level -{depth} at least once.")
        steps = [
            step("REFLECT", f"hit -{depth} and end {endpoint}",
                 f"unrestricted endpoint {reflected_endpoint}"),
            step("NCR", f"C({n}, {reflected_down})", favorable),
        ]
        power_step, total = _power_two(n)
        steps.extend([
            power_step,
            step("D", favorable, total, prob_txt(probability)),
            step("CHECK", "reflection is a path bijection", favorable),
        ])
        return problem, steps, prob_txt(probability)

    @staticmethod
    def _first_return():
        half = random.randint(2, 7)
        n = 2 * half
        central = math.comb(n, half)
        divisor = n - 1
        favorable = central // divisor
        total = 2 ** n
        probability = Fraction(favorable, total)
        problem = (f"{_context()} A simple symmetric walk starts at 0. Target: "
                   f"the probability that its first return to 0 occurs at n={n}.")
        steps = [
            step("REFLECT", "first return at 2m", "C(2m,m)/(2m-1) paths"),
            step("NCR", f"C({n}, {half})", central),
            step("D", central, divisor, favorable),
        ]
        power_step, total = _power_two(n)
        steps.extend([
            power_step,
            step("D", favorable, total, prob_txt(probability)),
            step("CHECK", "no earlier zero partial sum", "first return"),
        ])
        return problem, steps, prob_txt(probability)

    @staticmethod
    def _maximum():
        n = random.randint(3, 14)
        level = random.randint(1, min(4, n - 1))
        endpoints_at_or_above = list(range(level + ((n - level) % 2), n + 1, 2))
        endpoints_above = list(range(level + 1 + ((n - level - 1) % 2), n + 1, 2))
        endpoint_counts = {}
        for endpoint in sorted(set(endpoints_at_or_above + endpoints_above)):
            up = (n + endpoint) // 2
            endpoint_counts[endpoint] = math.comb(n, up)
        problem = (f"{_context()} A simple symmetric walk starts at 0 and takes "
                   f"n={n} steps. Target: P(max from t=0 to n of S_t is at "
                   f"least level a={level}).")
        steps = [step("REFLECT", f"maximum at least {level}",
                      "endpoints at least a plus endpoints greater than a")]
        for endpoint, count in endpoint_counts.items():
            up = (n + endpoint) // 2
            steps.extend([step("NCR", f"C({n}, {up})", count),
                          step("ENDPOINT_COUNT", endpoint, count)])
        first_sum = _sum_counts(
            steps, [endpoint_counts[value] for value in endpoints_at_or_above])
        second_sum = _sum_counts(
            steps, [endpoint_counts[value] for value in endpoints_above])
        favorable = first_sum + second_sum
        total = 2 ** n
        probability = Fraction(favorable, total)
        steps.extend([
            step("A", first_sum, second_sum, favorable),
        ])
        power_step, total = _power_two(n)
        steps.extend([
            power_step,
            step("D", favorable, total, prob_txt(probability)),
            step("CHECK", "reflection count", favorable),
        ])
        return problem, steps, prob_txt(probability)

    @staticmethod
    def _stay_nonnegative():
        n = random.randint(2, 14)
        choose = n // 2
        favorable = math.comb(n, choose)
        total = 2 ** n
        probability = Fraction(favorable, total)
        problem = (f"{_context()} A simple symmetric walk starts at 0 and takes "
                   f"n={n} steps. Target: the probability that S_t≥0 for every "
                   f"t from 0 through n.")
        steps = [
            step("REFLECT", "paths ever below 0", "reflect at first visit to -1"),
            step("NCR", f"C({n}, {choose})", favorable),
        ]
        power_step, total = _power_two(n)
        steps.extend([
            power_step,
            step("D", favorable, total, prob_txt(probability)),
            step("CHECK", "nonnegative path count", favorable),
        ])
        return problem, steps, prob_txt(probability)

    @staticmethod
    def _dyck():
        half = random.randint(2, 7)
        n = 2 * half
        central = math.comb(n, half)
        divisor = half + 1
        catalan = central // divisor
        total = 2 ** n
        probability = Fraction(catalan, total)
        problem = (f"{_context()} A simple symmetric walk starts at 0 and takes "
                   f"n={n} steps. Target: the probability that it stays "
                   f"nonnegative and ends at S_n=0.")
        steps = [
            step("CATALAN_FORMULA", "C_m=C(2m,m)/(m+1)"),
            step("NCR", f"C({n}, {half})", central),
            step("A", half, 1, divisor),
            step("D", central, divisor, catalan),
        ]
        power_step, total = _power_two(n)
        steps.extend([
            power_step,
            step("D", catalan, total, prob_txt(probability)),
            step("CHECK", "Dyck path count", catalan),
        ])
        return problem, steps, prob_txt(probability)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "ballot_probability":
            problem, steps, answer = self._ballot()
        elif variant == "paths_touching_level":
            problem, steps, answer = self._touching()
        elif variant == "first_return":
            problem, steps, answer = self._first_return()
        elif variant == "max_at_least":
            problem, steps, answer = self._maximum()
        elif variant == "stay_nonnegative":
            problem, steps, answer = self._stay_nonnegative()
        else:
            problem, steps, answer = self._dyck()
        problem = f"{problem} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_ballot_reflection_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
