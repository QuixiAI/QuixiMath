"""Compute exact negative-binomial probabilities and moments.

Variants: ``exact_trial``, ``mean``, ``variance``, ``at_most_trials``,
``failures_form``, and ``geometric_special_case``. Op-codes:
``NEGBIN_SETUP``, ``NEGBIN_FORMULA``, ``NCR``, ``POW``, ``TERM``, ``M``,
``A``, ``S``, ``D``, ``CHECK``, and ``Z``. Small r, n, and exact rational
success probabilities keep every weighted sequence hand-computable; varied
settings and five phrasings provide a large problem space.
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
P_BANK = (Fraction(1, 5), Fraction(1, 4), Fraction(1, 3), Fraction(2, 5),
          Fraction(1, 2), Fraction(3, 5), Fraction(2, 3), Fraction(3, 4),
          Fraction(4, 5))
QUERIES = {
    "exact_trial": (
        "Find the probability that the rth success occurs on the stated trial.",
        "Use the negative-binomial point-mass formula.",
        "Count placements of the earlier successes, then include the final success.",
        "What is the exact waiting-time probability?",
        "Compute P(N=n) for the rth-success trial.",
    ),
    "mean": (
        "Find the expected trial of the rth success.",
        "Use E[N]=r/p.",
        "Compute the exact negative-binomial mean.",
        "What is the expected waiting time in trials?",
        "Add the means of r geometric waiting times.",
    ),
    "variance": (
        "Find the variance of the rth-success trial.",
        "Use Var(N)=r(1−p)/p².",
        "Compute the exact negative-binomial variance.",
        "What is the spread of the waiting time?",
        "Add the variances of r geometric waiting times.",
    ),
    "at_most_trials": (
        "Find the probability that the rth success occurs by the stated trial.",
        "Sum the feasible negative-binomial point masses through n.",
        "Compute P(N≤n) exactly.",
        "What is the cumulative rth-success probability?",
        "Add the waiting-time terms from r through the cutoff.",
    ),
    "failures_form": (
        "Find the probability of the stated failures before the rth success.",
        "Use the failures-count form of the negative binomial.",
        "Place the failures and earlier successes before the final success.",
        "What is P(F=f) exactly?",
        "Evaluate C(f+r−1,f)p^r(1−p)^f.",
    ),
    "geometric_special_case": (
        "Find the exact trial probability and mean in the geometric special case.",
        "Set r=1 and compute both P(N=n) and E[N].",
        "Use the first-success waiting-time law.",
        "What are the point mass and expected trial?",
        "Verify that the negative binomial reduces to a geometric distribution.",
    ),
}


def _setting():
    return random.choice(VENUES), random.choice(CITIES), random.choice(NAMES)


def _power_step(base, exponent):
    value = base ** exponent
    return step("POW", f"base {prob_txt(base)}, exponent {exponent}",
                prob_txt(value)), value


def _term(r, n, p):
    return Fraction(math.comb(n - 1, r - 1)) * p ** r * (1 - p) ** (n - r)


def _ordinal(value):
    if 10 <= value % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(value % 10, "th")
    return f"{value}{suffix}"


def _point_steps(r, n, p):
    q = 1 - p
    coefficient = math.comb(n - 1, r - 1)
    p_step, p_power = _power_step(p, r)
    q_step, q_power = _power_step(q, n - r)
    partial = coefficient * p_power
    value = partial * q_power
    return [step("NCR", f"C({n - 1}, {r - 1})", coefficient),
            p_step, q_step,
            step("M", coefficient, prob_txt(p_power), prob_txt(partial)),
            step("M", prob_txt(partial), prob_txt(q_power), prob_txt(value))], value


class NegativeBinomialGenerator(ProblemGenerator):
    """Generate exact rth-success waiting-time exercises."""

    VARIANTS = ("exact_trial", "mean", "variance", "at_most_trials",
                "failures_form", "geometric_special_case")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _prefix(p, text):
        venue, city, name = _setting()
        return (f"At the {venue} in {city}, {name} repeats independent trials "
                f"with success probability p={prob_txt(p)}. {text}")

    @staticmethod
    def _exact():
        p, r = random.choice(P_BANK), random.randint(2, 4)
        n = random.randint(r + 1, min(10, r + 6))
        prefix = NegativeBinomialGenerator._prefix(
            p, f"Let N be the trial of the {_ordinal(r)} success. Target: P(N={n}).")
        steps = [step("NEGBIN_SETUP", f"r={r}, p={prob_txt(p)}, n={n}",
                      f"P(N={n})"),
                 step("NEGBIN_FORMULA",
                      "P(N=n)=C(n−1,r−1)p^r(1−p)^(n−r)")]
        extra, value = _point_steps(r, n, p)
        steps.extend(extra)
        return prefix, steps, prob_txt(value)

    @staticmethod
    def _moment(variance_variant):
        p, r = random.choice(P_BANK), random.randint(2, 6)
        prefix = NegativeBinomialGenerator._prefix(
            p, f"Let N be the trial of the {_ordinal(r)} success.")
        if not variance_variant:
            value = Fraction(r, 1) / p
            steps = [step("NEGBIN_SETUP", f"r={r}, p={prob_txt(p)}", "E[N]"),
                     step("NEGBIN_FORMULA", "E[N]=r/p"),
                     step("D", r, prob_txt(p), prob_txt(value)),
                     step("CHECK", "sum of r geometric means", prob_txt(value))]
        else:
            q = 1 - p
            p_square = p ** 2
            numerator = r * q
            value = numerator / p_square
            steps = [step("NEGBIN_SETUP", f"r={r}, p={prob_txt(p)}", "Var(N)"),
                     step("NEGBIN_FORMULA", "Var(N)=r(1−p)/p²"),
                     step("S", 1, prob_txt(p), prob_txt(q)),
                     step("M", r, prob_txt(q), prob_txt(numerator)),
                     step("POW", f"base {prob_txt(p)}, exponent 2",
                          prob_txt(p_square)),
                     step("D", prob_txt(numerator), prob_txt(p_square),
                          prob_txt(value)),
                     step("CHECK", "sum of r geometric variances",
                          prob_txt(value))]
        return prefix, steps, prob_txt(value)

    @staticmethod
    def _at_most():
        p, r = random.choice(P_BANK), random.randint(2, 4)
        n = random.randint(r + 1, min(10, r + 6))
        prefix = NegativeBinomialGenerator._prefix(
            p, f"Let N be the trial of the {_ordinal(r)} success. Target: P(N≤{n}).")
        steps = [step("NEGBIN_SETUP", f"r={r}, p={prob_txt(p)}, n={n}",
                      f"P(N≤{n})"),
                 step("NEGBIN_FORMULA", "P(N≤n)=Σ from m=r to n of P(N=m)")]
        terms = []
        for trial in range(r, n + 1):
            value = _term(r, trial, p)
            steps.append(step("TERM", f"m={trial}", prob_txt(value)))
            terms.append(value)
        running = terms[0]
        for value in terms[1:]:
            steps.append(step("A", prob_txt(running), prob_txt(value),
                              prob_txt(running + value)))
            running += value
        steps.append(step("CHECK", f"summed trials {r} through {n}",
                          prob_txt(running)))
        return prefix, steps, prob_txt(running)

    @staticmethod
    def _failures():
        p, r, failures = (random.choice(P_BANK), random.randint(2, 4),
                           random.randint(1, 6))
        n = r + failures
        prefix = NegativeBinomialGenerator._prefix(
            p, f"Let F count failures before the {_ordinal(r)} success. "
            f"Target: P(F={failures}).")
        steps = [step("NEGBIN_SETUP", f"r={r}, p={prob_txt(p)}, f={failures}",
                      f"P(F={failures})"),
                 step("NEGBIN_FORMULA",
                      "P(F=f)=C(f+r−1,f)p^r(1−p)^f")]
        extra, value = _point_steps(r, n, p)
        steps.extend(extra)
        return prefix, steps, prob_txt(value)

    @staticmethod
    def _geometric():
        p, n = random.choice(P_BANK), random.randint(2, 10)
        prefix = NegativeBinomialGenerator._prefix(
            p, f"Let N be the trial of the first success. Target: P(N={n}) and E[N].")
        q = 1 - p
        q_step, q_power = _power_step(q, n - 1)
        probability = q_power * p
        mean = 1 / p
        steps = [step("NEGBIN_SETUP", f"r=1, p={prob_txt(p)}, n={n}",
                      "geometric special case"),
                 step("NEGBIN_FORMULA", "P(N=n)=(1−p)^(n−1)p; E[N]=1/p"),
                 q_step,
                 step("M", prob_txt(q_power), prob_txt(p), prob_txt(probability)),
                 step("D", 1, prob_txt(p), prob_txt(mean)),
                 step("CHECK", "r=1 negative binomial equals geometric")]
        answer = f"P(N={n}) = {prob_txt(probability)}; E[N] = {prob_txt(mean)}"
        return prefix, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "exact_trial":
            prefix, steps, answer = self._exact()
        elif variant == "mean":
            prefix, steps, answer = self._moment(False)
        elif variant == "variance":
            prefix, steps, answer = self._moment(True)
        elif variant == "at_most_trials":
            prefix, steps, answer = self._at_most()
        elif variant == "failures_form":
            prefix, steps, answer = self._failures()
        else:
            prefix, steps, answer = self._geometric()
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_negative_binomial_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
