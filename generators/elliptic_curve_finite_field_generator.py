import random

from base_generator import ProblemGenerator
from helpers import step, jid


CURVES = [
    dict(p=17, a=2, b=2),
    dict(p=19, a=1, b=1),
    dict(p=23, a=1, b=4),
]

PROBLEM_TEMPLATES = [
    ("On the elliptic curve E: y^2 = x^3 + {a}x + {b} over F_{p}, {task}."),
    ("Work over F_{p} on E: y^2 = x^3 + {a}x + {b}; {task}."),
    ("For E/F_{p} given by y^2 = x^3 + {a}x + {b}, {task}."),
]


def point_text(point):
    if point is None:
        return "O"
    return f"({point[0]},{point[1]})"


def inv_mod(value, modulus):
    return pow(value % modulus, -1, modulus)


def enumerate_points(p, a, b):
    points = []
    for x in range(p):
        rhs = (x ** 3 + a * x + b) % p
        for y in range(p):
            if (y * y) % p == rhs:
                points.append((x, y))
    return points


def add_points(P, Q, p, a):
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if P == Q:
        slope = ((3 * x1 * x1 + a) * inv_mod(2 * y1, p)) % p
    else:
        slope = ((y2 - y1) * inv_mod(x2 - x1, p)) % p
    x3 = (slope * slope - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p
    return x3, y3


class EllipticCurveFiniteFieldGenerator(ProblemGenerator):
    """
    Elliptic-curve point arithmetic over small prime fields.

    Variants:
    - add: point addition P + Q
    - double: point doubling 2P
    - scalar: scalar multiplication by repeated addition

    Op-codes used:
    - EC_SETUP / EC_POINT_CHECK / EC_SLOPE_FORMULA / MOD_INVERSE
    - M / A / S / MOD_REDUCE (established/shared): slope and coordinates
    - EC_SLOPE / EC_X3 / EC_Y3 / EC_ACCUM / CHECK
    - Z: resulting point
    """

    VARIANTS = ["add", "double", "scalar"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        curve = random.choice(CURVES)
        p, a, b = curve["p"], curve["a"], curve["b"]
        points = enumerate_points(p, a, b)
        steps = [
            step("EC_SETUP", f"p={p}", f"a={a}", f"b={b}"),
        ]
        if variant == "add":
            P, Q = self._pick_add_points(points, p)
            result = self._append_add_steps(steps, P, Q, p, a, b, "P+Q")
            task = f"compute P + Q for P={point_text(P)} and Q={point_text(Q)}"
            answer = f"P+Q = {point_text(result)}"
        elif variant == "double":
            P = random.choice([pt for pt in points if pt[1] % p != 0])
            result = self._append_add_steps(steps, P, P, p, a, b, "2P")
            task = f"compute 2P for P={point_text(P)}"
            answer = f"2P = {point_text(result)}"
        else:
            P = random.choice([pt for pt in points if pt[1] % p != 0])
            k = random.randint(3, 6)
            acc = None
            steps.append(step("EC_SCALAR_SETUP", f"k={k}", f"P={point_text(P)}"))
            for i in range(1, k + 1):
                acc = self._append_add_steps(steps, acc, P, p, a, b,
                                             f"{i}P")
                steps.append(step("EC_ACCUM", f"{i}P", point_text(acc)))
            task = f"compute {k}P for P={point_text(P)}"
            answer = f"{k}P = {point_text(acc)}"
        problem = random.choice(PROBLEM_TEMPLATES).format(
            p=p,
            a=a,
            b=b,
            task=task,
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"elliptic_curve_finite_field_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _pick_add_points(self, points, p):
        candidates = []
        for P in points:
            for Q in points:
                if P != Q and not (P[0] == Q[0] and (P[1] + Q[1]) % p == 0):
                    candidates.append((P, Q))
        return random.choice(candidates)

    def _append_point_check(self, steps, point, p, a, b, label):
        if point is None:
            steps.append(step("EC_POINT_CHECK", label, "O", "identity"))
            return
        x, y = point
        lhs = (y * y) % p
        rhs_raw = x ** 3 + a * x + b
        rhs = rhs_raw % p
        steps.append(step("EC_POINT_CHECK", label, f"y^2 mod p = {lhs}",
                          f"x^3+ax+b mod p = {rhs}"))

    def _append_add_steps(self, steps, P, Q, p, a, b, label):
        self._append_point_check(steps, P, p, a, b, "P")
        self._append_point_check(steps, Q, p, a, b, "Q")
        if P is None:
            steps.append(step("EC_IDENTITY", "O + Q", point_text(Q)))
            return Q
        if Q is None:
            steps.append(step("EC_IDENTITY", "P + O", point_text(P)))
            return P

        x1, y1 = P
        x2, y2 = Q
        if x1 == x2 and (y1 + y2) % p == 0:
            steps.append(step("EC_INVERSE", point_text(P), point_text(Q),
                              "O"))
            return None

        if P == Q:
            numerator = 3 * x1 * x1 + a
            denominator = 2 * y1
            steps.append(step("EC_SLOPE_FORMULA", label,
                              "(3x1^2+a)/(2y1)"))
        else:
            numerator = y2 - y1
            denominator = x2 - x1
            steps.append(step("EC_SLOPE_FORMULA", label,
                              "(y2-y1)/(x2-x1)"))
        den_inv = inv_mod(denominator, p)
        slope = (numerator * den_inv) % p
        steps.append(step("MOD_INVERSE", f"{denominator} mod {p}", den_inv))
        steps.append(step("M", numerator, den_inv, numerator * den_inv))
        steps.append(step("MOD_REDUCE", numerator * den_inv, f"mod {p}",
                          slope))
        steps.append(step("EC_SLOPE", label, slope))

        raw_x3 = slope * slope - x1 - x2
        x3 = raw_x3 % p
        steps.append(step("M", slope, slope, slope * slope))
        steps.append(step("S", slope * slope, x1, slope * slope - x1))
        steps.append(step("S", slope * slope - x1, x2, raw_x3))
        steps.append(step("MOD_REDUCE", raw_x3, f"mod {p}", x3))
        steps.append(step("EC_X3", label, x3))

        raw_y3 = slope * (x1 - x3) - y1
        y3 = raw_y3 % p
        steps.append(step("S", x1, x3, x1 - x3))
        steps.append(step("M", slope, x1 - x3, slope * (x1 - x3)))
        steps.append(step("S", slope * (x1 - x3), y1, raw_y3))
        steps.append(step("MOD_REDUCE", raw_y3, f"mod {p}", y3))
        steps.append(step("EC_Y3", label, y3))
        result = (x3, y3)
        self._append_point_check(steps, result, p, a, b, "result")
        steps.append(step("CHECK", label, point_text(result)))
        return result
