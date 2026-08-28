"""Compute expectations by decomposing counts into indicators.

Variants: ``fixed_points``, ``distinct_values``, ``empty_bins``,
``heads_different_coins``, ``sum_dice``, ``adjacent_same_color``, and
``birthday_pairs``. Op-codes: ``INDICATOR``, ``LINEARITY``, ``NCR``,
``POW``, ``M``, ``A``, ``S``, ``D``, ``CHECK``, and ``Z``. All finite
spaces are small enough for exhaustive test oracles (at most 6^4 or 4^6
outcomes); varied exact parameters, settings, and five phrasings give a
large problem space.
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
PROBABILITIES = (Fraction(1, 5), Fraction(1, 4), Fraction(1, 3),
                 Fraction(2, 5), Fraction(1, 2), Fraction(3, 5),
                 Fraction(2, 3), Fraction(3, 4), Fraction(4, 5))
QUERIES = {
    "fixed_points": (
        "Find the expected number of fixed positions.",
        "Use one fixed-point indicator for each permutation position.",
        "Apply linearity without enumerating every permutation.",
        "What is E[X] for the fixed-position count?",
        "Add the identical expectations of all position indicators.",
    ),
    "distinct_values": (
        "Find the expected number of distinct values shown.",
        "Use one indicator for whether each face value appears.",
        "Apply linearity to the distinct-face count.",
        "What is E[X] for the number of represented die values?",
        "Complement the chance a value is absent, then sum over values.",
    ),
    "empty_bins": (
        "Find the expected number of empty bins.",
        "Use one indicator for each bin remaining empty.",
        "Apply linearity to the empty-bin count.",
        "What is E[X] after all labelled balls are placed?",
        "Compute one bin's empty probability and multiply by the bin count.",
    ),
    "heads_different_coins": (
        "Find the expected total number of heads.",
        "Add the head-indicator expectations for the different coins.",
        "Use linearity even though the coins have different biases.",
        "What is E[X] for the head count?",
        "Sum the stated success probabilities.",
    ),
    "sum_dice": (
        "Find the expected sum of the dice.",
        "Add the exact mean of each differently sided die.",
        "Apply linearity to the total face value.",
        "What is E[X] for this dice sum?",
        "Compute each die's center, then add the centers.",
    ),
    "adjacent_same_color": (
        "Find the expected number of equal adjacent pairs.",
        "Use one match indicator for every neighboring position pair.",
        "Apply linearity to the adjacent-color match count.",
        "What is E[X] for the number of neighboring matches?",
        "Find one adjacent match probability, then sum over all adjacencies.",
    ),
    "birthday_pairs": (
        "Find the expected number of matching birthday pairs.",
        "Use one equality indicator for every unordered pair of people.",
        "Apply linearity to the birthday-pair count.",
        "What is E[Y] for the number of pairs sharing a date?",
        "Multiply the number of person pairs by one pair's match probability.",
    ),
}


def _setting():
    return random.choice(VENUES), random.choice(CITIES), random.choice(NAMES)


def _sum_steps(values):
    steps = []
    running = values[0]
    for value in values[1:]:
        steps.append(step("A", prob_txt(running), prob_txt(value),
                          prob_txt(running + value)))
        running += value
    return steps, running


class LinearityOfExpectationGenerator(ProblemGenerator):
    """Generate finite indicator-variable expectation exercises."""

    VARIANTS = ("fixed_points", "distinct_values", "empty_bins",
                "heads_different_coins", "sum_dice", "adjacent_same_color",
                "birthday_pairs")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _fixed_points():
        size = random.randint(3, 6)
        venue, city, name = _setting()
        prefix = (f"At the {venue} in {city}, {name} studies a uniformly chosen "
                  f"permutation of 1 through {size}. Let X count positions i where the value "
                  "in position i equals i.")
        probability = Fraction(1, size)
        value = size * probability
        steps = [step("INDICATOR", "I_i = 1 if position i is fixed",
                      f"P(I_i = 1) = {prob_txt(probability)}"),
                 step("D", 1, size, prob_txt(probability)),
                 step("LINEARITY", "E[X] = Σ E[I_i]",
                      f"{size} × {prob_txt(probability)}"),
                 step("M", size, prob_txt(probability), prob_txt(value)),
                 step("CHECK", "constant-answer guard",
                      f"{size} indicators, each with chance 1/{size}", value)]
        return prefix, steps, f"{size} × 1/{size} = 1"

    @staticmethod
    def _distinct_values():
        rolls, faces = random.randint(2, 4), random.randint(4, 8)
        venue, city, name = _setting()
        prefix = (f"At the {venue} in {city}, {name} rolls {rolls} independent fair "
                  f"{faces}-sided dice. Let X count distinct face "
                  "values that appear.")
        absent_one = Fraction(faces - 1, faces)
        absent_all = absent_one ** rolls
        appears = 1 - absent_all
        value = faces * appears
        steps = [step("INDICATOR", "I_v = 1 if value v appears",
                      f"P(I_v = 1) = 1 − ({faces - 1}/{faces})^{rolls}"),
                 step("D", faces - 1, faces, prob_txt(absent_one)),
                 step("POW", f"({prob_txt(absent_one)})^{rolls}",
                      prob_txt(absent_all)),
                 step("S", 1, prob_txt(absent_all), prob_txt(appears)),
                 step("LINEARITY", "E[X] = Σ E[I_v]",
                      f"{faces} × {prob_txt(appears)}"),
                 step("M", faces, prob_txt(appears), prob_txt(value))]
        return prefix, steps, prob_txt(value)

    @staticmethod
    def _empty_bins():
        balls, bins = random.randint(2, 4), random.randint(3, 6)
        venue, city, name = _setting()
        prefix = (f"At the {venue} in {city}, {name} places {balls} labelled balls "
                  f"independently and uniformly into {bins} labelled bins. Let X "
                  "count empty bins.")
        avoid = Fraction(bins - 1, bins)
        empty = avoid ** balls
        value = bins * empty
        steps = [step("INDICATOR", "I_j = 1 if bin j is empty",
                      f"P(I_j = 1) = ({bins - 1}/{bins})^{balls}"),
                 step("D", bins - 1, bins, prob_txt(avoid)),
                 step("POW", f"({prob_txt(avoid)})^{balls}", prob_txt(empty)),
                 step("LINEARITY", "E[X] = Σ E[I_j]",
                      f"{bins} × {prob_txt(empty)}"),
                 step("M", bins, prob_txt(empty), prob_txt(value))]
        return prefix, steps, prob_txt(value)

    @staticmethod
    def _heads():
        count = random.randint(3, 6)
        probabilities = tuple(random.choice(PROBABILITIES) for _ in range(count))
        venue, city, name = _setting()
        data = ", ".join(f"p{i + 1}={prob_txt(value)}"
                         for i, value in enumerate(probabilities))
        prefix = (f"At the {venue} in {city}, {name} tosses {count} independent "
                  "coins with head "
                  f"probabilities {data}. Let X count heads.")
        steps = [step("INDICATOR", f"H_{index + 1} = 1 for a head",
                      f"E[H_{index + 1}] = {prob_txt(value)}")
                 for index, value in enumerate(probabilities)]
        additions, total = _sum_steps(probabilities)
        steps.insert(0, step("LINEARITY", "E[X] = Σ P(coin i is H)"))
        steps.extend(additions)
        steps.append(step("CHECK", "sum of head probabilities", prob_txt(total)))
        return prefix, steps, prob_txt(total)

    @staticmethod
    def _dice_sum():
        count = random.randint(2, 4)
        sides = tuple(random.randint(4, 6) for _ in range(count))
        venue, city, name = _setting()
        prefix = (f"At the {venue} in {city}, {name} rolls independent fair dice "
                  "with side "
                  f"counts {', '.join(map(str, sides))}. Let X be their face-value sum.")
        means = []
        steps = [step("LINEARITY", "E[X] = sum of individual die means")]
        for index, side_count in enumerate(sides):
            numerator = side_count + 1
            mean = Fraction(numerator, 2)
            steps.extend([step("A", side_count, 1, numerator),
                          step("D", numerator, 2, prob_txt(mean)),
                          step("INDICATOR", f"die {index + 1} mean",
                               prob_txt(mean))])
            means.append(mean)
        additions, total = _sum_steps(means)
        steps.extend(additions)
        return prefix, steps, prob_txt(total)

    @staticmethod
    def _adjacent():
        length, colors = random.randint(3, 6), random.randint(2, 4)
        venue, city, name = _setting()
        prefix = (f"At the {venue} in {city}, {name} records a sequence of length "
                  f"{length} that uses "
                  f"{colors} colors independently and uniformly. Let X count "
                  "adjacent position pairs with the same color.")
        probability = Fraction(1, colors)
        pairs = length - 1
        value = pairs * probability
        steps = [step("INDICATOR", "J_i = 1 if positions i and i+1 match",
                      f"P(J_i = 1) = {prob_txt(probability)}"),
                 step("D", 1, colors, prob_txt(probability)),
                 step("S", length, 1, pairs),
                 step("LINEARITY", "E[X] = Σ E[J_i]",
                      f"{pairs} × {prob_txt(probability)}"),
                 step("M", pairs, prob_txt(probability), prob_txt(value))]
        return prefix, steps, prob_txt(value)

    @staticmethod
    def _birthday_pairs():
        people, dates = random.randint(3, 4), random.randint(4, 6)
        venue, city, name = _setting()
        prefix = (f"At the {venue} in {city}, {name} observes {people} people who "
                  "independently choose "
                  f"a birthday date uniformly from {dates} labelled dates. Let Y "
                  "count unordered pairs who chose the same date.")
        pairs = math.comb(people, 2)
        probability = Fraction(1, dates)
        value = pairs * probability
        steps = [step("NCR", f"C({people}, 2)", pairs),
                 step("INDICATOR", "I_ab = 1 if pair a,b matches",
                      f"P(I_ab = 1) = {prob_txt(probability)}"),
                 step("D", 1, dates, prob_txt(probability)),
                 step("LINEARITY", "E[Y] = Σ E[I_ab]",
                      f"{pairs} × {prob_txt(probability)}"),
                 step("M", pairs, prob_txt(probability), prob_txt(value))]
        return prefix, steps, f"E[Y] = {prob_txt(value)}"

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        methods = {"fixed_points": self._fixed_points,
                   "distinct_values": self._distinct_values,
                   "empty_bins": self._empty_bins,
                   "heads_different_coins": self._heads,
                   "sum_dice": self._dice_sum,
                   "adjacent_same_color": self._adjacent,
                   "birthday_pairs": self._birthday_pairs}
        prefix, steps, answer = methods[variant]()
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_linearity_expectation_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
