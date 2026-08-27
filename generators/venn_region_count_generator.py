"""Recover every region of a consistent two- or three-set Venn diagram.

Variants:
- ``two_set`` uses card(U), card(A), card(B), and card(A ∩ B).
- ``three_set`` also supplies inclusive pairwise and triple intersections.
- ``word_problem`` places a two-set instance in a student-survey context.

Instances are built backward from nonnegative region counts.  Five phrasings
and independent region parameters give a problem space far above 100,000.

Op-codes:
- ``REGION_EQ``: identify a directly supplied region.
- ``S`` / ``A``: expose every subtraction and accumulation.
- ``REGION``: record one solved region count.
- ``CHECK``: verify that all disjoint regions sum to card(U).
- ``Z``: exact composite region answer.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step


FOUNDATIONS = True


QUERIES = {
    "two": (
        "Find only A, only B, both, and neither.",
        "Recover all four disjoint Venn regions.",
        "Use the supplied cardinalities to determine every region.",
        "Solve the two-set Venn diagram and report the regions.",
        "Separate the overlap, the two only-regions, and the outside region.",
    ),
    "three": (
        "Find all eight disjoint regions of the three-set Venn diagram.",
        "Recover every only, pair-only, triple, and outside count.",
        "Use the inclusive intersections to solve all Venn regions.",
        "Determine the eight atomic region counts.",
        "Work from the triple overlap outward and report every region.",
    ),
    "word": (
        "Find only A, only B, both, and neither for the survey.",
        "Determine all four disjoint survey groups.",
        "Use inclusion and subtraction to recover each survey region.",
        "Report the two only-groups, the overlap, and neither.",
        "Complete the Venn counts for this student survey.",
    ),
}


SURVEYS = (
    ("chess club", "science club"),
    ("soccer", "music lessons"),
    ("cats", "dogs"),
    ("bus riders", "bike riders"),
    ("fiction readers", "history readers"),
    ("art class", "coding club"),
)


class VennRegionCountGenerator(ProblemGenerator):
    """Generate backward-constructed Venn counts and pencil-and-paper solves."""

    VARIANTS = ("two_set", "three_set", "word_problem")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _two_regions():
        return tuple(random.randint(0, 40) for _ in range(4))

    @staticmethod
    def _sum_steps(values):
        steps = []
        total = values[0]
        for value in values[1:]:
            new_total = total + value
            steps.append(step("A", total, value, new_total))
            total = new_total
        return steps, total

    def _two(self, word_problem=False):
        only_a, only_b, both, neither = self._two_regions()
        card_a = only_a + both
        card_b = only_b + both
        card_u = only_a + only_b + both + neither
        if word_problem:
            topic_a, topic_b = random.choice(SURVEYS)
            problem = (
                f"Survey: {card_u} students total. Category A: {topic_a}. "
                f"Category B: {topic_b}. card(A) = {card_a}; "
                f"card(B) = {card_b}; card(A ∩ B) = {both}. "
                f"{random.choice(QUERIES['word'])}"
            )
        else:
            problem = (
                f"card(U) = {card_u}; card(A) = {card_a}; card(B) = {card_b}; "
                f"card(A ∩ B) = {both}. {random.choice(QUERIES['two'])}"
            )
        steps = [step("REGION_EQ", "A ∩ B", both),
                 step("S", card_a, both, only_a),
                 step("REGION", "only A", only_a),
                 step("S", card_b, both, only_b),
                 step("REGION", "only B", only_b)]
        sum_steps, inside = self._sum_steps((only_a, only_b, both))
        steps.extend(sum_steps)
        steps.append(step("S", card_u, inside, neither))
        steps.extend((step("REGION", "both", both),
                      step("REGION", "neither", neither),
                      step("CHECK", "sum of regions", card_u, "card(U)")))
        answer = (f"only A = {only_a}; only B = {only_b}; both = {both}; "
                  f"neither = {neither}")
        return problem, steps, answer

    def _three(self):
        (only_a, only_b, only_c, ab_only, ac_only, bc_only, triple,
         none) = tuple(random.randint(0, 25) for _ in range(8))
        ab = ab_only + triple
        ac = ac_only + triple
        bc = bc_only + triple
        card_a = only_a + ab_only + ac_only + triple
        card_b = only_b + ab_only + bc_only + triple
        card_c = only_c + ac_only + bc_only + triple
        card_u = sum((only_a, only_b, only_c, ab_only, ac_only, bc_only,
                      triple, none))
        problem = (
            f"card(U) = {card_u}; card(A) = {card_a}; card(B) = {card_b}; "
            f"card(C) = {card_c}; card(A ∩ B) = {ab}; card(A ∩ C) = {ac}; "
            f"card(B ∩ C) = {bc}; card(A ∩ B ∩ C) = {triple}. "
            f"{random.choice(QUERIES['three'])}"
        )
        steps = [step("REGION_EQ", "A ∩ B ∩ C", triple),
                 step("S", ab, triple, ab_only),
                 step("REGION", "A and B only", ab_only),
                 step("S", ac, triple, ac_only),
                 step("REGION", "A and C only", ac_only),
                 step("S", bc, triple, bc_only),
                 step("REGION", "B and C only", bc_only)]
        remaining_a = card_a - ab_only
        steps.append(step("S", card_a, ab_only, remaining_a))
        remaining_a2 = remaining_a - ac_only
        steps.append(step("S", remaining_a, ac_only, remaining_a2))
        steps.append(step("S", remaining_a2, triple, only_a))
        remaining_b = card_b - ab_only
        steps.append(step("S", card_b, ab_only, remaining_b))
        remaining_b2 = remaining_b - bc_only
        steps.append(step("S", remaining_b, bc_only, remaining_b2))
        steps.append(step("S", remaining_b2, triple, only_b))
        remaining_c = card_c - ac_only
        steps.append(step("S", card_c, ac_only, remaining_c))
        remaining_c2 = remaining_c - bc_only
        steps.append(step("S", remaining_c, bc_only, remaining_c2))
        steps.append(step("S", remaining_c2, triple, only_c))
        for label, value in (("only A", only_a), ("only B", only_b),
                             ("only C", only_c), ("all three", triple)):
            steps.append(step("REGION", label, value))
        disjoint_inside = (only_a, only_b, only_c, ab_only, ac_only,
                           bc_only, triple)
        sum_steps, inside = self._sum_steps(disjoint_inside)
        steps.extend(sum_steps)
        steps.append(step("S", card_u, inside, none))
        steps.extend((step("REGION", "none", none),
                      step("CHECK", "sum of regions", card_u, "card(U)")))
        answer = (
            f"only A = {only_a}; only B = {only_b}; only C = {only_c}; "
            f"A and B only = {ab_only}; A and C only = {ac_only}; "
            f"B and C only = {bc_only}; all three = {triple}; none = {none}"
        )
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "three_set":
            problem, steps, answer = self._three()
        else:
            problem, steps, answer = self._two(variant == "word_problem")
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"venn_region_count_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
