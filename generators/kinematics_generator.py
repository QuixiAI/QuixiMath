import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec


def exact(fr):
    """Terminating decimal when possible, else the reduced fraction."""
    d = fr.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    return dec(fr) if d == 1 else str(fr)


class KinematicsGenerator(ProblemGenerator):
    """
    Basic kinematics formula chains with consistent units: distance from
    d = vt, speed from v = d/t, time from t = d/v, and acceleration from
    a = (v_f - v_i)/t.

    Variants:
    - distance:      d = v*t
    - speed:         v = d/t
    - time:          t = d/v
    - acceleration:  a = Δv/t

    Op-codes used:
    - KIN_SETUP: givens and target
    - KIN_FORMULA: formula to use
    - S / M / D (established): exact arithmetic
    - UNIT_ATTACH: attach the correct unit to the numeric answer
    - Z: exact answer with units
    """

    VARIANTS = ["distance", "speed", "time", "acceleration"]
    LINEAR_UNITS = [
        ("meters", "seconds", "m/s"),
        ("kilometers", "hours", "km/hour"),
        ("miles", "hours", "miles/hour"),
        ("feet", "seconds", "ft/s"),
    ]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _distance(self):
        dist_unit, time_unit, speed_unit = random.choice(self.LINEAR_UNITS)
        speed = random.randint(3, 80)
        time = random.randint(2, 12)
        distance = speed * time
        answer = f"{distance} {dist_unit}"
        steps = [
            step("KIN_SETUP", f"v = {speed} {speed_unit}",
                 f"t = {time} {time_unit}", "distance"),
            step("KIN_FORMULA", "d = v*t"),
            step("M", speed, time, distance),
            step("UNIT_ATTACH", distance, dist_unit, answer),
            step("Z", answer),
        ]
        problem = (
            f"An object travels at {speed} {dist_unit} per {time_unit[:-1]} "
            f"for {time} {time_unit}. Find the distance."
        )
        return "distance", problem, steps, answer

    def _speed(self):
        dist_unit, time_unit, speed_unit = random.choice(self.LINEAR_UNITS)
        speed = random.randint(3, 80)
        time = random.randint(2, 12)
        distance = speed * time
        answer = f"{speed} {speed_unit}"
        steps = [
            step("KIN_SETUP", f"d = {distance} {dist_unit}",
                 f"t = {time} {time_unit}", "speed"),
            step("KIN_FORMULA", "v = d/t"),
            step("D", distance, time, speed),
            step("UNIT_ATTACH", speed, speed_unit, answer),
            step("Z", answer),
        ]
        problem = (
            f"An object travels {distance} {dist_unit} in {time} "
            f"{time_unit}. Find the speed."
        )
        return "speed", problem, steps, answer

    def _time(self):
        dist_unit, time_unit, speed_unit = random.choice(self.LINEAR_UNITS)
        speed = random.randint(3, 80)
        time = random.randint(2, 12)
        distance = speed * time
        answer = f"{time} {time_unit}"
        steps = [
            step("KIN_SETUP", f"d = {distance} {dist_unit}",
                 f"v = {speed} {speed_unit}", "time"),
            step("KIN_FORMULA", "t = d/v"),
            step("D", distance, speed, time),
            step("UNIT_ATTACH", time, time_unit, answer),
            step("Z", answer),
        ]
        problem = (
            f"An object travels {distance} {dist_unit} at {speed} "
            f"{dist_unit} per {time_unit[:-1]}. Find the time."
        )
        return "time", problem, steps, answer

    def _acceleration(self):
        time = random.randint(2, 10)
        start = random.randint(0, 20)
        accel = random.randint(1, 12)
        change = accel * time
        final = start + change
        answer = f"{accel} m/s^2"
        steps = [
            step("KIN_SETUP", f"v_i = {start} m/s",
                 f"v_f = {final} m/s, t = {time} s", "acceleration"),
            step("KIN_FORMULA", "a = (v_f - v_i)/t"),
            step("S", final, start, change),
            step("D", change, time, accel),
            step("UNIT_ATTACH", accel, "m/s^2", answer),
            step("Z", answer),
        ]
        problem = (
            f"A cart's velocity changes from {start} meters per second to "
            f"{final} meters per second in {time} seconds. Find the "
            "acceleration."
        )
        return "acceleration", problem, steps, answer

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "distance":
            op_suffix, problem, steps, answer = self._distance()
        elif variant == "speed":
            op_suffix, problem, steps, answer = self._speed()
        elif variant == "time":
            op_suffix, problem, steps, answer = self._time()
        else:
            op_suffix, problem, steps, answer = self._acceleration()

        return dict(
            problem_id=jid(),
            operation=f"kinematics_{op_suffix}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
