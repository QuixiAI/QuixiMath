import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec


def fmt(value):
    value = Fraction(value)
    return dec(value) if value.denominator in (1, 2, 4, 5, 8, 10, 20, 25) else str(value)


class EquilibriumICEGenerator(ProblemGenerator):
    """
    Chemistry equilibrium problems using ICE-table bookkeeping.

    Variants:
    - compute_k: compute K from equilibrium concentrations.
    - solve_x: solve for the exact reaction extent x in A ⇌ 2B.
    - direction: compare Q with K and predict reaction direction.

    Op-codes used:
    - ICE_ROW / K_EXPR / Q_EXPR / COMPARE
    - A / S / M / D (established)
    - Z: exact K, x, or composite direction
    """

    VARIANTS = ["compute_k", "solve_x", "direction"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "compute_k":
            a = Fraction(random.randint(1, 12), random.choice([1, 2, 4]))
            b = Fraction(random.randint(1, 12), random.choice([1, 2, 4]))
            K = b / a
            steps = [
                step("ICE_ROW", "equilibrium", f"[A]={fmt(a)}, [B]={fmt(b)}"),
                step("K_EXPR", "K = [B]/[A]"),
                step("D", fmt(b), fmt(a), fmt(K)),
            ]
            answer = f"K={fmt(K)}"
            problem = (
                f"For A ⇌ B, the equilibrium concentrations are [A]={fmt(a)} "
                f"and [B]={fmt(b)}. Compute K=[B]/[A]."
            )
        elif variant == "solve_x":
            a0 = random.randint(3, 12)
            x = random.randint(1, a0 - 1)
            K = Fraction(4 * x * x, a0 - x)
            b_eq = 2 * x
            a_eq = a0 - x
            steps = [
                step("ICE_ROW", "initial", f"[A]={a0}, [B]=0"),
                step("ICE_ROW", "change", f"[A]=-x, [B]=+2x"),
                step("ICE_ROW", "equilibrium", f"[A]={a0}-x, [B]=2x"),
                step("K_EXPR", "K = [B]^2/[A]",
                     f"{fmt(K)} = (2x)^2/({a0}-x)"),
                step("M", 2, x, b_eq),
                step("M", b_eq, b_eq, b_eq * b_eq),
                step("S", a0, x, a_eq),
                step("D", b_eq * b_eq, a_eq, fmt(K)),
                step("CHECK", "substitute x", f"x={x}", "matches K"),
            ]
            answer = f"x={x}; [A]={a_eq}, [B]={b_eq}"
            problem = (
                f"For A ⇌ 2B, initially [A]={a0} and [B]=0. At equilibrium "
                f"[A]={a0}-x and [B]=2x. Given K={fmt(K)} for K=[B]^2/[A], "
                f"find x."
            )
        else:
            K = Fraction(random.randint(1, 12), random.choice([1, 2, 3, 4]))
            a = Fraction(random.randint(1, 12), random.choice([1, 2, 4]))
            q_choice = random.choice(["forward", "reverse", "equilibrium"])
            if q_choice == "forward":
                Q = K / random.randint(2, 5)
            elif q_choice == "reverse":
                Q = K * random.randint(2, 5)
            else:
                Q = K
            b = Q * a
            rel = "<" if Q < K else (">" if Q > K else "=")
            direction = {
                "<": "forward",
                ">": "reverse",
                "=": "at equilibrium",
            }[rel]
            steps = [
                step("ICE_ROW", "current", f"[A]={fmt(a)}, [B]={fmt(b)}"),
                step("Q_EXPR", "Q = [B]/[A]"),
                step("D", fmt(b), fmt(a), fmt(Q)),
                step("COMPARE", f"Q {rel} K", f"{fmt(Q)} {rel} {fmt(K)}"),
            ]
            answer = f"{direction} (Q={fmt(Q)} {rel} K={fmt(K)})"
            problem = (
                f"For A ⇌ B with K={fmt(K)}, the current concentrations are "
                f"[A]={fmt(a)} and [B]={fmt(b)}. Compute Q=[B]/[A] and "
                f"predict the reaction direction."
            )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"equilibrium_ice_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
