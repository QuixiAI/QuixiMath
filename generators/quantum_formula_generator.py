import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class QuantumFormulaGenerator(ProblemGenerator):
    """
    Intro quantum formulas with supplied constants.

    Variants:
    - photoelectric: K_max = h f - phi
    - de_broglie: lambda = h / p
    - compton: Delta lambda = h/(m c) * (1 - cos theta)

    Op-codes used:
    - QUANTUM_SETUP: supplied constants and givens
    - QUANTUM_FORMULA: quantum relation
    - M / S / D (established/shared): exact arithmetic
    - Z: requested quantum quantity
    """

    VARIANTS = ["photoelectric", "de_broglie", "compton"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "photoelectric":
            problem, steps, answer = self._generate_photoelectric()
        elif variant == "de_broglie":
            problem, steps, answer = self._generate_de_broglie()
        else:
            problem, steps, answer = self._generate_compton()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"quantum_formula_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_photoelectric(self):
        h = random.randint(1, 20)
        frequency = random.randint(2, 30)
        photon_energy = h * frequency
        work_function = random.randint(1, photon_energy - 1)
        kinetic = photon_energy - work_function
        steps = [
            step("QUANTUM_SETUP", "photoelectric",
                 f"h={h}, f={frequency}", f"phi={work_function}"),
            step("QUANTUM_FORMULA", "K_max=h*f-phi"),
            step("M", h, frequency, photon_energy),
            step("S", photon_energy, work_function, kinetic),
        ]
        answer = f"K_max={kinetic} J"
        problem = (
            f"A photoelectric surface has work function phi={work_function} J. "
            f"Light has frequency f={frequency} Hz and h={h}. Find K_max."
        )
        return problem, steps, answer

    def _generate_de_broglie(self):
        h = random.randint(1, 80)
        momentum = random.randint(1, 40)
        wavelength = Fraction(h, momentum)
        steps = [
            step("QUANTUM_SETUP", "de_broglie", f"h={h}", f"p={momentum}"),
            step("QUANTUM_FORMULA", "lambda=h/p"),
            step("D", h, momentum, fraction_text(wavelength)),
        ]
        answer = f"lambda={fraction_text(wavelength)} m"
        problem = (
            f"A particle has momentum p={momentum} kg*m/s. Using h={h}, "
            "find its de Broglie wavelength."
        )
        return problem, steps, answer

    def _generate_compton(self):
        h = random.randint(1, 40)
        mass = random.randint(1, 20)
        c = random.randint(1, 20)
        one_minus_cos = Fraction(1, random.randint(1, 8))
        denominator = mass * c
        compton_factor = Fraction(h, denominator)
        shift = compton_factor * one_minus_cos
        steps = [
            step("QUANTUM_SETUP", "compton",
                 f"h={h}, m={mass}, c={c}",
                 f"one_minus_cos={fraction_text(one_minus_cos)}"),
            step("QUANTUM_FORMULA", "Delta_lambda=h/(m*c)*(1-cos(theta))"),
            step("M", mass, c, denominator),
            step("D", h, denominator, fraction_text(compton_factor)),
            step("M", fraction_text(compton_factor),
                 fraction_text(one_minus_cos), fraction_text(shift)),
        ]
        answer = f"Delta_lambda={fraction_text(shift)} m"
        problem = (
            f"In a Compton scattering setup, h={h}, particle mass m={mass}, "
            f"c={c}, and 1-cos(theta)={fraction_text(one_minus_cos)}. "
            "Find the wavelength shift Delta_lambda."
        )
        return problem, steps, answer
