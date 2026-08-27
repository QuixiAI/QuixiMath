"""Sort integers into two- and three-attribute Venn regions.

Variants:
- ``two_attributes``: report all four regions for attributes A and B.
- ``three_attributes``: report all eight regions for A, B, and C.
- ``neither_region``: report and count the values satisfying neither A nor B.

Five query phrasings share an explicit ``Numbers`` / ``Attributes`` data
block so every record can be solved from its problem text.  Attribute
families and number rosters are randomized, giving well over 1,000 distinct
problems.

Op-codes:
- ``ATTR_CHECK``: record one value's yes/no result for one named attribute.
- ``REGION``: record the canonical roster for one Venn region.
- ``COUNT``: count the requested neither-region values.
- ``Z``: exact composite answer.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from set_common import roster


FOUNDATIONS = True


QUERY_TEMPLATES = (
    "Sort the numbers into the requested Venn regions.",
    "Classify every number by the stated attributes and report the regions.",
    "Use the attribute tests to place each number in its Venn region.",
    "Build the Venn-region rosters for these numbers.",
    "Check each number against the attributes, then give the requested region rosters.",
)


class AttributeSortingGenerator(ProblemGenerator):
    """Generate explicit attribute checks followed by canonical region rosters."""

    VARIANTS = ("two_attributes", "three_attributes", "neither_region")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _attribute_pool():
        divisor_a, divisor_b = random.sample(range(3, 10), 2)
        low = random.randint(7, 22)
        high = random.randint(max(low + 5, 18), 48)
        return [
            ("even", lambda value: value % 2 == 0),
            ("odd", lambda value: value % 2 == 1),
            (f"multiple of {divisor_a}",
             lambda value, divisor=divisor_a: value % divisor == 0),
            (f"multiple of {divisor_b}",
             lambda value, divisor=divisor_b: value % divisor == 0),
            (f"greater than {low}", lambda value, bound=low: value > bound),
            (f"less than {high}", lambda value, bound=high: value < bound),
            ("one-digit", lambda value: value < 10),
        ]

    @staticmethod
    def _regions(numbers, attributes):
        regions = {}
        for number in numbers:
            key = tuple(predicate(number) for _, predicate in attributes)
            regions.setdefault(key, []).append(number)
        return regions

    @staticmethod
    def _answer_rows(variant, regions):
        if variant == "two_attributes":
            layout = (
                ((True, True), "both"),
                ((True, False), "only A"),
                ((False, True), "only B"),
                ((False, False), "neither"),
            )
            return [(label, regions.get(key, [])) for key, label in layout]
        if variant == "three_attributes":
            layout = (
                ((True, True, True), "all three"),
                ((True, True, False), "A and B only"),
                ((True, False, True), "A and C only"),
                ((False, True, True), "B and C only"),
                ((True, False, False), "A only"),
                ((False, True, False), "B only"),
                ((False, False, True), "C only"),
                ((False, False, False), "none"),
            )
            return [(label, regions.get(key, [])) for key, label in layout]
        return [("neither", regions.get((False, False), []))]

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        attribute_count = 3 if variant == "three_attributes" else 2
        attributes = random.sample(self._attribute_pool(), attribute_count)
        numbers = sorted(random.sample(range(1, 61), random.randint(8, 12)))
        regions = self._regions(numbers, attributes)
        rows = self._answer_rows(variant, regions)

        attribute_text = "; ".join(
            f"{chr(65 + index)} = {description}"
            for index, (description, _) in enumerate(attributes)
        )
        problem = (
            f"Numbers: [{', '.join(map(str, numbers))}]. "
            f"Attributes: {attribute_text}. {random.choice(QUERY_TEMPLATES)}"
        )
        if variant == "neither_region":
            problem += " Report only the neither region and its count."

        steps = []
        for number in numbers:
            for index, (description, predicate) in enumerate(attributes):
                label = chr(65 + index)
                steps.append(step("ATTR_CHECK", number,
                                  f"{label}: {description}",
                                  "yes" if predicate(number) else "no"))
        for label, values in rows:
            steps.append(step("REGION", label, roster(values)))

        if variant == "neither_region":
            values = rows[0][1]
            steps.append(step("COUNT", "neither", len(values)))
            answer = f"neither: {roster(values)}; count = {len(values)}"
        else:
            answer = "; ".join(f"{label}: {roster(values)}"
                               for label, values in rows)

        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"attribute_sorting_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
