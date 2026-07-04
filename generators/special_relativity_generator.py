import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


BETA_GAMMA = [
    (Fraction(3, 5), Fraction(5, 4)),
    (Fraction(5, 13), Fraction(13, 12)),
    (Fraction(8, 17), Fraction(17, 15)),
    (Fraction(7, 25), Fraction(25, 24)),
    (Fraction(20, 29), Fraction(29, 21)),
    (Fraction(12, 37), Fraction(37, 35)),
    (Fraction(9, 41), Fraction(41, 40)),
]


def fraction_text(value):
    return str(Fraction(value))


class SpecialRelativityGenerator(ProblemGenerator):
    """
    Special-relativity time dilation, length contraction, and 1D Lorentz
    event transformations with exact supplied beta and gamma.

    Variants:
    - time_dilation: t = gamma*tau.
    - length_contraction: L = L0/gamma.
    - lorentz_event: ct' = gamma(ct-beta*x), x' = gamma(x-beta*ct).

    Op-codes used:
    - REL_SETUP / REL_FORMULA
    - M / S / D (established/shared): exact Fraction arithmetic
    - Z: dilated time, contracted length, or transformed event
    """

    VARIANTS = ["time_dilation", "length_contraction", "lorentz_event"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "time_dilation":
            problem, steps, answer = self._generate_time_dilation()
        elif variant == "length_contraction":
            problem, steps, answer = self._generate_length_contraction()
        else:
            problem, steps, answer = self._generate_lorentz_event()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"special_relativity_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    @staticmethod
    def _beta_gamma():
        return random.choice(BETA_GAMMA)

    def _generate_time_dilation(self):
        beta, gamma = self._beta_gamma()
        proper_time = random.randint(1, 80)
        observed = gamma * proper_time
        steps = [
            step("REL_SETUP", "time_dilation",
                 f"beta={fraction_text(beta)}", f"gamma={fraction_text(gamma)}"),
            step("REL_FORMULA", "t=gamma*tau"),
            step("M", fraction_text(gamma), proper_time,
                 fraction_text(observed)),
        ]
        answer = f"t={fraction_text(observed)} s"
        problem = (
            f"A clock has proper time tau={proper_time} s and moves with "
            f"beta={fraction_text(beta)} where gamma={fraction_text(gamma)}. "
            "Find the dilated time t."
        )
        return problem, steps, answer

    def _generate_length_contraction(self):
        beta, gamma = self._beta_gamma()
        proper_length = random.randint(1, 80)
        contracted = Fraction(proper_length, 1) / gamma
        steps = [
            step("REL_SETUP", "length_contraction",
                 f"beta={fraction_text(beta)}", f"gamma={fraction_text(gamma)}"),
            step("REL_FORMULA", "L=L0/gamma"),
            step("D", proper_length, fraction_text(gamma),
                 fraction_text(contracted)),
        ]
        answer = f"L={fraction_text(contracted)} m"
        problem = (
            f"A rod has proper length L0={proper_length} m and moves with "
            f"beta={fraction_text(beta)} where gamma={fraction_text(gamma)}. "
            "Find the contracted length L."
        )
        return problem, steps, answer

    def _generate_lorentz_event(self):
        beta, gamma = self._beta_gamma()
        ct = random.randint(-30, 30)
        x = random.randint(-30, 30)
        if ct == 0 and x == 0:
            ct = 1
        beta_x = beta * x
        ct_minus = Fraction(ct) - beta_x
        ct_prime = gamma * ct_minus
        beta_ct = beta * ct
        x_minus = Fraction(x) - beta_ct
        x_prime = gamma * x_minus
        steps = [
            step("REL_SETUP", "lorentz_event",
                 f"beta={fraction_text(beta)}, gamma={fraction_text(gamma)}",
                 f"ct={ct}, x={x}"),
            step("REL_FORMULA",
                 "ct_prime=gamma*(ct-beta*x), x_prime=gamma*(x-beta*ct)"),
            step("M", fraction_text(beta), x, fraction_text(beta_x)),
            step("S", ct, fraction_text(beta_x), fraction_text(ct_minus)),
            step("M", fraction_text(gamma), fraction_text(ct_minus),
                 fraction_text(ct_prime)),
            step("M", fraction_text(beta), ct, fraction_text(beta_ct)),
            step("S", x, fraction_text(beta_ct), fraction_text(x_minus)),
            step("M", fraction_text(gamma), fraction_text(x_minus),
                 fraction_text(x_prime)),
        ]
        answer = (
            f"ct_prime={fraction_text(ct_prime)}; "
            f"x_prime={fraction_text(x_prime)}"
        )
        problem = (
            f"A frame has beta={fraction_text(beta)} and "
            f"gamma={fraction_text(gamma)}. For event ct={ct}, x={x} "
            "in c=1 units, compute ct_prime and x_prime."
        )
        return problem, steps, answer
