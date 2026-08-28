"""Convert exact arrangement and code counts into probabilities.

Variants: ``first_letter``, ``no_repeats_code``, ``friends_adjacent``,
``specific_position``, and ``ends_with_even``. Op-codes: ``COUNT_SETUP``,
``FACT``, ``E``, ``FCP``, ``M``, ``PROB_SETUP``, ``F``, and ``Z``.
Random distinct symbols, people, numbered cards, and five phrasings give an
unbounded problem space while every oracle space stays brute-forceable.
"""
import math
import random
import string
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt, roster


PROBABILITY = True
VOWELS = tuple("AEIOU")
VOWEL_SET = set(VOWELS)
CONSONANTS = tuple(letter for letter in string.ascii_uppercase
                   if letter not in VOWEL_SET)
NAMES = ("Ari", "Bea", "Cleo", "Dara", "Eli", "Finn", "Gia", "Hugo",
         "Iris", "Jae", "Kira", "Luca", "Mara", "Nico", "Omar", "Pia",
         "Quin", "Ravi", "Sage", "Tara", "Uma", "Vera", "Wade", "Xena",
         "Yara", "Zane", "Bo", "Cy", "Dee", "Flo", "Gus", "Hope")
QUERIES = {
    "first_letter": (
        "Find the probability that the arrangement begins with a vowel.",
        "Count the vowel-first arrangements and divide by all arrangements.",
        "What is the exact chance that a vowel occupies the first position?",
        "Use factorial counts to compute the probability of a vowel first.",
        "Determine the favorable-to-total ratio for a vowel beginning.",
    ),
    "no_repeats_code": (
        "Find the probability that the selected code has no repeated symbol.",
        "Count repetition-free codes and divide by the full code space.",
        "What is the exact chance that every code position is different?",
        "Use decreasing choices to compute the no-repeat probability.",
        "Determine the favorable-to-total ratio for distinct code symbols.",
    ),
    "friends_adjacent": (
        "Find the probability that the two named friends stand next to each other.",
        "Treat the friends as a block and compute the exact adjacent chance.",
        "Count lineups with the named pair together, then divide by all lineups.",
        "What is the probability that the selected friends are consecutive?",
        "Use the two internal friend orders and the block arrangements.",
    ),
    "specific_position": (
        "Find the probability that the target symbol occupies the stated position.",
        "Count arrangements fixing the target in place and divide by all arrangements.",
        "What is the exact chance of the requested symbol-position match?",
        "Use factorial counts for the fixed-position event.",
        "Determine the favorable-to-total ratio for the displayed position condition.",
    ),
    "ends_with_even": (
        "Find the probability that the arrangement ends with an even number.",
        "Count rows with an even final card and divide by all card arrangements.",
        "What is the exact chance that the last numbered card is even?",
        "Use the available even cards as the final-position choices.",
        "Determine the favorable-to-total ratio for an even ending.",
    ),
}


def _probability_steps(favorable, total):
    value = Fraction(favorable, total)
    raw = f"{favorable}/{total}"
    steps = [step("PROB_SETUP", favorable, total)]
    if raw != prob_txt(value):
        steps.append(step("F", raw, prob_txt(value)))
    return steps, prob_txt(value)


def _distinct_letters(count):
    return tuple(random.sample(string.ascii_uppercase, count))


class CountingToProbabilityGenerator(ProblemGenerator):
    """Generate probability exercises whose numerator is a counting result."""

    VARIANTS = ("first_letter", "no_repeats_code", "friends_adjacent",
                "specific_position", "ends_with_even")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _first_letter():
        n = random.randint(4, 7)
        vowel_count = random.randint(1, min(3, n - 1))
        letters = random.sample(VOWELS, vowel_count)
        letters += random.sample(CONSONANTS, n - vowel_count)
        random.shuffle(letters)
        codeword = "".join(letters)
        total = math.factorial(n)
        tail = math.factorial(n - 1)
        favorable = vowel_count * tail
        prefix = (f"The distinct letters of codeword {codeword} are arranged "
                  "uniformly at random.")
        steps = [step("COUNT_SETUP", f"arrangements of {codeword}", f"{n}!"),
                 step("FACT", n, total),
                 step("FCP", "first letter", vowel_count, vowel_count),
                 step("FACT", n - 1, tail),
                 step("M", vowel_count, tail, favorable)]
        extra, answer = _probability_steps(favorable, total)
        return prefix, steps + extra, answer

    @staticmethod
    def _no_repeats():
        base = random.randint(5, 10)
        length = random.randint(2, min(5, base))
        symbols = tuple(sorted(random.sample(string.ascii_uppercase, base)))
        total = base ** length
        steps = [step("COUNT_SETUP", f"all length-{length} codes", f"{base}^{length}"),
                 step("E", base, length, total)]
        running = 1
        for position in range(length):
            choices = base - position
            running *= choices
            steps.append(step("FCP", f"position {position + 1}", choices, running))
        prefix = (f"A code of length {length} is selected uniformly from all "
                  f"strings over symbols {roster(symbols)}; repetition is allowed "
                  "in the full space.")
        extra, answer = _probability_steps(running, total)
        return prefix, steps + extra, answer

    @staticmethod
    def _friends():
        n = random.randint(4, 7)
        people = tuple(random.sample(NAMES, n))
        first, second = random.sample(people, 2)
        total = math.factorial(n)
        block_arrangements = math.factorial(n - 1)
        favorable = 2 * block_arrangements
        prefix = (f"The people {roster(people)} line up uniformly at random. "
                  f"The named friends are {first} and {second}.")
        steps = [step("COUNT_SETUP", f"lineups of {n} people", f"{n}!"),
                 step("FACT", n, total),
                 step("COUNT_SETUP", "friend block", f"2 × {n - 1}!"),
                 step("FACT", n - 1, block_arrangements),
                 step("M", 2, block_arrangements, favorable)]
        extra, answer = _probability_steps(favorable, total)
        return prefix, steps + extra, answer

    @staticmethod
    def _specific_position():
        n = random.randint(4, 7)
        symbols = _distinct_letters(n)
        target = random.choice(symbols)
        position = random.randint(1, n)
        total = math.factorial(n)
        favorable = math.factorial(n - 1)
        prefix = (f"The distinct symbols {roster(symbols)} are arranged uniformly "
                  f"at random. Target: {target} in position {position}.")
        steps = [step("COUNT_SETUP", f"arrangements of {n} symbols", f"{n}!"),
                 step("FACT", n, total),
                 step("COUNT_SETUP", f"fix {target} in position {position}",
                      f"{n - 1}!"),
                 step("FACT", n - 1, favorable)]
        extra, answer = _probability_steps(favorable, total)
        return prefix, steps + extra, answer

    @staticmethod
    def _ends_even():
        n = random.randint(4, 7)
        while True:
            numbers = tuple(sorted(random.sample(range(0, 100), n)))
            even_count = sum(number % 2 == 0 for number in numbers)
            if 0 < even_count < n:
                break
        total = math.factorial(n)
        tail = math.factorial(n - 1)
        favorable = even_count * tail
        prefix = (f"The distinct numbered cards {roster(numbers)} are arranged "
                  "uniformly at random in a row.")
        steps = [step("COUNT_SETUP", f"arrangements of {n} cards", f"{n}!"),
                 step("FACT", n, total),
                 step("FCP", "even final card", even_count, even_count),
                 step("FACT", n - 1, tail),
                 step("M", even_count, tail, favorable)]
        extra, answer = _probability_steps(favorable, total)
        return prefix, steps + extra, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "first_letter":
            prefix, steps, answer = self._first_letter()
        elif variant == "no_repeats_code":
            prefix, steps, answer = self._no_repeats()
        elif variant == "friends_adjacent":
            prefix, steps, answer = self._friends()
        elif variant == "specific_position":
            prefix, steps, answer = self._specific_position()
        else:
            prefix, steps, answer = self._ends_even()
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_counting_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
