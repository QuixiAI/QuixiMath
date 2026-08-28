"""Estimate event probabilities by scanning supplied random digits.

Variants: ``estimate_from_digits``, ``assign_digits``,
``two_digit_blocks``, and ``compare_to_theoretical``. Op-codes:
``DIGIT_MAP``, ``DIGIT_SCAN``, ``COUNT``, ``PROB_SETUP``, ``F``, ``TERM``,
``SUM``, and ``Z``. Random digit streams, event thresholds, probabilities,
and five phrasings per variant give an unbounded problem space.
"""
import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt


PROBABILITY = True
QUERIES = {
    "estimate_from_digits": (
        "Estimate the event probability from these simulated games.",
        "Use the digit stream to find the relative frequency of the event.",
        "Scan every game and report the exact simulation estimate.",
        "Count the successful games, then divide by the number simulated.",
        "Determine the observed chance of meeting the make threshold.",
    ),
    "assign_digits": (
        "Assign the digits, run the simulation, and give the map with the estimate.",
        "Use the smallest-digit convention and report both assignment and result.",
        "State the success and failure ranges before giving the simulated chance.",
        "Build the digit map, scan the trials, and report the exact estimate.",
        "Give a composite answer containing the assignment and relative frequency.",
    ),
    "two_digit_blocks": (
        "Estimate the event probability from the two-digit blocks.",
        "Scan the 00-through-99 simulation and report its relative frequency.",
        "Count which two-digit values fall in the success range.",
        "Use every displayed block to compute the exact simulation estimate.",
        "Determine the observed success chance from this two-digit model.",
    ),
    "compare_to_theoretical": (
        "Compare the simulation estimate with the exact theoretical probability.",
        "Report both the observed fraction and the binomial-model probability.",
        "Scan the games, then calculate the theoretical chance for comparison.",
        "Give the simulated estimate and the exact probability side by side.",
        "Use the random digits and an exact binomial sum to compare the two values.",
    ),
}


def _digit_ranges(success_digits):
    """Canonical success/failure labels for a single random digit."""
    return f"0–{success_digits - 1}", f"{success_digits}–9"


def _blocks(width, count):
    return tuple("".join(str(random.randrange(10)) for _ in range(width))
                 for _ in range(count))


def _scan_games(blocks, success_digits, threshold):
    steps = []
    successful = 0
    for block in blocks:
        makes = sum(int(digit) < success_digits for digit in block)
        verdict = "yes" if makes >= threshold else "no"
        successful += verdict == "yes"
        steps.append(step("DIGIT_SCAN", block, f"makes {makes}", verdict))
    return steps, successful


def _estimate_steps(successful, total):
    value = Fraction(successful, total)
    steps = [step("COUNT", "successful blocks", successful),
             step("PROB_SETUP", successful, total)]
    raw = f"{successful}/{total}"
    if raw != prob_txt(value):
        steps.append(step("F", raw, prob_txt(value)))
    return steps, value


class RandomDigitSimulationGenerator(ProblemGenerator):
    """Generate exact random-digit simulation exercises."""

    VARIANTS = ("estimate_from_digits", "assign_digits",
                "two_digit_blocks", "compare_to_theoretical")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _single_digit(variant):
        success_digits = random.randint(1, 9)
        shots = random.randint(2, 5)
        threshold = random.randint(1, shots)
        blocks = _blocks(shots, random.randint(8, 20))
        success_range, failure_range = _digit_ranges(success_digits)
        probability = prob_txt(Fraction(success_digits, 10))

        if variant == "assign_digits":
            prefix = (f"An attempt succeeds with probability {probability}. Use the "
                      "convention that the smallest digits starting at 0 represent "
                      f"success. Each block of {shots} digits is one trial of "
                      f"{shots} attempts. Random digits: {' '.join(blocks)}. Event: "
                      f"at least {threshold} successes.")
            event_word = "success"
        else:
            prefix = (f"A free throw succeeds with probability {probability}. Digits "
                      f"{success_range} mean make and digits {failure_range} mean "
                      f"miss. Each block of {shots} digits is one game of {shots} "
                      f"shots. Random digits: {' '.join(blocks)}. Event: at least "
                      f"{threshold} makes.")
            event_word = "make"

        steps = [step("DIGIT_MAP", event_word,
                      f"{success_range} ({success_digits} of 10 digits)")]
        scan_steps, successful = _scan_games(blocks, success_digits, threshold)
        steps.extend(scan_steps)
        estimate_steps, estimate = _estimate_steps(successful, len(blocks))
        steps.extend(estimate_steps)

        if variant == "assign_digits":
            answer = (f"{success_range} success, {failure_range} failure; "
                      f"{prob_txt(estimate)}")
        elif variant == "compare_to_theoretical":
            p = Fraction(success_digits, 10)
            terms = []
            for makes in range(threshold, shots + 1):
                combinations = math.comb(shots, makes)
                term = combinations * p ** makes * (1 - p) ** (shots - makes)
                factors = []
                if combinations != 1:
                    factors.append(str(combinations))
                factors.append(f"({prob_txt(p)})" if makes == 1
                               else f"({prob_txt(p)})^{makes}")
                misses = shots - makes
                if misses == 1:
                    factors.append(f"({prob_txt(1 - p)})")
                elif misses > 1:
                    factors.append(f"({prob_txt(1 - p)})^{misses}")
                steps.append(step("TERM", f"{makes} makes", " × ".join(factors),
                                  prob_txt(term)))
                terms.append(term)
            theoretical = sum(terms, Fraction())
            steps.append(step("SUM", " + ".join(prob_txt(term) for term in terms),
                              prob_txt(theoretical)))
            answer = (f"estimate {prob_txt(estimate)}; theoretical "
                      f"{prob_txt(theoretical)}")
        else:
            answer = prob_txt(estimate)
        return prefix, steps, answer

    @staticmethod
    def _two_digit():
        success_count = random.randint(2, 98)
        blocks = _blocks(2, random.randint(10, 30))
        success_end = success_count - 1
        success_range = f"00–{success_end:02d}"
        failure_range = f"{success_count:02d}–99"
        probability = prob_txt(Fraction(success_count, 100))
        prefix = (f"An event has probability {probability}. Use two-digit blocks "
                  f"00 through 99: blocks {success_range} represent success and "
                  f"blocks {failure_range} represent failure. Random blocks: "
                  f"{' '.join(blocks)}.")
        steps = [step("DIGIT_MAP", "success",
                      f"{success_range} ({success_count} of 100 blocks)")]
        successful = 0
        for block in blocks:
            value = int(block)
            verdict = "yes" if value < success_count else "no"
            successful += verdict == "yes"
            steps.append(step("DIGIT_SCAN", block, f"value {value}", verdict))
        estimate_steps, estimate = _estimate_steps(successful, len(blocks))
        steps.extend(estimate_steps)
        return prefix, steps, prob_txt(estimate)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "two_digit_blocks":
            prefix, steps, answer = self._two_digit()
        else:
            prefix, steps, answer = self._single_digit(variant)
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_random_digit_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
