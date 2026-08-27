import math
import random
from base_generator import ProblemGenerator
from helpers import step, jid


def simp_sqrt(n):
    """√n simplified: returns (k, m) with n = k^2·m, m squarefree."""
    k = 1
    for f in range(int(math.isqrt(n)), 1, -1):
        if n % (f * f) == 0:
            k = f
            break
    return k, n // (k * k)


def sqrt_txt(n):
    """'6', '3√2', '√10'."""
    k, m = simp_sqrt(n)
    if m == 1:
        return str(k)
    return f"√{m}" if k == 1 else f"{k}√{m}"


UNITS = ["units", "centimeters", "millimeters", "meters", "inches",
         "feet", "yards", "cm", "mm", "ft", "yd"]

# (vertex, vertex, right-angle vertex, foot of the altitude) — all distinct.
LABEL_SETS = [
    ("A", "B", "C", "D"),
    ("P", "Q", "R", "S"),
    ("X", "Y", "Z", "W"),
    ("D", "E", "F", "G"),
    ("K", "L", "M", "N"),
    ("R", "S", "T", "U"),
    ("J", "K", "L", "M"),
    ("M", "N", "P", "Q"),
    ("B", "C", "D", "E"),
    ("S", "T", "U", "V"),
    ("E", "F", "G", "H"),
]

NAMES = ["Maya", "Diego", "Priya", "Owen", "Lena", "Marcus", "Ines",
         "Tariq", "Nora", "Felix", "Amara", "Jonas", "Rosa", "Kenji",
         "Hana", "Luis", "Ada", "Bianca", "Omar", "Sasha"]

STRUCTURES = ["roof truss", "garden trellis", "kite frame",
              "bridge gusset", "sail panel", "shelf bracket",
              "ramp support", "window brace", "quilt panel",
              "stained-glass pane", "awning frame", "tent flap",
              "signboard", "deck railing"]


def _scaled_pair(lo, hi, s, t):
    """Random (s·k, t·k) landing inside [lo, hi], or None."""
    kmax = hi // max(s, t)
    kmin = -(-lo // min(s, t))
    if kmin > kmax:
        return None
    k = random.randint(kmin, kmax)
    return s * k, t * k


def _square_pair(lo, hi):
    """Random (p, q) in [lo, hi] whose product is a perfect square."""
    top = math.isqrt(hi)
    for _ in range(40):
        a = random.randint(1, top)
        b = random.randint(1, top)
        pair = _scaled_pair(lo, hi, a * a, b * b)
        if pair:
            return pair
    return lo, lo


def _leg_square_pair(lo, hi):
    """Random (p, q) in [lo, hi] with p·(p + q) a perfect square."""
    top = math.isqrt(hi) + 1
    for _ in range(60):
        a = random.randint(1, top)
        b = random.randint(a + 1, top + 1)
        pair = _scaled_pair(lo, hi, a * a, b * b - a * a)
        if pair:
            return pair
    return lo, 3 * lo


def _divisors(n):
    """All positive divisors of n, ascending."""
    small, large = [], []
    i = 1
    while i * i <= n:
        if n % i == 0:
            small.append(i)
            if i != n // i:
                large.append(n // i)
        i += 1
    return small + large[::-1]


def _divisor_split(h, span=14):
    """Random divisor p of h^2 with 1 < p < h^2 and both parts modest."""
    sq = h * h
    cands = [d for d in _divisors(sq)
             if 2 <= d <= span * h and 2 <= sq // d <= span * h]
    if not cands:
        cands = [d for d in _divisors(sq) if 1 < d < sq] or [1]
    return random.choice(cands)


def _sq_txt(val):
    """'(3√2)^2' for radicals, '45^2' for integers."""
    return f"({val})^2" if "√" in val else f"{val}^2"


def _root_step(n, val):
    """ROOT_SIMPLIFY line: pull out the square factor, or say there is none."""
    if val == f"√{n}":
        return step("ROOT_SIMPLIFY", f"√{n} has no perfect-square factor")
    return step("ROOT_SIMPLIFY", f"√{n} = {val}")


class GeometricMeanGenerator(ProblemGenerator):
    """
    Geometric mean relationships in a right triangle with the altitude
    drawn to the hypotenuse: h = √(p·q), leg = √(p·c), the reverse solve
    q = h²/p, the hypotenuse solve c = leg²/p, and the bare mean
    proportional x = √(a·b). Radical answers are simplified.

    Op-codes used:
    - GEO_SETUP: the configuration and the goal (given, goal)
    - THEOREM: the geometric mean relation used (established)
    - A / M / E / D: hypotenuse sum and the arithmetic (established)
    - ROOT_SIMPLIFY: pull the square factor out (established)
    - CHECK: substitute / cross_products verification (established)
    - Z: 'h = 3√2 meters', 'leg = 6 inches', 'q = 9 units', 'x = 12'
    """

    VARIANTS = ["altitude", "leg", "find_segment", "hypotenuse",
                "proportional"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    # ---- problem phrasings -------------------------------------------------
    # Every phrasing states the given quantities in the same order, so the
    # numbers can be read straight out of the sentence.

    def _altitude_text(self, p, q, u, lab, name, thing):
        x, y, z, w = lab
        return random.choice([
            (f"In a right triangle, the altitude to the hypotenuse "
             f"splits it into segments of length {p} and {q} {u}. "
             f"Find the altitude h."),
            (f"Right triangle {x}{y}{z} has its right angle at {z}, and "
             f"the altitude from {z} meets the hypotenuse {x}{y} at {w}. "
             f"Given {x}{w} = {p} {u} and {w}{y} = {q} {u}, find the "
             f"length h of the altitude {z}{w}."),
            (f"The altitude drawn to the hypotenuse of a right triangle "
             f"cuts it into a piece {p} {u} long and a piece {q} {u} "
             f"long. How long is the altitude h?"),
            (f"In right triangle {x}{y}{z} the altitude {z}{w} lands on "
             f"the hypotenuse, leaving segments of {p} {u} and {q} {u}. "
             f"Compute h, the length of {z}{w}."),
            (f"{name} is laying out a right-triangular {thing}. The "
             f"perpendicular from the right angle to the longest side "
             f"divides that side into parts of {p} {u} and {q} {u}. "
             f"Find the length h of the perpendicular."),
        ])

    def _leg_text(self, p, q, u, lab, name, thing):
        x, y, z, w = lab
        return random.choice([
            (f"In a right triangle, the altitude to the hypotenuse "
             f"splits it into segments p = {p} {u} and q = {q} {u}. "
             f"Find the leg adjacent to the segment of length p."),
            (f"Right triangle {x}{y}{z} has its right angle at {z}; the "
             f"altitude {z}{w} divides the hypotenuse into {x}{w} = "
             f"{p} {u} and {w}{y} = {q} {u}. Find the length of the leg "
             f"{z}{x}, the one that meets segment {x}{w}."),
            (f"The altitude to the hypotenuse of a right triangle makes "
             f"two segments, {p} {u} beside one leg and {q} {u} beside "
             f"the other. How long is the leg that borders the first "
             f"segment?"),
            (f"{name} measures a right-triangular {thing}: the "
             f"perpendicular from the right angle splits the long side "
             f"into {p} {u} and {q} {u}. Find the length of the leg that "
             f"ends at the first of those two pieces."),
            (f"A right triangle's hypotenuse is divided by the altitude "
             f"from the right angle into p = {p} {u} and q = {q} {u}. "
             f"Determine the leg whose projection on the hypotenuse is "
             f"p."),
        ])

    def _find_segment_text(self, h, p, u, lab, name, thing):
        x, y, z, w = lab
        return random.choice([
            (f"The altitude to the hypotenuse of a right triangle has "
             f"length {h} {u}, and it splits the hypotenuse into two "
             f"segments, one of length {p} {u}. Find the other segment "
             f"q."),
            (f"In right triangle {x}{y}{z} the altitude {z}{w} to the "
             f"hypotenuse measures {h} {u}, and {x}{w} = {p} {u}. Find "
             f"the length q of {w}{y}."),
            (f"A right triangle's altitude to the hypotenuse is {h} {u} "
             f"long. One of the two pieces of the hypotenuse measures "
             f"{p} {u}. How long is the other piece q?"),
            (f"{name} draws the altitude of a right-triangular {thing} "
             f"from the right angle to the long side. The altitude is "
             f"{h} {u} and the piece of the long side on one side of "
             f"its foot is {p} {u}. Find the other piece q."),
            (f"Right triangle {x}{y}{z} has its right angle at {z}. The "
             f"altitude {z}{w} = {h} {u} meets the hypotenuse at {w}, "
             f"where {x}{w} = {p} {u}. Determine q, the length of "
             f"{w}{y}."),
        ])

    def _hypotenuse_text(self, leg, p, u, lab, name, thing):
        x, y, z, w = lab
        return random.choice([
            (f"In a right triangle one leg measures {leg} {u}, and its "
             f"projection on the hypotenuse is {p} {u}. Find the "
             f"hypotenuse c."),
            (f"Right triangle {x}{y}{z} has its right angle at {z}, and "
             f"the altitude {z}{w} meets the hypotenuse {x}{y} at {w}. "
             f"If the leg {z}{x} = {leg} {u} and {x}{w} = {p} {u}, find "
             f"the hypotenuse c, the length of {x}{y}."),
            (f"A right triangle has a leg of {leg} {u}. The altitude "
             f"from the right angle cuts off a piece of {p} {u} at that "
             f"leg's end of the hypotenuse. How long is the hypotenuse "
             f"c?"),
            (f"{name} checks a right-triangular {thing}: one leg is "
             f"{leg} {u} and the part of the long side directly beneath "
             f"that leg is {p} {u}. Find the length c of the long side."),
            (f"The leg of a right triangle is {leg} {u} and the segment "
             f"it projects onto the hypotenuse is {p} {u}. Determine the "
             f"hypotenuse c."),
        ])

    def _proportional_text(self, a, b, u, name, thing):
        """Returns (text, unit) — half the phrasings carry a length unit."""
        if random.random() < 0.5:
            return random.choice([
                (f"Two segments of a {thing} measure {a} {u} and {b} {u}. "
                 f"Find the length x of the mean proportional between "
                 f"them."),
                (f"{name} needs a brace whose length x is the geometric "
                 f"mean of {a} {u} and {b} {u}. How long is x?"),
                (f"Segments of {a} {u} and {b} {u} lie end to end on a "
                 f"line. Find the length x that is the geometric mean "
                 f"of those two segments."),
            ]), u
        return random.choice([
            f"Find the geometric mean x of {a} and {b}.",
            (f"Solve the proportion {a}/x = x/{b} for the positive "
             f"value of x."),
            f"What positive number x satisfies {a} : x = x : {b}?",
            (f"{name} needs the mean proportional x between {a} and "
             f"{b}. Find x."),
            (f"The numbers {a}, x, {b} form a geometric sequence with x "
             f"positive. Find x."),
        ]), None

    # ---- generation --------------------------------------------------------

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        u = random.choice(UNITS)
        lab = random.choice(LABEL_SETS)
        name = random.choice(NAMES)
        thing = random.choice(STRUCTURES)
        check = random.random() < 0.5

        if variant == "altitude":
            if random.random() < 0.15:
                p, q = _square_pair(2, 99)
            else:
                p = random.randint(2, 99)
                q = random.randint(2, 99)
            n = p * q
            val = sqrt_txt(n)
            steps = [
                step("GEO_SETUP",
                     f"right triangle, altitude to hypotenuse; the "
                     f"altitude splits the hypotenuse into p = {p} and "
                     f"q = {q}", "altitude h"),
                step("THEOREM", "geometric mean (altitude)",
                     "h = √(p·q)"),
                step("M", p, q, n),
            ]
            if "√" in val:
                steps.append(_root_step(n, val))
            else:
                steps.append(step("E", val, 2, n))
            if check:
                steps.append(step("CHECK", "substitute",
                                  f"h^2 = {_sq_txt(val)} = {n}",
                                  f"p·q = {p}·{q} = {n}"))
            answer = f"h = {val} {u}"
            problem = self._altitude_text(p, q, u, lab, name, thing)
        elif variant == "leg":
            if random.random() < 0.15:
                p, q = _leg_square_pair(2, 99)
            else:
                p = random.randint(2, 99)
                q = random.randint(2, 99)
            c = p + q
            n = p * c
            val = sqrt_txt(n)
            steps = [
                step("GEO_SETUP",
                     f"right triangle, altitude to hypotenuse; segments "
                     f"p = {p} (adjacent to the leg) and q = {q}",
                     "the leg adjacent to p"),
                step("A", p, q, c),
                step("THEOREM", "geometric mean (leg)",
                     "leg = √(p·c)"),
                step("M", p, c, n),
            ]
            if "√" in val:
                steps.append(_root_step(n, val))
            else:
                steps.append(step("E", val, 2, n))
            if check:
                steps.append(step("CHECK", "substitute",
                                  f"leg^2 = {_sq_txt(val)} = {n}",
                                  f"p·c = {p}·{c} = {n}"))
            answer = f"leg = {val} {u}"
            problem = self._leg_text(p, q, u, lab, name, thing)
        elif variant == "find_segment":
            h = random.randint(4, 140)
            p = _divisor_split(h)
            q = h * h // p
            steps = [
                step("GEO_SETUP",
                     f"right triangle, altitude h = {h} to the "
                     f"hypotenuse; one segment p = {p}",
                     "the other segment q"),
                step("THEOREM", "geometric mean (altitude)",
                     "h^2 = p·q"),
                step("E", h, 2, h * h),
                step("D", h * h, p, q),
            ]
            if check:
                steps.append(step("CHECK", "substitute",
                                  f"p·q = {p}·{q} = {h * h}",
                                  f"h^2 = {h}^2 = {h * h}"))
            answer = f"q = {q} {u}"
            problem = self._find_segment_text(h, p, u, lab, name, thing)
        elif variant == "hypotenuse":
            leg = random.randint(6, 140)
            sq = leg * leg
            cands = [d for d in _divisors(sq)
                     if max(1, leg // 20) <= d < leg]
            p = random.choice(cands or [1])
            c = sq // p
            steps = [
                step("GEO_SETUP",
                     f"right triangle, altitude to hypotenuse; leg = "
                     f"{leg} with projection p = {p} on the hypotenuse",
                     "the hypotenuse c"),
                step("THEOREM", "geometric mean (leg)",
                     "leg^2 = p·c"),
                step("E", leg, 2, sq),
                step("D", sq, p, c),
            ]
            if check:
                steps.append(step("CHECK", "substitute",
                                  f"p·c = {p}·{c} = {sq}",
                                  f"leg^2 = {leg}^2 = {sq}"))
            answer = f"c = {c} {u}"
            problem = self._hypotenuse_text(leg, p, u, lab, name, thing)
        else:
            if random.random() < 0.15:
                a, b = _square_pair(2, 120)
            else:
                a = random.randint(2, 120)
                b = random.randint(2, 120)
            n = a * b
            val = sqrt_txt(n)
            steps = [
                step("GEO_SETUP",
                     f"mean proportional between a = {a} and b = {b}",
                     "x with a/x = x/b"),
                step("THEOREM", "mean proportional", "x = √(a·b)"),
                step("M", a, b, n),
            ]
            if "√" in val:
                steps.append(_root_step(n, val))
            else:
                steps.append(step("E", val, 2, n))
            if check:
                steps.append(step("CHECK", "cross_products",
                                  f"a·b = {a}·{b} = {n}",
                                  f"x^2 = {_sq_txt(val)} = {n}"))
            problem, punit = self._proportional_text(a, b, u, name, thing)
            answer = f"x = {val} {punit}" if punit else f"x = {val}"
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"geometric_mean_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
