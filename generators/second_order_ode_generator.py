import random

from base_generator import ProblemGenerator
from helpers import step, jid


def fmt_terms(raw_terms):
    pieces = []
    for coeff, body in raw_terms:
        if coeff == 0:
            continue
        text = body if body and abs(coeff) == 1 else (
            f"{abs(coeff)}{body}" if body else str(abs(coeff))
        )
        if not pieces:
            pieces.append(text if coeff > 0 else f"-{text}")
        else:
            pieces.append(("+ " if coeff > 0 else "- ") + text)
    return " ".join(pieces) if pieces else "0"


def ode_lhs(p, q):
    return fmt_terms([(1, "y''"), (p, "y'"), (q, "y")])


def char_poly(p, q):
    return fmt_terms([(1, "r^2"), (p, "r"), (q, "")])


def exp_txt(rate):
    if rate == 1:
        return "e^x"
    if rate == -1:
        return "e^(-x)"
    return f"e^({rate}x)"


def factor_txt(root):
    return f"(r - {root})" if root > 0 else f"(r + {abs(root)})"


def signed_join(terms):
    pieces = []
    for coeff, body in terms:
        if coeff == 0:
            continue
        text = body if body and abs(coeff) == 1 else (
            f"{abs(coeff)}{body}" if body else str(abs(coeff))
        )
        if not pieces:
            pieces.append(text if coeff > 0 else f"-{text}")
        else:
            pieces.append(("+ " if coeff > 0 else "- ") + text)
    return " ".join(pieces) if pieces else "0"


def distinct_solution(c1, r1, c2, r2):
    return "y = " + signed_join([(c1, exp_txt(r1)), (c2, exp_txt(r2))])


def linear_x(c1, c2):
    return signed_join([(c1, ""), (c2, "x")])


def repeated_solution(c1, c2, r):
    return f"y = ({linear_x(c1, c2)}){exp_txt(r)}"


def trig_arg(beta):
    return "x" if beta == 1 else f"{beta}x"


def trig_combo(c1, c2, beta):
    arg = trig_arg(beta)
    return signed_join([(c1, f"cos({arg})"), (c2, f"sin({arg})")])


def complex_solution(c1, c2, alpha, beta):
    return f"y = {exp_txt(alpha)}({trig_combo(c1, c2, beta)})"


def derivative_exp_terms(r1, r2):
    return signed_join([
        (r1, f"C1{exp_txt(r1)}"),
        (r2, f"C2{exp_txt(r2)}"),
    ])


def constant_equation_terms(a, b):
    return signed_join([(a, "C1"), (b, "C2")])


class SecondOrderODEGenerator(ProblemGenerator):
    """
    Homogeneous second-order constant-coefficient ODEs.

    Variants:
    - distinct_real: two distinct real characteristic roots
    - repeated_root: repeated real characteristic root
    - complex_roots: complex conjugate characteristic roots

    Op-codes used:
    - ODE_SETUP (established): equation and initial conditions
    - CHAR_EQ: characteristic polynomial
    - FACTOR / CHAR_ROOTS: root computation
    - SOL_FORM: general solution form
    - SUBST / DERIV_FORM: initial-condition equations
    - M / S / D (established): constant-solving arithmetic
    - SOLVE_CONST: constants C1 and C2
    - Z: explicit solution
    """

    VARIANTS = ["distinct_real", "repeated_root", "complex_roots"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        nonzero = [-4, -3, -2, -1, 1, 2, 3, 4]

        if variant == "distinct_real":
            r1, r2 = sorted(random.sample(nonzero, 2))
            c1 = random.choice(nonzero)
            c2 = random.choice(nonzero)
            p = -(r1 + r2)
            q = r1 * r2
            y0 = c1 + c2
            v0 = c1 * r1 + c2 * r2
            prod = r2 * y0
            num = v0 - prod
            den = r1 - r2
            answer = distinct_solution(c1, r1, c2, r2)
            general = f"y = C1{exp_txt(r1)} + C2{exp_txt(r2)}"
            steps = [
                step("ODE_SETUP", f"{ode_lhs(p, q)} = 0",
                     f"y(0) = {y0}, y'(0) = {v0}"),
                step("CHAR_EQ", "assume y=e^(rx)",
                     f"{char_poly(p, q)} = 0"),
                step("FACTOR", char_poly(p, q),
                     f"{factor_txt(r1)}{factor_txt(r2)} = 0"),
                step("CHAR_ROOTS", f"r1 = {r1}, r2 = {r2}",
                     "distinct real"),
                step("SOL_FORM", general),
                step("SUBST", "x=0", f"C1 + C2 = {y0}"),
                step("DERIV_FORM", "y'", derivative_exp_terms(r1, r2)),
                step("SUBST", "x=0",
                     f"{constant_equation_terms(r1, r2)} = {v0}"),
                step("M", r2, y0, prod),
                step("S", v0, prod, num),
                step("S", r1, r2, den),
                step("D", num, den, c1),
                step("S", y0, c1, c2),
                step("SOLVE_CONST", f"C1 = {c1}", f"C2 = {c2}"),
            ]
        elif variant == "repeated_root":
            r = random.choice(nonzero)
            c1 = random.choice(nonzero)
            c2 = random.choice(nonzero)
            p = -2 * r
            q = r * r
            y0 = c1
            v0 = c2 + r * c1
            prod = r * c1
            answer = repeated_solution(c1, c2, r)
            steps = [
                step("ODE_SETUP", f"{ode_lhs(p, q)} = 0",
                     f"y(0) = {y0}, y'(0) = {v0}"),
                step("CHAR_EQ", "assume y=e^(rx)",
                     f"{char_poly(p, q)} = 0"),
                step("FACTOR", char_poly(p, q), f"{factor_txt(r)}^2 = 0"),
                step("CHAR_ROOTS", f"r = {r}", "repeated"),
                step("SOL_FORM", f"y = (C1 + C2x){exp_txt(r)}"),
                step("SUBST", "x=0", f"C1 = {y0}"),
                step("DERIV_FORM", "y'",
                     f"({signed_join([(1, 'C2'), (r, '(C1 + C2x)')])})"
                     f"{exp_txt(r)}"),
                step("SUBST", "x=0",
                     f"{signed_join([(1, 'C2'), (r, 'C1')])} = {v0}"),
                step("M", r, c1, prod),
                step("S", v0, prod, c2),
                step("SOLVE_CONST", f"C1 = {c1}", f"C2 = {c2}"),
            ]
        else:
            alpha = random.choice(nonzero)
            beta = random.randint(1, 4)
            c1 = random.choice(nonzero)
            c2 = random.choice(nonzero)
            p = -2 * alpha
            q = alpha * alpha + beta * beta
            y0 = c1
            v0 = alpha * c1 + beta * c2
            prod = alpha * c1
            num = v0 - prod
            answer = complex_solution(c1, c2, alpha, beta)
            steps = [
                step("ODE_SETUP", f"{ode_lhs(p, q)} = 0",
                     f"y(0) = {y0}, y'(0) = {v0}"),
                step("CHAR_EQ", "assume y=e^(rx)",
                     f"{char_poly(p, q)} = 0"),
                step("CHAR_ROOTS", f"r = {alpha} ± {beta}i",
                     "complex conjugates"),
                step("SOL_FORM",
                     f"y = {exp_txt(alpha)}(C1 cos({trig_arg(beta)}) + "
                     f"C2 sin({trig_arg(beta)}))"),
                step("SUBST", "x=0", f"C1 = {y0}"),
                step("DERIV_FORM", "y'(0)",
                     constant_equation_terms(alpha, beta)),
                step("SUBST", "x=0",
                     f"{constant_equation_terms(alpha, beta)} = {v0}"),
                step("M", alpha, c1, prod),
                step("S", v0, prod, num),
                step("D", num, beta, c2),
                step("SOLVE_CONST", f"C1 = {c1}", f"C2 = {c2}"),
            ]

        steps.append(step("Z", answer))
        problem = (
            f"Solve {ode_lhs(p, q)} = 0 with y(0) = {y0} and "
            f"y'(0) = {v0}."
        )
        return dict(
            problem_id=jid(),
            operation=f"second_order_ode_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
