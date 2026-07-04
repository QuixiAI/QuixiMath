import random
from fractions import Fraction
from math import factorial
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec

# Maclaurin families: name -> (derivative cycle description,
# coefficient of x^k as a Fraction).
SIN_DERIVS = ["sin(x)", "cos(x)", "-sin(x)", "-cos(x)"]
SIN_VALS = [0, 1, 0, -1]
COS_DERIVS = ["cos(x)", "-sin(x)", "-cos(x)", "sin(x)"]
COS_VALS = [1, 0, -1, 0]


def coeff(fname, k):
    """Maclaurin coefficient of x^k (exact Fraction)."""
    if fname == "e^x":
        return Fraction(1, factorial(k))
    if fname == "sin(x)":
        return Fraction(SIN_VALS[k % 4], factorial(k))
    if fname == "cos(x)":
        return Fraction(COS_VALS[k % 4], factorial(k))
    if fname == "ln(1 + x)":
        return Fraction(0) if k == 0 else \
            Fraction((-1) ** (k + 1), k)
    # 1/(1 - x)
    return Fraction(1)


def deriv_txt(fname, k):
    """The k-th derivative, as text."""
    if fname == "e^x":
        return "e^x"
    if fname == "sin(x)":
        return SIN_DERIVS[k % 4]
    if fname == "cos(x)":
        return COS_DERIVS[k % 4]
    if fname == "ln(1 + x)":
        if k == 0:
            return "ln(1 + x)"
        c = factorial(k - 1) * (-1) ** (k + 1)
        return f"{c}/(1 + x)^{k}" if k > 1 else "1/(1 + x)"
    if k == 0:
        return "1/(1 - x)"
    c = factorial(k)
    return f"{c}/(1 - x)^{k + 1}" if c > 1 else f"1/(1 - x)^{k + 1}"


def poly_txt(coeffs, var="x"):
    """Σ c_k var^k with fraction coefficients rendered as v^k/q."""
    parts = []
    for k, c in enumerate(coeffs):
        if c == 0:
            continue
        if k == 0:
            body = str(abs(c))
        else:
            v = var if k == 1 else f"{var}^{k}"
            n, d = abs(c.numerator), c.denominator
            if d == 1:
                body = v if n == 1 else f"{n}{v}" if var == "x" else \
                    f"{n}{var}^{k}" if k > 1 else f"{n}{var}"
            else:
                body = f"{v}/{d}" if n == 1 else f"{n}{v}/{d}"
        if not parts:
            parts.append(body if c > 0 else f"-{body}")
        else:
            parts.append(f"+ {body}" if c > 0 else f"- {body}")
    return " ".join(parts)


class TaylorSeriesGenerator(ProblemGenerator):
    """
    Taylor and Maclaurin polynomials: build them from a derivative
    table, use them to approximate nearby values with exact decimal
    arithmetic, and bound the error with the Lagrange remainder
    (M = 1 for sin/cos; M is supplied in the problem for e^x,
    Principle 5).

    Variants:
    - maclaurin: derivative table -> P_n for e^x, sin, cos,
      ln(1 + x), 1/(1 - x)
    - centered: ln(x) or 1/x at a = 1
    - approximate: P_n evaluated at a terminating decimal
    - error_bound: M·abs(x)^(n+1)/(n+1)! as an exact fraction

    Op-codes used:
    - TAYLOR_SETUP: the function, center, and task
    - TAYLOR_FORMULA: P_n(x) = Σ f^(k)(a)/k!·(x - a)^k
    - TABLE_ENTRY (established): one derivative-table row
    - THEOREM / EVAL / SUBST / REWRITE / E / M / A / S / D
      (established)
    - Z: the polynomial, decimal, or fraction bound
    """

    VARIANTS = ["maclaurin", "centered", "approximate", "error_bound"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        formula = step("TAYLOR_FORMULA",
                       "P_n(x) = Σ f^(k)(a)/k!·(x - a)^k")

        if variant == "maclaurin":
            fname = random.choice(["e^x", "sin(x)", "cos(x)",
                                   "ln(1 + x)", "1/(1 - x)"])
            deg = random.choice({"e^x": [3, 4], "sin(x)": [3, 5],
                                 "cos(x)": [2, 4], "ln(1 + x)": [3, 4],
                                 "1/(1 - x)": [3, 4]}[fname])
            coeffs = [coeff(fname, k) for k in range(deg + 1)]
            steps = [
                step("TAYLOR_SETUP", f"f(x) = {fname}, center a = 0",
                     f"Maclaurin polynomial of degree {deg}"),
            ]
            for k in range(deg + 1):
                fk = "f" if k == 0 else f"f^({k})" if k > 3 else \
                    "f" + "'" * k
                val = coeffs[k] * factorial(k)
                steps.append(step("TABLE_ENTRY",
                                  f"{fk}(x) = {deriv_txt(fname, k)}",
                                  f"{fk}(0) = {val}"))
            steps.append(formula)
            for k in range(2, deg + 1):
                if coeffs[k] == 0:
                    continue
                val = coeffs[k] * factorial(k)
                steps.append(step("EVAL", f"c_{k}",
                                  f"{val}/{k}! = {coeffs[k]}"))
            answer = poly_txt(coeffs)
            steps.append(step("REWRITE", f"P_{deg}(x) = {answer}"))
            problem = (f"Find the Maclaurin polynomial of degree "
                       f"{deg} for f(x) = {fname}.")
        elif variant == "centered":
            fname = random.choice(["ln(x)", "1/x"])
            deg = random.choice([2, 3, 4])
            if fname == "ln(x)":
                coeffs = [Fraction(0)] + \
                    [Fraction((-1) ** (k + 1), k)
                     for k in range(1, deg + 1)]

                def dtx(k):
                    if k == 0:
                        return "ln(x)"
                    c = factorial(k - 1) * (-1) ** (k + 1)
                    return (f"{c}/x^{k}" if abs(c) > 1 or k > 1
                            else "1/x")
            else:
                coeffs = [Fraction((-1) ** k)
                          for k in range(deg + 1)]

                def dtx(k):
                    c = factorial(k) * (-1) ** k
                    if k == 0:
                        return "1/x"
                    return f"{c}/x^{k + 1}"
            steps = [
                step("TAYLOR_SETUP", f"f(x) = {fname}, center a = 1",
                     f"Taylor polynomial of degree {deg}"),
            ]
            for k in range(deg + 1):
                fk = "f" if k == 0 else f"f^({k})" if k > 3 else \
                    "f" + "'" * k
                val = coeffs[k] * factorial(k)
                steps.append(step("TABLE_ENTRY",
                                  f"{fk}(x) = {dtx(k)}",
                                  f"{fk}(1) = {val}"))
            steps.append(formula)
            for k in range(2, deg + 1):
                val = coeffs[k] * factorial(k)
                steps.append(step("EVAL", f"c_{k}",
                                  f"{val}/{k}! = {coeffs[k]}"))
            answer = poly_txt(coeffs, var="(x - 1)")
            steps.append(step("REWRITE", f"P_{deg}(x) = {answer}"))
            problem = (f"Find the Taylor polynomial of degree {deg} "
                       f"for f(x) = {fname} centered at a = 1.")
        elif variant == "approximate":
            pick = random.choice([
                ("e^x", 2, ["0.1", "0.2", "0.3", "0.4"]),
                ("sin(x)", 3, ["0.3", "0.6"]),
                ("cos(x)", 2, ["0.1", "0.2", "0.3", "0.4", "0.5"]),
                ("ln(1 + x)", 2, ["0.1", "0.2", "0.3", "0.4", "0.5"]),
            ])
            fname, deg, xs = pick
            x = Fraction(random.choice(xs))
            coeffs = [coeff(fname, k) for k in range(deg + 1)]
            ptxt = poly_txt(coeffs)
            target = {"e^x": f"e^{dec(x)}",
                      "sin(x)": f"sin({dec(x)})",
                      "cos(x)": f"cos({dec(x)})",
                      "ln(1 + x)": f"ln({dec(1 + x)})"}[fname]
            value = sum(c * x ** k for k, c in enumerate(coeffs))
            steps = [
                step("TAYLOR_SETUP", f"f(x) = {fname}",
                     f"approximate {target} with P_{deg}"),
                step("REWRITE", f"P_{deg}(x) = {ptxt}"),
                step("SUBST", "x", dec(x),
                     ptxt.replace("x", f"({dec(x)})")),
            ]
            if fname == "e^x":
                sq = x * x
                steps += [
                    step("E", dec(x), 2, dec(sq)),
                    step("D", dec(sq), 2, dec(sq / 2)),
                    step("A", 1, dec(x), dec(1 + x)),
                    step("A", dec(1 + x), dec(sq / 2), dec(value)),
                ]
            elif fname == "sin(x)":
                cu = x ** 3
                steps += [
                    step("E", dec(x), 3, dec(cu)),
                    step("D", dec(cu), 6, dec(cu / 6)),
                    step("S", dec(x), dec(cu / 6), dec(value)),
                ]
            elif fname == "cos(x)":
                sq = x * x
                steps += [
                    step("E", dec(x), 2, dec(sq)),
                    step("D", dec(sq), 2, dec(sq / 2)),
                    step("S", 1, dec(sq / 2), dec(value)),
                ]
            else:
                sq = x * x
                steps += [
                    step("E", dec(x), 2, dec(sq)),
                    step("D", dec(sq), 2, dec(sq / 2)),
                    step("S", dec(x), dec(sq / 2), dec(value)),
                ]
            answer = dec(value)
            problem = (f"Use the degree-{deg} Maclaurin polynomial "
                       f"of f(x) = {fname} to approximate {target}.")
        else:
            fname = random.choice(["sin(x)", "cos(x)", "e^x"])
            n = random.choice([1, 2, 3, 4, 5])
            # M = 3 only bounds e^t on [0, 1], so keep x ≤ 1 there.
            x = random.choice([Fraction(1), Fraction(1, 2),
                               Fraction(1, 3), Fraction(1, 4),
                               Fraction(2, 3)] +
                              ([] if fname == "e^x" else
                               [Fraction(2), Fraction(3, 2)]))
            M = 3 if fname == "e^x" else 1
            # A bound above 1 is useless for these functions; take
            # more terms until the bound is informative.
            while M * x ** (n + 1) / factorial(n + 1) > 1:
                n += 1
            top = M * x ** (n + 1)
            bound = Fraction(top, factorial(n + 1))
            m_note = (" Use M = 3 as a bound for the derivatives "
                      "of e^x on the interval." if fname == "e^x"
                      else "")
            steps = [
                step("TAYLOR_SETUP",
                     f"f(x) = {fname}, P_{n} around 0",
                     f"bound the error at x = {x}"),
                step("THEOREM", "Lagrange error bound",
                     "abs(R_n) ≤ M·abs(x - a)^(n+1)/(n+1)!"),
                step("CHECK", "derivative bound",
                     f"M = 3 (given)" if fname == "e^x" else
                     f"derivatives of {fname} are bounded by 1",
                     f"M = {M}"),
                step("E", str(x), n + 1, str(x ** (n + 1))),
            ]
            if M != 1:
                steps.append(step("M", M, str(x ** (n + 1)),
                                  str(top)))
            steps += [
                step("EVAL", f"({n} + 1)!", factorial(n + 1)),
                step("D", str(top), factorial(n + 1), str(bound)),
            ]
            answer = str(bound)
            problem = (f"The Taylor polynomial P_{n} of "
                       f"f(x) = {fname} around 0 is used at "
                       f"x = {x}. Bound the error with the Lagrange "
                       f"remainder.{m_note}")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"taylor_series_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
