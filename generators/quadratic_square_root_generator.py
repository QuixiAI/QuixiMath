import random
from base_generator import ProblemGenerator
from helpers import step, jid

SQUARE_FREE = [2, 3, 5, 6, 7, 10, 11, 13, 14, 15, 17, 19, 21, 22, 23, 26]


class QuadraticSquareRootGenerator(ProblemGenerator):
    """
    Solves quadratics with no linear term by taking square roots of both
    sides — remembering the ± and expanding it into both branches.

    Variants:
    - simple:     x² = k, k a perfect square
    - irrational: x² = k, k square-free — exact answers ±√k
    - scaled:     ax² = k (divide first; half the time shown as ax² − k = 0
                  so a MOVE_TERM opens the solve)
    - shifted:    (x − h)² = k — two linear branches to finish

    Op-codes used:
    - EQ_SETUP / MOVE_TERM / EQ_OP_BOTH / EQ_RESULT (established)
    - ROOT: the square root fact used (value, root)
    - SQRT_BOTH_SIDES: take √ of both sides with ± (before, after)
    - PLUS_MINUS: expand ± into the two branches (with ±, the two equations)
    - CHECK: substitute back (method, work, expected)
    - Z: 'x = r1 or x = r2', ascending (A0)
    """

    VARIANTS = ["simple", "irrational", "scaled", "shifted"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        var = random.choice(["x", "x", "x", "y", "n"])
        steps = []

        if variant == "irrational":
            k = random.choice(SQUARE_FREE)
            original = f"{var}^2 = {k}"
            steps.append(step("EQ_SETUP", original))
            steps.append(step("SQRT_BOTH_SIDES", original,
                              f"{var} = ±√{k}"))
            steps.append(step("PLUS_MINUS", f"{var} = ±√{k}",
                              f"{var} = √{k} or {var} = -√{k}"))
            steps.append(step("CHECK", "substitute",
                              f"(√{k})^2 = {k}", str(k)))
            answer = f"{var} = -√{k} or {var} = √{k}"

        elif variant == "shifted":
            r = random.randint(2, 12)
            h = random.choice([v for v in range(-9, 10) if v != 0])
            sign = "-" if h > 0 else "+"
            inner = f"{var} {sign} {abs(h)}"
            original = f"({inner})^2 = {r * r}"
            lo, hi = sorted((h - r, h + r))
            steps.append(step("EQ_SETUP", original))
            steps.append(step("ROOT", r * r, r))
            steps.append(step("SQRT_BOTH_SIDES", original,
                              f"{inner} = ±{r}"))
            steps.append(step("PLUS_MINUS", f"{inner} = ±{r}",
                              f"{inner} = {r} or {inner} = -{r}"))
            verb = "add" if h > 0 else "subtract"
            steps.append(step("EQ_OP_BOTH", verb, abs(h), var, h + r))
            steps.append(step("EQ_RESULT", var, h + r))
            steps.append(step("EQ_OP_BOTH", verb, abs(h), var, h - r))
            steps.append(step("EQ_RESULT", var, h - r))
            for root in (lo, hi):
                rt = f"({root})" if root < 0 else str(root)
                steps.append(step("CHECK", "substitute",
                                  f"({rt} {sign} {abs(h)})^2 = {r * r}",
                                  str(r * r)))
            answer = f"{var} = {lo} or {var} = {hi}"

        else:
            r = random.randint(2, 12)
            if variant == "simple":
                original = f"{var}^2 = {r * r}"
                steps.append(step("EQ_SETUP", original))
            else:  # scaled
                a = random.randint(2, 6)
                rhs = a * r * r
                if random.random() < 0.5:
                    original = f"{a}{var}^2 - {rhs} = 0"
                    steps.append(step("EQ_SETUP", original))
                    steps.append(step("MOVE_TERM", str(rhs), "right",
                                      f"{a}{var}^2 = {rhs}"))
                else:
                    original = f"{a}{var}^2 = {rhs}"
                    steps.append(step("EQ_SETUP", original))
                steps.append(step("EQ_OP_BOTH", "divide", a, f"{var}^2",
                                  r * r))
            steps.append(step("ROOT", r * r, r))
            steps.append(step("SQRT_BOTH_SIDES", f"{var}^2 = {r * r}",
                              f"{var} = ±{r}"))
            steps.append(step("PLUS_MINUS", f"{var} = ±{r}",
                              f"{var} = {r} or {var} = -{r}"))
            for root in (-r, r):
                rt = f"({root})" if root < 0 else str(root)
                steps.append(step("CHECK", "substitute",
                                  f"{rt}^2 = {r * r}", str(r * r)))
            answer = f"{var} = {-r} or {var} = {r}"

        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="quadratic_by_square_roots",
            problem=f"Solve: {original}",
            steps=steps,
            final_answer=answer,
        )
