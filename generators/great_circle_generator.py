import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


CASES = [
    dict(lat1=0, lat2=0, delta=60, s1="0", s2="0", c1="1",
         c2="1", cd="1/2", theta=Fraction(1, 3)),
    dict(lat1=0, lat2=0, delta=90, s1="0", s2="0", c1="1",
         c2="1", cd="0", theta=Fraction(1, 2)),
    dict(lat1=0, lat2=0, delta=120, s1="0", s2="0", c1="1",
         c2="1", cd="-1/2", theta=Fraction(2, 3)),
    dict(lat1=0, lat2=0, delta=180, s1="0", s2="0", c1="1",
         c2="1", cd="-1", theta=Fraction(1, 1)),
    dict(lat1=0, lat2=60, delta=0, s1="0", s2="sqrt(3)/2",
         c1="1", c2="1/2", cd="1", theta=Fraction(1, 3)),
    dict(lat1=0, lat2=60, delta=180, s1="0", s2="sqrt(3)/2",
         c1="1", c2="1/2", cd="-1", theta=Fraction(2, 3)),
    dict(lat1=90, lat2=30, delta=60, s1="1", s2="1/2",
         c1="0", c2="sqrt(3)/2", cd="1/2", theta=Fraction(1, 3)),
    dict(lat1=90, lat2=0, delta=120, s1="1", s2="0",
         c1="0", c2="1", cd="-1/2", theta=Fraction(1, 2)),
    dict(lat1=90, lat2=-30, delta=90, s1="1", s2="-1/2",
         c1="0", c2="sqrt(3)/2", cd="0", theta=Fraction(2, 3)),
    dict(lat1=-90, lat2=30, delta=90, s1="-1", s2="1/2",
         c1="0", c2="sqrt(3)/2", cd="0", theta=Fraction(2, 3)),
]


RADII = [3, 4, 6, 8, 9, 12, 18, 24]
LONGITUDES = [-150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150]


def normalize_longitude(value):
    while value > 180:
        value -= 360
    while value <= -180:
        value += 360
    return value


def exact_value(text):
    if text == "sqrt(3)/2":
        return Fraction(0), Fraction(1, 2)
    if text == "-sqrt(3)/2":
        return Fraction(0), Fraction(-1, 2)
    return Fraction(text), Fraction(0)


def exact_text(value):
    rational, sqrt3 = value
    if sqrt3 == 0:
        return str(rational)
    if rational == 0:
        if sqrt3 == 1:
            return "sqrt(3)"
        if sqrt3 == -1:
            return "-sqrt(3)"
        if sqrt3 == Fraction(1, 2):
            return "sqrt(3)/2"
        if sqrt3 == Fraction(-1, 2):
            return "-sqrt(3)/2"
        return f"{sqrt3}*sqrt(3)"
    raise ValueError(f"cannot render mixed exact value {value}")


def exact_mul(left, right):
    a, b = exact_value(left)
    c, d = exact_value(right)
    return exact_text((a * c + 3 * b * d, a * d + b * c))


def exact_add(left, right):
    a, b = exact_value(left)
    c, d = exact_value(right)
    return exact_text((a + c, b + d))


def pi_text(multiplier):
    multiplier = Fraction(multiplier)
    if multiplier == 0:
        return "0"
    if multiplier == 1:
        return "pi"
    if multiplier == -1:
        return "-pi"
    if multiplier.denominator == 1:
        return f"{multiplier.numerator}pi"
    if multiplier.numerator == 1:
        return f"pi/{multiplier.denominator}"
    if multiplier.numerator == -1:
        return f"-pi/{multiplier.denominator}"
    return f"{multiplier.numerator}pi/{multiplier.denominator}"


class GreatCircleGenerator(ProblemGenerator):
    """
    Great-circle distances from latitude and longitude using the
    spherical law of cosines with all needed trig/arccos values supplied.

    Op-codes used:
    - GREAT_CIRCLE_SETUP / SPHERICAL_COSINES / TRIG_VALUE
    - ARCCOS: central angle from the supplied inverse-cosine value
    - M / A (established/shared): product and sum arithmetic
    - Z: exact distance in units of pi
    """

    def generate(self) -> dict:
        case = random.choice(CASES)
        radius = random.choice(RADII)
        lon1 = random.choice(LONGITUDES)
        lon2 = normalize_longitude(lon1 + case["delta"])
        sin_product = exact_mul(case["s1"], case["s2"])
        cos_pair = exact_mul(case["c1"], case["c2"])
        cos_product = exact_mul(cos_pair, case["cd"])
        cos_c = exact_add(sin_product, cos_product)
        theta = pi_text(case["theta"])
        distance = pi_text(radius * case["theta"])
        steps = [
            step("GREAT_CIRCLE_SETUP", f"R={radius}",
                 f"A=({case['lat1']},{lon1})",
                 f"B=({case['lat2']},{lon2})"),
            step("SPHERICAL_COSINES",
                 "cos(c)=sin(lat1)sin(lat2)+cos(lat1)cos(lat2)cos(dlon)"),
            step("TRIG_VALUE", f"sin(lat1)={case['s1']}",
                 f"sin(lat2)={case['s2']}", f"cos(dlon)={case['cd']}"),
            step("TRIG_VALUE", f"cos(lat1)={case['c1']}",
                 f"cos(lat2)={case['c2']}"),
            step("M", case["s1"], case["s2"], sin_product),
            step("M", case["c1"], case["c2"], cos_pair),
            step("M", cos_pair, case["cd"], cos_product),
            step("A", sin_product, cos_product, cos_c),
            step("ARCCOS", f"cos(c)={cos_c}", f"c={theta}"),
            step("M", radius, theta, distance),
        ]
        answer = f"distance = {distance}"
        steps.append(step("Z", answer))
        problem = (
            f"On a sphere of radius {radius}, point A is at latitude "
            f"{case['lat1']} deg, longitude {lon1} deg, and point B is "
            f"at latitude {case['lat2']} deg, longitude {lon2} deg. "
            f"The longitude difference is {case['delta']} deg. Given "
            f"sin(lat1)={case['s1']}, sin(lat2)={case['s2']}, "
            f"cos(lat1)={case['c1']}, cos(lat2)={case['c2']}, "
            f"cos(delta)={case['cd']}, and arccos({cos_c})={theta}, "
            f"find the great-circle distance."
        )
        return dict(
            problem_id=jid(),
            operation="great_circle_distance",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
