import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.arc_sector_generator import pi_txt

SIN_REF = {0: "0", 30: "1/2", 45: "√2/2", 60: "√3/2", 90: "1"}
COS_REF = {0: "1", 30: "√3/2", 45: "√2/2", 60: "1/2", 90: "0"}
TAN_REF = {0: "0", 30: "√3/3", 45: "1", 60: "√3"}

QUADRANT_SIGNS = {  # quadrant -> (sin, cos, tan) sign
    1: (1, 1, 1), 2: (1, -1, -1), 3: (-1, -1, 1), 4: (-1, 1, -1)}

UC_POINTS = {0: ("1", "0"), 90: ("0", "1"), 180: ("-1", "0"),
             270: ("0", "-1")}


def signed(txt, sign):
    return txt if sign > 0 or txt == "0" else f"-{txt}"


def exact_value(fn, deg):
    """Exact value of sin/cos/tan at a special angle (degrees)."""
    d = deg % 360
    if d in UC_POINTS:
        x, y = UC_POINTS[d]
        if fn == "sin":
            return y
        if fn == "cos":
            return x
        return "0" if y == "0" else None  # tan undefined at 90/270
    q = d // 90 + 1
    ref = d % 180
    ref = ref if ref <= 90 else 180 - ref
    sign = QUADRANT_SIGNS[q][{"sin": 0, "cos": 1, "tan": 2}[fn]]
    table = {"sin": SIN_REF, "cos": COS_REF, "tan": TAN_REF}[fn]
    return signed(table[ref], sign)


class UnitCircleGenerator(ProblemGenerator):
    """
    Exact unit-circle values and inverse trig, worked the way the unit
    circle is taught: quadrant, reference angle, sign rule, table
    value. Quadrantal angles read straight off the circle point.
    Radian inputs convert to degrees first.

    Variants:
    - evaluate: sin/cos/tan of a special angle (degree or radian form)
    - inverse:  arcsin/arccos/arctan of a table value, honoring each
                function's principal range

    Op-codes used:
    - TRIG_SETUP: the expression and the goal (established)
    - M: radian-to-degree conversion (established)
    - QUADRANT: the quadrant (established)
    - S: reference angle arithmetic (established)
    - SIGN_RULE: the ASTC sign for this function/quadrant
      (function and quadrant, sign)
    - UC_POINT: the circle point at a quadrantal angle (angle, point)
    - TABLE_LOOKUP: the reference-angle value (established)
    - DOMAIN_NOTE: the principal range of the inverse (established)
    - Z: the exact value or angle
    """

    VARIANTS = ["evaluate", "inverse"]
    ANGLES = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240,
              270, 300, 315, 330]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "evaluate":
            return self._evaluate()
        return self._inverse()

    def _evaluate(self):
        while True:
            fn = random.choice(["sin", "cos", "tan"])
            deg = random.choice(self.ANGLES)
            val = exact_value(fn, deg)
            if val is not None:
                break
        radians = random.random() < 0.4 and deg != 0
        if radians:
            fr = Fraction(deg, 180)
            expr = f"{fn}({pi_txt(fr)})"
        else:
            expr = f"{fn} {deg}°"

        steps = [step("TRIG_SETUP", expr, "exact value")]
        if radians:
            steps.append(step("M", fr, 180, deg))
        if deg in UC_POINTS:
            x, y = UC_POINTS[deg]
            steps.append(step("UC_POINT", f"{deg}°", f"({x}, {y})"))
            steps.append(step("TABLE_LOOKUP",
                              f"{fn} = {'y' if fn == 'sin' else 'x' if fn == 'cos' else 'y/x'}",
                              val))
        else:
            q = deg // 90 + 1
            roman = {1: "I", 2: "II", 3: "III", 4: "IV"}[q]
            ref = deg % 180
            ref = ref if ref <= 90 else 180 - ref
            steps.append(step("QUADRANT", f"{deg}°", f"quadrant {roman}"))
            if q == 2:
                steps.append(step("S", 180, deg, ref))
            elif q == 3:
                steps.append(step("S", deg, 180, ref))
            elif q == 4:
                steps.append(step("S", 360, deg, ref))
            sign = QUADRANT_SIGNS[q][{"sin": 0, "cos": 1, "tan": 2}[fn]]
            steps.append(step("SIGN_RULE", f"{fn}, quadrant {roman}",
                              "positive" if sign > 0 else "negative"))
            table = {"sin": SIN_REF, "cos": COS_REF, "tan": TAN_REF}[fn]
            steps.append(step("TABLE_LOOKUP", f"{fn} {ref}°",
                              table[ref]))
        steps.append(step("Z", val))

        return self._pack("unit_circle_evaluate",
                          f"Find the exact value of {expr}.", steps, val)

    def _inverse(self):
        fn = random.choice(["arcsin", "arccos", "arctan"])
        if fn == "arcsin":
            ref = random.choice([0, 30, 45, 60, 90])
            neg = ref != 0 and random.random() < 0.5
            val = signed(SIN_REF[ref], -1 if neg else 1)
            ans = -ref if neg else ref
            rng = "[-90°, 90°]"
            base_fn = "sin"
        elif fn == "arccos":
            ref = random.choice([0, 30, 45, 60, 90])
            neg = ref not in (90,) and random.random() < 0.5
            val = signed(COS_REF[ref], -1 if neg else 1)
            ans = 180 - ref if neg else ref
            rng = "[0°, 180°]"
            base_fn = "cos"
        else:
            ref = random.choice([0, 30, 45, 60])
            neg = ref != 0 and random.random() < 0.5
            val = signed(TAN_REF[ref], -1 if neg else 1)
            ans = -ref if neg else ref
            rng = "(-90°, 90°)"
            base_fn = "tan"

        steps = [
            step("TRIG_SETUP", f"{fn}({val})", "angle in degrees"),
            step("DOMAIN_NOTE", f"{fn} range", rng),
            step("TABLE_LOOKUP", f"{base_fn} {ref}°",
                 val.lstrip("-") if val != "0" else "0"),
        ]
        if neg:
            if fn == "arccos":
                steps.append(step("SIGN_RULE",
                                  "arccos of a negative",
                                  "second-quadrant angle"))
                steps.append(step("S", 180, ref, ans))
            else:
                steps.append(step("SIGN_RULE",
                                  f"{fn} of a negative",
                                  "negative angle"))
        answer = f"{ans}°"
        steps.append(step("Z", answer))
        return self._pack("unit_circle_inverse",
                          f"Evaluate {fn}({val}). Give the answer in "
                          f"degrees.", steps, answer)

    @staticmethod
    def _pack(op, problem, steps, answer):
        return dict(
            problem_id=jid(),
            operation=op,
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
