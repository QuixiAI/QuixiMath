import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


NAMES = [
    "Ana", "Bo", "Cleo", "Devi", "Emil", "Farid", "Greta", "Hana",
    "Ivan", "Jun", "Kira", "Liam", "Mira", "Noor", "Omar", "Pia",
]

POINTS = sorted({Fraction(p, q)
                 for q in (1, 2, 3, 4, 5, 6, 8, 10)
                 for p in range(-2 * q, 2 * q + 1)})

GS_TEMPLATES = [
    ("Use Gram-Schmidt on {basis} over [-1,1] to construct the Legendre "
     "polynomial {name} with leading coefficient {lead}. Then evaluate "
     "{series} at x = {x0} exactly."),
    ("Apply Gram-Schmidt to {basis} on [-1,1], scaling to leading "
     "coefficient {lead}, to obtain {name}. Then give the exact value of "
     "{series} at x = {x0}."),
    ("{who} builds the Legendre polynomial {name} by Gram-Schmidt from "
     "{basis} on [-1,1] with leading coefficient {lead}. Report {name} and "
     "the exact value of {series} at x = {x0}."),
    ("Orthogonalize {basis} over [-1,1] with the inner product "
     "<f,g> = integral_-1^1 f(x)g(x) dx to build {name} with leading "
     "coefficient {lead}, then evaluate {series} at x = {x0} exactly."),
    ("Construct {name} by Gram-Schmidt on {basis} over [-1,1], scaled to "
     "leading coefficient {lead}, and evaluate {series} exactly at "
     "x = {x0}."),
]

RECUR_TEMPLATES = [
    ("Given {given}, use Bonnet's recurrence "
     "(n+1)P_(n+1)(x) = (2n+1)x P_n(x) - n P_(n-1)(x) with n = {n} to find "
     "{name}. Then evaluate {series} at x = {x0} exactly."),
    ("{who} knows {given}. Apply Bonnet's recurrence "
     "(n+1)P_(n+1)(x) = (2n+1)x P_n(x) - n P_(n-1)(x) at n = {n} to get "
     "{name}, then evaluate {series} at x = {x0} exactly."),
    ("Starting from {given}, step Bonnet's recurrence "
     "(n+1)P_(n+1)(x) = (2n+1)x P_n(x) - n P_(n-1)(x) once with n = {n} to "
     "obtain {name}. Give {name} and the exact value of {series} at "
     "x = {x0}."),
    ("Use {given} and the three-term recurrence "
     "(n+1)P_(n+1)(x) = (2n+1)x P_n(x) - n P_(n-1)(x) with n = {n} to "
     "derive {name}, then evaluate {series} exactly at x = {x0}."),
    ("With {given} in hand, run Bonnet's recurrence "
     "(n+1)P_(n+1)(x) = (2n+1)x P_n(x) - n P_(n-1)(x) at n = {n} to build "
     "{name} and evaluate {series} at x = {x0} exactly."),
]


def fraction_text(value):
    return str(Fraction(value))


def legendre_coeffs(n):
    """Ascending coefficient list of P_n via Bonnet's recurrence."""
    polys = [[Fraction(1)], [Fraction(0), Fraction(1)]]
    for k in range(1, n):
        prev, cur = polys[k - 1], polys[k]
        shifted = [Fraction(0)] + [c * (2 * k + 1) for c in cur]
        out = list(shifted)
        for i, c in enumerate(prev):
            out[i] -= k * c
        polys.append([c / (k + 1) for c in out])
    return polys[n]


def poly_add(a, b):
    out = [Fraction(0)] * max(len(a), len(b))
    for i, c in enumerate(a):
        out[i] += c
    for i, c in enumerate(b):
        out[i] += c
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_scale(a, k):
    return [c * k for c in a]


def poly_eval(coeffs, x):
    total = Fraction(0)
    for c in reversed(coeffs):
        total = total * x + c
    return total


def int_poly_text(ints):
    """Descending integer polynomial, ASCII signs, no 1x or ^1."""
    pieces = []
    for power in range(len(ints) - 1, -1, -1):
        c = ints[power]
        if c == 0:
            continue
        mag = abs(c)
        if power == 0:
            body = str(mag)
        else:
            var = "x" if power == 1 else f"x^{power}"
            body = var if mag == 1 else f"{mag}{var}"
        if not pieces:
            pieces.append(("-" if c < 0 else "") + body)
        else:
            pieces.append(("- " if c < 0 else "+ ") + body)
    if not pieces:
        return "0"
    return " ".join(pieces)


def poly_text(coeffs):
    """Render a rational polynomial as (integer polynomial)/d."""
    den = 1
    for c in coeffs:
        den = den * c.denominator // __import__("math").gcd(den, c.denominator)
    ints = [int(c * den) for c in coeffs]
    body = int_poly_text(ints)
    if den == 1:
        return body
    if len(
        [c for c in ints if c != 0]
    ) == 1 and ints[-1] != 0 and len(ints) > 1:
        return f"{body}/{den}"
    return f"({body})/{den}"


def series_text(coeffs):
    """S(x) = 3P_2(x) - 2P_1(x) + P_0(x) style rendering."""
    pieces = []
    for i in range(len(coeffs) - 1, -1, -1):
        c = coeffs[i]
        if c == 0:
            continue
        mag = abs(c)
        body = f"P_{i}(x)" if mag == 1 else f"{mag}P_{i}(x)"
        if not pieces:
            pieces.append(("-" if c < 0 else "") + body)
        else:
            pieces.append(("- " if c < 0 else "+ ") + body)
    return "S(x) = " + " ".join(pieces)


def random_series(degree):
    """Integer coefficients c_0..c_degree with c_degree nonzero."""
    while True:
        coeffs = [random.randint(-9, 9) for _ in range(degree)]
        coeffs.append(random.choice([c for c in range(-9, 10) if c != 0]))
        if sum(1 for c in coeffs if c) >= 2:
            return coeffs


class LegendreConstructionGenerator(ProblemGenerator):
    """
    Construct a Legendre polynomial - P_2 or P_3 by Gram-Schmidt on
    {1, x, x^2, x^3} over [-1, 1], or P_4/P_5/P_6 by one step of Bonnet's
    recurrence from the two preceding polynomials - then evaluate a short
    Legendre series exactly at a rational point.

    Op-codes used:
    - LEGENDRE_SETUP / INTEGRAL / PROJECTION / POLY_SUB / POLY_SCALE
    - RECUR / SERIES_SETUP / SUBST / EVAL
    - A / S / M / D (established/shared): exact rational arithmetic
    - CHECK (expand_then_evaluate)
    - Z: constructed polynomial and the exact series value
    """

    VARIANTS = ["p2", "p3", "recurrence"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        who = random.choice(NAMES)
        if variant == "p2":
            degree = 2
            steps, name = self._gram_schmidt_steps(2)
            problem_head = random.choice(GS_TEMPLATES)
            head_args = dict(basis="{1, x, x^2}", name="P_2", lead="3/2")
        elif variant == "p3":
            degree = 3
            steps, name = self._gram_schmidt_steps(3)
            problem_head = random.choice(GS_TEMPLATES)
            head_args = dict(basis="{1, x, x^2, x^3}", name="P_3", lead="5/2")
        else:
            degree = random.choice([4, 5, 6])
            steps, name = self._recurrence_steps(degree)
            problem_head = random.choice(RECUR_TEMPLATES)
            given = (f"P_{degree - 1}(x) = "
                     f"{poly_text(legendre_coeffs(degree - 1))} and "
                     f"P_{degree - 2}(x) = "
                     f"{poly_text(legendre_coeffs(degree - 2))}")
            head_args = dict(given=given, n=degree - 1, name=f"P_{degree}")

        target_text = poly_text(legendre_coeffs(degree))
        if variant == "recurrence":
            series_coeffs = [0] * (degree - 2) + [
                random.randint(-9, 9), random.randint(-9, 9),
                random.choice([c for c in range(-9, 10) if c != 0]),
            ]
            if sum(1 for c in series_coeffs if c) < 2:
                series_coeffs[degree - 1] = random.choice([-3, -2, 2, 3])
        else:
            series_coeffs = random_series(degree)
        x0 = random.choice(POINTS)
        value = self._series_steps(steps, series_coeffs, x0)

        problem = problem_head.format(
            series=series_text(series_coeffs), x0=fraction_text(x0),
            who=who, **head_args)
        answer = (f"{name}(x) = {target_text}; "
                  f"S({fraction_text(x0)}) = {fraction_text(value)}")
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"legendre_construction_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _gram_schmidt_steps(self, degree):
        if degree == 2:
            numerator = Fraction(2, 3)
            denominator = Fraction(2)
            projection = numerator / denominator
            steps = [
                step("LEGENDRE_SETUP", "target=P_2",
                     "inner product integral_-1^1 f(x)g(x) dx"),
                step("INTEGRAL", "<1,1>", denominator),
                step("INTEGRAL", "<x^2,1>", numerator),
                step("D", fraction_text(numerator),
                     fraction_text(denominator), fraction_text(projection)),
                step("PROJECTION", "x^2 onto 1", fraction_text(projection)),
                step("POLY_SUB", "x^2", fraction_text(projection),
                     "x^2 - 1/3"),
                step("POLY_SCALE", "x^2 - 1/3", "3/2", "(3x^2 - 1)/2"),
            ]
            return steps, "P_2"
        numerator = Fraction(2, 5)
        denominator = Fraction(2, 3)
        projection = numerator / denominator
        steps = [
            step("LEGENDRE_SETUP", "target=P_3",
                 "inner product integral_-1^1 f(x)g(x) dx"),
            step("INTEGRAL", "<x,x>", denominator),
            step("INTEGRAL", "<x^3,x>", numerator),
            step("D", fraction_text(numerator), fraction_text(denominator),
                 fraction_text(projection)),
            step("PROJECTION", "x^3 onto x", fraction_text(projection)),
            step("POLY_SUB", "x^3", "3x/5", "x^3 - 3x/5"),
            step("POLY_SCALE", "x^3 - 3x/5", "5/2", "(5x^3 - 3x)/2"),
        ]
        return steps, "P_3"

    def _recurrence_steps(self, degree):
        n = degree - 1
        prev = legendre_coeffs(n - 1)
        cur = legendre_coeffs(n)
        shifted = poly_scale([Fraction(0)] + cur, 2 * n + 1)
        subtracted = poly_add(shifted, poly_scale(prev, -n))
        target = poly_scale(subtracted, Fraction(1, n + 1))
        steps = [
            step("LEGENDRE_SETUP", f"target=P_{degree}",
                 f"Bonnet recurrence with n={n}"),
            step("RECUR", f"{n + 1}P_{degree} = {2 * n + 1}x P_{n} - {n}P_{n - 1}",
                 f"P_{n} = {poly_text(cur)}", f"P_{n - 1} = {poly_text(prev)}"),
            step("M", f"{2 * n + 1}x", poly_text(cur), poly_text(shifted)),
            step("S", poly_text(shifted), poly_text(poly_scale(prev, n)),
                 poly_text(subtracted)),
            step("D", poly_text(subtracted), n + 1, poly_text(target)),
        ]
        return steps, f"P_{degree}"

    def _series_steps(self, steps, series_coeffs, x0):
        steps.append(step("SERIES_SETUP", series_text(series_coeffs),
                          f"x={fraction_text(x0)}"))
        combined = [Fraction(0)]
        total = Fraction(0)
        terms = []
        for i, c in enumerate(series_coeffs):
            if c == 0:
                continue
            coeffs = legendre_coeffs(i)
            pi = poly_eval(coeffs, x0)
            if i >= 2:
                steps.append(step("SUBST", "x", fraction_text(x0),
                                  f"P_{i} at x={fraction_text(x0)}"))
            steps.append(step("EVAL", f"P_{i}({fraction_text(x0)})",
                              fraction_text(pi)))
            term = c * pi
            steps.append(step("M", c, fraction_text(pi), fraction_text(term)))
            terms.append(term)
            combined = poly_add(combined, poly_scale(coeffs, Fraction(c)))
        total = terms[0]
        for term in terms[1:]:
            new_total = total + term
            steps.append(step("A", fraction_text(total), fraction_text(term),
                              fraction_text(new_total)))
            total = new_total
        steps.append(step("EVAL", f"S({fraction_text(x0)})",
                          fraction_text(total)))
        if random.random() < 0.5:
            direct = poly_eval(combined, x0)
            steps.append(step(
                "CHECK", "expand_then_evaluate",
                f"S(x) = {poly_text(combined)} gives {fraction_text(direct)}",
                f"term sum gives {fraction_text(total)}"))
        return total
