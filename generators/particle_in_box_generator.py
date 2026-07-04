import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class ParticleInBoxGenerator(ProblemGenerator):
    """
    One-dimensional particle-in-a-box energies and transition wavelengths.

    Variants:
    - energy_level: E_n = n^2 h^2/(8mL^2)
    - transition_wavelength: lambda = hc/DeltaE

    Op-codes used:
    - BOX_SETUP: quantum number and supplied constants
    - BOX_FORMULA: particle-in-box relation
    - S / M / D / E (established/shared): exact arithmetic
    - Z: energy level or transition wavelength
    """

    VARIANTS = ["energy_level", "transition_wavelength"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "energy_level":
            problem, steps, answer = self._generate_energy_level()
        else:
            problem, steps, answer = self._generate_transition()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"particle_in_box_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_energy_level(self):
        n = random.randint(1, 8)
        h = random.randint(1, 12)
        mass = random.randint(1, 12)
        length = random.randint(1, 12)
        n_sq = n ** 2
        h_sq = h ** 2
        numerator = n_sq * h_sq
        length_sq = length ** 2
        eight_m = 8 * mass
        denominator = eight_m * length_sq
        energy = Fraction(numerator, denominator)
        steps = [
            step("BOX_SETUP", "energy_level",
                 f"n={n}, h={h}", f"m={mass}, L={length}"),
            step("BOX_FORMULA", "E_n=n^2*h^2/(8*m*L^2)"),
            step("E", n, 2, n_sq),
            step("E", h, 2, h_sq),
            step("M", n_sq, h_sq, numerator),
            step("E", length, 2, length_sq),
            step("M", 8, mass, eight_m),
            step("M", eight_m, length_sq, denominator),
            step("D", numerator, denominator, fraction_text(energy)),
        ]
        answer = f"E_{n}={fraction_text(energy)} J"
        problem = (
            f"A particle in a 1D box has quantum number n={n}, h={h}, "
            f"mass m={mass}, and box length L={length}. Find E_n."
        )
        return problem, steps, answer

    def _generate_transition(self):
        n_low = random.randint(1, 5)
        n_high = random.randint(n_low + 1, n_low + 6)
        h = random.randint(1, 12)
        c = random.randint(1, 20)
        mass = random.randint(1, 12)
        length = random.randint(1, 12)
        n_low_sq = n_low ** 2
        n_high_sq = n_high ** 2
        delta_n_sq = n_high_sq - n_low_sq
        length_sq = length ** 2
        eight_m = 8 * mass
        numerator_left = eight_m * length_sq
        numerator = numerator_left * c
        denominator = delta_n_sq * h
        wavelength = Fraction(numerator, denominator)
        steps = [
            step("BOX_SETUP", "transition_wavelength",
                 f"n_low={n_low}, n_high={n_high}", f"h={h}, c={c}"),
            step("BOX_SETUP", f"m={mass}, L={length}"),
            step("BOX_FORMULA", "lambda=8*m*L^2*c/((n_high^2-n_low^2)*h)"),
            step("E", n_low, 2, n_low_sq),
            step("E", n_high, 2, n_high_sq),
            step("S", n_high_sq, n_low_sq, delta_n_sq),
            step("E", length, 2, length_sq),
            step("M", 8, mass, eight_m),
            step("M", eight_m, length_sq, numerator_left),
            step("M", numerator_left, c, numerator),
            step("M", delta_n_sq, h, denominator),
            step("D", numerator, denominator, fraction_text(wavelength)),
        ]
        answer = f"lambda={fraction_text(wavelength)} m"
        problem = (
            f"A particle in a 1D box transitions from n={n_high} to n={n_low}. "
            f"Use h={h}, c={c}, mass m={mass}, and length L={length} to "
            "find the emitted photon wavelength."
        )
        return problem, steps, answer
