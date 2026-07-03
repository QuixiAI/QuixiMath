import random
from base_generator import ProblemGenerator
from helpers import step, jid


class RatioTableGenerator(ProblemGenerator):
    """
    Generates ratio-table problems: a table of equivalent ratios with one
    missing entry. The scratchpad follows the pencil-and-paper procedure:
    read the table, reduce a complete column to the simplest ratio, find the
    scale factor for the incomplete column, multiply to fill the blank, and
    verify by cross-multiplication.

    Op-codes used:
    - RATIO_TABLE: Record the two rows of the table (row1, row2)
    - RATIO_BASE: Reduce a complete column to simplest form (pair, gcd, simplest)
    - D: Divide to find the scale factor (known, counterpart, factor)
    - M: Multiply to fill the blank (simplest_part, factor, missing_value)
    - CHECK: Verify by cross products (method, lhs_work, rhs_work)
    - Z: Final answer (the missing value)
    """

    CONTEXTS = [
        ("A recipe mixes flour and sugar in a fixed ratio.", "Flour (cups)", "Sugar (cups)"),
        ("A painter mixes red and blue paint in a fixed ratio.", "Red (liters)", "Blue (liters)"),
        ("A car travels at a constant speed.", "Distance (miles)", "Time (hours)"),
        ("Notebooks are sold at a constant price.", "Cost (dollars)", "Notebooks"),
        ("A juice blend mixes water and concentrate in a fixed ratio.", "Water (oz)", "Concentrate (oz)"),
        ("A farm plants trees in fixed-size rows.", "Trees", "Rows"),
    ]

    def _gcd(self, x, y):
        while y:
            x, y = y, x % y
        return x

    def generate(self) -> dict:
        # Coprime base ratio keeps every scale factor an integer.
        while True:
            a = random.randint(2, 12)
            b = random.randint(2, 12)
            if a != b and self._gcd(a, b) == 1:
                break

        ks = sorted(random.sample(range(1, 13), 4))
        row1 = [a * k for k in ks]
        row2 = [b * k for k in ks]

        missing_col = random.randrange(4)
        missing_row = random.randrange(2)
        anchor_col = 0 if missing_col != 0 else 1

        intro, name1, name2 = random.choice(self.CONTEXTS)

        def render(row, row_idx):
            cells = []
            for i, v in enumerate(row):
                cells.append("?" if (i == missing_col and row_idx == missing_row) else str(v))
            return ", ".join(cells)

        problem = (
            f"{intro} The table shows equivalent ratios. Find the missing value.\n"
            f"{name1}: {render(row1, 0)}\n"
            f"{name2}: {render(row2, 1)}"
        )

        # --- Scratchpad ---
        steps = []
        steps.append(step("RATIO_TABLE", f"{name1}: {render(row1, 0)}",
                          f"{name2}: {render(row2, 1)}"))

        # Reduce the anchor column to simplest form (gcd is ks[anchor_col],
        # since a and b are coprime).
        pair1, pair2 = row1[anchor_col], row2[anchor_col]
        g = self._gcd(pair1, pair2)
        steps.append(step("RATIO_BASE", f"{pair1}:{pair2}", g, f"{a}:{b}"))

        # Scale factor from the value that IS present in the missing column.
        if missing_row == 0:
            known, counterpart, simple_part = row2[missing_col], b, a
        else:
            known, counterpart, simple_part = row1[missing_col], a, b
        factor = known // counterpart
        steps.append(step("D", known, counterpart, factor))

        missing_value = simple_part * factor
        steps.append(step("M", simple_part, factor, missing_value))

        # Verify by cross-multiplication against the anchor column.
        if missing_row == 0:
            lhs = f"{pair1}×{known}={pair1 * known}"
            rhs = f"{pair2}×{missing_value}={pair2 * missing_value}"
        else:
            lhs = f"{pair1}×{missing_value}={pair1 * missing_value}"
            rhs = f"{pair2}×{known}={pair2 * known}"
        steps.append(step("CHECK", "cross_products", lhs, rhs))

        steps.append(step("Z", missing_value))

        return dict(
            problem_id=jid(),
            operation="ratio_table",
            problem=problem,
            steps=steps,
            final_answer=str(missing_value),
        )
