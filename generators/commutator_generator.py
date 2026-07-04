import random

from base_generator import ProblemGenerator
from helpers import step, jid


def power_text(exp):
    if exp == 0:
        return "1"
    if exp == 1:
        return "x"
    return f"x^{exp}"


def term_text(coeff, exp):
    if coeff == 0:
        return "0"
    body = power_text(exp)
    if exp == 0:
        return str(coeff)
    if coeff == 1:
        return body
    if coeff == -1:
        return f"-{body}"
    return f"{coeff}*{body}"


def imag_term_text(coeff, exp):
    if coeff == 0:
        return "0"
    body = power_text(exp)
    if coeff == 1:
        head = "i"
    elif coeff == -1:
        head = "-i"
    else:
        head = f"{coeff}i"
    if exp == 0:
        return head
    return f"{head}*{body}"


class CommutatorGenerator(ProblemGenerator):
    """
    Operator commutators applied to monomial test functions.

    Variants:
    - d_x: compute [D,x]f and verify it acts like the identity.
    - d_x_squared: compute [D,x^2]f and verify multiplication by 2x.
    - x_p: compute [x,p]f for p=-i*hbar*D and verify i*hbar.

    Op-codes used:
    - COMM_SETUP / COMM_FORMULA / APPLY_OPERATOR / COMM_RESULT
    - POWER_RULE (established): derivative of a monomial
    - A / S / M (established/shared): exact coefficient arithmetic
    - CHECK / Z: identity verification and final commutator action
    """

    VARIANTS = ["d_x", "d_x_squared", "x_p"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "d_x":
            problem, steps, answer = self._generate_d_x()
        elif variant == "d_x_squared":
            problem, steps, answer = self._generate_d_x_squared()
        else:
            problem, steps, answer = self._generate_x_p()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"commutator_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_d_x(self):
        n = random.randint(1, 24)
        n_plus_1 = n + 1
        xf = power_text(n_plus_1)
        d_xf = term_text(n_plus_1, n)
        df = term_text(n, n - 1)
        x_df = term_text(n, n)
        coeff = n_plus_1 - n
        result = term_text(coeff, n)
        steps = [
            step("COMM_SETUP", "[D,x]f", f"f={power_text(n)}", "D=d/dx"),
            step("COMM_FORMULA", "[A,B]f=A(Bf)-B(Af)"),
            step("APPLY_OPERATOR", "x f", xf),
            step("A", n, 1, n_plus_1),
            step("POWER_RULE", xf, d_xf),
            step("POWER_RULE", power_text(n), df),
            step("APPLY_OPERATOR", "x Df", x_df),
            step("S", n_plus_1, n, coeff),
            step("COMM_RESULT", "[D,x]f", result),
            step("CHECK", "identity", "[D,x]=1", "matches f"),
        ]
        answer = f"[D,x]f={result}"
        problem = (
            f"For test function f(x)={power_text(n)}, compute [D,x]f "
            "where D=d/dx."
        )
        return problem, steps, answer

    def _generate_d_x_squared(self):
        n = random.randint(1, 24)
        n_plus_2 = n + 2
        x2f = power_text(n_plus_2)
        d_x2f = term_text(n_plus_2, n + 1)
        df = term_text(n, n - 1)
        x2_df = term_text(n, n + 1)
        coeff = n_plus_2 - n
        result = term_text(coeff, n + 1)
        steps = [
            step("COMM_SETUP", "[D,x^2]f", f"f={power_text(n)}", "D=d/dx"),
            step("COMM_FORMULA", "[A,B]f=A(Bf)-B(Af)"),
            step("APPLY_OPERATOR", "x^2 f", x2f),
            step("A", n, 2, n_plus_2),
            step("POWER_RULE", x2f, d_x2f),
            step("POWER_RULE", power_text(n), df),
            step("APPLY_OPERATOR", "x^2 Df", x2_df),
            step("S", n_plus_2, n, coeff),
            step("COMM_RESULT", "[D,x^2]f", result),
            step("CHECK", "identity", "[D,x^2]=2x", "matches 2x f"),
        ]
        answer = f"[D,x^2]f={result}"
        problem = (
            f"For test function f(x)={power_text(n)}, compute [D,x^2]f "
            "where D=d/dx."
        )
        return problem, steps, answer

    def _generate_x_p(self):
        n = random.randint(1, 24)
        hbar = random.randint(1, 18)
        n_plus_1 = n + 1
        df = term_text(n, n - 1)
        hbar_n = hbar * n
        pf = imag_term_text(-hbar_n, n - 1)
        x_pf = imag_term_text(-hbar_n, n)
        xf = power_text(n_plus_1)
        d_xf = term_text(n_plus_1, n)
        hbar_n_plus_1 = hbar * n_plus_1
        p_xf = imag_term_text(-hbar_n_plus_1, n)
        coeff = -hbar_n - (-hbar_n_plus_1)
        result = imag_term_text(coeff, n)
        steps = [
            step("COMM_SETUP", "[x,p]f", f"f={power_text(n)}",
                 f"p=-i*hbar*D, hbar={hbar}"),
            step("COMM_FORMULA", "[A,B]f=A(Bf)-B(Af)"),
            step("POWER_RULE", power_text(n), df),
            step("M", hbar, n, hbar_n),
            step("APPLY_OPERATOR", "p f", pf),
            step("APPLY_OPERATOR", "x p f", x_pf),
            step("APPLY_OPERATOR", "x f", xf),
            step("A", n, 1, n_plus_1),
            step("POWER_RULE", xf, d_xf),
            step("M", hbar, n_plus_1, hbar_n_plus_1),
            step("APPLY_OPERATOR", "p(x f)", p_xf),
            step("S", -hbar_n, -hbar_n_plus_1, coeff),
            step("COMM_RESULT", "[x,p]f", result),
            step("CHECK", "identity", "[x,p]=i*hbar", f"matches {result}"),
        ]
        answer = f"[x,p]f={result}"
        problem = (
            f"For test function f(x)={power_text(n)} with hbar={hbar}, "
            "compute [x,p]f where p=-i*hbar*d/dx."
        )
        return problem, steps, answer
