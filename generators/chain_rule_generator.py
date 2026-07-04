import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.domain_range_generator import lin


class ChainRuleGenerator(ProblemGenerator):
    """
    The chain rule with an explicit substitution for every layer.

    Variants:
    - linear_power:    y = (ax + b)^n — one substitution, constants
                       multiplied through
    - quadratic_power: y = (x² + bx + c)^n — answer left in product
                       form n(inner)^(n-1)·(2x + b)
    - nested:          y = ((x² + a)^m + b)^k — two substitutions,
                       peeled outside-in, all constants collected

    Op-codes used:
    - DERIV_SETUP / DERIV_RULE / POWER_RULE (established)
    - SUBST: name each layer u, v (established)
    - M: multiply the layer constants (established)
    - REWRITE / Z: the assembled derivative (established)
    """

    VARIANTS = ["linear_power", "quadratic_power", "nested"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "linear_power":
            a = random.choice([v for v in range(-5, 6)
                               if v not in (-1, 0, 1)])
            b = random.choice([v for v in range(-9, 10) if v != 0])
            n = random.randint(3, 6)
            inner = lin(a, b, "x")
            coef = n * a
            answer = f"y' = {coef}({inner})^{n - 1}"
            steps = [
                step("DERIV_SETUP", f"y = ({inner})^{n}", "y'"),
                step("DERIV_RULE", "chain rule",
                     "dy/dx = dy/du · du/dx"),
                step("SUBST", "u", inner, f"y = u^{n}"),
                step("POWER_RULE", f"u^{n}", f"{n}u^{n - 1}"),
                step("POWER_RULE", inner, str(a)),
                step("M", n, a, coef),
                step("REWRITE", answer),
            ]
            problem = f"Differentiate y = ({inner})^{n}."
        elif variant == "quadratic_power":
            b = random.choice([v for v in range(-6, 7) if v != 0])
            c = random.choice([v for v in range(-9, 10) if v != 0])
            n = random.randint(2, 4)
            inner = (f"x^2 {'+' if b > 0 else '-'} "
                     f"{'x' if abs(b) == 1 else str(abs(b)) + 'x'} "
                     f"{'+' if c > 0 else '-'} {abs(c)}")
            dinner = lin(2, b, "x")
            ip = f"({inner})" if n == 2 else f"({inner})^{n - 1}"
            up = "u" if n == 2 else f"u^{n - 1}"
            answer = f"y' = {n}{ip}({dinner})"
            steps = [
                step("DERIV_SETUP", f"y = ({inner})^{n}", "y'"),
                step("DERIV_RULE", "chain rule",
                     "dy/dx = dy/du · du/dx"),
                step("SUBST", "u", inner, f"y = u^{n}"),
                step("POWER_RULE", f"u^{n}", f"{n}{up}"),
                step("POWER_RULE", inner, dinner),
                step("REWRITE", answer),
            ]
            problem = f"Differentiate y = ({inner})^{n}."
        else:
            a = random.choice([v for v in range(-6, 7) if v != 0])
            b = random.choice([v for v in range(-9, 10) if v != 0])
            k, m = random.choice([(2, 3), (3, 2), (2, 2)])
            v_txt = f"x^2 {'+' if a > 0 else '-'} {abs(a)}"
            u_txt = (f"({v_txt})^{m} {'+' if b > 0 else '-'} {abs(b)}")
            y_txt = f"(({v_txt})^{m} {'+' if b > 0 else '-'} {abs(b)})^{k}"
            coef = k * m * 2

            def pw(base, e):
                return base if e == 1 else f"{base}^{e}"

            answer = (f"y' = {coef}x{pw(f'({v_txt})', m - 1)}"
                      f"{pw(f'({u_txt})', k - 1)}")
            steps = [
                step("DERIV_SETUP", f"y = {y_txt}", "y'"),
                step("DERIV_RULE", "chain rule (two layers)",
                     "peel from the outside in"),
                step("SUBST", "u", u_txt, f"y = u^{k}"),
                step("POWER_RULE", f"u^{k}", f"{k}{pw('u', k - 1)}"),
                step("SUBST", "v", v_txt,
                     f"u = v^{m} {'+' if b > 0 else '-'} {abs(b)}"),
                step("POWER_RULE", f"v^{m}", f"{m}{pw('v', m - 1)}"),
                step("POWER_RULE", v_txt, "2x"),
                step("M", k, m, k * m),
                step("M", k * m, 2, coef),
                step("REWRITE", answer),
            ]
            problem = f"Differentiate y = {y_txt}."
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"chain_rule_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
