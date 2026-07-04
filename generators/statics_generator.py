import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class StaticsGenerator(ProblemGenerator):
    """
    Static equilibrium for levers and simply supported beams.

    Variants:
    - lever_balance: balance clockwise and counterclockwise torques
    - supported_beam: use torque balance and vertical force balance

    Op-codes used:
    - STATICS_SETUP: geometry, loads, and support labels
    - STATICS_FORMULA: equilibrium relation being applied
    - A / S / M / D (established/shared): exact statics arithmetic
    - CHECK: equilibrium verification
    - Z: requested support force or balancing force
    """

    VARIANTS = ["lever_balance", "supported_beam"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "lever_balance":
            problem, steps, answer = self._generate_lever_balance()
        else:
            problem, steps, answer = self._generate_supported_beam()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"statics_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_lever_balance(self):
        force1 = random.randint(5, 80)
        distance1 = random.randint(2, 12)
        distance2 = random.randint(2, 12)
        torque = force1 * distance1
        force2 = Fraction(torque, distance2)
        check_torque = force2 * distance2
        steps = [
            step("STATICS_SETUP", "lever_balance", f"F1={force1}",
                 f"d1={distance1}, d2={distance2}"),
            step("STATICS_FORMULA", "F1*d1=F2*d2"),
            step("M", force1, distance1, torque),
            step("D", torque, distance2, fraction_text(force2)),
            step("M", fraction_text(force2), distance2,
                 fraction_text(check_torque)),
            step("CHECK", "left torque", torque,
                 f"right torque {fraction_text(check_torque)}"),
        ]
        answer = f"F2={fraction_text(force2)} N"
        problem = (
            f"A lever is in static equilibrium. A {force1} N downward force "
            f"acts {distance1} m left of the fulcrum. What downward force "
            f"must act {distance2} m right of the fulcrum to balance torques?"
        )
        return problem, steps, answer

    def _generate_supported_beam(self):
        length = random.randint(4, 20)
        load_position = random.randint(1, length - 1)
        load = random.randint(20, 200)
        load_torque = load * load_position
        right_reaction = Fraction(load_torque, length)
        left_reaction = Fraction(load) - right_reaction
        force_sum = left_reaction + right_reaction
        steps = [
            step("STATICS_SETUP", "supported_beam", f"W={load}, L={length}",
                 f"x={load_position}"),
            step("STATICS_FORMULA", "sum_tau_left=0 => RB*L=W*x"),
            step("M", load, load_position, load_torque),
            step("D", load_torque, length, fraction_text(right_reaction)),
            step("STATICS_FORMULA", "sum_Fy=0 => RA+RB=W"),
            step("S", load, fraction_text(right_reaction),
                 fraction_text(left_reaction)),
            step("A", fraction_text(left_reaction),
                 fraction_text(right_reaction), fraction_text(force_sum)),
            step("CHECK", "vertical forces", fraction_text(force_sum),
                 f"load {load}"),
        ]
        answer = (
            f"RA={fraction_text(left_reaction)} N; "
            f"RB={fraction_text(right_reaction)} N"
        )
        problem = (
            f"A simply supported beam is {length} m long with supports at "
            f"A and B. A {load} N point load acts {load_position} m from "
            "support A. Find reactions RA and RB."
        )
        return problem, steps, answer
