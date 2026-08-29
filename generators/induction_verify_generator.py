import random

from base_generator import ProblemGenerator
from helpers import step, jid


FOUNDATIONS = True


INTROS = (
    "Verify by induction",
    "Use induction to verify",
    "Check the base case and induction step to verify",
    "Give a complete induction verification",
    "Establish by induction",
)
WELL_ORDERING_INTROS = (
    "Use well-ordering to justify the division algorithm.",
    "Apply the well-ordering principle to justify the division algorithm.",
    "Give a well-ordering argument for the division algorithm.",
    "Justify the division algorithm with a well-ordering proof.",
    "Use the well-ordering principle to establish the division algorithm.",
)


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
    - strong_induction: every n≥12 is 4a+5b for nonnegative a,b.
    - well_ordering: least-remainder proof of the division algorithm.

    Op-codes used:
    - INDUCT_BASE / INDUCT_ASSUME / INDUCT_STEP / REWRITE / CHECK
    - WITNESS / SETUP / LEAST / ASSUME / CONTRADICTION / DIVMOD
    - A / M / D (established)
    - Z: composite verification statement
    """

    VARIANTS = ["sum_linear", "sum_squares", "sum_odds", "geometric",
                "divisibility", "strong_induction", "well_ordering"]
    WEIGHTS = [0.01, 0.01, 0.01, 0.01, 0.01, 0.475, 0.475]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choices(self.VARIANTS,
                                                 weights=self.WEIGHTS, k=1)[0]
        check_n = random.randint(2, 40) if variant == "geometric" else random.randint(2, 120)
        intro = random.choice(INTROS)
        if variant == "strong_induction":
            check_n = random.randint(16, 100000)
            for witness_b in range(check_n // 5 + 1):
                remainder = check_n - 5 * witness_b
                if remainder >= 0 and remainder % 4 == 0:
                    witness_a = remainder // 4
                    break
            problem = (
                f"{intro} that every integer n≥12 can be written as n=4a+5b "
                "for nonnegative integers a,b. Use base cases 12 through 15 "
                "and the step n→n+4. "
                f"Also report the first witness at n={check_n}."
            )
            steps = [
                step("INDUCT_BASE", "n=12", "12 = 4·3 + 5·0"),
                step("INDUCT_BASE", "n=13", "13 = 4·2 + 5·1"),
                step("INDUCT_BASE", "n=14", "14 = 4·1 + 5·2"),
                step("INDUCT_BASE", "n=15", "15 = 4·0 + 5·3"),
                step("INDUCT_ASSUME", "n = 4a + 5b", "a,b nonnegative"),
                step("INDUCT_STEP", "n → n+4",
                     "n+4 = 4(a+1) + 5b"),
                step("WITNESS", f"n={check_n}", f"a={witness_a}",
                     f"b={witness_b}"),
                step("CHECK", f"4·{witness_a} + 5·{witness_b}", check_n,
                     "matches n"),
            ]
            answer = (f"check n={check_n}: {check_n} = 4·{witness_a} + "
                      f"5·{witness_b}; strong induction confirmed")
        elif variant == "well_ordering":
            number = random.randint(100, 1000000)
            divisor = random.randint(2, min(1000, number - 1))
            quotient, remainder = divmod(number, divisor)
            problem = (
                f"{random.choice(WELL_ORDERING_INTROS)} "
                f"For N={number} and d={divisor}, consider the nonnegative "
                "values N−dq, choose the least r, and show r<d. "
                "Report the resulting quotient and remainder."
            )
            steps = [
                step("SETUP", "S = nonnegative values N−dq", "S is nonempty"),
                step("LEAST", "r = least element of S"),
                step("ASSUME", "r ≥ d"),
                step("CONTRADICTION", "r−d is nonnegative and in S",
                     "r−d < r"),
                step("DIVMOD", number, divisor,
                     f"{quotient} R {remainder}"),
                step("CHECK", f"{divisor}·{quotient} + {remainder}", number,
                     f"0 ≤ {remainder} < {divisor}"),
            ]
            answer = (f"q={quotient}, r={remainder}; "
                      "least-remainder argument confirmed")
        elif variant == "sum_linear":
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
