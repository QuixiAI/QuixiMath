"""Sum exact branch probabilities in two- and three-stage trees.

Variants: ``different_colors``, ``same_color``, ``exactly_one``,
``with_replacement``, ``three_coins_exactly_two_heads``, and
``spinner_then_coin``. Op-codes: ``TREE_BRANCH``, ``BRANCH_SUM``,
``CHECK``, and ``Z``. Random branch counts, labels, and five phrasings give an
unbounded problem space.
"""
import itertools
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt, roster


PROBABILITY = True
COLORS = ("amber", "blue", "green", "orange", "purple", "red", "teal")
COIN_NAMES = ("amber", "blue", "copper", "gold", "green", "indigo",
              "orange", "purple", "red", "silver", "teal", "white")
QUERIES = {
    "different_colors": (
        "Use the tree to find the probability of different colors.",
        "Add the two mixed-color branches.",
        "Compute each favorable different-color path, then sum them.",
        "Follow the without-replacement tree to determine P(A).",
        "Build the full branch check for the different-color event.",
    ),
    "same_color": (
        "Use the tree to find the probability of matching colors.",
        "Add the two same-color branches.",
        "Compute each favorable matching-color path, then sum them.",
        "Follow the without-replacement tree for the same-color event.",
        "Build the full branch check for matching draws.",
    ),
    "exactly_one": (
        "Use the tree to find the probability of exactly one success.",
        "Add the success-failure and failure-success branches.",
        "Compute both exactly-one paths, then sum them.",
        "Follow the independent-stage tree to determine P(A).",
        "Build the full branch check for exactly one success.",
    ),
    "with_replacement": (
        "Use the with-replacement tree to find P(A).",
        "Compute each favorable replacement branch, then add the paths.",
        "Follow the restored bag counts through both draws.",
        "Sum the mutually exclusive replacement paths in event A.",
        "Build the full with-replacement branch check.",
    ),
    "three_coins_exactly_two_heads": (
        "Use the three-coin tree to find the probability of exactly two heads.",
        "Add the three branches containing exactly two heads.",
        "Compute the HHT, HTH, and THH path probabilities.",
        "Follow all eight coin branches and determine P(A).",
        "Build the complete branch check for exactly two heads.",
    ),
    "spinner_then_coin": (
        "Use the spinner-coin tree to find P(A).",
        "Add the favorable sector-and-heads branches.",
        "Compute each matching spinner-coin path, then sum them.",
        "Follow every sector into its two coin branches.",
        "Build the complete spinner-then-coin branch check.",
    ),
}


def branch_steps(branches, favorable):
    steps = []
    favorable_values = []
    for label, factors in branches:
        value = Fraction(1)
        for factor in factors:
            value *= factor
        expression = " × ".join(prob_txt(factor) for factor in factors)
        if label in favorable:
            steps.append(step("TREE_BRANCH", label, expression, prob_txt(value)))
            favorable_values.append((label, value))
    result = sum((value for _, value in favorable_values), Fraction())
    steps.append(step("BRANCH_SUM", " + ".join(label for label, _ in favorable_values),
                      " + ".join(prob_txt(value) for _, value in favorable_values),
                      prob_txt(result)))
    all_values = []
    for _, factors in branches:
        value = Fraction(1)
        for factor in factors:
            value *= factor
        all_values.append(value)
    steps.append(step("CHECK", "all branches",
                      " + ".join(prob_txt(value) for value in all_values), "1"))
    return steps, prob_txt(result)


class TreeDiagramProbabilityGenerator(ProblemGenerator):
    """Generate exact path-summing exercises for small probability trees."""

    VARIANTS = ("different_colors", "same_color", "exactly_one",
                "with_replacement", "three_coins_exactly_two_heads",
                "spinner_then_coin")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _bag(variant):
        first_color, second_color = random.sample(COLORS, 2)
        first_count, second_count = random.randint(2, 60), random.randint(2, 60)
        replacement = variant == "with_replacement"
        total = first_count + second_count
        branches = []
        for first, first_n in (("A", first_count), ("B", second_count)):
            for second, second_n in (("A", first_count), ("B", second_count)):
                numerator = second_n if replacement else second_n - (first == second)
                denominator = total if replacement else total - 1
                branches.append((first + second,
                                 (Fraction(first_n, total),
                                  Fraction(numerator, denominator))))
        if variant == "different_colors":
            event_text, favorable = "the two colors differ", {"AB", "BA"}
        elif variant == "same_color":
            event_text, favorable = "the two colors match", {"AA", "BB"}
        else:
            if random.choice((True, False)):
                event_text, favorable = "the two colors differ", {"AB", "BA"}
            else:
                event_text, favorable = "the two colors match", {"AA", "BB"}
        method = "with replacement" if replacement else "without replacement"
        prefix = (f"A bag has {first_count} {first_color} and {second_count} "
                  f"{second_color} marbles. Draw two {method}. Use A for "
                  f"{first_color} and B for {second_color}. Event A: {event_text}.")
        steps, answer = branch_steps(branches, favorable)
        return prefix, steps, answer

    @staticmethod
    def _exactly_one():
        first_total, second_total = random.randint(3, 30), random.randint(3, 30)
        first_success = random.randint(1, first_total - 1)
        second_success = random.randint(1, second_total - 1)
        p, q = Fraction(first_success, first_total), Fraction(second_success, second_total)
        branches = (("SS", (p, q)), ("SF", (p, 1 - q)),
                    ("FS", (1 - p, q)), ("FF", (1 - p, 1 - q)))
        prefix = (f"Two independent stages have success counts "
                  f"{first_success}/{first_total} and "
                  f"{second_success}/{second_total}. Event A: exactly one "
                  "stage succeeds. Use S for success and F for failure.")
        steps, answer = branch_steps(branches, {"SF", "FS"})
        return prefix, steps, answer

    @staticmethod
    def _three_coins():
        names = random.sample(COIN_NAMES, 3)
        outcomes = tuple("".join(bits) for bits in itertools.product("HT", repeat=3))
        branches = tuple((outcome, (Fraction(1, 2),) * 3) for outcome in outcomes)
        favorable = {outcome for outcome in outcomes if outcome.count("H") == 2}
        prefix = (f"Flip the {names[0]}, {names[1]}, and {names[2]} coins in "
                  "that order. Event A: exactly two heads.")
        steps, answer = branch_steps(branches, favorable)
        return prefix, steps, answer

    @staticmethod
    def _spinner_coin():
        sectors = tuple(sorted(random.sample(range(1, 100), random.randint(2, 8))))
        parity = random.choice(("odd", "even"))
        wanted = 1 if parity == "odd" else 0
        branches = tuple((f"{sector}{face}",
                          (Fraction(1, len(sectors)), Fraction(1, 2)))
                         for sector in sectors for face in ("H", "T"))
        favorable = {label for label, _ in branches
                     if int(label[:-1]) % 2 == wanted and label[-1] == "H"}
        if not favorable:
            parity = "odd" if parity == "even" else "even"
            wanted = 1 - wanted
            favorable = {label for label, _ in branches
                         if int(label[:-1]) % 2 == wanted and label[-1] == "H"}
        prefix = (f"Spin equal sectors {roster(sectors)}, then flip a fair "
                  f"coin. Event A: a {parity} sector and heads. Branch labels "
                  "write sector then coin face.")
        steps, answer = branch_steps(branches, favorable)
        return prefix, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant in ("different_colors", "same_color", "with_replacement"):
            prefix, steps, answer = self._bag(variant)
        elif variant == "exactly_one":
            prefix, steps, answer = self._exactly_one()
        elif variant == "three_coins_exactly_two_heads":
            prefix, steps, answer = self._three_coins()
        else:
            prefix, steps, answer = self._spinner_coin()
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_tree_diagram_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
