"""Solve classic finite probability puzzles by explicit exact models.

Variants: ``monty_hall``, ``monty_hall_n_doors``, ``birthday``,
``birthday_specific_person``, ``birthday_expected_pairs``, ``two_child``,
and ``bertrand_box``. Op-codes: ``MONTY_SETUP``, ``CASE``, ``COMPLEMENT``,
``FCP``, ``POW``, ``NCR``, ``SAMPLE_SPACE``, ``COUNT``, ``FRAC_BUILD``,
``M``, ``A``, ``S``, ``D``, ``CHECK``, and ``Z``. All spaces are finite;
birthday parameters are bounded for hand arithmetic, while varied venues,
cities, people, prizes, materials, and five phrasings provide ample diversity.
"""
import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt


PROBABILITY = True
VENUES = ("amber arcade", "birch fair", "cedar club", "delta studio",
          "ember hall", "forest lodge", "granite center", "harbor pavilion",
          "indigo gallery", "jade theater", "kestrel house", "lunar salon",
          "maple room", "nova arena", "onyx exhibit", "pearl workshop",
          "quartz forum", "river festival", "solar museum", "topaz lounge",
          "umber market", "violet campus", "willow library", "zephyr lab")
CITIES = ("Albany", "Boston", "Cedarville", "Dover", "Erie", "Fresno",
          "Galveston", "Hartford", "Ithaca", "Juneau", "Kingston", "Lowell",
          "Madison", "Norfolk", "Olympia", "Portland", "Quincy", "Raleigh",
          "Salem", "Trenton", "Utica", "Ventura", "Wichita", "Yonkers")
NAMES = ("Aiko", "Ben", "Chidi", "Daria", "Elena", "Farah", "Gita", "Hugo",
         "Imani", "Jae", "Kira", "Luca", "Mina", "Noah", "Omar", "Priya",
         "Quinn", "Ravi", "Sofia", "Tariq", "Uma", "Vera", "Wen", "Zola")
FAMILIES = ("Adams", "Bennett", "Chen", "Diaz", "Evans", "Foster", "Gupta",
            "Harris", "Ito", "Jones", "Khan", "Lopez", "Morgan", "Nguyen",
            "Owens", "Patel", "Quinn", "Rivera", "Singh", "Turner", "Usman",
            "Vega", "Wang", "Young")
PRIZES = ("bicycle", "camera", "canoe", "computer", "drone", "guitar",
          "kayak", "laptop", "microscope", "piano", "robot", "scooter",
          "telescope", "violin", "watch", "workstation")
MATERIAL_PAIRS = (("gold", "silver"), ("red", "blue"), ("amber", "teal"),
                  ("black", "white"), ("copper", "steel"), ("jade", "pearl"),
                  ("orange", "purple"), ("rose", "gray"))
BIRTHDAY_DAYS = (7, 10, 12, 20, 24, 30, 52, 60, 100, 365)
QUERIES = {
    "monty_hall": (
        "Determine whether switching or staying is better in the three-door game.",
        "Compare the exact win probabilities for the two strategies.",
        "Should the contestant switch, and what are both probabilities?",
        "Use the host's information to evaluate stay versus switch.",
        "Report the better strategy with switch and stay probabilities.",
    ),
    "monty_hall_n_doors": (
        "Determine whether switching or staying is better in this many-door game.",
        "Compare the exact win probabilities after the host opens these doors.",
        "Should the contestant switch in this generalized game?",
        "Account for the random remaining switch choice and compare strategies.",
        "Report the better strategy with generalized switch and stay probabilities.",
    ),
    "birthday": (
        "Find the probability that at least two people share a birthday.",
        "Use the complement of all birthdays being different.",
        "Compute the exact birthday-collision probability.",
        "What is the chance of at least one shared birthday?",
        "Count distinct birthday assignments, then take the complement.",
    ),
    "birthday_specific_person": (
        "Find the probability that someone else shares the named person's birthday.",
        "Use the complement that every other birthday differs from the named one.",
        "Compute this specific-person birthday-match probability.",
        "What is the chance of at least one match with the named person?",
        "Compare all other birthdays with the fixed person's birthday.",
    ),
    "birthday_expected_pairs": (
        "Find the expected number of matching birthday pairs.",
        "Use one indicator for each unordered pair of people.",
        "Compute the exact mean count of birthday-sharing pairs.",
        "How many matching pairs are expected?",
        "Apply linearity of expectation across all person pairs.",
    ),
    "two_child": (
        "Find the conditional probability and show the conditioned sample space.",
        "Enumerate the ordered child outcomes consistent with the information.",
        "Compute the exact chance that both children are B.",
        "Condition the four equally likely ordered outcomes on the stated fact.",
        "Use the remaining ordered family outcomes to answer the puzzle.",
    ),
    "bertrand_box": (
        "Find the probability that the other token has the observed material.",
        "Condition on the observed token by enumerating all six token positions.",
        "Compute the exact other-token probability in the three-box puzzle.",
        "Among observation-compatible token sides, count those with a matching mate.",
        "Use the six equally likely box-and-token outcomes to update the box type.",
    ),
}


def _setting():
    return random.choice(VENUES), random.choice(CITIES)


def _pow_step(base, exponent):
    value = base ** exponent
    return step("POW", f"({prob_txt(base)})^{exponent}", prob_txt(value)), value


def _birthday_n(days):
    upper = 3 if days == 365 else 4 if days >= 30 else 6
    return random.randint(3, upper)


class ClassicProbabilityPuzzlesGenerator(ProblemGenerator):
    """Generate exact Monty Hall, birthday, child, and box puzzles."""

    VARIANTS = ("monty_hall", "monty_hall_n_doors", "birthday",
                "birthday_specific_person", "birthday_expected_pairs",
                "two_child", "bertrand_box")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _monty(generalized):
        doors = random.randint(4, 12) if generalized else 3
        opened = random.randint(1, doors - 2) if generalized else 1
        pick = random.randint(1, doors)
        contestant = random.choice(NAMES)
        prize = random.choice(PRIZES)
        venue, city = _setting()
        remaining_switch = doors - 1 - opened
        stay = Fraction(1, doors)
        car_elsewhere = Fraction(doors - 1, doors)
        random_remaining = Fraction(1, remaining_switch)
        switch = car_elsewhere * random_remaining
        prefix = (f"At the {venue} in {city}, {contestant} plays for a {prize}. "
                  f"There are {doors} doors and {contestant} initially chooses door "
                  f"{pick}. The host knows the prize location and opens {opened} "
                  "losing doors uniformly among valid choices. If switching, the "
                  "contestant chooses uniformly among the other unopened doors.")
        steps = [
            step("MONTY_SETUP", f"doors={doors}, opened={opened}, pick={pick}",
                 "host never opens the prize door"),
            step("D", 1, doors, prob_txt(stay)),
            step("CASE", "prize behind initial choice", prob_txt(stay),
                 "stay wins"),
            step("S", doors, 1, doors - 1),
            step("D", doors - 1, doors, prob_txt(car_elsewhere)),
            step("S", doors - 1, opened, remaining_switch),
            step("D", 1, remaining_switch, prob_txt(random_remaining)),
            step("M", prob_txt(car_elsewhere), prob_txt(random_remaining),
                 prob_txt(switch)),
            step("CASE", "prize not behind initial choice",
                 f"{prob_txt(car_elsewhere)} × {prob_txt(random_remaining)}",
                 f"switch wins with probability {prob_txt(switch)}"),
            step("CHECK", "switch exceeds stay", f"{prob_txt(switch)} > {prob_txt(stay)}",
                 "switch"),
        ]
        answer = f"switch; {prob_txt(switch)} vs {prob_txt(stay)}"
        return prefix, steps, answer

    @staticmethod
    def _birthday():
        days = random.choice(BIRTHDAY_DAYS)
        people = _birthday_n(days)
        venue, city = _setting()
        prefix = (f"At the {venue} in {city}, {people} people have birthdays "
                  f"independently and uniformly among {days} calendar days.")
        steps = [step("COMPLEMENT", "P(shared) = 1 − P(all different)")]
        favorable = 1
        for index in range(people):
            choices = days - index
            favorable *= choices
            steps.append(step("FCP", f"person {index + 1}", choices, favorable))
        all_assignments = days ** people
        different = Fraction(favorable, all_assignments)
        shared = 1 - different
        steps.extend([
            step("POW", f"{days}^{people}", all_assignments),
            step("FRAC_BUILD", f"{favorable}/{all_assignments}",
                 prob_txt(different)),
            step("S", 1, prob_txt(different), prob_txt(shared)),
        ])
        return prefix, steps, prob_txt(shared)

    @staticmethod
    def _birthday_specific():
        days = random.choice(BIRTHDAY_DAYS)
        people = _birthday_n(days)
        person = random.choice(NAMES)
        venue, city = _setting()
        prefix = (f"At the {venue} in {city}, {person} is one of {people} people "
                  f"whose birthdays are independent and uniform among {days} "
                  "calendar days.")
        miss = Fraction(days - 1, days)
        power_step, none_match = _pow_step(miss, people - 1)
        value = 1 - none_match
        steps = [step("COMPLEMENT",
                      "P(someone matches named person) = 1 − P(no one matches)"),
                 step("FRAC_BUILD", f"{days - 1}/{days}", prob_txt(miss)),
                 power_step,
                 step("S", 1, prob_txt(none_match), prob_txt(value))]
        return prefix, steps, prob_txt(value)

    @staticmethod
    def _birthday_pairs():
        days = random.choice(BIRTHDAY_DAYS)
        people = random.randint(3, 30)
        venue, city = _setting()
        prefix = (f"At the {venue} in {city}, {people} people have birthdays "
                  f"independently and uniformly among {days} calendar days. Let "
                  "Y count unordered pairs who share a birthday.")
        pairs = math.comb(people, 2)
        value = Fraction(pairs, days)
        steps = [step("NCR", f"C({people}, 2)", pairs),
                 step("D", pairs, days, prob_txt(value)),
                 step("CHECK", "linearity over pair indicators",
                      f"{pairs} × 1/{days}", prob_txt(value))]
        return prefix, steps, f"E[matching pairs] = {prob_txt(value)}"

    @staticmethod
    def _two_child():
        family = random.choice(FAMILIES)
        venue, city = _setting()
        condition = random.choice(("at least one child is B",
                                   "the older child is B"))
        prefix = (f"The {family} family is visiting the {venue} in {city}. Two "
                  "children are independently equally likely to be B or G, ordered "
                  f"older then younger. Information: {condition}.")
        if condition == "at least one child is B":
            space = "{BB, BG, GB}"
            denominator = 3
        else:
            space = "{BB, BG}"
            denominator = 2
        value = Fraction(1, denominator)
        steps = [step("SAMPLE_SPACE", condition, space),
                 step("COUNT", "both children are B", 1),
                 step("COUNT", "conditioned outcomes", denominator),
                 step("FRAC_BUILD", f"1/{denominator}", prob_txt(value)),
                 step("CHECK", "ordered outcomes are equally likely", space)]
        answer = f"{prob_txt(value)}; sample space {space}"
        return prefix, steps, answer

    @staticmethod
    def _bertrand():
        first, second = random.choice(MATERIAL_PAIRS)
        venue, city = _setting()
        prefix = (f"At the {venue} in {city}, three boxes contain {first}-{first}, "
                  f"{first}-{second}, and {second}-{second} tokens. A box is chosen "
                  f"uniformly, then one token from it is observed uniformly and is "
                  f"{first}. Target: P(the other token is {first}).")
        cases = ((f"{first}-{first} token 1", True, True),
                 (f"{first}-{first} token 2", True, True),
                 (f"{first}-{second} token 1", True, False),
                 (f"{first}-{second} token 2", False, True),
                 (f"{second}-{second} token 1", False, False),
                 (f"{second}-{second} token 2", False, False))
        steps = [step("SAMPLE_SPACE", "six equally likely box-token positions")]
        for label, observed, mate in cases:
            steps.append(step("CASE", label,
                              f"observed {first}" if observed else f"observed {second}",
                              f"other {first}" if mate else f"other {second}"))
        value = Fraction(2, 3)
        steps.extend([step("COUNT", f"observed {first}", 3),
                      step("COUNT", f"observed {first} and other {first}", 2),
                      step("FRAC_BUILD", "2/3", prob_txt(value)),
                      step("CHECK", "condition on observed token", "2 favorable of 3")])
        return prefix, steps, prob_txt(value)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "monty_hall":
            prefix, steps, answer = self._monty(False)
        elif variant == "monty_hall_n_doors":
            prefix, steps, answer = self._monty(True)
        elif variant == "birthday":
            prefix, steps, answer = self._birthday()
        elif variant == "birthday_specific_person":
            prefix, steps, answer = self._birthday_specific()
        elif variant == "birthday_expected_pairs":
            prefix, steps, answer = self._birthday_pairs()
        elif variant == "two_child":
            prefix, steps, answer = self._two_child()
        else:
            prefix, steps, answer = self._bertrand()
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_classic_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
