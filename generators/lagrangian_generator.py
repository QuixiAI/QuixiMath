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


class LagrangianGenerator(ProblemGenerator):
    """
    Build L = T - V and apply the Euler-Lagrange equation.

    Variants:
    - mass_spring: one-dimensional spring oscillator
    - pendulum: simple pendulum in theta
    - atwood: Atwood machine with one generalized coordinate

    Op-codes used:
    - LAG_SETUP: generalized coordinate and givens
    - ENERGY_TERM: kinetic or potential energy term
    - LAGRANGIAN: construct L = T - V
    - PARTIAL: symbolic partial derivative
    - TIME_DERIV: time derivative of momentum-like partial
    - EL_EQUATION: Euler-Lagrange equation
    - EL_SOLVE: isolated equation of motion
    - A / S / M / D / E (established/shared): exact coefficient arithmetic
    - Z: equation of motion
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
            operation=f"lagrangian_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_mass_spring(self):
        mass = random.randint(1, 12)
        spring_k = random.randint(1, 60)
        coeff = Fraction(spring_k, mass)
        acceleration = neg_coeff_times(coeff, "x")
        steps = [
            step("LAG_SETUP", "mass_spring", f"m={mass}, k={spring_k}",
                 "q=x"),
            step("ENERGY_TERM", "T=1/2*m*xdot^2"),
            step("ENERGY_TERM", "V=1/2*k*x^2"),
            step("LAGRANGIAN", "L=T-V",
                 "1/2*m*xdot^2 - 1/2*k*x^2"),
            step("PARTIAL", "dL/dxdot", "m*xdot"),
            step("TIME_DERIV", "d/dt(m*xdot)", "m*xddot"),
            step("PARTIAL", "dL/dx", "-k*x"),
            step("EL_EQUATION", "d/dt(dL/dxdot)-dL/dx=0"),
            step("EL_EQUATION", "m*xddot+k*x=0"),
            step("D", spring_k, mass, fraction_text(coeff)),
            step("EL_SOLVE", "xddot", acceleration),
        ]
        answer = f"xddot={acceleration}"
        problem = (
            f"For a mass-spring system with mass m={mass} and spring "
            f"constant k={spring_k}, write L=T-V and apply the "
            "Euler-Lagrange equation to find xddot."
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
        coeff = Fraction(gravity_coeff, inertia_coeff)
        acceleration = neg_coeff_times(coeff, "sin(theta)")
        steps = [
            step("LAG_SETUP", "pendulum", f"m={mass}, L={length}",
                 f"g={g}, q=theta"),
            step("ENERGY_TERM", "T=1/2*m*L^2*thetadot^2"),
            step("E", length, 2, length_sq),
            step("M", mass, length_sq, inertia_coeff),
            step("ENERGY_TERM", "V=m*g*L*(1-cos(theta))"),
            step("M", mass, g, mg),
            step("M", mg, length, gravity_coeff),
            step("LAGRANGIAN", "L=T-V"),
            step("PARTIAL", "dL/dthetadot", "m*L^2*thetadot"),
            step("TIME_DERIV", "d/dt(m*L^2*thetadot)",
                 "m*L^2*thetaddot"),
            step("PARTIAL", "dL/dtheta", "-m*g*L*sin(theta)"),
            step("EL_EQUATION", "mL^2*thetaddot+mgL*sin(theta)=0"),
            step("D", gravity_coeff, inertia_coeff, fraction_text(coeff)),
            step("EL_SOLVE", "thetaddot", acceleration),
        ]
        answer = f"thetaddot={acceleration}"
        problem = (
            f"For a simple pendulum with mass m={mass}, length L={length}, "
            "and g=10, write L=T-V and apply the Euler-Lagrange equation "
            "to find thetaddot."
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
        steps = [
            step("LAG_SETUP", "atwood", f"m1={m1}, m2={m2}",
                 f"g={g}, q=y"),
            step("ENERGY_TERM", "T=1/2*(m1+m2)*ydot^2"),
            step("A", m1, m2, total_mass),
            step("ENERGY_TERM", "V=(m1-m2)*g*y"),
            step("S", m1, m2, potential_diff),
            step("M", potential_diff, g, potential_coeff),
            step("LAGRANGIAN", "L=T-V"),
            step("PARTIAL", "dL/dydot", "(m1+m2)*ydot"),
            step("TIME_DERIV", "d/dt((m1+m2)*ydot)",
                 "(m1+m2)*yddot"),
            step("PARTIAL", "dL/dy", "(m2-m1)*g"),
            step("S", m2, m1, driving_diff),
            step("M", driving_diff, g, driving_force),
            step("EL_EQUATION", "(m1+m2)*yddot-(m2-m1)g=0"),
            step("D", driving_force, total_mass, fraction_text(acceleration)),
            step("EL_SOLVE", "yddot", f"{fraction_text(acceleration)}"),
        ]
        answer = f"yddot={fraction_text(acceleration)} m/s^2 downward for m2"
        problem = (
            f"An Atwood machine has masses m1={m1} and m2={m2} with m2 "
            "heavier. Let y be downward displacement of m2. Write L=T-V "
            "and apply the Euler-Lagrange equation to find yddot."
        )
        return problem, steps, answer
