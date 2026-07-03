import random
from base_generator import ProblemGenerator
from helpers import step, jid


def row(n):
    """Row n of Pascal's triangle (row 0 is [1])."""
    r = [1]
    for k in range(n):
        r.append(r[-1] * (n - k) // (k + 1))
    return r


class PascalTriangleGenerator(ProblemGenerator):
    """
    Builds Pascal's triangle row by row - each entry as an explicit
    addition of the two above it - then reads off the requested value.

    Variants:
    - row:  build up to row n and give the whole row
    - ncr:  build up to row n and read entry k as nCr (bridge to
      binomial coefficients)

    Op-codes used:
    - PASCAL_SETUP: the goal (target)
    - PASCAL_ROW: one completed row (row number, entries)
    - A: one interior entry as the sum of the two above (established)
    - TABLE_LOOKUP: read the requested entry (established)
    - Z: final answer
    """

    VARIANTS = ["row", "ncr"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        n = random.randint(3, 10)

        steps = []
        if variant == "row":
            goal = f"row {n}"
            problem = (f"Build Pascal's triangle down to row {n} "
                       f"(row 0 is 1). Give row {n}.")
        else:
            k = random.randint(1, n - 1)  # interior entries are the point
            goal = f"{n}C{k}"
            problem = (f"Use Pascal's triangle to find {n}C{k} "
                       f"(row 0 is 1).")
        steps.append(step("PASCAL_SETUP", goal))
        steps.append(step("PASCAL_ROW", 0, "1"))
        steps.append(step("PASCAL_ROW", 1, "1, 1"))
        prev = [1, 1]
        for r_num in range(2, n + 1):
            cur = [1]
            for i in range(len(prev) - 1):
                s = prev[i] + prev[i + 1]
                steps.append(step("A", prev[i], prev[i + 1], s))
                cur.append(s)
            cur.append(1)
            steps.append(step("PASCAL_ROW", r_num,
                              ", ".join(str(v) for v in cur)))
            prev = cur

        if variant == "row":
            answer = ", ".join(str(v) for v in prev)
        else:
            answer = str(prev[k])
            steps.append(step("TABLE_LOOKUP",
                              f"row {n}, entry {k}", answer))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"pascal_triangle_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
