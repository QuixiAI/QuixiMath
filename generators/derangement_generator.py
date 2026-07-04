import random

from base_generator import ProblemGenerator
from helpers import step, jid


OBJECTS = [
    "hats", "keys", "books", "badges", "tickets", "coats", "folders",
    "cards", "gifts", "laptops", "notebooks", "packages", "labels",
    "forms", "passes", "tokens", "umbrellas", "phones", "envelopes",
    "receipts",
]


class DerangementGenerator(ProblemGenerator):
    """
    Derangement counts by the recurrence D_n=(n-1)(D_(n-1)+D_(n-2)).

    Variant:
    - recurrence

    Op-codes used:
    - DERANGE_SETUP: number of items and no-fixed-point condition
    - RECURRENCE: derangement recurrence
    - INITIAL: D_0 and D_1
    - A / M (established): recurrence arithmetic
    - DERANGE_VALUE: computed D_m
    - Z: exact derangement count
    """

    VARIANTS = ["recurrence"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        n = random.randint(4, 14)
        obj = random.choice(OBJECTS)
        values = [1, 0]
        steps = [
            step("DERANGE_SETUP", f"n = {n}", "no item fixed"),
            step("RECURRENCE", "D_n", "(n-1)(D_(n-1)+D_(n-2))"),
            step("INITIAL", "D_0 = 1", "D_1 = 0"),
        ]
        for m in range(2, n + 1):
            subtotal = values[m - 1] + values[m - 2]
            value = (m - 1) * subtotal
            steps.extend([
                step("A", values[m - 1], values[m - 2], subtotal),
                step("M", m - 1, subtotal, value),
                step("DERANGE_VALUE", f"D_{m}", value),
            ])
            values.append(value)
        answer = f"D_{n} = {values[n]}"
        steps.append(step("Z", answer))
        problem = (
            f"How many derangements are there of {n} distinct {obj}?"
        )
        return dict(
            problem_id=jid(),
            operation="derangement_recurrence",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
