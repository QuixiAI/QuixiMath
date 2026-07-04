import random

from base_generator import ProblemGenerator
from helpers import step, jid


class PhysicsFormulaGenerator(ProblemGenerator):
    """
    Work, force, power, and energy formula chains with unit-consistent
    arithmetic. Minute-based variants explicitly convert minutes to seconds
    before using watts = joules/second.

    Variants:
    - work:          W = F*d
    - force:         F = W/d
    - power_seconds: P = W/t with seconds given
    - power_minutes: convert minutes to seconds, then P = W/t
    - energy:        convert minutes to seconds, then W = P*t

    Op-codes used:
    - PHYS_SETUP: givens and target
    - PHYS_FORMULA: formula to use
    - UNIT_CONVERT: unit conversion step
    - M / D (established): exact arithmetic
    - UNIT_ATTACH: attach the correct unit to the numeric answer
    - Z: exact answer with units
    """

    VARIANTS = ["work", "force", "power_seconds", "power_minutes",
                "energy"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _work(self):
        force = random.randint(5, 80)
        distance = random.randint(2, 30)
        work = force * distance
        answer = f"{work} joules"
        steps = [
            step("PHYS_SETUP", f"F = {force} newtons",
                 f"d = {distance} meters", "work"),
            step("PHYS_FORMULA", "W = F*d"),
            step("M", force, distance, work),
            step("UNIT_ATTACH", work, "joules", answer),
            step("Z", answer),
        ]
        problem = (
            f"A force of {force} newtons moves an object {distance} "
            "meters. Find the work done."
        )
        return "work", problem, steps, answer

    def _force(self):
        force = random.randint(5, 80)
        distance = random.randint(2, 30)
        work = force * distance
        answer = f"{force} newtons"
        steps = [
            step("PHYS_SETUP", f"W = {work} joules",
                 f"d = {distance} meters", "force"),
            step("PHYS_FORMULA", "F = W/d"),
            step("D", work, distance, force),
            step("UNIT_ATTACH", force, "newtons", answer),
            step("Z", answer),
        ]
        problem = (
            f"{work} joules of work move an object {distance} meters. "
            "Find the force."
        )
        return "force", problem, steps, answer

    def _power_seconds(self):
        power = random.randint(10, 200)
        time = random.randint(2, 30)
        work = power * time
        answer = f"{power} watts"
        steps = [
            step("PHYS_SETUP", f"W = {work} joules",
                 f"t = {time} seconds", "power"),
            step("PHYS_FORMULA", "P = W/t"),
            step("D", work, time, power),
            step("UNIT_ATTACH", power, "watts", answer),
            step("Z", answer),
        ]
        problem = (
            f"A machine does {work} joules of work in {time} seconds. "
            "Find the power."
        )
        return "power_seconds", problem, steps, answer

    def _power_minutes(self):
        power = random.randint(10, 200)
        minutes = random.randint(1, 8)
        minute_unit = "minute" if minutes == 1 else "minutes"
        seconds = minutes * 60
        work = power * seconds
        answer = f"{power} watts"
        steps = [
            step("PHYS_SETUP", f"W = {work} joules",
                 f"t = {minutes} {minute_unit}", "power"),
            step("UNIT_CONVERT", f"{minutes} {minute_unit}", f"{seconds} seconds"),
            step("PHYS_FORMULA", "P = W/t"),
            step("D", work, seconds, power),
            step("UNIT_ATTACH", power, "watts", answer),
            step("Z", answer),
        ]
        problem = (
            f"A machine does {work} joules of work in {minutes} {minute_unit}. "
            "Find the power in watts."
        )
        return "power_minutes", problem, steps, answer

    def _energy(self):
        power = random.randint(10, 200)
        minutes = random.randint(1, 8)
        minute_unit = "minute" if minutes == 1 else "minutes"
        seconds = minutes * 60
        work = power * seconds
        answer = f"{work} joules"
        steps = [
            step("PHYS_SETUP", f"P = {power} watts",
                 f"t = {minutes} {minute_unit}", "energy"),
            step("UNIT_CONVERT", f"{minutes} {minute_unit}", f"{seconds} seconds"),
            step("PHYS_FORMULA", "W = P*t"),
            step("M", power, seconds, work),
            step("UNIT_ATTACH", work, "joules", answer),
            step("Z", answer),
        ]
        problem = (
            f"A device runs at {power} watts for {minutes} {minute_unit}. "
            "How much energy does it use in joules?"
        )
        return "energy", problem, steps, answer

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "work":
            op_suffix, problem, steps, answer = self._work()
        elif variant == "force":
            op_suffix, problem, steps, answer = self._force()
        elif variant == "power_seconds":
            op_suffix, problem, steps, answer = self._power_seconds()
        elif variant == "power_minutes":
            op_suffix, problem, steps, answer = self._power_minutes()
        else:
            op_suffix, problem, steps, answer = self._energy()

        return dict(
            problem_id=jid(),
            operation=f"physics_formula_{op_suffix}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
