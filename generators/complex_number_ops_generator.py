import random
from base_generator import ProblemGenerator
from helpers import step, jid


def cx(re, im):
    """Renders a + bi in standard form: '5 - 3i', '-i', '7', '4i'."""
    if im == 0:
        return str(re)
    if im == 1:
        imt = "i"
    elif im == -1:
        imt = "-i"
    else:
        imt = f"{im}i"
    if re == 0:
        return imt
    return f"{re} + {imt}" if im > 0 else f"{re} - {imt.lstrip('-')}"


def wrap_i(coef):
    """Coefficient-of-i factor for FOIL text: '4i', '(-7i)'."""
    t = cx(0, coef)
    return f"({t})" if coef < 0 else t


class ComplexNumberOpsGenerator(ProblemGenerator):
    """
    Complex number arithmetic: powers of i, addition, subtraction, and
    multiplication.

    Powers of i reduce through the 4-cycle explicitly: divide the
    exponent by 4, keep the remainder, rewrite, and read the cycle.
    Multiplication FOILs, converts the i^2 term with an explicit
    substitution, then combines real and imaginary parts.

    Op-codes used:
    - CX_SETUP: the expression and the operation (expression, goal)
    - D / R: exponent divided by 4, quotient and remainder (established)
    - REWRITE: i^n split as (i^4)^q · i^r; grouped real/imag parts
    - I_CYCLE: read i^r from the cycle (power, value)
    - FOIL_SETUP / FOIL_F / FOIL_O / FOIL_I / FOIL_L: the expansion
      (established)
    - I_SQUARE: substitute i^2 = -1 (term with i^2, converted value)
    - A / S: combining parts (established)
    - Z: final answer in standard form
    """

    VARIANTS = ["power_i", "add", "subtract", "multiply"]
    CYCLE = {0: "1", 1: "i", 2: "-1", 3: "-i"}

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "power_i":
            n = random.randint(5, 50)
            q, r = divmod(n, 4)
            answer = self.CYCLE[r]
            steps = [
                step("CX_SETUP", f"i^{n}", "simplify"),
                step("D", n, 4, q),
                step("R", r),
                step("REWRITE", f"i^{n} = (i^4)^{q} · i^{r}"),
                step("I_CYCLE", f"i^{r}", answer),
                step("Z", answer),
            ]
            problem = f"Simplify: i^{n}."
            return self._pack("complex_power_i", problem, steps, answer)

        a, b = (random.choice([v for v in range(-9, 10) if v != 0])
                for _ in range(2))
        c, d = (random.choice([v for v in range(-9, 10) if v != 0])
                for _ in range(2))
        z1, z2 = cx(a, b), cx(c, d)

        if variant in ("add", "subtract"):
            sign = 1 if variant == "add" else -1
            re_v, im_v = a + sign * c, b + sign * d
            answer = cx(re_v, im_v)
            op_txt = "+" if variant == "add" else "-"
            wc = f"({c})" if c < 0 else str(c)
            wd = f"({d})" if d < 0 else str(d)
            steps = [
                step("CX_SETUP", f"({z1}) {op_txt} ({z2})", variant),
                step("REWRITE",
                     f"({a} {op_txt} {wc}) + ({b} {op_txt} {wd})i"),
                step("A" if sign == 1 else "S", a, c, re_v),
                step("A" if sign == 1 else "S", b, d, im_v),
                step("Z", answer),
            ]
            problem = (f"{'Add' if sign == 1 else 'Subtract'}: "
                       f"({z1}) {op_txt} ({z2}).")
            return self._pack(f"complex_{variant}", problem, steps, answer)

        f_v = a * c
        o_v = a * d          # coefficient of i
        i_v = b * c          # coefficient of i
        l_v = b * d          # coefficient of i^2
        re_v = f_v - l_v
        im_v = o_v + i_v
        answer = cx(re_v, im_v)
        wa = f"({a})" if a < 0 else str(a)
        wc = f"({c})" if c < 0 else str(c)
        steps = [
            step("CX_SETUP", f"({z1})({z2})", "multiply"),
            step("FOIL_SETUP", f"({z1})({z2})"),
            step("FOIL_F", f"First: {wa} * {wc}", f_v),
            step("FOIL_O", f"Outer: {wa} * {wrap_i(d)}", cx(0, o_v)),
            step("FOIL_I", f"Inner: {wrap_i(b)} * {wc}", cx(0, i_v)),
            step("FOIL_L", f"Last: {wrap_i(b)} * {wrap_i(d)}",
                 f"{l_v}i^2"),
            step("I_SQUARE", f"{l_v}i^2", -l_v),
            step("A", f_v, -l_v, re_v),
            step("A", o_v, i_v, im_v),
            step("Z", answer),
        ]
        problem = f"Multiply: ({z1})({z2})."
        return self._pack("complex_multiply", problem, steps, answer)

    @staticmethod
    def _pack(op, problem, steps, answer):
        return dict(
            problem_id=jid(),
            operation=op,
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
