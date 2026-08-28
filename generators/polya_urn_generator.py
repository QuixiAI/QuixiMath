"""Compute exact probabilities in a two-color Polya urn.

Variants: ``sequence_probability``, ``exchangeability_check``,
``kth_draw_marginal``, ``count_after_n``, ``expected_red_fraction``, and
``reinforcement_c``. Op-codes: ``POLYA_SETUP``, ``POLYA_STEP``,
``POLYA_COUNT_FORMULA``, ``RISING_FACTOR``, ``NCR``, ``A``, ``M``, ``D``,
``CHECK``, and ``Z``. Draw counts use n at most 6 so tests can recurse over
the full urn-state tree independently.
"""
import itertools
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
QUERIES = {
    "sequence_probability": (
        "Find the exact probability of the stated draw sequence.",
        "Update the urn after every draw and multiply the branch weights.",
        "Compute this ordered Polya-urn path probability.",
        "Evaluate the successive conditional draw probabilities.",
        "Track the reinforced composition along the sequence.",
    ),
    "exchangeability_check": (
        "Find both sequence probabilities and verify exchangeability.",
        "Compute the two reordered path weights and compare them.",
        "Show that only the color totals determine the probability.",
        "Evaluate these equal-count sequences exactly.",
        "Confirm the Polya urn's finite-sequence exchangeability.",
    ),
    "kth_draw_marginal": (
        "Find the exact probability that draw k is red.",
        "Sum every length-k branch ending in red.",
        "Compute the kth-draw red marginal by total probability.",
        "Evaluate the red chance after averaging over prior histories.",
        "Verify that the marginal red probability stays at its initial value.",
    ),
    "count_after_n": (
        "Find the probability of exactly k red draws among n draws.",
        "Use the beta-binomial rising-product formula.",
        "Compute the exact reinforced red-count probability.",
        "Count orderings and weight their common exchangeable probability.",
        "Evaluate this Polya-urn count mass.",
    ),
    "expected_red_fraction": (
        "Find the expected red fraction after n draws.",
        "Use the martingale property of the urn proportion.",
        "Compute the exact expected reinforced composition ratio.",
        "Show that the mean red proportion remains unchanged.",
        "Evaluate the future expected red fraction.",
    ),
    "reinforcement_c": (
        "Find the exact sequence probability with reinforcement c.",
        "Add c matching balls after each replacement and multiply the weights.",
        "Compute this generalized Polya-urn path probability.",
        "Track the c-ball reinforcement through the ordered draws.",
        "Evaluate the stated sequence under non-unit reinforcement.",
    ),
}


def _context():
    return (f"At the {random.choice(VENUES)} in {random.choice(CITIES)}, "
            f"{random.choice(NAMES)} runs a Polya urn experiment.")


def _sequence_text(sequence):
    return ", ".join(sequence)


def _base_problem(red, blue, reinforcement, target):
    return (f"{_context()} Initially the urn has r={red} red and b={blue} blue "
            f"balls. After each draw, the ball is returned with c={reinforcement} "
            f"additional balls of the same color. Target: {target}.")


def _sequence_steps(red, blue, reinforcement, sequence, label=""):
    steps = []
    factors = []
    current_red, current_blue = red, blue
    for index, color in enumerate(sequence, 1):
        total = current_red + current_blue
        numerator = current_red if color == "R" else current_blue
        probability = Fraction(numerator, total)
        if color == "R":
            current_red += reinforcement
        else:
            current_blue += reinforcement
        draw_label = f"{label} draw {index}: {color}" if label else f"draw {index}: {color}"
        steps.extend([
            step("D", numerator, total, prob_txt(probability)),
            step("POLYA_STEP", draw_label, prob_txt(probability),
                 f"{current_red}R {current_blue}B"),
        ])
        factors.append(probability)
    running = factors[0]
    for probability in factors[1:]:
        steps.append(step("M", prob_txt(running), prob_txt(probability),
                          prob_txt(running * probability)))
        running *= probability
    return steps, running


def _rising_steps(start, count, reinforcement, label):
    factors = [start + index * reinforcement for index in range(count)]
    if not factors:
        return [step("RISING_FACTOR", label, "empty product", 1)], 1
    steps = [step("RISING_FACTOR", f"{label} factor {index + 1}", factor)
             for index, factor in enumerate(factors)]
    running = factors[0]
    for factor in factors[1:]:
        steps.append(step("M", running, factor, running * factor))
        running *= factor
    return steps, running


class PolyaUrnGenerator(ProblemGenerator):
    """Generate exact two-color reinforced-urn exercises."""

    VARIANTS = ("sequence_probability", "exchangeability_check",
                "kth_draw_marginal", "count_after_n",
                "expected_red_fraction", "reinforcement_c")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _sequence(general):
        red, blue = random.randint(1, 5), random.randint(1, 5)
        reinforcement = random.randint(2, 4) if general else 1
        length = random.randint(2, 5)
        sequence = [random.choice(("R", "B")) for _ in range(length)]
        target = f"P(sequence {_sequence_text(sequence)})"
        problem = _base_problem(red, blue, reinforcement, target)
        steps = [step("POLYA_SETUP", f"r={red}, b={blue}, c={reinforcement}",
                      target)]
        extra, probability = _sequence_steps(red, blue, reinforcement, sequence)
        steps.extend(extra)
        steps.append(step("CHECK", "one conditional factor per draw", length))
        answer = f"P({_sequence_text(sequence)}) = {prob_txt(probability)}"
        return problem, steps, answer

    @staticmethod
    def _exchangeability():
        red, blue = random.randint(1, 5), random.randint(1, 5)
        reinforcement = random.choice((1, 1, 2, 3))
        length = random.randint(3, 5)
        red_count = random.randint(1, length - 1)
        base = ["R"] * red_count + ["B"] * (length - red_count)
        first = list(base)
        random.shuffle(first)
        second = list(first)
        while second == first:
            random.shuffle(second)
        target = (f"compare P({_sequence_text(first)}) and "
                  f"P({_sequence_text(second)})")
        problem = _base_problem(red, blue, reinforcement, target)
        steps = [step("POLYA_SETUP", f"r={red}, b={blue}, c={reinforcement}",
                      target)]
        first_steps, first_probability = _sequence_steps(
            red, blue, reinforcement, first, "A")
        second_steps, second_probability = _sequence_steps(
            red, blue, reinforcement, second, "B")
        steps.extend(first_steps + second_steps)
        steps.append(step("CHECK", "exchangeability", prob_txt(first_probability),
                          prob_txt(second_probability)))
        answer = (f"P({_sequence_text(first)}) = {prob_txt(first_probability)}; "
                  f"P({_sequence_text(second)}) = {prob_txt(second_probability)}; "
                  f"equal (exchangeable)")
        return problem, steps, answer

    @staticmethod
    def _marginal():
        red, blue = random.randint(1, 5), random.randint(1, 5)
        reinforcement = random.choice((1, 2, 3))
        draw = random.randint(2, 4)
        target = f"P(draw {draw} is R)"
        problem = _base_problem(red, blue, reinforcement, target)
        steps = [step("POLYA_SETUP", f"r={red}, b={blue}, c={reinforcement}",
                      target)]
        branch_probabilities = []
        for prefix in itertools.product(("R", "B"), repeat=draw - 1):
            sequence = list(prefix) + ["R"]
            branch_steps, probability = _sequence_steps(
                red, blue, reinforcement, sequence, "branch")
            steps.extend(branch_steps)
            branch_probabilities.append(probability)
        running = branch_probabilities[0]
        for probability in branch_probabilities[1:]:
            steps.append(step("A", prob_txt(running), prob_txt(probability),
                              prob_txt(running + probability)))
            running += probability
        initial = Fraction(red, red + blue)
        steps.extend([
            step("D", red, red + blue, prob_txt(initial)),
            step("CHECK", "total probability equals initial red fraction",
                 prob_txt(running), prob_txt(initial)),
        ])
        return problem, steps, f"P(draw {draw} is R) = {prob_txt(running)}"

    @staticmethod
    def _count():
        red, blue = random.randint(1, 5), random.randint(1, 5)
        reinforcement = random.choice((1, 2, 3))
        draws = random.randint(2, 6)
        red_draws = random.randint(0, draws)
        blue_draws = draws - red_draws
        target = f"P(exactly {red_draws} red draws among n={draws})"
        problem = _base_problem(red, blue, reinforcement, target)
        coefficient = math.comb(draws, red_draws)
        red_steps, red_product = _rising_steps(red, red_draws, reinforcement, "red")
        blue_steps, blue_product = _rising_steps(blue, blue_draws, reinforcement, "blue")
        total_steps, total_product = _rising_steps(
            red + blue, draws, reinforcement, "total")
        first = coefficient * red_product
        numerator = first * blue_product
        probability = Fraction(numerator, total_product)
        steps = [
            step("POLYA_SETUP", f"r={red}, b={blue}, c={reinforcement}", target),
            step("POLYA_COUNT_FORMULA", "C(n,k)(r)_(k,c)(b)_(n-k,c)/(r+b)_(n,c)"),
            step("NCR", f"C({draws}, {red_draws})", coefficient),
        ]
        steps.extend(red_steps + blue_steps + total_steps)
        steps.extend([
            step("M", coefficient, red_product, first),
            step("M", first, blue_product, numerator),
            step("D", numerator, total_product, prob_txt(probability)),
            step("CHECK", "exchangeable sequences with this red count", coefficient),
        ])
        answer = f"P({red_draws} red draws in {draws}) = {prob_txt(probability)}"
        return problem, steps, answer

    @staticmethod
    def _expected_fraction():
        red, blue = random.randint(1, 6), random.randint(1, 6)
        reinforcement = random.choice((1, 2, 3, 4))
        draws = random.randint(2, 8)
        initial_total = red + blue
        value = Fraction(red, initial_total)
        target = f"expected red fraction after n={draws} draws"
        problem = _base_problem(red, blue, reinforcement, target)
        steps = [
            step("POLYA_SETUP", f"r={red}, b={blue}, c={reinforcement}", target),
            step("D", red, initial_total, prob_txt(value)),
            step("CHECK", "red fraction is a bounded martingale",
                 f"E[future fraction]={prob_txt(value)}"),
        ]
        return problem, steps, f"expected red fraction after {draws} draws = {prob_txt(value)}"

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "sequence_probability":
            problem, steps, answer = self._sequence(False)
        elif variant == "exchangeability_check":
            problem, steps, answer = self._exchangeability()
        elif variant == "kth_draw_marginal":
            problem, steps, answer = self._marginal()
        elif variant == "count_after_n":
            problem, steps, answer = self._count()
        elif variant == "expected_red_fraction":
            problem, steps, answer = self._expected_fraction()
        else:
            problem, steps, answer = self._sequence(True)
        problem = f"{problem} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_polya_urn_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
