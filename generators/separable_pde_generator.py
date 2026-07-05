import random

from base_generator import ProblemGenerator
from helpers import step, jid


def sq(n):
    return n * n


class SeparablePDEGenerator(ProblemGenerator):
    """
    Exact single-mode separable PDE examples.

    Variants:
    - heat_single_mode: heat equation on [0,L] with one sine mode.
    - wave_dalembert: wave equation value from d'Alembert with f(x)=x^2
      and zero initial velocity.

    Op-codes used:
    - PDE_SETUP / SEPARATE / EIGENVALUE / DALEMBERT
    - M / A (established)
    - Z: exact symbolic solution or value
    """

    VARIANTS = ["heat_single_mode", "wave_dalembert"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "heat_single_mode":
            alpha = random.randint(1, 12)
            L = random.randint(2, 12)
            n = random.randint(1, 10)
            amp = random.randint(1, 20)
            lam = f"({n}π/{L})^2"
            decay = f"e^(-{alpha}{lam}t)"
            answer = f"u(x,t)={amp}{decay}sin({n}πx/{L})"
            steps = [
                step("PDE_SETUP", f"u_t = {alpha}u_xx on [0,{L}]",
                     f"u(x,0)={amp}sin({n}πx/{L})"),
                step("SEPARATE", "X'' + λX = 0", "T' = -αλT"),
                step("EIGENVALUE", f"λ = {lam}"),
                step("REWRITE", answer),
            ]
            problem = (
                f"Solve u_t = {alpha}u_xx on 0≤x≤{L} with zero endpoint "
                f"conditions and u(x,0)={amp}sin({n}πx/{L})."
            )
        else:
            c = random.randint(1, 12)
            x0 = random.randint(1, 30)
            t0 = random.randint(1, 20)
            left = x0 - c * t0
            right = x0 + c * t0
            value = (sq(left) + sq(right)) // 2
            steps = [
                step("PDE_SETUP", f"u_tt = {c * c}u_xx",
                     "u(x,0)=x^2, u_t(x,0)=0"),
                step("DALEMBERT", "u=(f(x-ct)+f(x+ct))/2"),
                step("S", x0, c * t0, left),
                step("A", x0, c * t0, right),
                step("M", left, left, sq(left)),
                step("M", right, right, sq(right)),
                step("A", sq(left), sq(right), sq(left) + sq(right)),
                step("D", sq(left) + sq(right), 2, value),
            ]
            answer = f"u({x0},{t0})={value}"
            problem = (
                f"For u_tt = {c * c}u_xx with u(x,0)=x^2 and u_t(x,0)=0, "
                f"use d'Alembert's formula to find u({x0},{t0})."
            )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"separable_pde_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
