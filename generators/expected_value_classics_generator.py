"""Compute classic exact expectations and matching probabilities.

Variants: ``coupon_collector``, ``coupon_next``, ``coupon_first_k``,
``coupon_all_in_n``, ``matching_at_least_one``, ``matching_exactly_k``,
``buffon_probability``, ``buffon_pi_estimate``, and
``st_petersburg_truncated``. Op-codes: ``LINEARITY``, ``COUPON_STAGE``,
``HARMONIC_NUMBER``, ``IE_FORMULA``, ``DERANGE_ROW``, ``BUFFON_FORMULA``,
``PI_FORM``, ``STP_TERM``, ``NCR``, ``FACT``, ``POW``, ``A``, ``S``, ``M``,
``D``, ``CHECK``, and ``Z``.
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
ITEMS = ("toys", "cards", "badges", "stickers", "tokens", "figures",
         "posters", "codes")
QUERIES = {
    "coupon_collector": (
        "Find the exact expected draws needed to collect every type.",
        "Use the coupon-collector harmonic sum.",
        "Compute the total expected waiting time for a complete collection.",
        "Add the stagewise waits for all remaining new types.",
        "Evaluate n times H_n exactly.",
    ),
    "coupon_next": (
        "Find the expected additional draws until the next new type.",
        "Use the current probability of drawing an unseen type.",
        "Compute the exact one-stage coupon wait.",
        "How long is the expected wait for one more distinct type?",
        "Evaluate the reciprocal new-type probability.",
    ),
    "coupon_first_k": (
        "Find the expected draws needed to collect k distinct types.",
        "Add the stagewise waits through the kth new type.",
        "Compute this partial coupon-collector expectation.",
        "Evaluate the exact wait for the first k distinct outcomes.",
        "Use linearity over the successive collection stages.",
    ),
    "coupon_all_in_n": (
        "Find the exact probability that every type appears.",
        "Count the draw orders containing each type once.",
        "Compute the probability of completing the collection in exactly n draws.",
        "Evaluate n factorial divided by n to the nth power.",
        "Find the chance that the first n draws are all different.",
    ),
    "matching_at_least_one": (
        "Find the probability of at least one fixed point.",
        "Use inclusion-exclusion on the matching events.",
        "Compute the classic matching probability exactly.",
        "What is the chance that someone receives their own item?",
        "Evaluate the alternating fixed-point sum.",
    ),
    "matching_exactly_k": (
        "Find the probability of exactly k fixed points.",
        "Choose the fixed positions and derange the rest.",
        "Compute this exact matching-count probability.",
        "Evaluate C(n,k)D_(n-k)/n factorial.",
        "Count permutations with precisely the requested matches.",
    ),
    "buffon_probability": (
        "Find the exact symbolic crossing probability.",
        "Use Buffon's needle formula for L no greater than d.",
        "Compute 2L divided by pi times d.",
        "Evaluate the crossing chance as a reduced pi-form.",
        "Find the exact line-crossing probability.",
    ),
    "buffon_pi_estimate": (
        "Find the exact rational estimate of pi.",
        "Use pi approximately equal to 2n divided by the crossing count.",
        "Compute the Buffon estimate from these trials.",
        "Invert the observed crossing fraction to estimate pi.",
        "Evaluate the equal-length Buffon estimator exactly.",
    ),
    "st_petersburg_truncated": (
        "Find the exact expected payout of the truncated game.",
        "Add the first-tail payout contributions through the cutoff.",
        "Compute the finite St. Petersburg expectation.",
        "Evaluate each probability-times-payout term and sum them.",
        "Find the mean payout when no tail by the cutoff pays zero.",
    ),
}


def _context():
    return (f"At the {random.choice(VENUES)} in {random.choice(CITIES)}, "
            f"{random.choice(NAMES)} analyzes a classic probability model.")


def _power(base, exponent):
    value = base ** exponent
    return step("POW", f"base {prob_txt(base)}, exponent {exponent}",
                prob_txt(value)), value


def _sum_values(steps, values):
    running = values[0]
    for value in values[1:]:
        steps.append(step("A", prob_txt(running), prob_txt(value),
                          prob_txt(running + value)))
        running += value
    return running


def _derangement_steps(size):
    values = [1]
    steps = [step("DERANGE_ROW", 0, 1)]
    if size == 0:
        return steps, 1
    values.append(0)
    steps.append(step("DERANGE_ROW", 1, 0))
    for index in range(2, size + 1):
        subtotal = values[index - 1] + values[index - 2]
        value = (index - 1) * subtotal
        steps.extend([
            step("A", values[index - 1], values[index - 2], subtotal),
            step("M", index - 1, subtotal, value),
            step("DERANGE_ROW", index, value),
        ])
        values.append(value)
    return steps, values[size]


def _pi_form(coefficient):
    coefficient = Fraction(coefficient)
    numerator, denominator = coefficient.numerator, coefficient.denominator
    if denominator == 1:
        return "1/π" if numerator == 1 else f"{numerator}/π"
    if numerator == 1:
        return f"1/({denominator}π)"
    return f"{numerator}/({denominator}π)"


class ExpectedValueClassicsGenerator(ProblemGenerator):
    """Generate coupon, matching, Buffon, and St. Petersburg exercises."""

    VARIANTS = ("coupon_collector", "coupon_next", "coupon_first_k",
                "coupon_all_in_n", "matching_at_least_one",
                "matching_exactly_k", "buffon_probability",
                "buffon_pi_estimate", "st_petersburg_truncated")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _coupon_collector():
        count = random.randint(3, 8)
        item = random.choice(ITEMS)
        problem = (f"{_context()} Each draw independently produces one of n="
                   f"{count} equally likely {item}. Target: the expected draws "
                   f"to collect all {count} types.")
        terms = [Fraction(1, remaining) for remaining in range(1, count + 1)]
        steps = [step("LINEARITY", "E[T]=n*H_n",
                      " + ".join("1" if value == 1 else f"1/{value}"
                                 for value in range(1, count + 1)))]
        for remaining, term in enumerate(terms, 1):
            steps.append(step("D", 1, remaining, prob_txt(term)))
        harmonic = _sum_values(steps, terms)
        expectation = count * harmonic
        steps.extend([
            step("HARMONIC_NUMBER", f"H_{count}", prob_txt(harmonic)),
            step("M", count, prob_txt(harmonic), prob_txt(expectation)),
            step("CHECK", "last unseen type has expected wait", count),
        ])
        return problem, steps, prob_txt(expectation)

    @staticmethod
    def _coupon_next():
        count = random.randint(4, 10)
        collected = random.randint(1, count - 1)
        unseen = count - collected
        new_probability = Fraction(unseen, count)
        expectation = 1 / new_probability
        item = random.choice(ITEMS)
        problem = (f"{_context()} There are n={count} equally likely {item}, "
                   f"and {collected} distinct types have been collected. Target: "
                   f"the expected additional draws until a new type appears.")
        steps = [
            step("COUPON_STAGE", f"collected={collected}, unseen={unseen}",
                 f"new probability={prob_txt(new_probability)}"),
            step("D", unseen, count, prob_txt(new_probability)),
            step("D", 1, prob_txt(new_probability), prob_txt(expectation)),
            step("CHECK", "geometric wait for a new type", prob_txt(expectation)),
        ]
        return problem, steps, prob_txt(expectation)

    @staticmethod
    def _coupon_first_k():
        count = random.randint(4, 10)
        target_count = random.randint(2, count - 1)
        item = random.choice(ITEMS)
        problem = (f"{_context()} Each draw independently produces one of n="
                   f"{count} equally likely {item}. Target: the expected draws "
                   f"to collect k={target_count} distinct types.")
        steps = [step("LINEARITY", "sum stagewise waits",
                      f"stages 0 through {target_count - 1} collected")]
        terms = []
        for collected in range(target_count):
            unseen = count - collected
            probability = Fraction(unseen, count)
            wait = 1 / probability
            steps.extend([
                step("COUPON_STAGE", f"collected={collected}, unseen={unseen}",
                     f"new probability={prob_txt(probability)}"),
                step("D", count, unseen, prob_txt(wait)),
            ])
            terms.append(wait)
        expectation = _sum_values(steps, terms)
        steps.append(step("CHECK", f"{target_count} collection stages",
                          prob_txt(expectation)))
        return problem, steps, prob_txt(expectation)

    @staticmethod
    def _coupon_all_in_n():
        count = random.randint(3, 6)
        item = random.choice(ITEMS)
        factorial = math.factorial(count)
        power = count ** count
        probability = Fraction(factorial, power)
        problem = (f"{_context()} Each of n={count} draws independently produces "
                   f"one of {count} equally likely {item}. Target: the probability "
                   f"that all {count} types appear in these {count} draws.")
        steps = [
            step("LINEARITY", "favorable orders=n!", "total sequences=n^n"),
            step("FACT", count, factorial),
            step("POW", f"base {count}, exponent {count}", power),
            step("D", factorial, power, prob_txt(probability)),
            step("CHECK", "all types in n draws means each appears once",
                 factorial),
        ]
        return problem, steps, prob_txt(probability)

    @staticmethod
    def _matching_at_least_one():
        count = random.randint(3, 7)
        problem = (f"{_context()} A uniformly random permutation assigns n="
                   f"{count} labeled items to {count} labeled owners. Target: "
                   f"the probability of at least one fixed point.")
        steps = [step("IE_FORMULA", "P(at least one)=sum from j=1 to n of "
                      "(-1)^(j+1)/j!")]
        terms = []
        for index in range(1, count + 1):
            factorial = math.factorial(index)
            magnitude = Fraction(1, factorial)
            term = magnitude if index % 2 else -magnitude
            steps.extend([
                step("FACT", index, factorial),
                step("D", 1, factorial, prob_txt(magnitude)),
            ])
            if term < 0:
                steps.append(step("M", prob_txt(magnitude), -1, prob_txt(term)))
            terms.append(term)
        probability = _sum_values(steps, terms)
        steps.append(step("CHECK", "inclusion-exclusion result in [0,1]",
                          prob_txt(probability)))
        return problem, steps, prob_txt(probability)

    @staticmethod
    def _matching_exactly_k():
        count = random.randint(3, 7)
        feasible = list(range(count - 1))
        fixed = random.choice(feasible)
        remaining = count - fixed
        problem = (f"{_context()} A uniformly random permutation assigns n="
                   f"{count} labeled items to {count} labeled owners. Target: "
                   f"the probability of exactly k={fixed} fixed points.")
        coefficient = math.comb(count, fixed)
        derange_steps, derangements = _derangement_steps(remaining)
        favorable = coefficient * derangements
        total = math.factorial(count)
        probability = Fraction(favorable, total)
        steps = [
            step("IE_FORMULA", "exactly k fixed points=C(n,k)D_(n-k)/n!"),
            step("NCR", f"C({count}, {fixed})", coefficient),
        ]
        steps.extend(derange_steps)
        steps.extend([
            step("M", coefficient, derangements, favorable),
            step("FACT", count, total),
            step("D", favorable, total, prob_txt(probability)),
            step("CHECK", f"remaining {remaining} positions deranged",
                 derangements),
        ])
        return problem, steps, prob_txt(probability)

    @staticmethod
    def _buffon_probability():
        spacing = random.randint(2, 12)
        length = random.randint(1, spacing)
        numerator = 2 * length
        coefficient = Fraction(numerator, spacing)
        answer = _pi_form(coefficient)
        problem = (f"{_context()} Parallel lines are d={spacing} units apart, "
                   f"and a randomly dropped needle has length L={length}, with "
                   f"L≤d. Target: the exact Buffon crossing probability.")
        steps = [
            step("BUFFON_FORMULA", "P(cross)=2L/(pi*d)"),
            step("M", 2, length, numerator),
            step("D", numerator, spacing, prob_txt(coefficient)),
            step("PI_FORM", f"{prob_txt(coefficient)}/pi", answer),
            step("CHECK", "L≤d", f"{length}≤{spacing}"),
        ]
        return problem, steps, answer

    @staticmethod
    def _buffon_estimate():
        trials = random.choice((40, 50, 60, 80, 100, 120, 160, 200))
        crossings = random.randint(max(1, trials // 3), max(2, 4 * trials // 5))
        twice_trials = 2 * trials
        estimate = Fraction(twice_trials, crossings)
        problem = (f"{_context()} A Buffon experiment uses needle length L equal "
                   f"to line spacing d. Among n={trials} drops, crossings="
                   f"{crossings}. Target: the estimate pi≈2n/crossings.")
        steps = [
            step("BUFFON_FORMULA", "crossing fraction≈2/pi",
                 "pi estimate=2n/crossings"),
            step("M", 2, trials, twice_trials),
            step("D", twice_trials, crossings, prob_txt(estimate)),
            step("CHECK", "positive crossing count", crossings),
        ]
        return problem, steps, f"pi estimate = {prob_txt(estimate)}"

    @staticmethod
    def _st_petersburg():
        cutoff = random.randint(3, 9)
        problem = (f"{_context()} A fair coin is tossed until the first tail or "
                   f"a cutoff of m={cutoff} tosses. If the first tail is on toss "
                   f"k≤m, the payout is 2^k units; no tail by m pays 0. Target: "
                   f"the exact expected payout.")
        steps = [step("LINEARITY", "sum probability times payout", f"k=1 to {cutoff}")]
        contributions = []
        for index in range(1, cutoff + 1):
            probability_step, probability = _power(Fraction(1, 2), index)
            payout_step, payout = _power(Fraction(2), index)
            contribution = probability * payout
            steps.extend([
                probability_step, payout_step,
                step("M", prob_txt(probability), payout, prob_txt(contribution)),
                step("STP_TERM", f"k={index}", prob_txt(contribution)),
            ])
            contributions.append(contribution)
        expectation = _sum_values(steps, contributions)
        steps.append(step("CHECK", "no-tail-by-m payout contribution", 0))
        return problem, steps, f"expected payout = {prob_txt(expectation)}"

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "coupon_collector":
            problem, steps, answer = self._coupon_collector()
        elif variant == "coupon_next":
            problem, steps, answer = self._coupon_next()
        elif variant == "coupon_first_k":
            problem, steps, answer = self._coupon_first_k()
        elif variant == "coupon_all_in_n":
            problem, steps, answer = self._coupon_all_in_n()
        elif variant == "matching_at_least_one":
            problem, steps, answer = self._matching_at_least_one()
        elif variant == "matching_exactly_k":
            problem, steps, answer = self._matching_exactly_k()
        elif variant == "buffon_probability":
            problem, steps, answer = self._buffon_probability()
        elif variant == "buffon_pi_estimate":
            problem, steps, answer = self._buffon_estimate()
        else:
            problem, steps, answer = self._st_petersburg()
        problem = f"{problem} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_expected_value_classics_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
