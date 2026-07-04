import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class ProjectileMotionGenerator(ProblemGenerator):
    """
    Projectile motion from velocity components with g=10 m/s^2.

    Op-codes used:
    - PROJECTILE_SETUP: initial components and gravity
    - FORMULA: kinematic formula being applied
    - E / M / D (established/shared): exact arithmetic
    - Z: time of flight, range, and max height
    """

    def generate(self) -> dict:
        vx = random.randint(5, 60)
        vy = random.randint(5, 60)
        g = 10
        time_up = Fraction(vy, g)
        flight_time = 2 * time_up
        range_value = vx * flight_time
        vy_sq = vy ** 2
        two_g = 2 * g
        max_height = Fraction(vy_sq, two_g)
        steps = [
            step("PROJECTILE_SETUP", f"vx={vx}", f"vy={vy}", f"g={g}"),
            step("FORMULA", "t_up=vy/g"),
            step("D", vy, g, fraction_text(time_up)),
            step("FORMULA", "T=2*t_up"),
            step("M", 2, fraction_text(time_up), fraction_text(flight_time)),
            step("FORMULA", "range=vx*T"),
            step("M", vx, fraction_text(flight_time),
                 fraction_text(range_value)),
            step("FORMULA", "h_max=vy^2/(2g)"),
            step("E", vy, 2, vy_sq),
            step("M", 2, g, two_g),
            step("D", vy_sq, two_g, fraction_text(max_height)),
        ]
        answer = (
            f"time={fraction_text(flight_time)} s; "
            f"range={fraction_text(range_value)} m; "
            f"max height={fraction_text(max_height)} m"
        )
        steps.append(step("Z", answer))
        problem = (
            f"A projectile is launched from ground level with horizontal "
            f"velocity {vx} m/s and vertical velocity {vy} m/s. Use g=10 "
            "m/s^2 to compute time of flight, range, and maximum height."
        )
        return dict(
            problem_id=jid(),
            operation="projectile_motion_components",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
