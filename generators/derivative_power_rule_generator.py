import random
from base_generator import ProblemGenerator
from helpers import step, jid


def term_pow(c, n, var="x"):
    """One term c·x^n: '4x^3', 'x', '-x^2', '7', '3x^(-2)'."""
    if n == 0:
        return str(c)
    head = {1: "", -1: "-"}.get(c, str(c))
    if n == 1:
        return f"{head}{var}"
    p = f"^{n}" if n > 0 else f"^({n})"
    return f"{head}{var}{p}"


def poly_pow(terms, var="x"):
    """Sign-aware sum of (c, n) terms, highest power first."""
    parts = []
    for c, n in terms:
        if c == 0:
            continue
        t = term_pow(abs(c), n, var)
        if not parts:
            parts.append(term_pow(c, n, var))
        else:
            parts.append(f"+ {t}" if c > 0 else f"- {t}")
    return " ".join(parts) if parts else "0"


class DerivativePowerRuleGenerator(ProblemGenerator):
    """
    The power rule over sums: every term differentiated with its
    coefficient product shown, the linear term dropping to a constant,
    and the constant term explicitly sent to 0. A variant mixes in
    negative exponents.

    Op-codes used:
    - DERIV_SETUP: the function and the goal (function, goal)
    - DERIV_RULE: the rule statement (name, formula)
    - M: c·n for each term (established)
    - POWER_RULE: one term differentiated (term, derivative)
    - REWRITE / Z: the assembled derivative (established)
    """

    VARIANTS = ["polynomial", "negative_power"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or \
            random.choice(["polynomial", "polynomial", "negative_power"])

        if variant == "polynomial":
            degs = sorted(random.sample(range(0, 6), random.randint(3, 4)),
                          reverse=True)
        else:
            pos = sorted(random.sample(range(1, 4), 2), reverse=True)
            negs = sorted(random.sample([-1, -2, -3], 1))
            degs = pos + negs
        terms = [(random.choice([v for v in range(-7, 8) if v != 0]), n)
                 for n in degs]

        f_txt = poly_pow(terms)
        steps = [
            step("DERIV_SETUP", f"f(x) = {f_txt}", "f'(x)"),
            step("DERIV_RULE", "power rule",
                 "d/dx of c·x^n = c·n·x^(n-1)"),
        ]
        dterms = []
        for c, n in terms:
            if n == 0:
                steps.append(step("POWER_RULE", term_pow(c, 0),
                                  "0 (constant rule)"))
                continue
            if n != 1:
                steps.append(step("M", c, n, c * n))
            d = (c * n, n - 1)
            steps.append(step("POWER_RULE", term_pow(c, n),
                              term_pow(*d)))
            dterms.append(d)
        deriv = poly_pow(dterms)
        answer = f"f'(x) = {deriv}"
        steps.append(step("REWRITE", answer))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"derivative_power_{variant}",
            problem=f"Differentiate f(x) = {f_txt}.",
            steps=steps,
            final_answer=answer,
        )
