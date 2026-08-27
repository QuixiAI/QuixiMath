import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.domain_range_generator import lin


# Variables that never collide with the chain-rule placeholder `u`.
VARS = ["x", "t", "s", "w", "z", "r", "v"]

TRIG_RULES = {
    "sin": ("d/dx sin(u) = cos(u)·u'", "cos({inner})", 1),
    "cos": ("d/dx cos(u) = -sin(u)·u'", "sin({inner})", -1),
    "tan": ("d/dx tan(u) = sec^2(u)·u'", "sec^2({inner})", 1),
    "sec": ("d/dx sec(u) = sec(u)tan(u)·u'", "sec({inner})tan({inner})", 1),
    "csc": ("d/dx csc(u) = -csc(u)cot(u)·u'", "csc({inner})cot({inner})", -1),
    "cot": ("d/dx cot(u) = -csc^2(u)·u'", "csc^2({inner})", -1),
}

BASES = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12]


def cmul(c, body):
    """c·body with unit coefficients hidden: '5 sin(3x)', '-e^(2x)',
    '-4·5^x' (explicit dot before a numeric base)."""
    if c == 1:
        return body
    if c == -1:
        return f"-{body}"
    if body[0].isdigit():
        return f"{c}·{body}"
    return f"{c} {body}" if body[0].isalpha() else f"{c}{body}"


def over(num, den):
    """num/den with the numerator always shown (1/x, -3/x, 12/x)."""
    return f"{num}/{den}"


class DerivativeTranscendentalGenerator(ProblemGenerator):
    """
    Derivatives of trig, exponential, and logarithmic functions with a
    linear (or power) inner function, the chain factor shown every time.

    Variants:
    - trig: c·f(kx) and c·f(ax + b) for f in sin, cos, tan, sec, csc, cot
    - exp:  c·e^(inner), c·a^x with the ln a factor, and c·a^(inner)
    - log:  c·ln(kx) — where the k cancels to c/x — c·ln(ax + b),
      c·ln(x^m) via the power-of-a-log rewrite, c·log_a(x), and
      c·log_a(ax + b)

    Op-codes used:
    - DERIV_SETUP / DERIV_RULE / POWER_RULE / M / CANCEL / REWRITE
      (established)
    - LOG_POWER: pull the exponent out of a logarithm before differentiating
    - Z: the derivative
    """

    VARIANTS = ["trig", "exp", "log"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    # ------------------------------------------------------------ context

    @staticmethod
    def _coefficient():
        return random.choice([v for v in range(-15, 16) if v != 0])

    @staticmethod
    def _inner(var, allow_shift=True):
        """Returns (text, slope). Either kx or ax + b."""
        if allow_shift and random.random() < 0.65:
            a = random.randint(2, 9)
            b = random.choice([v for v in range(-9, 10) if v != 0])
            return lin(a, b, var), a
        k = random.randint(2, 15)
        return f"{k}{var}", k

    @staticmethod
    def _phrase(body, var):
        idx = random.randrange(5)
        if idx == 0:
            return f"Differentiate y = {body}."
        if idx == 1:
            return f"Find dy/d{var} for y = {body}."
        if idx == 2:
            return f"Compute y' for the function y = {body}."
        if idx == 3:
            return f"Let y = {body}. Find y'."
        return f"What is the derivative of y = {body} with respect to {var}?"

    # ------------------------------------------------------------ variants

    def _trig(self, var):
        c = self._coefficient()
        fn = random.choice(list(TRIG_RULES))
        inner, slope = self._inner(var)
        rule, out_body, sign = TRIG_RULES[fn]
        body = cmul(c, f"{fn}({inner})")
        out_c = sign * c * slope
        answer = f"y' = {cmul(out_c, out_body.format(inner=inner))}"
        steps = [
            step("DERIV_SETUP", f"y = {body}", "y'"),
            step("DERIV_RULE", rule, f"u = {inner}"),
            step("POWER_RULE", inner, str(slope)),
            step("M", sign * c, slope, out_c),
            step("REWRITE", answer),
        ]
        return body, answer, steps

    def _exp(self, var):
        c = self._coefficient()
        roll = random.random()
        if roll < 0.45:
            inner, slope = self._inner(var)
            body = cmul(c, f"e^({inner})")
            out_c = c * slope
            answer = f"y' = {cmul(out_c, f'e^({inner})')}"
            steps = [
                step("DERIV_SETUP", f"y = {body}", "y'"),
                step("DERIV_RULE", "d/dx e^u = e^u·u'", f"u = {inner}"),
                step("POWER_RULE", inner, str(slope)),
                step("M", c, slope, out_c),
                step("REWRITE", answer),
            ]
        elif roll < 0.60:
            base = random.choice(BASES)
            body = cmul(c, f"{base}^{var}")
            answer = f"y' = {cmul(c, f'{base}^{var}')} ln {base}"
            steps = [
                step("DERIV_SETUP", f"y = {body}", "y'"),
                step("DERIV_RULE", "d/dx a^x = a^x ln a", f"a = {base}"),
                step("REWRITE", answer),
            ]
        else:
            base = random.choice(BASES)
            inner, slope = self._inner(var)
            body = cmul(c, f"{base}^({inner})")
            out_c = c * slope
            answer = f"y' = {cmul(out_c, f'{base}^({inner})')} ln {base}"
            steps = [
                step("DERIV_SETUP", f"y = {body}", "y'"),
                step("DERIV_RULE", "d/dx a^u = a^u ln a·u'",
                     f"a = {base}, u = {inner}"),
                step("POWER_RULE", inner, str(slope)),
                step("M", c, slope, out_c),
                step("REWRITE", answer),
            ]
        return body, answer, steps

    def _log(self, var):
        c = self._coefficient()
        roll = random.random()
        if roll < 0.15:
            k = random.randint(2, 15)
            inner = f"{k}{var}"
            body = cmul(c, f"ln({inner})")
            answer = f"y' = {over(c, var)}"
            steps = [
                step("DERIV_SETUP", f"y = {body}", "y'"),
                step("DERIV_RULE", "d/dx ln(u) = u'/u", f"u = {inner}"),
                step("POWER_RULE", inner, str(k)),
                step("REWRITE", f"y' = {cmul(c, f'{k}/({inner})')}"),
                step("CANCEL", str(k), over(c, var)),
                step("REWRITE", answer),
            ]
        elif roll < 0.55:
            a = random.randint(2, 9)
            b = random.choice([v for v in range(-9, 10) if v != 0])
            inner = lin(a, b, var)
            body = cmul(c, f"ln({inner})")
            num = c * a
            answer = f"y' = {num}/({inner})"
            steps = [
                step("DERIV_SETUP", f"y = {body}", "y'"),
                step("DERIV_RULE", "d/dx ln(u) = u'/u", f"u = {inner}"),
                step("POWER_RULE", inner, str(a)),
                step("M", c, a, num),
                step("REWRITE", answer),
            ]
        elif roll < 0.65:
            m = random.randint(2, 15)
            body = cmul(c, f"ln({var}^{m})")
            num = c * m
            answer = f"y' = {over(num, var)}"
            steps = [
                step("DERIV_SETUP", f"y = {body}", "y'"),
                step("LOG_POWER", f"ln({var}^{m})", f"{m} ln({var})"),
                step("M", c, m, num),
                step("REWRITE", f"y = {cmul(num, f'ln({var})')}"),
                step("DERIV_RULE", "d/dx ln(x) = 1/x", f"u = {var}"),
                step("REWRITE", answer),
            ]
        elif roll < 0.75:
            base = random.choice(BASES)
            body = cmul(c, f"log_{base}({var})")
            answer = f"y' = {c}/({var} ln {base})"
            steps = [
                step("DERIV_SETUP", f"y = {body}", "y'"),
                step("DERIV_RULE", "d/dx log_a(x) = 1/(x ln a)",
                     f"a = {base}"),
                step("REWRITE", answer),
            ]
        else:
            base = random.choice(BASES)
            inner, slope = self._inner(var)
            body = cmul(c, f"log_{base}({inner})")
            num = c * slope
            answer = f"y' = {num}/(({inner}) ln {base})"
            steps = [
                step("DERIV_SETUP", f"y = {body}", "y'"),
                step("DERIV_RULE", "d/dx log_a(u) = u'/(u ln a)",
                     f"a = {base}, u = {inner}"),
                step("POWER_RULE", inner, str(slope)),
                step("M", c, slope, num),
                step("REWRITE", answer),
            ]
        return body, answer, steps

    # ------------------------------------------------------------ generate

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        var = random.choice(VARS)
        builder = {"trig": self._trig, "exp": self._exp, "log": self._log}
        body, answer, steps = builder[variant](var)
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"derivative_transcendental_{variant}",
            problem=self._phrase(body, var),
            steps=steps,
            final_answer=answer,
        )
