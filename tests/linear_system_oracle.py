"""Shared independent oracle for 2x2 linear-system generators.

Parses the two equations out of a "Solve the system:\n1) ...\n2) ..."
problem statement and solves them with Cramer's rule in exact Fractions —
a different route from the generators' construct-from-solution logic.
"""
import re
from fractions import Fraction

# 1x / -1y coefficients, 0x / 0y terms, and "+ -3" sign glitches are
# rendering regressions (AGENTS.md testing guidelines)
RENDER_WART_RE = (
    r"(?<![\d.])1[xy]\b|(?<![\d.])0[xy]\b|\+ -|- -"
)

TERM_RE = re.compile(r"[+-]?\d*[xy]|[+-]?\d+")


def parse_linear(text):
    """Parse 'a*x + b*y + c' shaped text into (a, b, c) Fractions."""
    a = b = c = Fraction(0)
    for token in TERM_RE.findall(text.replace(" ", "")):
        if token[-1] in "xy":
            coeff_text = token[:-1]
            if coeff_text in ("", "+"):
                coeff = Fraction(1)
            elif coeff_text == "-":
                coeff = Fraction(-1)
            else:
                coeff = Fraction(coeff_text)
            if token[-1] == "x":
                a += coeff
            else:
                b += coeff
        else:
            c += Fraction(token)
    return a, b, c


def solve_system_problem(problem):
    """Solve the two numbered equations; returns (x, y) as ints when exact."""
    equations = []
    for line in problem.splitlines():
        match = re.match(r"\d\)\s*(.+)", line.strip())
        if match:
            equations.append(match.group(1))
    assert len(equations) == 2, problem

    rows = []
    for equation in equations:
        lhs, rhs = equation.split("=")
        a1, b1, c1 = parse_linear(lhs)
        a2, b2, c2 = parse_linear(rhs)
        rows.append((a1 - a2, b1 - b2, c2 - c1))

    (a, b, e), (c, d, f) = rows
    det = a * d - b * c
    assert det != 0, f"singular system: {problem}"
    x = Fraction(e * d - b * f, det)
    y = Fraction(a * f - e * c, det)

    def as_int(value):
        return value.numerator if value.denominator == 1 else value

    return as_int(x), as_int(y)
