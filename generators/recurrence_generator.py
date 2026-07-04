import random

from base_generator import ProblemGenerator
from helpers import step, jid


ROOT_PAIRS_HOMOGENEOUS = [
    (2, 3),
    (-2, -3),
    (4, 2),
    (4, -2),
    (-4, 2),
]

ROOT_PAIRS_NONHOMOGENEOUS = [
    (2, 3),
    (-2, -3),
    (4, 2),
    (4, -2),
    (-4, 2),
]


def nonzero_int(lo, hi):
    choices = [value for value in range(lo, hi + 1) if value != 0]
    return random.choice(choices)


def recurrence_coefficients(r, s):
    return r + s, -r * s


def char_poly_text(p, q):
    return f"lambda^2 - ({p})lambda - ({q}) = 0"


def factor_text(r, s):
    return f"(lambda - ({r}))(lambda - ({s})) = 0"


def coeff_term(coef, body):
    if coef == 1:
        return body
    if coef == -1:
        return f"-{body}"
    return f"{coef} {body}"


def signed_term(coef, body):
    sign = "+" if coef >= 0 else "-"
    magnitude = abs(coef)
    term_body = body if magnitude == 1 else f"{magnitude} {body}"
    return f"{sign} {term_body}"


def signed_const(value):
    sign = "+" if value >= 0 else "-"
    return f"{sign} {abs(value)}"


def compact_coeff(coef, body):
    if coef == 1:
        return body
    if coef == -1:
        return f"-{body}"
    return f"{coef}{body}"


def compact_signed_coeff(coef, body):
    sign = "+" if coef >= 0 else "-"
    magnitude = abs(coef)
    term_body = body if magnitude == 1 else f"{magnitude}{body}"
    return f"{sign} {term_body}"


def recurrence_text(p, q, b=None):
    text = f"a_n = {coeff_term(p, 'a_(n-1)')} {signed_term(q, 'a_(n-2)')}"
    if b is not None:
        text = f"{text} {signed_const(b)}"
    return text


def constant_check_text(p, q, b):
    return (
        f"{compact_coeff(p, 'K')} {compact_signed_coeff(q, 'K')} "
        f"{signed_const(b)} = K"
    )


def initial_equation_text(r, s):
    return f"{compact_coeff(r, 'C1')} {compact_signed_coeff(s, 'C2')}"


def general_text(c1_root, c2_root, offset=None):
    text = f"C1({c1_root})^n + C2({c2_root})^n"
    if offset is not None:
        text = f"{text} {signed_const(offset)}"
    return text


def power_steps(base, exponent):
    value = base ** exponent
    return step("POW", f"({base})^{exponent}", value), value


def solve_constants_steps(b0, b1, r, s):
    s_b0 = s * b0
    numer = b1 - s_b0
    denom = r - s
    c1 = numer // denom
    c2 = b0 - c1
    return [
        step("INITIAL_EQ", "C1 + C2", b0),
        step("INITIAL_EQ", initial_equation_text(r, s), b1),
        step("M", s, b0, s_b0),
        step("S", b1, s_b0, numer),
        step("S", r, s, denom),
        step("D", numer, denom, c1),
        step("S", b0, c1, c2),
        step("CONST_SOLVE", f"C1 = {c1}", f"C2 = {c2}"),
    ], c1, c2


def evaluate_steps(c1, c2, r, s, n, offset=0):
    steps = []
    pow_step, r_pow = power_steps(r, n)
    steps.append(pow_step)
    term1 = c1 * r_pow
    steps.append(step("M", c1, r_pow, term1))
    pow_step, s_pow = power_steps(s, n)
    steps.append(pow_step)
    term2 = c2 * s_pow
    steps.append(step("M", c2, s_pow, term2))
    subtotal = term1 + term2
    steps.append(step("A", term1, term2, subtotal))
    value = subtotal
    if offset:
        value = subtotal + offset
        steps.append(step("A", subtotal, offset, value))
    return steps, value


class RecurrenceGenerator(ProblemGenerator):
    """
    Linear recurrences solved by characteristic roots.

    Variants:
    - homogeneous: a_n = p a_(n-1) + q a_(n-2)
    - constant: a_n = p a_(n-1) + q a_(n-2) + b

    Op-codes used:
    - REC_SETUP: recurrence and initial values
    - CHAR_POLY / CHAR_ROOTS: characteristic equation and roots
    - PARTICULAR_TRY / PARTICULAR_CHECK: constant particular solution
    - SHIFT: subtract the particular solution
    - GENERAL / INITIAL_EQ / CONST_SOLVE: closed-form setup and constants
    - POW: exact integer powers
    - A / S / M / D (established): arithmetic
    - Z: exact requested term
    """

    VARIANTS = ["homogeneous", "constant"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "homogeneous":
            r, s = random.choice(ROOT_PAIRS_HOMOGENEOUS)
            c1 = nonzero_int(-4, 5)
            c2 = nonzero_int(-4, 5)
            n = random.randint(5, 9)
            p, q = recurrence_coefficients(r, s)
            a0 = c1 + c2
            a1 = c1 * r + c2 * s
            steps = [
                step("REC_SETUP", recurrence_text(p, q),
                     f"a_0 = {a0}, a_1 = {a1}"),
                step("CHAR_POLY", char_poly_text(p, q), factor_text(r, s)),
                step("CHAR_ROOTS", f"lambda = {r}, {s}", "distinct"),
                step("GENERAL", "a_n", general_text(r, s)),
            ]
            solve_steps, c1, c2 = solve_constants_steps(a0, a1, r, s)
            steps += solve_steps
            eval_steps, value = evaluate_steps(c1, c2, r, s, n)
            steps += eval_steps
            problem = (
                f"For n >= 2, {recurrence_text(p, q)}, "
                f"with a_0 = {a0} and a_1 = {a1}. Use the "
                f"characteristic-root method to find a_{n}."
            )
        else:
            r, s = random.choice(ROOT_PAIRS_NONHOMOGENEOUS)
            c1 = nonzero_int(-3, 4)
            c2 = nonzero_int(-3, 4)
            offset = nonzero_int(-5, 6)
            n = random.randint(5, 8)
            p, q = recurrence_coefficients(r, s)
            denom = 1 - p - q
            b = offset * denom
            a0 = c1 + c2 + offset
            a1 = c1 * r + c2 * s + offset
            pq_sum = p + q
            steps = [
                step("REC_SETUP",
                     recurrence_text(p, q, b),
                     f"a_0 = {a0}, a_1 = {a1}"),
                step("CHAR_POLY", char_poly_text(p, q), factor_text(r, s)),
                step("CHAR_ROOTS", f"lambda = {r}, {s}", "distinct"),
                step("PARTICULAR_TRY", "a_n = K", "constant forcing"),
                step("A", p, q, pq_sum),
                step("S", 1, pq_sum, denom),
                step("D", b, denom, offset),
                step("PARTICULAR_CHECK", f"K = {offset}",
                     constant_check_text(p, q, b)),
            ]
            b0 = a0 - offset
            b1 = a1 - offset
            steps += [
                step("S", a0, offset, b0),
                step("S", a1, offset, b1),
                step("SHIFT", "b_n = a_n - K",
                     f"b_0 = {b0}, b_1 = {b1}"),
                step("GENERAL", "a_n", general_text(r, s, offset)),
            ]
            solve_steps, c1, c2 = solve_constants_steps(b0, b1, r, s)
            steps += solve_steps
            eval_steps, value = evaluate_steps(c1, c2, r, s, n, offset)
            steps += eval_steps
            problem = (
                f"For n >= 2, {recurrence_text(p, q, b)}, "
                f"with a_0 = {a0} and a_1 = {a1}. Use the "
                f"characteristic-root method to find a_{n}."
            )

        answer = f"a_{n} = {value}"
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"recurrence_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
