import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def over_pi_text(value):
    coeff = Fraction(value)
    if coeff.denominator == 1:
        return f"{coeff.numerator}/π"
    return f"{coeff.numerator}/({coeff.denominator}π)"


class GaussLawGenerator(ProblemGenerator):
    """
    Gauss's law for spherical, cylindrical, and planar symmetry.

    Variants:
    - sphere: E*4πr^2 = Q/epsilon0, with epsilon0=1
    - line_charge: E*2πrL = lambda L, with epsilon0=1
    - sheet_charge: 2EA = sigma A, with epsilon0=1

    Op-codes used:
    - GAUSS_SETUP: symmetric Gaussian surface and givens
    - GAUSS_FORMULA: flux equation
    - PI_DEN: attach a symbolic π in the denominator
    - M / D / E (established/shared): exact arithmetic
    - Z: electric field magnitude or signed field
    """

    VARIANTS = ["sphere", "line_charge", "sheet_charge"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "sphere":
            problem, steps, answer = self._generate_sphere()
        elif variant == "line_charge":
            problem, steps, answer = self._generate_line_charge()
        else:
            problem, steps, answer = self._generate_sheet_charge()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"gauss_law_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_sphere(self):
        charge = random.randint(1, 80)
        radius = random.randint(1, 12)
        radius_sq = radius ** 2
        area_coeff = 4 * radius_sq
        coeff = Fraction(charge, area_coeff)
        field = over_pi_text(coeff)
        steps = [
            step("GAUSS_SETUP", "sphere", f"Q={charge}", f"r={radius}"),
            step("GAUSS_FORMULA", "E*(4πr^2)=Q"),
            step("E", radius, 2, radius_sq),
            step("M", 4, radius_sq, area_coeff),
            step("D", charge, area_coeff, fraction_text(coeff)),
            step("PI_DEN", fraction_text(coeff), "π", field),
        ]
        answer = f"E={field} N/C outward-positive"
        problem = (
            f"A spherical Gaussian surface of radius r={radius} m encloses "
            f"charge Q={charge} C. Use epsilon0=1 and Gauss's law to find "
            "the electric field on the surface."
        )
        return problem, steps, answer

    def _generate_line_charge(self):
        line_density = random.randint(1, 40)
        radius = random.randint(1, 12)
        length = random.randint(1, 12)
        enclosed = line_density * length
        two_r = 2 * radius
        area_coeff = two_r * length
        coeff = Fraction(enclosed, area_coeff)
        field = over_pi_text(coeff)
        steps = [
            step("GAUSS_SETUP", "line_charge",
                 f"lambda={line_density}, r={radius}", f"L={length}"),
            step("GAUSS_FORMULA", "E*(2πrL)=lambda*L"),
            step("M", line_density, length, enclosed),
            step("M", 2, radius, two_r),
            step("M", two_r, length, area_coeff),
            step("D", enclosed, area_coeff, fraction_text(coeff)),
            step("PI_DEN", fraction_text(coeff), "π", field),
        ]
        answer = f"E={field} N/C outward-positive"
        problem = (
            f"An infinite line charge has lambda={line_density} C/m. A "
            f"cylindrical Gaussian surface has radius r={radius} m and "
            f"length L={length} m. Use epsilon0=1 to find the electric field."
        )
        return problem, steps, answer

    def _generate_sheet_charge(self):
        sigma = random.randint(1, 80)
        area = random.randint(1, 30)
        enclosed = sigma * area
        flux_coeff = 2 * area
        field = Fraction(enclosed, flux_coeff)
        steps = [
            step("GAUSS_SETUP", "sheet_charge", f"sigma={sigma}",
                 f"A={area}"),
            step("GAUSS_FORMULA", "2*E*A=sigma*A"),
            step("M", sigma, area, enclosed),
            step("M", 2, area, flux_coeff),
            step("D", enclosed, flux_coeff, fraction_text(field)),
        ]
        answer = f"E={fraction_text(field)} N/C away from sheet"
        problem = (
            f"An infinite sheet has surface charge density sigma={sigma} C/m^2. "
            f"A pillbox Gaussian surface has cap area A={area} m^2. Use "
            "epsilon0=1 to find the electric field on each side."
        )
        return problem, steps, answer
