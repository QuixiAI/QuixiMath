import random
from math import gcd, isqrt

from base_generator import ProblemGenerator
from helpers import step, jid


def sq_term(coef, var, power=2):
    """'4x^2' / 'x^2' for the squared leading term."""
    c = "" if coef == 1 else str(coef)
    return f"{c}{var}^{power}"


def lin(coef, var):
    """'2x' / 'x' for a linear term."""
    return var if coef == 1 else f"{coef}{var}"


def mono(coef, parts):
    """Monomial from a positive coefficient and (variable, power) pairs."""
    body = "".join(v if p == 1 else f"{v}^{p}" for v, p in parts if p)
    if not body:
        return str(coef)
    return body if coef == 1 else f"{coef}{body}"


def poly(terms):
    """Signed terms [(coef, parts), ...] -> 'a^2x^2 - 2abxy + b^2y^2'."""
    out = ""
    for coef, parts in terms:
        body = mono(abs(coef), parts)
        if not out:
            out = body if coef > 0 else f"-{body}"
        else:
            out += f" + {body}" if coef > 0 else f" - {body}"
    return out


def is_square(n):
    return isqrt(n) ** 2 == n


def is_cube(n):
    r = round(n ** (1 / 3))
    for c in (r - 1, r, r + 1):
        if c >= 0 and c ** 3 == n:
            return True
    return False


VARS = ["x", "y", "z", "n", "m", "t", "p", "q", "r", "s", "u", "v", "w", "k"]

NAMES = [
    "Aya", "Boris", "Ciara", "Dev", "Edith", "Farouk", "Gemma", "Hugo",
    "Ilse", "Jae", "Kwesi", "Lorna", "Milos", "Nkechi", "Osman", "Petra",
    "Rune", "Selma", "Theo", "Ulla", "Viktor", "Wanda", "Xander", "Yohan",
    "Zofia", "Ada", "Bram", "Celia", "Dagny", "Ephraim", "Fenna", "Gilles",
    "Hana", "Iker", "Jutta", "Kaito", "Lina", "Mirko", "Noa", "Otto",
]

BARE_TEMPLATES = [
    "Factor: {poly}",
    "Factor completely: {poly}",
    "Write {poly} in factored form.",
    "Rewrite {poly} as a product of factors.",
    "Factor the expression {poly} over the integers.",
]

NAMED_TEMPLATES = [
    "{name} is asked to factor {poly} completely. Give the factored form.",
    "{name} sees {poly} on a worksheet. Factor it completely.",
    "A review sheet gives {name} the expression {poly}. Factor it.",
    "{name} needs {poly} written as a product. Factor it completely.",
]


class FactorSpecialFormsGenerator(ProblemGenerator):
    """
    Factors the special forms by pattern recognition:
    - difference of squares:      a² − b² = (a − b)(a + b)
    - perfect-square trinomials:  a² ± 2ab + b² = (a ± b)²
    - sum / difference of cubes:  a³ ± b³ = (a ± b)(a² ∓ ab + b²)

    The scratchpad identifies the pattern, extracts the roots, VERIFIES the
    pattern actually applies (the PST middle-term check is the load-bearing
    one), and expands back as the final check. All inputs are primitive
    (gcd of the two roots is 1) so no GCF hides inside, and when the inner
    variable carries a higher power the roots are screened so the binomial
    factor cannot be broken down any further.

    Widened axes: roots up to 12 and 20 (6 and 12 for cubes), fourteen
    variable letters, one- and two-variable forms, inner powers x, x^2,
    x^3, and nine phrasings over forty names.

    Op-codes used:
    - POLY_SETUP: the polynomial (string)
    - FORM_IDENTIFY: the pattern (name, formula)
    - ROOT: square root, numeric or symbolic (value, root)
    - CBRT: cube root, numeric or symbolic (value, root)
    - M / E: arithmetic for the cube-trinomial coefficients
    - CHECK: middle-term verification or expansion (method, lhs, rhs)
    - REWRITE: the factored form (string)
    - Z: final answer
    """

    VARIANTS = ["difference_of_squares", "perfect_square",
                "sum_of_cubes", "difference_of_cubes"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    # -- instance construction ------------------------------------------
    @staticmethod
    def _roots(a_hi, b_hi, deg):
        """Coprime roots; for a raised inner power they must also leave the
        binomial factor irreducible (not both squares, not both cubes)."""
        while True:
            a = random.randint(1, a_hi)
            b = random.randint(1, b_hi)
            if gcd(a, b) != 1:
                continue
            if deg > 1 and is_square(a) and is_square(b):
                continue
            if deg > 1 and is_cube(a) and is_cube(b):
                continue
            return a, b

    @staticmethod
    def _shape(deg_choices):
        """Pick one- or two-variable shape.

        Returns ``(x_parts_fn, y_parts_fn, deg)`` where a power of the
        'a-side' is ``x^(deg*k)`` and the 'b-side' is either a constant or
        ``y^k``.
        """
        if random.random() < 0.5:
            var = random.choice(VARS)
            deg = random.choice(deg_choices)
            return (lambda k: [(var, deg * k)]), (lambda k: []), deg
        v1, v2 = random.sample(VARS, 2)
        return (lambda k: [(v1, k)]), (lambda k: [(v2, k)]), 1

    def _phrase(self, expr):
        if random.random() < 0.3:
            return random.choice(BARE_TEMPLATES).format(poly=expr)
        return random.choice(NAMED_TEMPLATES).format(
            poly=expr, name=random.choice(NAMES))

    # -- generation ------------------------------------------------------
    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "difference_of_squares":
            xp, yp, deg = self._shape([1, 2, 3])
            a, b = self._roots(12, 20, deg)
            A, B = mono(a, xp(1)), mono(b, yp(1))
            original = poly([(a * a, xp(2)), (-b * b, yp(2))])
            factored = f"({A} - {B})({A} + {B})"
            cross = mono(a * b, xp(1) + yp(1))
            steps = [
                step("POLY_SETUP", original),
                step("FORM_IDENTIFY", "difference_of_squares",
                     "a^2 - b^2 = (a - b)(a + b)"),
                step("ROOT", mono(a * a, xp(2)), A),
                step("ROOT", mono(b * b, yp(2)), B),
                step("REWRITE", factored),
                step("CHECK", "foil",
                     poly([(a * a, xp(2)), (a * b, xp(1) + yp(1)),
                           (-a * b, xp(1) + yp(1)), (-b * b, yp(2))]),
                     original),
                step("Z", factored),
            ]
            op = "factor_difference_of_squares"

        elif variant == "perfect_square":
            xp, yp, deg = self._shape([1, 2, 3])
            a, b = self._roots(12, 20, deg)
            sign = random.choice(["+", "-"])
            s = 1 if sign == "+" else -1
            A, B = mono(a, xp(1)), mono(b, yp(1))
            original = poly([(a * a, xp(2)),
                             (s * 2 * a * b, xp(1) + yp(1)),
                             (b * b, yp(2))])
            factored = f"({A} {sign} {B})^2"
            formula = ("a^2 + 2ab + b^2 = (a + b)^2" if s > 0
                       else "a^2 - 2ab + b^2 = (a - b)^2")
            mid = mono(2 * a * b, xp(1) + yp(1))
            mid_txt = f"-{mid}" if s < 0 else mid
            steps = [
                step("POLY_SETUP", original),
                step("FORM_IDENTIFY", "perfect_square_trinomial", formula),
                step("ROOT", mono(a * a, xp(2)), A),
                step("ROOT", mono(b * b, yp(2)), B),
                step("CHECK", "middle_term",
                     f"{'-' if s < 0 else ''}2·({A})·({B}) = {mid_txt}",
                     mid_txt),
                step("REWRITE", factored),
                step("Z", factored),
            ]
            op = "factor_perfect_square"

        else:
            xp, yp, deg = self._shape([1, 2])
            a, b = self._roots(6, 12, deg)
            plus = variant == "sum_of_cubes"
            sign, inner = ("+", "-") if plus else ("-", "+")
            si = 1 if plus else -1
            A, B = mono(a, xp(1)), mono(b, yp(1))
            original = poly([(a ** 3, xp(3)), (si * b ** 3, yp(3))])
            trinomial = poly([(a * a, xp(2)),
                              (-si * a * b, xp(1) + yp(1)),
                              (b * b, yp(2))])
            factored = f"({A} {sign} {B})({trinomial})"
            formula = ("a^3 + b^3 = (a + b)(a^2 - ab + b^2)" if plus
                       else "a^3 - b^3 = (a - b)(a^2 + ab + b^2)")
            # (A ± B)(A^2 ∓ AB + B^2) written out term by term.
            expansion = poly([
                (a ** 3, xp(3)),
                (-si * a * a * b, xp(2) + yp(1)),
                (a * b * b, xp(1) + yp(2)),
                (si * a * a * b, xp(2) + yp(1)),
                (-a * b * b, xp(1) + yp(2)),
                (si * b ** 3, yp(3)),
            ])
            steps = [
                step("POLY_SETUP", original),
                step("FORM_IDENTIFY",
                     "sum_of_cubes" if plus else "difference_of_cubes",
                     formula),
                step("CBRT", mono(a ** 3, xp(3)), A),
                step("CBRT", mono(b ** 3, yp(3)), B),
                step("E", A, 2, mono(a * a, xp(2))),
                step("M", A, B, mono(a * b, xp(1) + yp(1))),
                step("E", B, 2, mono(b * b, yp(2))),
                step("REWRITE", factored),
                step("CHECK", "expand", expansion, original),
                step("Z", factored),
            ]
            op = f"factor_{variant}"

        return dict(
            problem_id=jid(),
            operation=op,
            problem=self._phrase(original),
            steps=steps,
            final_answer=factored,
        )
