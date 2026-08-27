import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid


def pi_txt(fr):
    """Exact multiple of π: '6π', '49π/8', 'π/3'."""
    if fr.denominator == 1:
        return "π" if fr == 1 else f"{fr.numerator}π"
    head = "π" if fr.numerator == 1 else f"{fr.numerator}π"
    return f"{head}/{fr.denominator}"


NOUNS = [
    "garden", "rug", "pond", "tabletop", "mirror", "tray", "window",
    "patio", "logo", "badge", "platform", "clock face", "dial", "plate",
    "lid", "sign", "pool", "fountain", "stage", "mat", "turntable",
    "flowerbed", "griddle", "medallion",
]

# Radian angles worth writing on a diagram: p/q · π with a small q.
RADIAN_ANGLES = sorted({
    Fraction(p, q)
    for q in (1, 2, 3, 4, 5, 6, 8, 9, 10, 12)
    for p in range(1, 2 * q + 1)
    if Fraction(p, q).denominator == q
})

LETTERS = ["O", "P", "Q", "A", "B", "C", "M", "N", "T", "K", "R", "S"]

ARC_TEMPLATES = [
    ("Circle {L} has radius {r}. Find the length of the arc cut off by a "
     "central angle of {theta}°. Give the exact answer in terms of π."),
    ("A circular {noun} has radius {r}. A central angle of {theta}° cuts "
     "off an arc along its edge. Find the exact arc length in terms of π."),
    ("On a circular {noun} of radius {r}, an arc is intercepted by a "
     "central angle measuring {theta}°. How long is that arc? Give the "
     "exact answer in terms of π."),
    ("A central angle of {theta}° is drawn in circle {L}, which has "
     "radius {r}. Find the exact length of the intercepted arc in terms "
     "of π."),
    ("A circular {noun} has radius {r}. Find the exact length, in terms "
     "of π, of the arc swept out by a turn of {theta}° about the center."),
]

SECTOR_TEMPLATES = [
    ("Circle {L} has radius {r}. Find the area of the sector with central "
     "angle {theta}°. Give the exact answer in terms of π."),
    ("A circular {noun} has radius {r}. Find the exact area, in terms of "
     "π, of the sector with a central angle of {theta}°."),
    ("A sector of {theta}° is cut from a circular {noun} of radius {r}. "
     "What is its exact area in terms of π?"),
    ("In circle {L} of radius {r}, a central angle of {theta}° determines "
     "a sector. Find the sector's exact area in terms of π."),
    ("A circular {noun} of radius {r} has two radii meeting at a central "
     "angle of {theta}°. Find the exact area of the sector they bound, in "
     "terms of π."),
]

ARC_RAD_TEMPLATES = [
    ("Circle {L} has radius {r}. A central angle of {ang} radians cuts "
     "off an arc. Find its exact length in terms of π."),
    ("A circular {noun} has radius {r}. Find the exact arc length, in "
     "terms of π, intercepted by a central angle of {ang} radians."),
    ("In circle {L} of radius {r}, a central angle measures {ang} "
     "radians. Find the exact length of the arc it intercepts, in terms "
     "of π."),
    ("A point on the rim of a circular {noun} of radius {r} turns through "
     "{ang} radians. Find the exact distance it travels, in terms of π."),
]

SECTOR_RAD_TEMPLATES = [
    ("Circle {L} has radius {r}. Find the exact area, in terms of π, of "
     "the sector with central angle {ang} radians."),
    ("A circular {noun} has radius {r}. A central angle of {ang} radians "
     "bounds a sector. Find its exact area in terms of π."),
    ("In circle {L} of radius {r}, a sector has central angle {ang} "
     "radians. Find the sector's exact area in terms of π."),
    ("A sector of a circular {noun} of radius {r} has central angle {ang} "
     "radians. Give its exact area in terms of π."),
]


class ArcSectorGenerator(ProblemGenerator):
    """
    Arc length and sector area, kept exact in terms of π: reduce the
    angle fraction θ/360 first, then apply it to 2πr or πr².

    Variants:
    - arc / sector: central angle in degrees, via θ/360
    - arc_radians / sector_radians: central angle already in radians,
      via L = rθ and A = r²θ/2

    Op-codes used:
    - ARC_SETUP: radius, central angle, and the goal (given, goal)
    - ARC_FORMULA / SECTOR_FORMULA: the formula (established shape)
    - FRAC_REDUCE: θ/360 in lowest terms (established)
    - PI_COEFF: the π-coefficient of a radian angle (angle, coefficient)
    - M / E: the arithmetic, exact fractions (established)
    - Z: exact answer like '6π' or '49π/8'
    """

    VARIANTS = ["arc", "sector", "arc_radians", "sector_radians"]
    ANGLES = list(range(5, 356, 5))
    RADII = list(range(2, 61))

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        r = random.choice(self.RADII)
        noun = random.choice(NOUNS)
        letter = random.choice(LETTERS)
        if variant in ("arc", "sector"):
            theta = random.choice(self.ANGLES)
            frac = Fraction(theta, 360)
            goal = "arc length" if variant == "arc" else "sector area"
            steps = [
                step("ARC_SETUP",
                     f"circle r = {r}, central angle {theta}°", goal),
                step("ARC_FORMULA" if variant == "arc" else "SECTOR_FORMULA",
                     "L = (θ/360)·2πr" if variant == "arc"
                     else "A = (θ/360)·πr^2"),
                step("FRAC_REDUCE", f"{theta}/360", frac),
            ]
            if variant == "arc":
                steps.append(step("M", 2, r, 2 * r))
                value = frac * 2 * r
                steps.append(step("M", frac, 2 * r, value))
                templates = ARC_TEMPLATES
            else:
                steps.append(step("E", r, 2, r * r))
                value = frac * r * r
                steps.append(step("M", frac, r * r, value))
                templates = SECTOR_TEMPLATES
            problem = random.choice(templates).format(
                r=r, theta=theta, noun=noun, L=letter)
        else:
            angle = random.choice(RADIAN_ANGLES)
            angle_txt = pi_txt(angle)
            goal = ("arc length" if variant == "arc_radians"
                    else "sector area")
            steps = [
                step("ARC_SETUP",
                     f"circle r = {r}, central angle {angle_txt} rad", goal),
                step("ARC_FORMULA" if variant == "arc_radians"
                     else "SECTOR_FORMULA",
                     "L = rθ" if variant == "arc_radians"
                     else "A = (1/2)r^2θ"),
                step("PI_COEFF", angle_txt, angle),
            ]
            if variant == "arc_radians":
                value = r * angle
                steps.append(step("M", r, angle, value))
                templates = ARC_RAD_TEMPLATES
            else:
                steps.append(step("E", r, 2, r * r))
                half = Fraction(r * r, 2)
                steps.append(step("M", Fraction(1, 2), r * r, half))
                value = half * angle
                steps.append(step("M", half, angle, value))
                templates = SECTOR_RAD_TEMPLATES
            problem = random.choice(templates).format(
                r=r, ang=angle_txt, noun=noun, L=letter)

        answer = pi_txt(value)
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"{variant}_measure",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
