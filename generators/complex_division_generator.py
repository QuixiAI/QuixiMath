import math
import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.complex_number_ops_generator import cx, wrap_i


def cxf(re, im):
    """Standard form with exact Fraction parts: '7/5 - (4/5)i'."""
    def imt(v):
        if v == 1:
            return "i"
        if v == -1:
            return "-i"
        if v.denominator == 1:
            return f"{v}i"
        return f"({v})i" if v > 0 else f"-({-v})i"

    if im == 0:
        return str(re)
    if re == 0:
        return imt(im)
    if im > 0:
        return f"{re} + {imt(im)}"
    return f"{re} - {imt(-im).lstrip('-') if im.denominator == 1 else imt(-im)}"


class ComplexDivisionGenerator(ProblemGenerator):
    """
    Divides complex numbers by multiplying numerator and denominator by
    the conjugate. The numerator is FOILed in full with the i^2
    substitution; the denominator uses c^2 + d^2 with both squares
    computed. Each part of the quotient is reduced to lowest terms.

    Op-codes used:
    - CX_SETUP: the quotient and the operation (established)
    - CONJUGATE: the conjugate of the denominator (denominator, conjugate)
    - REWRITE: the multiply-by-conjugate plan and intermediate forms
    - FOIL_SETUP / FOIL_F / FOIL_O / FOIL_I / FOIL_L: numerator expansion
    - I_SQUARE: substitute i^2 = -1 (established)
    - E / A: denominator squares and sums (established)
    - EVAL: record numerator and denominator values (established)
    - FRAC_REDUCE: reduce one part to lowest terms (established)
    - Z: final answer in standard form
    """

    def generate(self) -> dict:
        a, b, c, d = (random.choice([v for v in range(-6, 7) if v != 0])
                      for _ in range(4))
        z1, z2 = cx(a, b), cx(c, d)
        conj = cx(c, -d)

        f_v = a * c
        o_v = -a * d
        i_v = b * c
        l_v = -b * d          # coefficient of i^2
        num_re = f_v - l_v
        num_im = o_v + i_v
        den = c * c + d * d
        re = Fraction(num_re, den)
        im = Fraction(num_im, den)
        answer = cxf(re, im)

        # 1-coefficients drop the digit: i^2, -i^2 (never 1i^2 / -1i^2)
        isq_txt = "" if l_v == 1 else "-" if l_v == -1 else str(l_v)
        wa = f"({a})" if a < 0 else str(a)
        wc = f"({c})" if c < 0 else str(c)
        steps = [
            step("CX_SETUP", f"({z1})/({z2})", "divide"),
            step("CONJUGATE", z2, conj),
            step("REWRITE",
                 f"multiply numerator and denominator by {conj}"),
            step("FOIL_SETUP", f"({z1})({conj})"),
            step("FOIL_F", f"First: {wa} * {wc}", f_v),
            step("FOIL_O", f"Outer: {wa} * {wrap_i(-d)}", cx(0, o_v)),
            step("FOIL_I", f"Inner: {wrap_i(b)} * {wc}", cx(0, i_v)),
            step("FOIL_L", f"Last: {wrap_i(b)} * {wrap_i(-d)}",
                 f"{isq_txt}i^2"),
            step("I_SQUARE", f"{isq_txt}i^2", -l_v),
            step("A", f_v, -l_v, num_re),
            step("A", o_v, i_v, num_im),
            step("EVAL", "numerator", cx(num_re, num_im)),
            step("REWRITE", f"({z2})({conj}) = {abs(c)}^2 + {abs(d)}^2"),
            step("E", abs(c), 2, c * c),
            step("E", abs(d), 2, d * d),
            step("A", c * c, d * d, den),
            step("EVAL", "denominator", den),
            step("REWRITE", f"({cx(num_re, num_im)})/{den}"),
        ]
        if num_re != 0 and math.gcd(abs(num_re), den) > 1:
            steps.append(step("FRAC_REDUCE", f"{num_re}/{den}", re))
        if num_im != 0 and math.gcd(abs(num_im), den) > 1:
            steps.append(step("FRAC_REDUCE", f"{num_im}/{den}", im))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="complex_division",
            problem=f"Divide: ({z1})/({z2}). Give the answer in "
                    f"standard form.",
            steps=steps,
            final_answer=answer,
        )
