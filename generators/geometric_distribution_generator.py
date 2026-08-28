"""Compute exact geometric probabilities, tails, and waiting times.

Variants: ``exact_k``, ``at_most``, ``after_k``, ``mean``,
``memoryless_verify``, ``conditional_tail``, and ``remaining_wait``.
Op-codes: ``GEOM_SETUP``, ``GEOM_FORMULA``, ``POW``, ``M``, ``S``, ``D``,
``CHECK``, and ``Z``. Context banks and five phrasings per variant provide
large capacity while every answer stays an exact reduced fraction.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt


PROBABILITY = True
PS = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 4), Fraction(1, 5),
      Fraction(2, 5), Fraction(3, 10), Fraction(3, 4), Fraction(7, 10),
      Fraction(1, 6), Fraction(5, 6), Fraction(2, 3), Fraction(3, 5),
      Fraction(4, 5))
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
    "exact_k": (
        "Find this exact first-success probability.",
        "Use the geometric point-mass formula.",
        "Compute the chance of first succeeding on the target trial.",
        "Evaluate P(X=k) as a reduced fraction.",
        "Account for the preceding failures and final success.",
    ),
    "at_most": (
        "Find this exact cumulative probability.",
        "Use the complement of failing every stated trial.",
        "Compute the chance of success by the target trial.",
        "Evaluate P(X≤k) as a reduced fraction.",
        "Find the geometric cdf at the stated cutoff.",
    ),
    "after_k": (
        "Find this exact tail probability.",
        "Compute the chance that all stated trials fail.",
        "Use the geometric survival function.",
        "Evaluate P(X>k) as a reduced fraction.",
        "Find the probability that the first success comes later.",
    ),
    "mean": (
        "Find the expected trial number of the first success.",
        "Compute the exact geometric mean.",
        "Use E[X]=1/p.",
        "What is the expected waiting time in trials?",
        "Evaluate the first-success mean exactly.",
    ),
    "memoryless_verify": (
        "Verify the memoryless identity with a composite exact answer.",
        "Compute both equal tail probabilities and display their equality.",
        "Show that prior failures do not change the remaining tail chance.",
        "Evaluate the conditional tail and its fresh-start counterpart.",
        "Confirm geometric memorylessness for these cutoffs.",
    ),
    "conditional_tail": (
        "Find this exact conditional tail probability.",
        "Use the memoryless property to remove the elapsed failures.",
        "Compute the chance of waiting beyond the later cutoff given the earlier one.",
        "Evaluate the conditional geometric survival probability.",
        "Reduce this given-tail probability to lowest terms.",
    ),
    "remaining_wait": (
        "Find the expected additional wait after the stated failures.",
        "Use memorylessness to compute the remaining mean.",
        "Evaluate the conditional expected trials still needed.",
        "What is E[X-m given X>m] exactly?",
        "Find the fresh-start expected wait after the elapsed trials.",
    ),
}


def exact(fr):
    """Compatibility alias for the probability strand's fraction renderer."""
    return prob_txt(fr)


def pow_step(base, exponent):
    value = base ** exponent
    return step("POW", f"base {prob_txt(base)}, exponent {exponent}",
                prob_txt(value)), value


def _prefix(p, target):
    venue = random.choice(VENUES)
    city = random.choice(CITIES)
    name = random.choice(NAMES)
    return (f"At the {venue} in {city}, {name} repeats independent trials with "
            f"success probability p={prob_txt(p)}. Let X be the trial number of "
            f"the first success. Target: {target}.")


class GeometricDistributionGenerator(ProblemGenerator):
    """Generate exact geometric distribution and memorylessness exercises."""

    VARIANTS = ("exact_k", "at_most", "after_k", "mean",
                "memoryless_verify", "conditional_tail", "remaining_wait")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _exact_k(p, q):
        k = random.randint(2, 9)
        raw, q_power = pow_step(q, k - 1)
        probability = q_power * p
        steps = [
            step("GEOM_SETUP", f"p={prob_txt(p)}, q={prob_txt(q)}", f"P(X={k})"),
            step("GEOM_FORMULA", "P(X=k)=q^(k-1)p"),
            raw,
            step("M", prob_txt(q_power), prob_txt(p), prob_txt(probability)),
            step("CHECK", f"{k - 1} failures then success", prob_txt(probability)),
        ]
        return _prefix(p, f"P(X={k})"), steps, prob_txt(probability)

    @staticmethod
    def _at_most(p, q):
        k = random.randint(2, 9)
        raw, q_power = pow_step(q, k)
        probability = 1 - q_power
        steps = [
            step("GEOM_SETUP", f"p={prob_txt(p)}, q={prob_txt(q)}", f"P(X≤{k})"),
            step("GEOM_FORMULA", "P(X≤k)=1-q^k"),
            raw,
            step("S", 1, prob_txt(q_power), prob_txt(probability)),
            step("CHECK", "success by k plus fail through k", 1),
        ]
        return _prefix(p, f"P(X≤{k})"), steps, prob_txt(probability)

    @staticmethod
    def _after(p, q):
        k = random.randint(1, 9)
        raw, probability = pow_step(q, k)
        steps = [
            step("GEOM_SETUP", f"p={prob_txt(p)}, q={prob_txt(q)}", f"P(X>{k})"),
            step("GEOM_FORMULA", "P(X>k)=q^k"),
            raw,
            step("CHECK", f"first {k} trials all fail", prob_txt(probability)),
        ]
        return _prefix(p, f"P(X>{k})"), steps, prob_txt(probability)

    @staticmethod
    def _mean(p):
        mean = 1 / p
        steps = [
            step("GEOM_SETUP", f"p={prob_txt(p)}", "E[X]"),
            step("GEOM_FORMULA", "E[X]=1/p"),
            step("D", 1, prob_txt(p), prob_txt(mean)),
            step("CHECK", "first-step equation E[X]=1+(1-p)E[X]",
                 prob_txt(mean)),
        ]
        return _prefix(p, "E[X]"), steps, prob_txt(mean)

    @staticmethod
    def _conditional(p, q, verify):
        earlier = random.randint(1, 5)
        later = random.randint(earlier + 1, earlier + 6)
        gap = later - earlier
        raw, probability = pow_step(q, gap)
        target = f"P(X>{later} given X>{earlier})"
        steps = [
            step("GEOM_SETUP", f"p={prob_txt(p)}, q={prob_txt(q)}", target),
            step("GEOM_FORMULA", "P(X>n given X>m)=q^(n-m)=P(X>n-m)"),
            step("S", later, earlier, gap),
            raw,
            step("CHECK", target, f"P(X>{gap})", prob_txt(probability)),
        ]
        problem = _prefix(p, target)
        if verify:
            answer = (f"P(X > {later} given X > {earlier}) = "
                      f"{prob_txt(probability)} = P(X > {gap})")
        else:
            answer = prob_txt(probability)
        return problem, steps, answer

    @staticmethod
    def _remaining(p):
        elapsed = random.randint(1, 8)
        mean = 1 / p
        target = f"E[X-{elapsed} given X>{elapsed}]"
        steps = [
            step("GEOM_SETUP", f"p={prob_txt(p)}, elapsed={elapsed}", target),
            step("GEOM_FORMULA", "E[X-m given X>m]=1/p"),
            step("D", 1, prob_txt(p), prob_txt(mean)),
            step("CHECK", "remaining wait has fresh geometric law", prob_txt(mean)),
        ]
        answer = f"E[X - {elapsed} given X > {elapsed}] = {prob_txt(mean)}"
        return _prefix(p, target), steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        p = random.choice(PS)
        q = 1 - p
        if variant == "exact_k":
            problem, steps, answer = self._exact_k(p, q)
        elif variant == "at_most":
            problem, steps, answer = self._at_most(p, q)
        elif variant == "after_k":
            problem, steps, answer = self._after(p, q)
        elif variant == "mean":
            problem, steps, answer = self._mean(p)
        elif variant == "memoryless_verify":
            problem, steps, answer = self._conditional(p, q, True)
        elif variant == "conditional_tail":
            problem, steps, answer = self._conditional(p, q, False)
        else:
            problem, steps, answer = self._remaining(p)
        problem = f"{problem} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"geometric_distribution_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
