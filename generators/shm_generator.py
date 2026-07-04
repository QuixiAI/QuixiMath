import random
from fractions import Fraction

from base_generator import ProblemGenerator
from generators.arc_sector_generator import pi_txt
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class SHMGenerator(ProblemGenerator):
    """
    Simple harmonic motion: angular frequency, period, and energy exchange.

    Variants:
    - mass_spring_energy: omega, period, K, and U for a spring oscillator
    - pendulum_period: small-angle pendulum omega and period

    Op-codes used:
    - SHM_SETUP: oscillator givens
    - SHM_FORMULA: SHM relation being applied
    - PI_MULT: exact coefficient times π
    - A / S / M / D / E / ROOT (established/shared): exact arithmetic
    - CHECK: energy verification
    - Z: requested SHM quantities
    """

    VARIANTS = ["mass_spring_energy", "pendulum_period"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "mass_spring_energy":
            problem, steps, answer = self._generate_mass_spring_energy()
        else:
            problem, steps, answer = self._generate_pendulum_period()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"shm_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_mass_spring_energy(self):
        mass = random.randint(1, 20)
        omega = random.randint(1, 10)
        spring_k = mass * omega ** 2
        amplitude = random.randint(2, 12)
        displacement = random.randint(1, amplitude - 1)
        omega_sq = omega ** 2
        period_coeff = Fraction(2, omega)
        period = pi_txt(period_coeff)
        amplitude_sq = amplitude ** 2
        spring_amp = spring_k * amplitude_sq
        total_energy = Fraction(spring_amp, 2)
        displacement_sq = displacement ** 2
        spring_disp = spring_k * displacement_sq
        potential_energy = Fraction(spring_disp, 2)
        kinetic_energy = total_energy - potential_energy
        energy_sum = kinetic_energy + potential_energy
        steps = [
            step("SHM_SETUP", "mass_spring_energy",
                 f"m={mass}, k={spring_k}", f"A={amplitude}, x={displacement}"),
            step("SHM_FORMULA", "omega^2=k/m"),
            step("D", spring_k, mass, omega_sq),
            step("ROOT", omega_sq, omega),
            step("SHM_FORMULA", "T=2π/omega"),
            step("D", 2, omega, fraction_text(period_coeff)),
            step("PI_MULT", fraction_text(period_coeff), "π", period),
            step("SHM_FORMULA", "E_total=1/2*k*A^2"),
            step("E", amplitude, 2, amplitude_sq),
            step("M", spring_k, amplitude_sq, spring_amp),
            step("D", spring_amp, 2, fraction_text(total_energy)),
            step("SHM_FORMULA", "U=1/2*k*x^2"),
            step("E", displacement, 2, displacement_sq),
            step("M", spring_k, displacement_sq, spring_disp),
            step("D", spring_disp, 2, fraction_text(potential_energy)),
            step("S", fraction_text(total_energy),
                 fraction_text(potential_energy), fraction_text(kinetic_energy)),
            step("A", fraction_text(kinetic_energy),
                 fraction_text(potential_energy), fraction_text(energy_sum)),
            step("CHECK", "K+U", fraction_text(energy_sum),
                 f"E {fraction_text(total_energy)}"),
        ]
        answer = (
            f"omega={omega} rad/s; T={period} s; "
            f"K={fraction_text(kinetic_energy)} J; "
            f"U={fraction_text(potential_energy)} J"
        )
        problem = (
            f"A mass-spring oscillator has m={mass} kg, k={spring_k} N/m, "
            f"amplitude A={amplitude} m, and is at displacement "
            f"x={displacement} m. Find omega, period, kinetic energy, and "
            "potential energy."
        )
        return problem, steps, answer

    def _generate_pendulum_period(self):
        omega = random.choice([1, 2, 5, 10])
        g = 10
        length = Fraction(g, omega ** 2)
        omega_sq = omega ** 2
        period_coeff = Fraction(2, omega)
        period = pi_txt(period_coeff)
        steps = [
            step("SHM_SETUP", "pendulum_period", f"g={g}",
                 f"L={fraction_text(length)}"),
            step("SHM_FORMULA", "omega^2=g/L"),
            step("D", g, fraction_text(length), omega_sq),
            step("ROOT", omega_sq, omega),
            step("SHM_FORMULA", "T=2π/omega"),
            step("D", 2, omega, fraction_text(period_coeff)),
            step("PI_MULT", fraction_text(period_coeff), "π", period),
        ]
        answer = f"omega={omega} rad/s; T={period} s"
        problem = (
            f"A small-angle pendulum uses g=10 m/s^2 and length "
            f"L={fraction_text(length)} m. Find angular frequency and period."
        )
        return problem, steps, answer
