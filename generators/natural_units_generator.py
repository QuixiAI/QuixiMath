import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def random_scale():
    return Fraction(random.randint(1, 30), random.randint(1, 30))


class NaturalUnitsGenerator(ProblemGenerator):
    """
    Natural-unit conversion chains with hbar = c = 1.

    Energy and mass both use GeV. Length and time both use GeV^-1, with
    E*L = 1 and c=1 making t=L for light-crossing scales.

    Op-codes used:
    - NATURAL_SETUP: starting quantity and hbar=c=1 convention
    - UNIT_RULE: dimensional-analysis rule being applied
    - M / D (established/shared): exact arithmetic and reciprocal checks
    - Z: requested converted quantities with units
    """

    VARIANTS = ["energy", "mass", "length", "time"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "energy":
            problem, steps, answer = self._generate_energy()
        elif variant == "mass":
            problem, steps, answer = self._generate_mass()
        elif variant == "length":
            problem, steps, answer = self._generate_length()
        else:
            problem, steps, answer = self._generate_time()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"natural_units_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_energy(self):
        energy = Fraction(random.randint(1, 30), 1)
        mass = energy
        length = Fraction(1, 1) / energy
        time = length
        steps = [
            step("NATURAL_SETUP", "energy", "hbar=1,c=1",
                 f"E={fraction_text(energy)} GeV"),
            step("UNIT_RULE", "c=1", "m=E", "mass uses GeV"),
            step("M", fraction_text(energy), 1, fraction_text(mass)),
            step("UNIT_RULE", "hbar=1", "L=1/E", "GeV^-1"),
            step("D", 1, fraction_text(energy), fraction_text(length)),
            step("UNIT_RULE", "c=1", "t=L", "GeV^-1"),
            step("M", fraction_text(length), 1, fraction_text(time)),
            step("M", fraction_text(energy), fraction_text(length), 1),
        ]
        answer = (
            f"m = {fraction_text(mass)} GeV, "
            f"L = {fraction_text(length)} GeV^-1, "
            f"t = {fraction_text(time)} GeV^-1"
        )
        problem = (
            "In natural units with hbar=c=1, a particle has energy "
            f"E={fraction_text(energy)} GeV. Compute its mass m, length "
            "scale L=1/E, and time scale t=L."
        )
        return problem, steps, answer

    def _generate_mass(self):
        mass = Fraction(random.randint(1, 30), 1)
        energy = mass
        length = Fraction(1, 1) / energy
        time = length
        steps = [
            step("NATURAL_SETUP", "mass", "hbar=1,c=1",
                 f"m={fraction_text(mass)} GeV"),
            step("UNIT_RULE", "c=1", "E=m", "energy uses GeV"),
            step("M", fraction_text(mass), 1, fraction_text(energy)),
            step("UNIT_RULE", "hbar=1", "L=1/E", "GeV^-1"),
            step("D", 1, fraction_text(energy), fraction_text(length)),
            step("UNIT_RULE", "c=1", "t=L", "GeV^-1"),
            step("M", fraction_text(length), 1, fraction_text(time)),
            step("M", fraction_text(energy), fraction_text(length), 1),
        ]
        answer = (
            f"E = {fraction_text(energy)} GeV, "
            f"L = {fraction_text(length)} GeV^-1, "
            f"t = {fraction_text(time)} GeV^-1"
        )
        problem = (
            "In natural units with hbar=c=1, a particle has mass "
            f"m={fraction_text(mass)} GeV. Compute its energy E, length "
            "scale L=1/E, and time scale t=L."
        )
        return problem, steps, answer

    def _generate_length(self):
        length = random_scale()
        energy = Fraction(1, 1) / length
        mass = energy
        time = length
        steps = [
            step("NATURAL_SETUP", "length", "hbar=1,c=1",
                 f"L={fraction_text(length)} GeV^-1"),
            step("UNIT_RULE", "hbar=1", "E=1/L", "GeV"),
            step("D", 1, fraction_text(length), fraction_text(energy)),
            step("UNIT_RULE", "c=1", "m=E", "mass uses GeV"),
            step("M", fraction_text(energy), 1, fraction_text(mass)),
            step("UNIT_RULE", "c=1", "t=L", "GeV^-1"),
            step("M", fraction_text(length), 1, fraction_text(time)),
            step("M", fraction_text(energy), fraction_text(length), 1),
        ]
        answer = (
            f"E = {fraction_text(energy)} GeV, "
            f"m = {fraction_text(mass)} GeV, "
            f"t = {fraction_text(time)} GeV^-1"
        )
        problem = (
            "In natural units with hbar=c=1, a length scale "
            f"L={fraction_text(length)} GeV^-1 is given. Compute "
            "E=1/L, mass m=E, and time scale t=L."
        )
        return problem, steps, answer

    def _generate_time(self):
        time = random_scale()
        length = time
        energy = Fraction(1, 1) / length
        mass = energy
        steps = [
            step("NATURAL_SETUP", "time", "hbar=1,c=1",
                 f"t={fraction_text(time)} GeV^-1"),
            step("UNIT_RULE", "c=1", "L=t", "GeV^-1"),
            step("M", fraction_text(time), 1, fraction_text(length)),
            step("UNIT_RULE", "hbar=1", "E=1/L", "GeV"),
            step("D", 1, fraction_text(length), fraction_text(energy)),
            step("UNIT_RULE", "c=1", "m=E", "mass uses GeV"),
            step("M", fraction_text(energy), 1, fraction_text(mass)),
            step("M", fraction_text(energy), fraction_text(length), 1),
        ]
        answer = (
            f"L = {fraction_text(length)} GeV^-1, "
            f"E = {fraction_text(energy)} GeV, "
            f"m = {fraction_text(mass)} GeV"
        )
        problem = (
            "In natural units with hbar=c=1, a time scale "
            f"t={fraction_text(time)} GeV^-1 is given. Compute "
            "length L=t, energy E=1/t, and mass m=E."
        )
        return problem, steps, answer
