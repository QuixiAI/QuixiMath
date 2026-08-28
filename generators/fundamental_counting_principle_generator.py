"""Count multistage choices and convert counts to exact probabilities.

Variants: ``count_only``, ``count_then_probability``, ``codes``,
``tree_count``, and ``with_restriction``. Op-codes: ``FCP``, ``TREE_LEVEL``,
``EVENT``, ``PROB_SETUP``, ``F``, ``S``, ``CHECK``, and ``Z``. Random choice
systems, contexts, and five phrasings give an unbounded problem space.
"""
import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt


PROBABILITY = True
SYSTEMS = (
    ("lunch menu", ("sandwiches", "drinks", "fruits", "desserts")),
    ("outfit planner", ("shirts", "pants", "hats", "shoes")),
    ("workshop schedule", ("topics", "rooms", "times", "activities")),
    ("design palette", ("fonts", "colors", "backgrounds", "covers")),
    ("travel itinerary", ("routes", "rooms", "times", "activities")),
    ("course selector", ("topics", "rooms", "times", "formats")),
    ("party plan", ("starters", "mains", "drinks", "desserts")),
    ("game configuration", ("avatars", "maps", "modes", "colors")),
    ("book design", ("covers", "fonts", "colors", "formats")),
)
CODE_USES = (
    "locker code", "badge identifier", "ticket code", "device PIN",
    "inventory tag", "room code", "game key", "entry code", "parcel tag",
    "quiz identifier", "robot command", "catalog key",
)
QUERIES = {
    "count_only": (
        "How many complete selections are possible?",
        "Use the fundamental counting principle to count all choices.",
        "Multiply the stage counts and report the total number of selections.",
        "Find the size of the complete product choice space.",
        "Count every possible one-from-each-category selection.",
    ),
    "count_then_probability": (
        "Count all selections, then find the probability of event A.",
        "Use product counts for the sample space and favorable event.",
        "Find the total combinations and the exact event chance.",
        "Apply the counting principle before computing P(A).",
        "Count the full choice space and the constrained selections.",
    ),
    "codes": (
        "Count the no-repeat codes and find their probability in the full code space.",
        "Compare falling-factorial codes with all repetition-allowed codes.",
        "Use the counting principle to determine the no-repeat event chance.",
        "Find both the number and probability of codes with distinct symbols.",
        "Count injective code strings and divide by all possible strings.",
    ),
    "tree_count": (
        "Use the tree levels to count all complete paths.",
        "Multiply the branch counts and report the number of leaves.",
        "Build the staged tree count from left to right.",
        "Find how many terminal paths the choice tree has.",
        "Apply one counting-principle step at each tree level.",
    ),
    "with_restriction": (
        "Count the valid selections after excluding the forbidden pair.",
        "Subtract the combinations containing both restricted options.",
        "Use total minus forbidden to find the allowed count.",
        "Count the full product space, then enforce the incompatibility.",
        "Determine how many selections avoid the stated option pair.",
    ),
}


def system_text(names, counts):
    return "; ".join(f"{name}={count}" for name, count in zip(names, counts))


def product_steps(names, counts, opcode="FCP"):
    running = 1
    steps = []
    for name, count in zip(names, counts):
        running *= count
        steps.append(step(opcode, name, count, running))
    return steps, running


class FundamentalCountingPrincipleGenerator(ProblemGenerator):
    """Generate exact multistage counting and probability exercises."""

    VARIANTS = ("count_only", "count_then_probability", "codes",
                "tree_count", "with_restriction")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _choice_system():
        size = random.randint(2, 4)
        context, pool = random.choice(SYSTEMS)
        names = tuple(random.sample(pool, size))
        counts = tuple(random.randint(2, 12) for _ in names)
        return context, pool, names, counts

    def _count_only(self, tree=False):
        context, _, names, counts = self._choice_system()
        opcode = "TREE_LEVEL" if tree else "FCP"
        steps, total = product_steps(names, counts, opcode)
        prefix = (f"A {context} has choice counts: {system_text(names, counts)}. "
                  "Choose exactly one option from each category.")
        steps.append(step("CHECK", "product of branch counts", total))
        return prefix, steps, f"{total} selections"

    def _count_probability(self):
        context, _, names, counts = self._choice_system()
        constrained = tuple(sorted(random.sample(
            range(len(names)), random.randint(1, len(names) - 1))))
        steps, total = product_steps(names, counts)
        favorable = math.prod(count for index, count in enumerate(counts)
                               if index not in constrained)
        requirements = ", ".join(f"{names[index]} option 1"
                                 for index in constrained)
        value = Fraction(favorable, total)
        prefix = (f"A {context} has choice counts: "
                  f"{system_text(names, counts)}. Choose one from each. "
                  f"Event A requires {requirements}.")
        steps.extend([step("EVENT", "A", requirements, favorable),
                      step("PROB_SETUP", favorable, total)])
        if value.denominator != total:
            steps.append(step("F", f"{favorable}/{total}", prob_txt(value)))
        steps.append(step("CHECK", "event choices divide total", prob_txt(value)))
        return prefix, steps, f"{total} selections; {prob_txt(value)}"

    @staticmethod
    def _codes():
        length = random.randint(2, 6)
        alphabet = random.randint(length, 36)
        full = alphabet ** length
        no_repeat = math.prod(range(alphabet - length + 1, alphabet + 1))
        value = Fraction(no_repeat, full)
        use = random.choice(CODE_USES)
        prefix = (f"A {use} has length {length} and an alphabet of {alphabet} "
                  "symbols. Repetition is allowed in the full code space. "
                  "Event A is that no symbol repeats.")
        steps = []
        running = 1
        for position in range(1, length + 1):
            choices = alphabet - position + 1
            running *= choices
            steps.append(step("FCP", f"no-repeat position {position}",
                              choices, running))
        steps.extend([step("FCP", "all codes", f"{alphabet}^{length}", full),
                      step("EVENT", "no repeats", no_repeat),
                      step("PROB_SETUP", no_repeat, full)])
        if value.denominator != full:
            steps.append(step("F", f"{no_repeat}/{full}", prob_txt(value)))
        steps.append(step("CHECK", "no-repeat count", running))
        return prefix, steps, f"{no_repeat} no-repeat codes; {prob_txt(value)}"

    def _restriction(self):
        context, pool, names, counts = self._choice_system()
        if len(names) < 3:
            extra = random.choice([name for name in pool if name not in names])
            names = names + (extra,)
            counts = counts + (random.randint(2, 12),)
        first, second = random.sample(range(len(names)), 2)
        steps, total = product_steps(names, counts)
        forbidden = math.prod(count for index, count in enumerate(counts)
                              if index not in (first, second))
        valid = total - forbidden
        restriction = (f"{names[first]} option 1 cannot be paired with "
                       f"{names[second]} option 1")
        prefix = (f"A {context} has choice counts: "
                  f"{system_text(names, counts)}. Choose one from each. "
                  f"Restriction: {restriction}.")
        steps.extend([step("EVENT", "forbidden pair", restriction, forbidden),
                      step("S", total, forbidden, valid),
                      step("CHECK", "valid + forbidden", f"{valid} + {forbidden}",
                           total)])
        return prefix, steps, f"{valid} valid selections"

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "count_only":
            prefix, steps, answer = self._count_only()
        elif variant == "count_then_probability":
            prefix, steps, answer = self._count_probability()
        elif variant == "codes":
            prefix, steps, answer = self._codes()
        elif variant == "tree_count":
            prefix, steps, answer = self._count_only(tree=True)
        else:
            prefix, steps, answer = self._restriction()
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_fundamental_counting_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
