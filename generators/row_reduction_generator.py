import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.matrix_ops_generator import mat


def row_op_txt(j, m, i):
    """'R3 → R3 - 2·R2' (m is the multiplier being subtracted)."""
    if m == 1:
        tail = f"- R{i}"
    elif m == -1:
        tail = f"+ R{i}"
    elif m > 0:
        tail = f"- {m}·R{i}"
    else:
        tail = f"+ {-m}·R{i}"
    return f"R{j} → R{j} {tail}"


class RowReductionGenerator(ProblemGenerator):
    """
    Gaussian elimination on an augmented matrix — the tabular
    scratchpad: each row operation names its multiplier and shows the
    new row, the triangular form is written out, and back-substitution
    finishes with explicit arithmetic. Systems are built as L·U with
    unit pivots, so every multiplier and every intermediate entry is a
    small integer.

    Variants: 2×2 and 3×3 systems.

    Op-codes used:
    - MAT_SETUP: the augmented matrix and the goal (established)
    - ROW_OP: one elimination step (operation, resulting row)
    - REWRITE: the triangular form (established)
    - M / S / A / EVAL: back-substitution (established)
    - Z: 'x = ..., y = ...[, z = ...]'
    """

    VARIANTS = ["two", "three"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(["two", "three", "three"])
        n = 2 if variant == "two" else 3

        U = [[0] * n for _ in range(n)]
        for i in range(n):
            U[i][i] = 1
            for j in range(i + 1, n):
                U[i][j] = random.randint(-3, 3)
        mults = {}
        L = [[0] * n for _ in range(n)]
        for i in range(n):
            L[i][i] = 1
            for j in range(i):
                mults[(i, j)] = random.choice(
                    [v for v in range(-3, 4) if v != 0])
                L[i][j] = mults[(i, j)]
        A = [[sum(L[i][t] * U[t][j] for t in range(n))
              for j in range(n)] for i in range(n)]
        x0 = [random.randint(-4, 4) for _ in range(n)]
        b = [sum(A[i][j] * x0[j] for j in range(n)) for i in range(n)]

        aug = [A[i] + [b[i]] for i in range(n)]
        steps = [step("MAT_SETUP", f"augmented matrix {mat(aug)}",
                      "solve by row reduction")]

        work = [row[:] for row in aug]
        for j in range(n):          # pivot column
            for i in range(j + 1, n):
                m = mults[(i, j)]
                new = [work[i][t] - m * work[j][t]
                       for t in range(n + 1)]
                steps.append(step("ROW_OP", row_op_txt(i + 1, m, j + 1),
                                  mat([new])[1:-1]))
                work[i] = new
        steps.append(step("REWRITE", f"triangular form {mat(work)}"))

        names = ["x", "y", "z"][:n]
        sol = {}
        c = [row[n] for row in work]
        for i in range(n - 1, -1, -1):
            expr_val = c[i]
            for j in range(i + 1, n):
                coef = work[i][j]
                if coef:
                    prod = coef * sol[names[j]]
                    steps.append(step("M", coef, sol[names[j]], prod))
                    steps.append(step("S", expr_val, prod,
                                      expr_val - prod))
                    expr_val -= prod
            sol[names[i]] = expr_val
            steps.append(step("EVAL", names[i], expr_val))
        assert [sol[nm] for nm in names] == x0

        answer = ", ".join(f"{nm} = {sol[nm]}" for nm in names)
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"row_reduction_{variant}",
            problem=(f"Solve the system with augmented matrix "
                     f"{mat(aug)} using row reduction."),
            steps=steps,
            final_answer=answer,
        )
