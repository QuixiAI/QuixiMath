import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class BlackbodyGenerator(ProblemGenerator):
    """
    Blackbody radiation computations with supplied constants.

    Variants:
    - wien_peak: lambda_max = b/T
    - stefan_power: P = sigma*A*T^4

    Op-codes used:
    - BLACKBODY_SETUP: constants and physical givens
    - BLACKBODY_FORMULA: Wien or Stefan-Boltzmann relation
    - E / M / D (established/shared): exact arithmetic
    - Z: wavelength or radiated power
    """

    VARIANTS = ["wien_peak", "stefan_power"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "wien_peak":
            problem, steps, answer = self._generate_wien_peak()
        else:
            problem, steps, answer = self._generate_stefan_power()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"blackbody_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_wien_peak(self):
        temperature = random.randint(100, 1200)
        wavelength = random.randint(1, 40)
        wien_constant = temperature * wavelength
        steps = [
            step("BLACKBODY_SETUP", "wien_peak",
                 f"b={wien_constant}", f"T={temperature}"),
            step("BLACKBODY_FORMULA", "lambda_max=b/T"),
            step("D", wien_constant, temperature, wavelength),
        ]
        answer = f"lambda_max={wavelength} m"
        problem = (
            f"A blackbody has temperature T={temperature} K. Using Wien "
            f"constant b={wien_constant} m*K, find peak wavelength lambda_max."
        )
        return problem, steps, answer

    def _generate_stefan_power(self):
        sigma = random.randint(1, 12)
        area = random.randint(1, 20)
        temperature = random.randint(2, 20)
        t_fourth = temperature ** 4
        sigma_area = sigma * area
        power = sigma_area * t_fourth
        steps = [
            step("BLACKBODY_SETUP", "stefan_power",
                 f"sigma={sigma}, A={area}", f"T={temperature}"),
            step("BLACKBODY_FORMULA", "P=sigma*A*T^4"),
            step("E", temperature, 4, t_fourth),
            step("M", sigma, area, sigma_area),
            step("M", sigma_area, t_fourth, power),
        ]
        answer = f"P={power} W"
        problem = (
            f"A blackbody has area A={area} m^2 and temperature T={temperature} "
            f"K. Using Stefan-Boltzmann constant sigma={sigma}, find radiated "
            "power P."
        )
        return problem, steps, answer
