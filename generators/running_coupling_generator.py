import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class RunningCouplingGenerator(ProblemGenerator):
    """
    One-loop running coupling in reciprocal form.

    The logarithm L = ln(mu/mu0) is supplied in the problem, so the trace only
    performs exact rational arithmetic:
        1/alpha(mu) = 1/alpha0 + beta*L.

    Op-codes used:
    - RG_SETUP: supplied alpha0, beta, and log ratio L
    - D / M / A (established/shared): exact reciprocal arithmetic
    - CHECK: reciprocal consistency alpha(mu)*(1/alpha(mu)) = 1
    - Z: evolved coupling
    """

    VARIANTS = ["evolve"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        alpha0 = Fraction(random.randint(1, 5), random.randint(10, 60))
        beta = Fraction(random.randint(1, 8), random.randint(1, 6))
        log_ratio = Fraction(random.randint(1, 8), random.randint(1, 6))
        inv_alpha0 = Fraction(1, 1) / alpha0
        shift = beta * log_ratio
        inv_alpha_mu = inv_alpha0 + shift
        alpha_mu = Fraction(1, 1) / inv_alpha_mu
        steps = [
            step("RG_SETUP", "one_loop",
                 f"alpha0={fraction_text(alpha0)}",
                 f"beta={fraction_text(beta)},L={fraction_text(log_ratio)}"),
            step("D", 1, fraction_text(alpha0), fraction_text(inv_alpha0)),
            step("M", fraction_text(beta), fraction_text(log_ratio),
                 fraction_text(shift)),
            step("A", fraction_text(inv_alpha0), fraction_text(shift),
                 fraction_text(inv_alpha_mu)),
            step("D", 1, fraction_text(inv_alpha_mu),
                 fraction_text(alpha_mu)),
            step("M", fraction_text(alpha_mu), fraction_text(inv_alpha_mu),
                 1),
            step("CHECK", "reciprocal",
                 "alpha_mu*inv_alpha_mu", 1),
        ]
        answer = f"alpha(mu) = {fraction_text(alpha_mu)}"
        steps.append(step("Z", answer))
        problem = (
            "At one loop, use 1/alpha(mu)=1/alpha0+beta*L with "
            "L=ln(mu/mu0) supplied. Given "
            f"alpha0={fraction_text(alpha0)}, beta={fraction_text(beta)}, "
            f"and L={fraction_text(log_ratio)}, compute alpha(mu)."
        )
        return dict(
            problem_id=jid(),
            operation="running_coupling_evolve",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
