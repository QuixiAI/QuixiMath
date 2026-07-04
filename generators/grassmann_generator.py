import random

from base_generator import ProblemGenerator
from helpers import step, jid


def coeff_text(value):
    if value == 1:
        return ""
    if value == -1:
        return "-"
    return str(value)


def theta_term(coeff):
    if coeff == 0:
        return ""
    return f"{coeff_text(coeff)}theta"


def grass_expr(constant, theta_coeff):
    parts = []
    if constant != 0:
        parts.append(str(constant))
    if theta_coeff != 0:
        body = theta_term(abs(theta_coeff))
        if not parts:
            parts.append(theta_term(theta_coeff))
        elif theta_coeff > 0:
            parts.append(f"+ {body}")
        else:
            parts.append(f"- {body}")
    return " ".join(parts) if parts else "0"


def random_coeff():
    return random.choice([n for n in range(-9, 10) if n != 0])


class GrassmannGenerator(ProblemGenerator):
    """
    One-generator Grassmann arithmetic with theta^2 = 0.

    Expressions have the form a + btheta. Products drop the theta^2 term,
    exponentials truncate after the linear term, and Berezin integration
    selects the theta coefficient.

    Op-codes used:
    - GRASSMANN_SETUP: task and input expressions
    - NILPOTENT: theta^2 terms vanish
    - SERIES_TERM: finite series term kept before truncation
    - BEREZIN_RULE: integration rules for 1 and theta
    - GRASSMANN_RESULT: collect constant/theta coefficients
    - M / A (established/shared): exact coefficient arithmetic
    - Z: product, series, or integral result
    """

    VARIANTS = ["multiply", "exponential", "integrate",
                "multiply_integrate"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "multiply":
            problem, steps, answer = self._generate_multiply()
        elif variant == "exponential":
            problem, steps, answer = self._generate_exponential()
        elif variant == "integrate":
            problem, steps, answer = self._generate_integrate()
        else:
            problem, steps, answer = self._generate_multiply_integrate()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"grassmann_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _random_expr(self):
        return random_coeff(), random_coeff()

    def _multiply_steps(self, steps, a, b, c, d):
        constant = a * c
        ad = a * d
        bc = b * c
        bd = b * d
        theta_coeff = ad + bc
        result = grass_expr(constant, theta_coeff)
        steps.extend([
            step("M", a, c, constant),
            step("M", a, d, ad),
            step("M", b, c, bc),
            step("M", b, d, bd),
            step("NILPOTENT", "theta^2=0", f"{bd}theta^2", 0),
            step("A", ad, bc, theta_coeff),
            step("GRASSMANN_RESULT", f"constant={constant}",
                 f"theta={theta_coeff}", result),
        ])
        return constant, theta_coeff, result

    def _generate_multiply(self):
        a, b = self._random_expr()
        c, d = self._random_expr()
        x = grass_expr(a, b)
        y = grass_expr(c, d)
        steps = [
            step("GRASSMANN_SETUP", "multiply", f"x={x}", f"y={y}"),
        ]
        _, _, result = self._multiply_steps(steps, a, b, c, d)
        answer = f"x*y = {result}"
        problem = f"Let theta^2=0. Multiply x={x} by y={y}."
        return problem, steps, answer

    def _generate_exponential(self):
        k = random_coeff()
        argument = theta_term(k)
        result = grass_expr(1, k)
        steps = [
            step("GRASSMANN_SETUP", "exponential", f"arg={argument}",
                 "theta^2=0"),
            step("SERIES_TERM", "n=0", 1, 1),
            step("SERIES_TERM", "n=1", argument, argument),
            step("NILPOTENT", "n>=2", "theta^2=0", 0),
            step("GRASSMANN_RESULT", "constant=1", f"theta={k}", result),
        ]
        answer = f"exp({argument}) = {result}"
        problem = (
            f"Let theta^2=0. Expand exp({argument}) as a finite "
            "Grassmann series."
        )
        return problem, steps, answer

    def _generate_integrate(self):
        a, b = self._random_expr()
        expr = grass_expr(a, b)
        const_part = a * 0
        theta_part = b * 1
        integral = const_part + theta_part
        steps = [
            step("GRASSMANN_SETUP", "integrate", f"expr={expr}",
                 "int1=0,inttheta=1"),
            step("BEREZIN_RULE", "int dtheta 1", 0),
            step("BEREZIN_RULE", "int dtheta theta", 1),
            step("M", a, 0, const_part),
            step("M", b, 1, theta_part),
            step("A", const_part, theta_part, integral),
        ]
        answer = f"integral = {integral}"
        problem = (
            "Using Berezin rules int dtheta 1=0 and int dtheta theta=1, "
            f"compute int dtheta ({expr})."
        )
        return problem, steps, answer

    def _generate_multiply_integrate(self):
        a, b = self._random_expr()
        c, d = self._random_expr()
        x = grass_expr(a, b)
        y = grass_expr(c, d)
        steps = [
            step("GRASSMANN_SETUP", "multiply_integrate",
                 f"x={x}", f"y={y}"),
        ]
        constant, theta_coeff, _ = self._multiply_steps(steps, a, b, c, d)
        const_part = constant * 0
        theta_part = theta_coeff * 1
        integral = const_part + theta_part
        steps.extend([
            step("BEREZIN_RULE", "int dtheta 1", 0),
            step("BEREZIN_RULE", "int dtheta theta", 1),
            step("M", constant, 0, const_part),
            step("M", theta_coeff, 1, theta_part),
            step("A", const_part, theta_part, integral),
        ])
        answer = f"integral = {integral}"
        problem = (
            "Let theta^2=0 with Berezin rules int dtheta 1=0 and "
            f"int dtheta theta=1. Compute int dtheta [(x)*(y)] for "
            f"x={x} and y={y}."
        )
        return problem, steps, answer
