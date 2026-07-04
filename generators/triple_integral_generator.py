import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fmt_frac(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def fmt_pi(coeff):
    coeff = Fraction(coeff)
    if coeff == 1:
        return "pi"
    if coeff == -1:
        return "-pi"
    return f"{fmt_frac(coeff)}*pi"


def fmt_pi_product(factors):
    pieces = [fmt_frac(f) for f in factors if Fraction(f) != 1]
    pieces.append("pi")
    return "*".join(pieces)


class TripleIntegralGenerator(ProblemGenerator):
    """
    Triple integrals in cylindrical and spherical coordinates.

    Variants:
    - cylindrical: integrate z over a right circular cylinder
    - spherical:   integrate 1 over a ball

    Op-codes used:
    - TRIPLE_SETUP: integrand, solid, and target
    - CYL_CONVERT / SPHERICAL_CONVERT: coordinate rewrite and Jacobian
    - CYL_BOUNDS / SPHERICAL_BOUNDS: coordinate bounds
    - INNER_ANTIDERIV / INNER_EVAL (established): first integral
    - MIDDLE_EVAL: second coordinate integral
    - ANGLE_EVAL: angular integral
    - TRIPLE_EVAL: assembled exact value
    - Z: final value
    """

    VARIANTS = ["cylindrical", "spherical"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "cylindrical":
            radius = random.randint(2, 12)
            height = random.randint(2, 12)
            coeff_z = random.randint(1, 6)
            integrand = "z" if coeff_z == 1 else f"{coeff_z}*z"
            cyl_integrand = "z*r dz dr dtheta" if coeff_z == 1 else (
                f"{coeff_z}*z*r dz dr dtheta")
            z_part = Fraction(height * height, 2)
            r_part = Fraction(radius * radius, 2)
            coeff = coeff_z * 2 * z_part * r_part
            value = fmt_pi(coeff)
            answer = f"value {value}"
            steps = [
                step("TRIPLE_SETUP", f"integrand {integrand}",
                     f"cylinder radius {radius}, height {height}",
                     "cylindrical"),
                step("CYL_CONVERT", f"{integrand} dV", cyl_integrand),
                step("CYL_BOUNDS", "z", f"0..{height}"),
                step("CYL_BOUNDS", "r", f"0..{radius}"),
                step("CYL_BOUNDS", "theta", "0..2*pi"),
                step("INNER_ANTIDERIV", "dz", "z^2/2"),
                step("INNER_EVAL", f"z=0..{height}",
                     f"{height}^2/2", fmt_frac(z_part)),
                step("MIDDLE_EVAL", f"r=0..{radius}",
                     f"{radius}^2/2", fmt_frac(r_part)),
                step("ANGLE_EVAL", "theta=0..2*pi", "2*pi"),
                step("TRIPLE_EVAL", "z_part * r_part * angle",
                     fmt_pi_product([coeff_z, z_part, r_part, 2]),
                     value),
                step("Z", answer),
            ]
            problem = (
                f"Convert to cylindrical and evaluate the triple integral "
                f"of {integrand} over the solid x^2 + y^2 <= "
                f"{radius * radius}, "
                f"0 <= z <= {height}."
            )
        else:
            radius = random.randint(2, 12)
            coeff_const = random.randint(1, 6)
            integrand = str(coeff_const)
            spherical_integrand = (
                "rho^2*sin(phi) drho dphi dtheta" if coeff_const == 1
                else f"{coeff_const}*rho^2*sin(phi) drho dphi dtheta")
            rho_part = Fraction(radius ** 3, 3)
            phi_part = 2
            theta_part = 2
            coeff = coeff_const * rho_part * phi_part * theta_part
            value = fmt_pi(coeff)
            answer = f"value {value}"
            steps = [
                step("TRIPLE_SETUP", f"integrand {integrand}",
                     f"ball radius {radius}", "spherical"),
                step("SPHERICAL_CONVERT", f"{integrand} dV",
                     spherical_integrand),
                step("SPHERICAL_BOUNDS", "rho", f"0..{radius}"),
                step("SPHERICAL_BOUNDS", "phi", "0..pi"),
                step("SPHERICAL_BOUNDS", "theta", "0..2*pi"),
                step("INNER_ANTIDERIV", "drho", "rho^3/3"),
                step("INNER_EVAL", f"rho=0..{radius}",
                     f"{radius}^3/3", fmt_frac(rho_part)),
                step("MIDDLE_EVAL", "phi=0..pi",
                     "int sin(phi) dphi = 2", phi_part),
                step("ANGLE_EVAL", "theta=0..2*pi", "2*pi"),
                step("TRIPLE_EVAL", "rho_part * phi_part * angle",
                     fmt_pi_product([coeff_const, rho_part, 2, 2]),
                     value),
                step("Z", answer),
            ]
            problem = (
                f"Convert to spherical and evaluate the triple integral "
                f"of {integrand} over the ball x^2 + y^2 + z^2 <= "
                f"{radius * radius}."
            )

        return dict(
            problem_id=jid(),
            operation=f"triple_integral_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
