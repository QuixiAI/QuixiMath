import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


PLACES = [
    "geometry seminar", "relativity lab", "tensor workshop",
    "university classroom", "modeling group", "research institute",
    "physics department", "mathematics department", "training center",
    "science museum", "technical college", "simulation laboratory",
    "curvature study group", "graduate seminar", "analysis laboratory",
    "observatory", "computing center", "engineering institute",
    "research station", "lecture hall",
]

CONTEXTS = [
    "A calculation at the {place} uses the following chart data.",
    "During a session at the {place}, the following sphere is studied.",
    "A worksheet from the {place} gives this exact coordinate data.",
    "In a model prepared by the {place}, the following values are supplied.",
]


def fraction_text(value):
    return str(Fraction(value))


def sphere_point():
    """Return exact positive sine and cosine values from a primitive triple."""
    while True:
        outer = random.randint(2, 10)
        inner = random.randint(1, outer - 1)
        if math.gcd(outer, inner) == 1 and (outer - inner) % 2 == 1:
            break
    leg_a = outer * outer - inner * inner
    leg_b = 2 * outer * inner
    hypotenuse = outer * outer + inner * inner
    if random.choice([False, True]):
        leg_a, leg_b = leg_b, leg_a
    return Fraction(leg_a, hypotenuse), Fraction(leg_b, hypotenuse)


def sphere_radius():
    while True:
        radius = Fraction(random.randint(2, 120), random.randint(1, 20))
        if radius > 1:
            return radius


def context_text():
    return random.choice(CONTEXTS).format(place=random.choice(PLACES))


class RiemannTensorGenerator(ProblemGenerator):
    """
    Riemann -> Ricci -> scalar curvature for a 2-sphere at exact rational
    trigonometric points constructed from primitive Pythagorean triples.

    Uses the Christoffel-symbol sphere cases from ChristoffelGenerator:
    Gamma^phi_thetatheta = -sin(phi)cos(phi) and
    Gamma^theta_phitheta = cot(phi).

    Op-codes used:
    - RIEMANN_SETUP / CHRISTOFFEL_VALUE / DERIV / RIEMANN_ENTRY
    - RICCI_ENTRY / INVERSE_METRIC / CHECK
    - E / M / D / S / A (established/shared): exact arithmetic
    - Z: scalar curvature
    """

    def generate(self) -> dict:
        radius = sphere_radius()
        sin_phi, cos_phi = sphere_point()
        sin_sq = sin_phi ** 2
        cos_sq = cos_phi ** 2
        sin_cos = sin_phi * cos_phi
        gamma_phi = -sin_cos
        gamma_theta = cos_phi / sin_phi
        deriv_gamma = sin_sq - cos_sq
        radius_sq = radius ** 2
        inv_radius_sq = Fraction(1, radius_sq)
        gamma_product = gamma_phi * gamma_theta
        riemann_phi = deriv_gamma - gamma_product
        ricci_phiphi = Fraction(1)
        ricci_thetatheta = riemann_phi
        inverse_theta = inv_radius_sq / sin_sq
        theta_contraction = inverse_theta * ricci_thetatheta
        scalar = 2 * inv_radius_sq
        steps = [
            step("RIEMANN_SETUP", "sphere", f"R={fraction_text(radius)}",
                 f"sin(phi)={fraction_text(sin_phi)}, "
                 f"cos(phi)={fraction_text(cos_phi)}"),
            step("E", fraction_text(sin_phi), 2, fraction_text(sin_sq)),
            step("E", fraction_text(cos_phi), 2, fraction_text(cos_sq)),
            step("M", fraction_text(sin_phi), fraction_text(cos_phi),
                 fraction_text(sin_cos)),
            step("M", -1, fraction_text(sin_cos), fraction_text(gamma_phi)),
            step("D", fraction_text(cos_phi), fraction_text(sin_phi),
                 fraction_text(gamma_theta)),
            step("S", fraction_text(sin_sq), fraction_text(cos_sq),
                 fraction_text(deriv_gamma)),
            step("CHRISTOFFEL_VALUE", "Gamma^phi_thetatheta",
                 fraction_text(gamma_phi)),
            step("CHRISTOFFEL_VALUE", "Gamma^theta_phitheta",
                 fraction_text(gamma_theta)),
            step("DERIV", "d_phi Gamma^phi_thetatheta",
                 fraction_text(deriv_gamma)),
            step("M", fraction_text(gamma_phi),
                 fraction_text(gamma_theta),
                 fraction_text(gamma_product)),
            step("S", fraction_text(deriv_gamma),
                 fraction_text(gamma_product), fraction_text(riemann_phi)),
            step("RIEMANN_ENTRY", "R^phi_theta phi theta",
                 fraction_text(riemann_phi)),
            step("RIEMANN_ENTRY", "R^theta_phi theta phi", "1"),
            step("RICCI_ENTRY", "R_phiphi", "1"),
            step("RICCI_ENTRY", "R_thetatheta",
                 fraction_text(ricci_thetatheta)),
            step("E", fraction_text(radius), 2, fraction_text(radius_sq)),
            step("D", 1, fraction_text(radius_sq),
                 fraction_text(inv_radius_sq)),
            step("INVERSE_METRIC", "g^phiphi=1/R^2",
                 "g^thetatheta=1/(R^2 sin^2(phi))"),
            step("D", fraction_text(inv_radius_sq), fraction_text(sin_sq),
                 fraction_text(inverse_theta)),
            step("M", fraction_text(inverse_theta),
                 fraction_text(ricci_thetatheta),
                 fraction_text(theta_contraction)),
            step("CHECK", "g^thetatheta R_thetatheta",
                 fraction_text(theta_contraction), "sin^2 cancels"),
            step("A", fraction_text(inv_radius_sq),
                 fraction_text(inv_radius_sq), fraction_text(scalar)),
        ]
        answer = f"scalar curvature = {fraction_text(scalar)}"
        steps.append(step("Z", answer))
        problem = (
            f"{context_text()} For a 2-sphere of radius "
            f"R={fraction_text(radius)} at a point with "
            f"sin(phi)={fraction_text(sin_phi)} and "
            f"cos(phi)={fraction_text(cos_phi)}, compute "
            "R^phi_theta phi theta, the Ricci entries, and scalar curvature."
        )
        return dict(
            problem_id=jid(),
            operation="riemann_tensor_sphere",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
