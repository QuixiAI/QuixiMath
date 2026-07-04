import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.arc_sector_generator import pi_txt


class AngleMeasureGenerator(ProblemGenerator):
    """
    Angle measure conversions and normalizations: degrees to exact
    radian fractions of π and back, coterminal angles brought into
    [0°, 360°) by whole turns, and reference angles by quadrant rule.

    Op-codes used:
    - ANGLE_FORMULA: the conversion or rule being used
    - FRAC_REDUCE / M / S / A: the arithmetic (established)
    - QUADRANT: which quadrant the angle lies in (angle, quadrant)
    - Z: exact radian form, or degrees
    """

    VARIANTS = ["deg_to_rad", "rad_to_deg", "coterminal", "reference"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "deg_to_rad":
            deg = random.choice([v for v in range(15, 361, 15)
                                 if v not in (360,)])
            fr = Fraction(deg, 180)
            steps = [
                step("ANGLE_FORMULA", "radians = degrees · π/180"),
                step("FRAC_REDUCE", f"{deg}/180", fr),
                step("Z", pi_txt(fr)),
            ]
            answer = pi_txt(fr)
            problem = (f"Convert {deg}° to radians. Give an exact "
                       f"answer in terms of π.")
        elif variant == "rad_to_deg":
            deg = random.choice([v for v in range(15, 361, 15)])
            fr = Fraction(deg, 180)
            deg_back = fr * 180
            steps = [
                step("ANGLE_FORMULA", "degrees = radians · 180/π"),
                step("M", fr, 180, deg),
                step("Z", f"{deg}°"),
            ]
            answer = f"{deg}°"
            problem = f"Convert {pi_txt(fr)} radians to degrees."
        elif variant == "coterminal":
            base = random.randint(10, 350)
            wraps = random.choice([1, 1, 2, -1, -1])
            theta = base + 360 * wraps
            steps = [step("ANGLE_FORMULA",
                          "add or subtract 360° until 0° ≤ θ < 360°")]
            cur = theta
            while cur >= 360:
                steps.append(step("S", cur, 360, cur - 360))
                cur -= 360
            while cur < 0:
                steps.append(step("A", cur, 360, cur + 360))
                cur += 360
            answer = f"{cur}°"
            steps.append(step("Z", answer))
            problem = (f"Find the angle between 0° and 360° that is "
                       f"coterminal with {theta}°.")
        else:
            quadrant = random.randint(1, 4)
            offset = random.randint(5, 85)
            theta = {1: offset, 2: 180 - offset, 3: 180 + offset,
                     4: 360 - offset}[quadrant]
            roman = {1: "I", 2: "II", 3: "III", 4: "IV"}[quadrant]
            steps = [step("QUADRANT", f"{theta}°",
                          f"quadrant {roman}")]
            if quadrant == 1:
                steps.append(step("ANGLE_FORMULA",
                                  "quadrant I: reference = θ"))
            elif quadrant == 2:
                steps.append(step("ANGLE_FORMULA",
                                  "quadrant II: reference = 180° - θ"))
                steps.append(step("S", 180, theta, offset))
            elif quadrant == 3:
                steps.append(step("ANGLE_FORMULA",
                                  "quadrant III: reference = θ - 180°"))
                steps.append(step("S", theta, 180, offset))
            else:
                steps.append(step("ANGLE_FORMULA",
                                  "quadrant IV: reference = 360° - θ"))
                steps.append(step("S", 360, theta, offset))
            answer = f"{offset}°"
            steps.append(step("Z", answer))
            problem = f"Find the reference angle of {theta}°."

        return dict(
            problem_id=jid(),
            operation=f"angle_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
