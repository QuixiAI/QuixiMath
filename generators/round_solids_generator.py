import math
import random
from base_generator import ProblemGenerator
from helpers import step, jid


PLACES = [
    "architecture studio", "engineering classroom", "design workshop",
    "science museum", "technical college", "modeling lab",
    "construction office", "fabrication shop", "surveying class",
    "robotics lab", "university classroom", "training center",
    "prototype bay", "materials lab", "research station", "drafting room",
    "geometry seminar", "instrument shop", "field laboratory", "makerspace",
]

CONTEXTS = [
    "At the {place}, a solid is being analyzed.",
    "During a session at the {place}, the following solid is studied.",
    "A worksheet from the {place} gives these dimensions.",
    "In a model prepared by the {place}, the following measurements apply.",
    "An exercise used at the {place} asks about this solid.",
    "The {place} records a new set of solid measurements.",
    "A review prepared by the {place} includes the following dimensions.",
    "In a lesson at the {place}, this solid is analyzed.",
    "A design note from the {place} specifies the following solid.",
    "The next exercise at the {place} uses these measurements.",
]


def context_text():
    return random.choice(CONTEXTS).format(place=random.choice(PLACES))


def cone_triple():
    while True:
        outer = random.randint(2, 7)
        inner = random.randint(1, outer - 1)
        primitive_a = outer * outer - inner * inner
        primitive_b = 2 * outer * inner
        if (math.gcd(outer, inner) == 1 and (outer - inner) % 2 == 1
                and max(primitive_a, primitive_b) <= 100):
            break
    max_scale = max(1, min(4, 100 // max(primitive_a, primitive_b)))
    scale = random.randint(1, max_scale)
    leg_a = scale * primitive_a
    leg_b = scale * primitive_b
    hypotenuse = scale * (outer * outer + inner * inner)
    if random.choice([False, True]):
        leg_a, leg_b = leg_b, leg_a
    return leg_a, leg_b, hypotenuse


class RoundSolidsGenerator(ProblemGenerator):
    """
    Volume and surface area of pyramids, cones, and spheres — the round and
    pointed solids missing from the prism/cylinder generators. Everything is
    exact: π stays symbolic, cone slants come from Pythagorean triples, and
    volumes divisible by 3 are arranged by construction (a sphere volume may
    keep the /3: '500π/3 cubic units').

    Op-codes used (shared with the existing 3D generators):
    - VOL_FORMULA / SA_FORMULA: state the formula (formula)
    - VOL_BASE_AREA: base area for the pyramid (calculation, result)
    - VOL_CALCULATE: numeric volume work (calculation, result)
    - SA_TOTAL: assemble the surface area (calculation, result)
    - E: raise to a power (base, exponent, result)
    - A / M: add / multiply (x, y, result)
    - ROOT: square root (value, root)
    - Z: final answer
    """

    VARIANTS = ["volume_pyramid", "volume_cone", "volume_sphere",
                "surface_area_pyramid", "surface_area_cone",
                "surface_area_sphere"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        return getattr(self, f"_{variant}")()

    # ---------------- volumes ----------------

    def _volume_pyramid(self):
        while True:
            l, w, h = (random.randint(2, 30) for _ in range(3))
            if (l * w * h) % 3 == 0:
                break
        base_area = l * w
        volume = l * w * h // 3
        steps = [
            step("VOL_FORMULA", "V = (1/3) × Base Area × h"),
            step("VOL_BASE_AREA", f"{l} × {w}", base_area),
            step("VOL_CALCULATE", f"V = (1/3) × {base_area} × {h}", volume),
            step("Z", f"{volume} cubic units"),
        ]
        return dict(
            problem_id=jid(), operation="volume_pyramid",
            problem=(f"{context_text()} Find the volume of a pyramid with a "
                     f"rectangular base "
                     f"{l} units by {w} units and height {h} units."),
            steps=steps, final_answer=f"{volume} cubic units")

    def _volume_cone(self):
        while True:
            r = random.randint(2, 25)
            h = random.randint(3, 30)
            if (r * r * h) % 3 == 0:
                break
        coef = r * r * h // 3
        steps = [
            step("VOL_FORMULA", "V = (1/3)πr²h"),
            step("E", r, 2, r * r),
            step("VOL_CALCULATE", f"V = (1/3) × π × {r * r} × {h}", f"{coef}π"),
            step("Z", f"{coef}π cubic units"),
        ]
        return dict(
            problem_id=jid(), operation="volume_cone",
            problem=(f"{context_text()} Find the volume of a cone with radius "
                     f"{r} units and "
                     f"height {h} units. Leave the answer in terms of π."),
            steps=steps, final_answer=f"{coef}π cubic units")

    def _volume_sphere(self):
        r = random.randint(2, 50)
        give_diameter = random.random() < 0.5
        cubed = r ** 3
        if (4 * cubed) % 3 == 0:
            coef_txt = f"{4 * cubed // 3}π"
        else:
            coef_txt = f"{4 * cubed}π/3"
        answer = f"{coef_txt} cubic units"
        steps = [step("VOL_FORMULA", "V = (4/3)πr³")]
        if give_diameter:
            steps.append(step("D", 2 * r, 2, r))
        steps += [
            step("E", r, 3, cubed),
            step("VOL_CALCULATE", f"V = (4/3) × π × {cubed}", coef_txt),
            step("Z", answer),
        ]
        dim = (f"diameter {2 * r} units" if give_diameter
               else f"radius {r} units")
        return dict(
            problem_id=jid(), operation="volume_sphere",
            problem=(f"{context_text()} Find the volume of a sphere with "
                     f"{dim}. "
                     f"Leave the answer in terms of π."),
            steps=steps, final_answer=answer)

    # ---------------- surface areas ----------------

    def _surface_area_pyramid(self):
        b = random.randint(2, 30)
        slant = random.randint(3, 35)
        base_sq = b * b
        lateral = 2 * b * slant
        total = base_sq + lateral
        steps = [
            step("SA_FORMULA", "SA = b² + 2bl (square base, slant height l)"),
            step("E", b, 2, base_sq),
            step("M", b, slant, b * slant),
            step("M", 2, b * slant, lateral),
            step("A", base_sq, lateral, total),
            step("Z", f"{total} square units"),
        ]
        return dict(
            problem_id=jid(), operation="surface_area_pyramid",
            problem=(f"{context_text()} Find the surface area of a square "
                     f"pyramid with base "
                     f"side {b} units and slant height {slant} units."),
            steps=steps, final_answer=f"{total} square units")

    def _surface_area_cone(self):
        r, h, slant = cone_triple()
        r_sq, h_sq = r * r, h * h
        rl = r * slant
        coef = r_sq + rl
        steps = [
            step("SA_FORMULA", "SA = πr² + πrl (l = slant height)"),
            step("E", r, 2, r_sq),
            step("E", h, 2, h_sq),
            step("A", r_sq, h_sq, slant * slant),
            step("ROOT", slant * slant, slant),
            step("M", r, slant, rl),
            step("A", r_sq, rl, coef),
            step("SA_TOTAL", f"SA = π({r_sq} + {rl})", f"{coef}π"),
            step("Z", f"{coef}π square units"),
        ]
        return dict(
            problem_id=jid(), operation="surface_area_cone",
            problem=(f"{context_text()} Find the surface area of a cone with "
                     f"radius {r} units "
                     f"and height {h} units. Leave the answer in terms of π."),
            steps=steps, final_answer=f"{coef}π square units")

    def _surface_area_sphere(self):
        r = random.randint(2, 50)
        give_diameter = random.random() < 0.5
        r_sq = r * r
        coef = 4 * r_sq
        steps = [step("SA_FORMULA", "SA = 4πr²")]
        if give_diameter:
            steps.append(step("D", 2 * r, 2, r))
        steps += [
            step("E", r, 2, r_sq),
            step("M", 4, r_sq, coef),
            step("Z", f"{coef}π square units"),
        ]
        dim = (f"diameter {2 * r} units" if give_diameter
               else f"radius {r} units")
        return dict(
            problem_id=jid(), operation="surface_area_sphere",
            problem=(f"{context_text()} Find the surface area of a sphere "
                     f"with {dim}. "
                     f"Leave the answer in terms of π."),
            steps=steps, final_answer=f"{coef}π square units")
