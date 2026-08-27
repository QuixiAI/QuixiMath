import random
from base_generator import ProblemGenerator
from helpers import step, jid


ROW_TEMPLATES = [
    ("Build Pascal's triangle down to row {n} (row 0 is 1). Give row "
     "{n}, the coefficient row for (u_{left} + v_{right})^{n}."),
    ("The expansion of (u_{left} + v_{right})^{n} uses row {n} of "
     "Pascal's triangle. Build the triangle from row 0 = 1 and give "
     "row {n}."),
    ("Starting with row 0 = 1, construct Pascal's triangle through "
     "row {n}. Give row {n} as the coefficient list for "
     "(u_{left} + v_{right})^{n}."),
    ("Find the coefficient row of (u_{left} + v_{right})^{n} by "
     "building Pascal's triangle from row 0 = 1 through row {n}. "
     "Give row {n}."),
]

NCR_TEMPLATES = [
    ("Use Pascal's triangle to find {n}C{k} (row 0 is 1). This counts "
     "the {k}-element subsets of {{a_{start}, ..., a_{end}}}."),
    ("The set {{a_{start}, ..., a_{end}}} has {n} elements. Use "
     "Pascal's triangle, with row 0 = 1, to find {n}C{k}, the number "
     "of its {k}-element subsets."),
    ("How many {k}-element subsets does {{a_{start}, ..., a_{end}}} "
     "have? Build Pascal's triangle from row 0 = 1 and find {n}C{k}."),
    ("For the labeled set {{a_{start}, ..., a_{end}}}, use row {n} "
     "of Pascal's triangle to find {n}C{k}. Take row 0 to be 1."),
]


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
        n = random.randint(3, 18)

        steps = []
        if variant == "row":
            goal = f"row {n}"
            problem = random.choice(ROW_TEMPLATES).format(
                n=n,
                left=random.randint(1, 100),
                right=random.randint(1, 100),
            )
        else:
            k = random.randint(1, n - 1)  # interior entries are the point
            goal = f"{n}C{k}"
            start = random.randint(1, 2000)
            problem = random.choice(NCR_TEMPLATES).format(
                n=n, k=k, start=start, end=start + n - 1,
            )
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
