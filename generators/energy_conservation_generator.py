import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class EnergyConservationGenerator(ProblemGenerator):
    """
    Work-energy theorem and mechanical energy conservation.

    Variants:
    - work_energy: W_net = delta K to find final speed
    - gravity_drop: mgh converts to kinetic energy

    Op-codes used:
    - ENERGY_SETUP: physical givens
    - ENERGY_FORMULA: energy relation
    - A / S / M / D / E / ROOT (established/shared): exact arithmetic
    - Z: requested speed or energy result
    """

    VARIANTS = ["work_energy", "gravity_drop"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "work_energy":
            problem, steps, answer = self._generate_work_energy()
        else:
            problem, steps, answer = self._generate_gravity_drop()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"energy_conservation_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_work_energy(self):
        mass = random.randint(1, 30)
        vi = random.randint(0, 20)
        vf = random.randint(vi + 1, vi + 25)
        vi_sq = vi ** 2
        vf_sq = vf ** 2
        delta_sq = vf_sq - vi_sq
        work = Fraction(mass * delta_sq, 2)
        two_work = 2 * work
        two_work_over_m = two_work / mass
        final_sq = vi_sq + two_work_over_m
        steps = [
            step("ENERGY_SETUP", "work_energy", f"m={mass}",
                 f"vi={vi}, W={fraction_text(work)}"),
            step("ENERGY_FORMULA", "vf^2=vi^2+2W/m"),
            step("E", vi, 2, vi_sq),
            step("M", 2, fraction_text(work), fraction_text(two_work)),
            step("D", fraction_text(two_work), mass,
                 fraction_text(two_work_over_m)),
            step("A", vi_sq, fraction_text(two_work_over_m),
                 fraction_text(final_sq)),
            step("ROOT", fraction_text(final_sq), vf),
        ]
        answer = f"vf={vf} m/s"
        problem = (
            f"A {mass} kg object starts at {vi} m/s and net work "
            f"{fraction_text(work)} J is done on it. Use the work-energy "
            "theorem to find the final speed."
        )
        return problem, steps, answer

    def _generate_gravity_drop(self):
        mass = random.randint(1, 30)
        r = random.randint(1, 12)
        g = 10
        height = 5 * r * r
        speed = 10 * r
        potential = mass * g * height
        two_g = 2 * g
        speed_sq = two_g * height
        steps = [
            step("ENERGY_SETUP", "gravity_drop", f"m={mass}",
                 f"h={height}, g={g}"),
            step("ENERGY_FORMULA", "mgh=1/2*m*v^2"),
            step("M", mass, g, mass * g),
            step("M", mass * g, height, potential),
            step("ENERGY_FORMULA", "v^2=2gh"),
            step("M", 2, g, two_g),
            step("M", two_g, height, speed_sq),
            step("ROOT", speed_sq, speed),
        ]
        answer = f"impact speed={speed} m/s; potential energy={potential} J"
        problem = (
            f"A {mass} kg object is dropped from height {height} m. Use "
            "g=10 m/s^2 and energy conservation to find impact speed and "
            "initial potential energy."
        )
        return problem, steps, answer
