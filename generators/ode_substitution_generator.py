import random

from base_generator import ProblemGenerator
from helpers import step, jid


def exp_txt(rate):
    if rate == 1:
        return "e^x"
    if rate == -1:
        return "e^(-x)"
    return f"e^({rate}x)"


def coeff_exp_txt(coeff, rate):
    if coeff == 1:
        return exp_txt(rate)
    if coeff == -1:
        return f"-{exp_txt(rate)}"
    return f"{coeff}{exp_txt(rate)}"


def bernoulli_left(a):
    return "dy/dx + y" if a == 1 else f"dy/dx + {a}y"


def y_squared_txt(coeff):
    return "y^2" if coeff == 1 else f"{coeff}y^2"


def exp_term(coeff, rate):
    body = exp_txt(rate)
    return body if abs(coeff) == 1 else f"{abs(coeff)}{body}"


def denominator_txt(m, C, rate):
    body = exp_term(C, rate)
    return f"{m} + {body}" if C > 0 else f"{m} - {body}"


def signed_const(c):
    return f"+ {c}" if c > 0 else f"- {abs(c)}"


def subtract_term(coeff, var):
    return f"- {var}" if coeff == 1 else f"- {coeff}{var}"


def add_term(coeff, var):
    return f"+ {var}" if coeff == 1 else f"+ {coeff}{var}"


def ln_term(coeff):
    if coeff == 1:
        return "ln(x)"
    if coeff == -1:
        return "-ln(x)"
    return f"{coeff} ln(x)"


def ln_combo(coeff, const):
    pieces = [ln_term(coeff)]
    if const > 0:
        pieces.append(f"+ {const}")
    elif const < 0:
        pieces.append(f"- {abs(const)}")
    return " ".join(pieces)


def dx_over_x(coeff):
    if coeff == 1:
        return "dx/x"
    if coeff == -1:
        return "-dx/x"
    return f"{coeff} dx/x"


def if_left_txt(a):
    if a == 1:
        return f"{exp_txt(-a)}u' - {exp_txt(-a)}u"
    return f"{exp_txt(-a)}u' - {a}{exp_txt(-a)}u"


class ODESubstitutionGenerator(ProblemGenerator):
    """
    First-order ODE substitutions.

    Variants:
    - bernoulli:   dy/dx + ay = by^2, u = y^(-1)
    - homogeneous: dy/dx = y/x + c, y = vx

    Op-codes used:
    - ODE_SETUP (established): equation and initial condition
    - SUBSTITUTION: the variable substitution and derivative relation
    - DIVIDE_EQ: divide an equation by a common factor
    - REWRITE / SUBST / ANTIDERIV / INTEG_RULE (established)
    - IFACTOR / MULTIPLY_IF (established in ODE flows)
    - SOLVE_U / BACK_SUB / SOLVE_Y: isolate substituted/original variables
    - D / S / EVAL (established): coefficient and constant arithmetic
    - Z: explicit solution
    """

    VARIANTS = ["bernoulli", "homogeneous"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "bernoulli":
            a = random.randint(1, 5)
            m = random.randint(1, 5)
            b = a * m
            q_choices = [v for v in range(2, 10) if v != m]
            q = random.choice(q_choices)
            C = q - m
            answer = f"y = 1/({denominator_txt(m, C, a)})"
            steps = [
                step("ODE_SETUP",
                     f"{bernoulli_left(a)} = {y_squared_txt(b)}, "
                     f"y(0) = 1/{q}",
                     "Bernoulli n=2"),
                step("SUBSTITUTION", "u = y^(-1)",
                     "u' = -y^(-2) dy/dx"),
                step("DIVIDE_EQ", "divide by y^2",
                     f"y^(-2)dy/dx {add_term(a, 'y^(-1)')} = {b}"),
                step("REWRITE", f"-u' {add_term(a, 'u')} = {b}"),
                step("REWRITE", f"u' {subtract_term(a, 'u')} = {-b}"),
                step("IFACTOR", f"mu = e^(∫ {-a} dx)", exp_txt(-a)),
                step("MULTIPLY_IF", if_left_txt(a), coeff_exp_txt(-b, -a)),
                step("REWRITE", f"({exp_txt(-a)}u)' = "
                     f"{coeff_exp_txt(-b, -a)}"),
                step("D", -b, -a, m),
                step("ANTIDERIV", f"{coeff_exp_txt(-b, -a)} dx",
                     f"{coeff_exp_txt(m, -a)} + C"),
                step("SOLVE_U", f"{exp_txt(-a)}u = "
                     f"{coeff_exp_txt(m, -a)} + C",
                     f"u = {m} + C{exp_txt(a)}"),
                step("SUBST", "x", 0, f"{q} = {m} + C"),
                step("S", q, m, C),
                step("BACK_SUB", "u = 1/y", answer),
            ]
            problem = (
                f"Solve {bernoulli_left(a)} = {y_squared_txt(b)} with "
                f"y(0) = 1/{q} using the Bernoulli substitution "
                f"u = y^(-1)."
            )
        else:
            c = random.choice([v for v in range(-5, 6) if v != 0])
            y1 = random.choice([v for v in range(-5, 6) if v != 0])
            combo = ln_combo(c, y1)
            answer = f"y = x({combo})"
            steps = [
                step("ODE_SETUP",
                     f"dy/dx = y/x {signed_const(c)}, y(1) = {y1}",
                     "homogeneous substitution"),
                step("SUBSTITUTION", "y = vx", "dy/dx = v + x dv/dx"),
                step("SUBST", "y/x = v",
                     f"v + x dv/dx = v {signed_const(c)}"),
                step("REWRITE", f"x dv/dx = {c}"),
                step("SEPARATE", f"dv = {dx_over_x(c)}"),
                step("INTEG_RULE", "both sides",
                     f"∫ dv = ∫ {dx_over_x(c)}"),
                step("ANTIDERIV", "dv", "v"),
                step("ANTIDERIV", dx_over_x(c), f"{ln_term(c)} + C"),
                step("REWRITE", f"v = {ln_term(c)} + C"),
                step("BACK_SUB", "v = y/x",
                     f"y/x = {ln_term(c)} + C"),
                step("EVAL", "ln(1)", 0),
                step("SUBST", "x=1", f"y={y1}", f"{y1} = C"),
                step("SOLVE_Y", f"y/x = {combo}", answer),
            ]
            problem = (
                f"Solve dy/dx = y/x {signed_const(c)} with y(1) = {y1} "
                f"using y = vx (x > 0)."
            )

        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"ode_substitution_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
