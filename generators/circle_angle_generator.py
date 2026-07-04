import random
from base_generator import ProblemGenerator
from helpers import step, jid


class CircleAngleGenerator(ProblemGenerator):
    """
    Central and inscribed angle relationships: an inscribed angle is
    half the central angle (equivalently half the intercepted arc), and
    an angle inscribed in a semicircle is right (Thales).

    Variants:
    - inscribed_from_central: halve the central angle
    - central_from_inscribed: double the inscribed angle
    - arc_from_inscribed:     the intercepted arc is twice the
                              inscribed angle
    - semicircle:             Thales plus the triangle angle sum

    Op-codes used:
    - CIRCLE_ANGLE_SETUP: the given angle and the goal (given, goal)
    - THEOREM: the relationship used (established)
    - M / D / S: double, halve, or subtract (established)
    - Z: 'x°'
    """

    VARIANTS = ["inscribed_from_central", "central_from_inscribed",
                "arc_from_inscribed", "semicircle"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "inscribed_from_central":
            central = 2 * random.randint(20, 160)
            ans = central // 2
            steps = [
                step("CIRCLE_ANGLE_SETUP",
                     f"central angle {central}° subtends an arc",
                     "inscribed angle on the same arc"),
                step("THEOREM", "inscribed angle theorem",
                     "inscribed = central / 2"),
                step("D", central, 2, ans),
            ]
            problem = (f"A central angle of {central}° and an inscribed "
                       f"angle subtend the same arc. Find the inscribed "
                       f"angle.")
        elif variant == "central_from_inscribed":
            ins = random.randint(15, 85)
            ans = 2 * ins
            steps = [
                step("CIRCLE_ANGLE_SETUP",
                     f"inscribed angle {ins}°",
                     "central angle on the same arc"),
                step("THEOREM", "inscribed angle theorem",
                     "central = 2 · inscribed"),
                step("M", 2, ins, ans),
            ]
            problem = (f"An inscribed angle measures {ins}°. Find the "
                       f"central angle subtending the same arc.")
        elif variant == "arc_from_inscribed":
            ins = random.randint(15, 85)
            ans = 2 * ins
            steps = [
                step("CIRCLE_ANGLE_SETUP",
                     f"inscribed angle {ins}°", "intercepted arc"),
                step("THEOREM", "inscribed angle theorem",
                     "arc = 2 · inscribed"),
                step("M", 2, ins, ans),
            ]
            problem = (f"An inscribed angle measures {ins}°. Find the "
                       f"measure of its intercepted arc.")
        else:
            a = random.randint(15, 75)
            ans = 90 - a
            steps = [
                step("CIRCLE_ANGLE_SETUP",
                     f"triangle inscribed in a circle with one side a "
                     f"diameter; one acute angle is {a}°",
                     "the other acute angle"),
                step("THEOREM", "Thales",
                     "the angle opposite the diameter is 90°"),
                step("S", 90, a, ans),
            ]
            problem = (f"A triangle is inscribed in a circle with one "
                       f"side a diameter. One of its acute angles "
                       f"measures {a}°. Find the other acute angle.")

        answer = f"{ans}°"
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"circle_angle_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
