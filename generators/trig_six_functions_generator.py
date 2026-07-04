import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid

TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25),
           (20, 21, 29), (9, 40, 41)]

SIGNS = {  # quadrant -> (sin, cos, tan)
    1: (1, 1, 1), 2: (1, -1, -1), 3: (-1, -1, 1), 4: (-1, 1, -1)}
ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV"}


def frac_txt(sign, num, den):
    f = Fraction(sign * num, den)
    return str(f)


class TrigSixFunctionsGenerator(ProblemGenerator):
    """
    All six trig functions from one given ratio and a quadrant. The
    missing side comes from the Pythagorean identity (or the
    hypotenuse from the two legs when tangent is given), the sign of
    each derived function comes from the quadrant, and the three
    reciprocals are flipped explicitly.

    Op-codes used:
    - TRIG_SETUP: the given ratio and quadrant (established)
    - THEOREM: the Pythagorean identity used (established)
    - E / A / S: squares and sums, exact fractions (established)
    - REWRITE: the ± root before the sign is fixed (established)
    - SIGN_RULE: the quadrant sign for each derived function
      (established)
    - EVAL: each function's final value (established)
    - D: tan = sin/cos (established)
    - RECIPROCAL: csc, sec, cot flipped from sin, cos, tan
      (definition, value)
    - Z: all six values
    """

    VARIANTS = ["given_sin", "given_cos", "given_tan"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        a, b, c = random.choice(TRIPLES)
        if random.random() < 0.5:
            a, b = b, a
        q = random.randint(1, 4)
        ss, cs, ts = SIGNS[q]

        sin_v = Fraction(ss * a, c)
        cos_v = Fraction(cs * b, c)
        tan_v = Fraction(ts * a, b)

        if variant == "given_sin":
            given = f"sin θ = {sin_v}"
            steps = [
                step("TRIG_SETUP", f"{given}, θ in quadrant {ROMAN[q]}",
                     "all six trig functions"),
                step("THEOREM", "Pythagorean identity",
                     "sin^2 θ + cos^2 θ = 1"),
                step("E", sin_v, 2, sin_v ** 2),
                step("S", 1, sin_v ** 2, 1 - sin_v ** 2),
                step("REWRITE", f"cos θ = ±{Fraction(b, c)}"),
                step("SIGN_RULE", f"cos, quadrant {ROMAN[q]}",
                     "positive" if cs > 0 else "negative"),
                step("EVAL", "cos θ", cos_v),
                step("D", sin_v, cos_v, tan_v),
                step("EVAL", "tan θ", tan_v),
            ]
        elif variant == "given_cos":
            given = f"cos θ = {cos_v}"
            steps = [
                step("TRIG_SETUP", f"{given}, θ in quadrant {ROMAN[q]}",
                     "all six trig functions"),
                step("THEOREM", "Pythagorean identity",
                     "sin^2 θ + cos^2 θ = 1"),
                step("E", cos_v, 2, cos_v ** 2),
                step("S", 1, cos_v ** 2, 1 - cos_v ** 2),
                step("REWRITE", f"sin θ = ±{Fraction(a, c)}"),
                step("SIGN_RULE", f"sin, quadrant {ROMAN[q]}",
                     "positive" if ss > 0 else "negative"),
                step("EVAL", "sin θ", sin_v),
                step("D", sin_v, cos_v, tan_v),
                step("EVAL", "tan θ", tan_v),
            ]
        else:
            given = f"tan θ = {tan_v}"
            steps = [
                step("TRIG_SETUP", f"{given}, θ in quadrant {ROMAN[q]}",
                     "all six trig functions"),
                step("THEOREM", "Pythagorean triple",
                     "hypotenuse from the two legs"),
                step("E", a, 2, a * a),
                step("E", b, 2, b * b),
                step("A", a * a, b * b, c * c),
                step("E", c, 2, c * c),
                step("EVAL", "hypotenuse", c),
                step("SIGN_RULE", f"sin, quadrant {ROMAN[q]}",
                     "positive" if ss > 0 else "negative"),
                step("EVAL", "sin θ", sin_v),
                step("SIGN_RULE", f"cos, quadrant {ROMAN[q]}",
                     "positive" if cs > 0 else "negative"),
                step("EVAL", "cos θ", cos_v),
            ]

        csc_v = 1 / sin_v
        sec_v = 1 / cos_v
        cot_v = 1 / tan_v
        steps.append(step("RECIPROCAL", "csc θ = 1/sin θ", csc_v))
        steps.append(step("RECIPROCAL", "sec θ = 1/cos θ", sec_v))
        steps.append(step("RECIPROCAL", "cot θ = 1/tan θ", cot_v))

        answer = (f"sin θ = {sin_v}; cos θ = {cos_v}; tan θ = {tan_v}; "
                  f"csc θ = {csc_v}; sec θ = {sec_v}; cot θ = {cot_v}")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"trig_six_{variant}",
            problem=(f"Given {given} with θ in quadrant {ROMAN[q]}, "
                     f"find all six trigonometric functions of θ."),
            steps=steps,
            final_answer=answer,
        )
