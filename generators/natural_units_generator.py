import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


ENERGY_UNITS = ["GeV", "MeV", "TeV", "keV", "eV"]

SUBJECTS = [
    "a particle",
    "a resonance",
    "a bound state",
    "an excited state",
    "a heavy mode",
    "a test particle",
    "a field quantum",
    "a quasiparticle",
    "a scalar excitation",
    "a wave packet",
    "a collider fragment",
    "a lattice mode",
]

ENERGY_PHRASINGS = [
    "In natural units with hbar=c=1, {subject} has energy E={value} {unit}. "
    "Compute its mass m, length scale L=1/E, and time scale t=L.",
    "Working with hbar=c=1, {subject} carries energy E={value} {unit}. Give "
    "the mass m, the length scale L=1/E, and the time scale t=L.",
    "Set hbar=c=1. If {subject} has energy E={value} {unit}, find the mass m, "
    "the length scale L=1/E, and the time scale t=L.",
    "Natural units (hbar=c=1) are in use and {subject} is measured at energy "
    "E={value} {unit}. Report m, L=1/E, and t=L.",
    "Using hbar=c=1, convert the energy E={value} {unit} of {subject} into a "
    "mass m, a length scale L=1/E, and a time scale t=L.",
]

MASS_PHRASINGS = [
    "In natural units with hbar=c=1, {subject} has mass m={value} {unit}. "
    "Compute its energy E, length scale L=1/E, and time scale t=L.",
    "Working with hbar=c=1, {subject} has rest mass m={value} {unit}. Give "
    "the energy E, the length scale L=1/E, and the time scale t=L.",
    "Set hbar=c=1. If {subject} has mass m={value} {unit}, find the energy E, "
    "the length scale L=1/E, and the time scale t=L.",
    "Natural units (hbar=c=1) are in use and {subject} has mass m={value} "
    "{unit}. Report E, L=1/E, and t=L.",
    "Using hbar=c=1, convert the mass m={value} {unit} of {subject} into an "
    "energy E, a length scale L=1/E, and a time scale t=L.",
]

LENGTH_PHRASINGS = [
    "In natural units with hbar=c=1, a length scale L={value} {iunit} is "
    "given. Compute E=1/L, mass m=E, and time scale t=L.",
    "Working with hbar=c=1, {subject} has size L={value} {iunit}. Give E=1/L, "
    "the mass m=E, and the time scale t=L.",
    "Set hbar=c=1. A length scale L={value} {iunit} describes {subject}; find "
    "E=1/L, m=E, and t=L.",
    "Natural units (hbar=c=1) are in use and {subject} spans L={value} "
    "{iunit}. Report E=1/L, m=E, and t=L.",
    "Using hbar=c=1, convert the length scale L={value} {iunit} of {subject} "
    "into an energy E=1/L, a mass m=E, and a time t=L.",
]

TIME_PHRASINGS = [
    "In natural units with hbar=c=1, a time scale t={value} {iunit} is given. "
    "Compute length L=t, energy E=1/t, and mass m=E.",
    "Working with hbar=c=1, {subject} lives for t={value} {iunit}. Give the "
    "length L=t, the energy E=1/t, and the mass m=E.",
    "Set hbar=c=1. A time scale t={value} {iunit} is attached to {subject}; "
    "find L=t, E=1/t, and m=E.",
    "Natural units (hbar=c=1) are in use and {subject} evolves on the time "
    "scale t={value} {iunit}. Report L=t, E=1/t, and m=E.",
    "Using hbar=c=1, convert the time scale t={value} {iunit} of {subject} "
    "into a length L=t, an energy E=1/t, and a mass m=E.",
]

CROSS_SECTION_PHRASINGS = [
    "In natural units with hbar=c=1, {subject} has energy E={value} {unit}. "
    "Compute the length scale L=1/E and the geometric cross section "
    "sigma=L^2.",
    "Working with hbar=c=1, {subject} is probed at energy E={value} {unit}. "
    "Give L=1/E and sigma=L^2.",
    "Set hbar=c=1. At energy E={value} {unit}, {subject} has length scale "
    "L=1/E; find L and the cross section sigma=L^2.",
    "Natural units (hbar=c=1) are in use and {subject} scatters at energy "
    "E={value} {unit}. Report L=1/E and sigma=L^2.",
    "Using hbar=c=1, turn the energy E={value} {unit} of {subject} into a "
    "length scale L=1/E and a cross section sigma=L^2.",
]


def fraction_text(value):
    return str(Fraction(value))


def random_scale(num_hi=40, den_hi=40):
    return Fraction(random.randint(1, num_hi), random.randint(1, den_hi))


def random_energy():
    return Fraction(random.randint(1, 80), random.randint(1, 16))


class NaturalUnitsGenerator(ProblemGenerator):
    """
    Natural-unit conversion chains with hbar = c = 1.

    Energy and mass both use the chosen energy unit (eV through TeV); length
    and time both use its inverse, with E*L = 1 and c=1 making t=L for
    light-crossing scales. Cross sections pick up the inverse square.

    Variants: energy, mass, length, time, cross_section.

    Op-codes used:
    - NATURAL_SETUP: starting quantity and hbar=c=1 convention
    - UNIT_RULE: dimensional-analysis rule being applied
    - M / D / E (established/shared): exact arithmetic and reciprocal checks
    - Z: requested converted quantities with units
    """

    VARIANTS = ["energy", "mass", "length", "time", "cross_section"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        unit = random.choice(ENERGY_UNITS)
        subject = random.choice(SUBJECTS)
        context = dict(unit=unit, iunit=f"{unit}^-1", subject=subject)
        builder = {
            "energy": self._generate_energy,
            "mass": self._generate_mass,
            "length": self._generate_length,
            "time": self._generate_time,
            "cross_section": self._generate_cross_section,
        }[variant]
        problem, steps, answer = builder(context)
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"natural_units_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_energy(self, ctx):
        unit, iunit = ctx["unit"], ctx["iunit"]
        energy = random_energy()
        mass = energy
        length = Fraction(1, 1) / energy
        time = length
        steps = [
            step("NATURAL_SETUP", "energy", "hbar=1,c=1",
                 f"E={fraction_text(energy)} {unit}"),
            step("UNIT_RULE", "c=1", "m=E", f"mass uses {unit}"),
            step("M", fraction_text(energy), 1, fraction_text(mass)),
            step("UNIT_RULE", "hbar=1", "L=1/E", iunit),
            step("D", 1, fraction_text(energy), fraction_text(length)),
            step("UNIT_RULE", "c=1", "t=L", iunit),
            step("M", fraction_text(length), 1, fraction_text(time)),
            step("M", fraction_text(energy), fraction_text(length), 1),
        ]
        answer = (
            f"m = {fraction_text(mass)} {unit}, "
            f"L = {fraction_text(length)} {iunit}, "
            f"t = {fraction_text(time)} {iunit}"
        )
        problem = random.choice(ENERGY_PHRASINGS).format(
            value=fraction_text(energy), **ctx)
        return problem, steps, answer

    def _generate_mass(self, ctx):
        unit, iunit = ctx["unit"], ctx["iunit"]
        mass = random_energy()
        energy = mass
        length = Fraction(1, 1) / energy
        time = length
        steps = [
            step("NATURAL_SETUP", "mass", "hbar=1,c=1",
                 f"m={fraction_text(mass)} {unit}"),
            step("UNIT_RULE", "c=1", "E=m", f"energy uses {unit}"),
            step("M", fraction_text(mass), 1, fraction_text(energy)),
            step("UNIT_RULE", "hbar=1", "L=1/E", iunit),
            step("D", 1, fraction_text(energy), fraction_text(length)),
            step("UNIT_RULE", "c=1", "t=L", iunit),
            step("M", fraction_text(length), 1, fraction_text(time)),
            step("M", fraction_text(energy), fraction_text(length), 1),
        ]
        answer = (
            f"E = {fraction_text(energy)} {unit}, "
            f"L = {fraction_text(length)} {iunit}, "
            f"t = {fraction_text(time)} {iunit}"
        )
        problem = random.choice(MASS_PHRASINGS).format(
            value=fraction_text(mass), **ctx)
        return problem, steps, answer

    def _generate_length(self, ctx):
        unit, iunit = ctx["unit"], ctx["iunit"]
        length = random_scale()
        energy = Fraction(1, 1) / length
        mass = energy
        time = length
        steps = [
            step("NATURAL_SETUP", "length", "hbar=1,c=1",
                 f"L={fraction_text(length)} {iunit}"),
            step("UNIT_RULE", "hbar=1", "E=1/L", unit),
            step("D", 1, fraction_text(length), fraction_text(energy)),
            step("UNIT_RULE", "c=1", "m=E", f"mass uses {unit}"),
            step("M", fraction_text(energy), 1, fraction_text(mass)),
            step("UNIT_RULE", "c=1", "t=L", iunit),
            step("M", fraction_text(length), 1, fraction_text(time)),
            step("M", fraction_text(energy), fraction_text(length), 1),
        ]
        answer = (
            f"E = {fraction_text(energy)} {unit}, "
            f"m = {fraction_text(mass)} {unit}, "
            f"t = {fraction_text(time)} {iunit}"
        )
        problem = random.choice(LENGTH_PHRASINGS).format(
            value=fraction_text(length), **ctx)
        return problem, steps, answer

    def _generate_time(self, ctx):
        unit, iunit = ctx["unit"], ctx["iunit"]
        time = random_scale()
        length = time
        energy = Fraction(1, 1) / length
        mass = energy
        steps = [
            step("NATURAL_SETUP", "time", "hbar=1,c=1",
                 f"t={fraction_text(time)} {iunit}"),
            step("UNIT_RULE", "c=1", "L=t", iunit),
            step("M", fraction_text(time), 1, fraction_text(length)),
            step("UNIT_RULE", "hbar=1", "E=1/L", unit),
            step("D", 1, fraction_text(length), fraction_text(energy)),
            step("UNIT_RULE", "c=1", "m=E", f"mass uses {unit}"),
            step("M", fraction_text(energy), 1, fraction_text(mass)),
            step("M", fraction_text(energy), fraction_text(length), 1),
        ]
        answer = (
            f"L = {fraction_text(length)} {iunit}, "
            f"E = {fraction_text(energy)} {unit}, "
            f"m = {fraction_text(mass)} {unit}"
        )
        problem = random.choice(TIME_PHRASINGS).format(
            value=fraction_text(time), **ctx)
        return problem, steps, answer

    def _generate_cross_section(self, ctx):
        unit, iunit = ctx["unit"], ctx["iunit"]
        sq_unit = f"{unit}^-2"
        energy = random_energy()
        length = Fraction(1, 1) / energy
        sigma = length ** 2
        steps = [
            step("NATURAL_SETUP", "cross section", "hbar=1,c=1",
                 f"E={fraction_text(energy)} {unit}"),
            step("UNIT_RULE", "hbar=1", "L=1/E", iunit),
            step("D", 1, fraction_text(energy), fraction_text(length)),
            step("UNIT_RULE", "area", "sigma=L^2", sq_unit),
            step("E", fraction_text(length), 2, fraction_text(sigma)),
            step("M", fraction_text(sigma), fraction_text(energy ** 2), 1),
        ]
        answer = (
            f"L = {fraction_text(length)} {iunit}, "
            f"sigma = {fraction_text(sigma)} {sq_unit}"
        )
        problem = random.choice(CROSS_SECTION_PHRASINGS).format(
            value=fraction_text(energy), **ctx)
        return problem, steps, answer
