import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


PLACES = [
    "accelerator lab", "university laboratory", "simulation center",
    "research station", "physics classroom", "detector facility",
    "computing lab", "observatory", "engineering institute",
    "particle laboratory", "training center", "science museum",
    "modeling group", "technical college", "prototype facility",
    "measurement lab", "theory group", "instrument center",
    "research institute", "analysis laboratory",
]

CONTEXTS = [
    "Simulation run {run} was prepared at the {place}.",
    "The {place} recorded model {run}.",
    "Laboratory run {run} comes from the {place}.",
    "Analysis case {run} was supplied by the {place}.",
]


def fraction_text(value):
    return str(Fraction(value))


def context_text():
    return random.choice(CONTEXTS).format(
        run=random.randint(100, 9999), place=random.choice(PLACES))


def proper_velocity():
    """Return a hand-friendly exact speed strictly between -1 and 1."""
    denominator = random.randint(2, 15)
    numerator = random.randint(-(denominator - 1), denominator - 1)
    return Fraction(numerator, denominator)


def mass_shell_triple():
    """Construct a scaled Pythagorean triple using Euclid's formula."""
    while True:
        outer = random.randint(2, 10)
        inner = random.randint(1, outer - 1)
        if math.gcd(outer, inner) == 1 and (outer - inner) % 2 == 1:
            break
    scale = random.randint(1, 10)
    leg_a = scale * (outer * outer - inner * inner)
    leg_b = scale * (2 * outer * inner)
    hypotenuse = scale * (outer * outer + inner * inner)
    if random.choice([False, True]):
        leg_a, leg_b = leg_b, leg_a
    return leg_a, leg_b, hypotenuse


class RelativisticEnergyGenerator(ProblemGenerator):
    """
    Relativistic rest energy, mass-shell energy, and velocity addition.

    Variants:
    - rest_energy: E=m*c^2.
    - energy_momentum: E^2=p^2+m^2 in c=1 units.
    - velocity_addition: w=(u+v)/(1+uv) in c=1 units.

    Op-codes used:
    - REL_ENERGY_SETUP / REL_ENERGY_FORMULA
    - A / M / D / E / ROOT (established/shared): exact arithmetic
    - Z: rest energy, total energy, or composed velocity
    """

    VARIANTS = ["rest_energy", "energy_momentum", "velocity_addition"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        context = context_text()
        if variant == "rest_energy":
            problem, steps, answer = self._generate_rest_energy(context)
        elif variant == "energy_momentum":
            problem, steps, answer = self._generate_energy_momentum(context)
        else:
            problem, steps, answer = self._generate_velocity_addition(context)
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"relativistic_energy_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_rest_energy(self, context):
        mass = random.randint(1, 100)
        c = random.randint(2, 50)
        c_sq = c ** 2
        energy = mass * c_sq
        steps = [
            step("REL_ENERGY_SETUP", "rest_energy", f"m={mass}", f"c={c}"),
            step("REL_ENERGY_FORMULA", "E=m*c^2"),
            step("E", c, 2, c_sq),
            step("M", mass, c_sq, energy),
        ]
        answer = f"E={energy} J"
        problem = (
            f"{context} Using E=m*c^2, find the rest energy for mass "
            f"m={mass} kg "
            f"and c={c} m/s."
        )
        return problem, steps, answer

    def _generate_energy_momentum(self, context):
        momentum, mass, energy = mass_shell_triple()
        p_sq = momentum ** 2
        m_sq = mass ** 2
        e_sq = p_sq + m_sq
        steps = [
            step("REL_ENERGY_SETUP", "energy_momentum", "c=1",
                 f"p={momentum}, m={mass}"),
            step("REL_ENERGY_FORMULA", "E=sqrt(p^2+m^2)"),
            step("E", momentum, 2, p_sq),
            step("E", mass, 2, m_sq),
            step("A", p_sq, m_sq, e_sq),
            step("ROOT", f"sqrt({e_sq})", energy),
        ]
        answer = f"E={energy}"
        problem = (
            f"{context} In c=1 units, a particle has momentum p={momentum} and "
            f"mass m={mass}. Find E from E^2=p^2+m^2."
        )
        return problem, steps, answer

    def _generate_velocity_addition(self, context):
        u = proper_velocity()
        v = proper_velocity()
        denominator = 1 + u * v
        numerator = u + v
        product = u * v
        velocity = numerator / denominator
        steps = [
            step("REL_ENERGY_SETUP", "velocity_addition",
                 f"u={fraction_text(u)}", f"v={fraction_text(v)}"),
            step("REL_ENERGY_FORMULA", "w=(u+v)/(1+u*v), c=1"),
            step("A", fraction_text(u), fraction_text(v),
                 fraction_text(numerator)),
            step("M", fraction_text(u), fraction_text(v),
                 fraction_text(product)),
            step("A", 1, fraction_text(product), fraction_text(denominator)),
            step("D", fraction_text(numerator), fraction_text(denominator),
                 fraction_text(velocity)),
        ]
        answer = f"w={fraction_text(velocity)}"
        problem = (
            f"{context} In c=1 units, velocities u={fraction_text(u)} and "
            f"v={fraction_text(v)} are collinear. Compute the relativistic "
            "velocity sum w."
        )
        return problem, steps, answer
