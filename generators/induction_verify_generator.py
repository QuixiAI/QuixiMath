import random

from base_generator import ProblemGenerator
from helpers import step, jid


class InductionVerifyGenerator(ProblemGenerator):
    """
    Verification-style induction problems: check the base case, then show
    the algebraic k to k+1 step for standard identities.

    Variants:
    - sum_linear: 1+...+n = n(n+1)/2.
    - sum_squares: 1^2+...+n^2 = n(n+1)(2n+1)/6.
    - sum_odds: first n odd numbers sum to n^2.
    - geometric: 1+r+...+r^n = (r^(n+1)-1)/(r-1).
    - divisibility: 6 divides n^3-n.

    Op-codes used:
    - INDUCT_BASE / INDUCT_ASSUME / INDUCT_STEP / REWRITE / CHECK
    - A / M / D (established)
    - Z: composite verification statement
    """

    VARIANTS = ["sum_linear", "sum_squares", "sum_odds", "geometric",
                "divisibility"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        check_n = random.randint(2, 40) if variant == "geometric" else random.randint(2, 120)
        intro = random.choice([
            "Verify by induction",
            "Use induction to verify",
            "Check the base case and induction step to verify",
        ])
        if variant == "sum_linear":
            check_value = check_n * (check_n + 1) // 2
            problem = (
                f"{intro} that 1+2+...+n = n(n+1)/2 for n≥1. "
                f"Also report the check at n={check_n}."
            )
            steps = [
                step("INDUCT_BASE", "n=1", "1 = 1(2)/2"),
                step("INDUCT_ASSUME", "1+...+k = k(k+1)/2"),
                step("INDUCT_STEP", "add k+1",
                     "k(k+1)/2 + (k+1)"),
                step("REWRITE", "(k+1)(k/2 + 1)",
                     "(k+1)(k+2)/2"),
                step("CHECK", f"n={check_n}", check_value, "formula value"),
            ]
            answer = f"check n={check_n} value={check_value}; inductive step confirmed"
        elif variant == "sum_squares":
            check_value = check_n * (check_n + 1) * (2 * check_n + 1) // 6
            problem = (
                f"{intro} that 1^2+2^2+...+n^2 = "
                "n(n+1)(2n+1)/6 for n≥1. "
                f"Also report the check at n={check_n}."
            )
            steps = [
                step("INDUCT_BASE", "n=1", "1 = 1(2)(3)/6"),
                step("INDUCT_ASSUME", "sum to k = k(k+1)(2k+1)/6"),
                step("INDUCT_STEP", "add (k+1)^2"),
                step("REWRITE",
                     "k(k+1)(2k+1)/6 + (k+1)^2",
                     "(k+1)(k+2)(2k+3)/6"),
                step("CHECK", f"n={check_n}", check_value, "formula value"),
            ]
            answer = f"check n={check_n} value={check_value}; inductive step confirmed"
        elif variant == "sum_odds":
            check_value = check_n * check_n
            problem = (
                f"{intro} that 1+3+...+(2n-1) = n^2 for n≥1. "
                f"Also report the check at n={check_n}."
            )
            steps = [
                step("INDUCT_BASE", "n=1", "1 = 1^2"),
                step("INDUCT_ASSUME", "sum to k = k^2"),
                step("INDUCT_STEP", "add 2(k+1)-1", "k^2 + 2k + 1"),
                step("REWRITE", "k^2 + 2k + 1", "(k+1)^2"),
                step("CHECK", f"n={check_n}", check_value, "formula value"),
            ]
            answer = f"check n={check_n} value={check_value}; inductive step confirmed"
        elif variant == "geometric":
            r = random.randint(2, 10)
            check_value = (r ** (check_n + 1) - 1) // (r - 1)
            problem = (
                f"{intro} that 1+{r}+...+{r}^n = "
                f"({r}^(n+1)-1)/({r}-1) for n≥0. "
                f"Also report the check at n={check_n}."
            )
            steps = [
                step("INDUCT_BASE", "n=0", "1 = (r^1-1)/(r-1)"),
                step("INDUCT_ASSUME", f"sum to k = ({r}^(k+1)-1)/({r}-1)"),
                step("INDUCT_STEP", f"add {r}^(k+1)"),
                step("REWRITE",
                     f"({r}^(k+1)-1)/({r}-1) + {r}^(k+1)",
                     f"({r}^(k+2)-1)/({r}-1)"),
                step("CHECK", f"n={check_n}", check_value, "formula value"),
            ]
            answer = f"check n={check_n} value={check_value}; inductive step confirmed"
        else:
            check_value = check_n ** 3 - check_n
            problem = (
                f"{intro} that 6 divides n^3 - n for n≥1. "
                f"Also report the check at n={check_n}."
            )
            steps = [
                step("INDUCT_BASE", "n=1", "1^3 - 1 = 0"),
                step("INDUCT_ASSUME", "6 divides k^3-k"),
                step("INDUCT_STEP", "(k+1)^3-(k+1)",
                     "(k^3-k) + 3k(k+1)"),
                step("CHECK", "3k(k+1)", "even times 3",
                     "divisible by 6"),
                step("CHECK", f"n={check_n}", check_value,
                     "divisible by 6"),
            ]
            answer = f"check n={check_n} value={check_value}; inductive divisibility confirmed"
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"induction_verify_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
