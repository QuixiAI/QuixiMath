import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def neg_coeff_times(coeff, body):
    coeff = Fraction(coeff)
    if coeff == 1:
        return f"-{body}"
    if coeff.denominator == 1:
        return f"-{coeff.numerator}*{body}"
    return f"-({coeff})*{body}"


def momentum_over(momentum, denom):
    if denom == 1:
        return momentum
    return f"{momentum}/{denom}"


class HamiltonianGenerator(ProblemGenerator):
    """
    Hamilton's equations for mass-spring, pendulum, and Atwood systems.

    Variants:
    - mass_spring: H = p_x^2/(2m) + 1/2 kx^2
    - pendulum: H = p_theta^2/(2mL^2) + mgL(1-cos theta)
    - atwood: H = p_y^2/(2(m1+m2)) + (m1-m2)gy

    Op-codes used:
    - HAM_SETUP: canonical coordinate, momentum, and givens
    - HAMILTONIAN: construct H
    - PARTIAL: symbolic partial derivative
    - HAM_EQ: Hamilton equation or consequence
    - A / S / M / D / E (established/shared): exact coefficient arithmetic
    - Z: Hamilton equations and acceleration where useful
    """

    VARIANTS = ["mass_spring", "pendulum", "atwood"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "mass_spring":
            problem, steps, answer = self._generate_mass_spring()
        elif variant == "pendulum":
            problem, steps, answer = self._generate_pendulum()
        else:
            problem, steps, answer = self._generate_atwood()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"hamiltonian_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_mass_spring(self):
        mass = random.randint(1, 12)
        spring_k = random.randint(1, 60)
        xdot = momentum_over("p_x", mass)
        p_dot = neg_coeff_times(spring_k, "x")
        acceleration_coeff = Fraction(spring_k, mass)
        acceleration = neg_coeff_times(acceleration_coeff, "x")
        steps = [
            step("HAM_SETUP", "mass_spring", f"m={mass}, k={spring_k}",
                 "q=x, p=p_x"),
            step("HAMILTONIAN", "H=p_x^2/(2m)+1/2*k*x^2"),
            step("PARTIAL", "dH/dp_x", "p_x/m"),
            step("HAM_EQ", "xdot=dH/dp_x", f"xdot={xdot}"),
            step("PARTIAL", "dH/dx", "k*x"),
            step("HAM_EQ", "p_xdot=-dH/dx", f"p_xdot={p_dot}"),
            step("D", spring_k, mass, fraction_text(acceleration_coeff)),
            step("HAM_EQ", "xddot=p_xdot/m", f"xddot={acceleration}"),
        ]
        answer = f"xdot={xdot}; p_xdot={p_dot}; xddot={acceleration}"
        problem = (
            f"For a mass-spring Hamiltonian with mass m={mass} and spring "
            f"constant k={spring_k}, write H and Hamilton's equations."
        )
        return problem, steps, answer

    def _generate_pendulum(self):
        mass = random.randint(1, 12)
        length = random.randint(1, 10)
        g = 10
        length_sq = length ** 2
        inertia_coeff = mass * length_sq
        mg = mass * g
        gravity_coeff = mg * length
        theta_dot = momentum_over("p_theta", inertia_coeff)
        p_dot = neg_coeff_times(gravity_coeff, "sin(theta)")
        acceleration_coeff = Fraction(gravity_coeff, inertia_coeff)
        acceleration = neg_coeff_times(acceleration_coeff, "sin(theta)")
        steps = [
            step("HAM_SETUP", "pendulum", f"m={mass}, L={length}",
                 f"g={g}, q=theta"),
            step("E", length, 2, length_sq),
            step("M", mass, length_sq, inertia_coeff),
            step("M", mass, g, mg),
            step("M", mg, length, gravity_coeff),
            step("HAMILTONIAN",
                 "H=p_theta^2/(2mL^2)+mgL*(1-cos(theta))"),
            step("PARTIAL", "dH/dp_theta", "p_theta/(mL^2)"),
            step("HAM_EQ", "thetadot=dH/dp_theta",
                 f"thetadot={theta_dot}"),
            step("PARTIAL", "dH/dtheta", "mgL*sin(theta)"),
            step("HAM_EQ", "p_thetadot=-dH/dtheta",
                 f"p_thetadot={p_dot}"),
            step("D", gravity_coeff, inertia_coeff,
                 fraction_text(acceleration_coeff)),
            step("HAM_EQ", "thetaddot=p_thetadot/(mL^2)",
                 f"thetaddot={acceleration}"),
        ]
        answer = (
            f"thetadot={theta_dot}; p_thetadot={p_dot}; "
            f"thetaddot={acceleration}"
        )
        problem = (
            f"For a pendulum Hamiltonian with mass m={mass}, length "
            f"L={length}, and g=10, write H and Hamilton's equations."
        )
        return problem, steps, answer

    def _generate_atwood(self):
        m1 = random.randint(1, 20)
        m2 = random.randint(m1 + 1, m1 + 25)
        g = 10
        total_mass = m1 + m2
        potential_diff = m1 - m2
        potential_coeff = potential_diff * g
        driving_diff = m2 - m1
        driving_force = driving_diff * g
        acceleration = Fraction(driving_force, total_mass)
        ydot = momentum_over("p_y", total_mass)
        steps = [
            step("HAM_SETUP", "atwood", f"m1={m1}, m2={m2}",
                 f"g={g}, q=y, p=p_y"),
            step("A", m1, m2, total_mass),
            step("S", m1, m2, potential_diff),
            step("M", potential_diff, g, potential_coeff),
            step("S", m2, m1, driving_diff),
            step("M", driving_diff, g, driving_force),
            step("HAMILTONIAN", "H=p_y^2/(2(m1+m2))+(m1-m2)g*y"),
            step("PARTIAL", "dH/dp_y", "p_y/(m1+m2)"),
            step("HAM_EQ", "ydot=dH/dp_y", f"ydot={ydot}"),
            step("PARTIAL", "dH/dy", "(m1-m2)g"),
            step("HAM_EQ", "p_ydot=-dH/dy", f"p_ydot={driving_force}"),
            step("D", driving_force, total_mass, fraction_text(acceleration)),
            step("HAM_EQ", "yddot=p_ydot/(m1+m2)",
                 f"yddot={fraction_text(acceleration)}"),
        ]
        answer = (
            f"ydot={ydot}; p_ydot={driving_force}; "
            f"yddot={fraction_text(acceleration)} m/s^2 downward for m2"
        )
        problem = (
            f"For an Atwood Hamiltonian with masses m1={m1} and m2={m2}, "
            "m2 heavier, and g=10, use y downward for m2. Write H and "
            "Hamilton's equations."
        )
        return problem, steps, answer
