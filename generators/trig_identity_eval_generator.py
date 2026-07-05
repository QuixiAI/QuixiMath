import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.trig_six_functions_generator import TRIPLES, SIGNS, ROMAN

UC = {30: ("1/2", "√3/2"), 45: ("√2/2", "√2/2"), 60: ("√3/2", "1/2"),
      120: ("√3/2", "-1/2"), 135: ("√2/2", "-√2/2")}

# angle -> (A, B, op); value tables for sin/cos at these angles
DECOMP = {15: (45, 30, "-"), 75: (45, 30, "+"),
          105: (60, 45, "+"), 165: (135, 30, "+")}
SUM_ANSWERS = {
    ("sin", 15): "(√6 - √2)/4", ("cos", 15): "(√6 + √2)/4",
    ("sin", 75): "(√6 + √2)/4", ("cos", 75): "(√6 - √2)/4",
    ("sin", 105): "(√6 + √2)/4", ("cos", 105): "(√2 - √6)/4",
    ("sin", 165): "(√6 - √2)/4", ("cos", 165): "-(√6 + √2)/4",
}


class TrigIdentityEvalGenerator(ProblemGenerator):
    """
    Exact evaluations through identities.

    Variants:
    - sum_diff: sin/cos of 15°, 75°, 105°, 165° decomposed into special
      angles, all four table values shown
    - double:   given one ratio and quadrant, evaluate sin 2θ and
      cos 2θ with exact fractions
    - half:     given cos θ (built from a Pythagorean triple so the
      half-angle roots are rational), evaluate sin(θ/2) and cos(θ/2)

    Op-codes used:
    - TRIG_SETUP / THEOREM / TABLE_LOOKUP / SIGN_RULE / EVAL / REWRITE
      (established)
    - E / M / S / D: exact fraction arithmetic (established)
    - Z: exact value(s)
    """

    VARIANTS = ["sum_diff", "double", "half"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        return getattr(self, f"_{variant}")()

    def _sum_diff(self):
        fn = random.choice(["sin", "cos"])
        angle = random.choice(list(DECOMP))
        A, B, op = DECOMP[angle]
        sA, cA = UC[A]
        sB, cB = UC[B]
        if fn == "sin":
            ident = f"sin(A {op} B) = sin A cos B {op} cos A sin B"
            expr = f"({sA})({cB}) {op} ({cA})({sB})"
        else:
            flip = "-" if op == "+" else "+"
            ident = f"cos(A {op} B) = cos A cos B {flip} sin A sin B"
            expr = f"({cA})({cB}) {flip} ({sA})({sB})"
        answer = SUM_ANSWERS[(fn, angle)]
        steps = [
            step("TRIG_SETUP", f"{fn} {angle}°", "exact value"),
            step("REWRITE", f"{angle}° = {A}° {op} {B}°"),
            step("THEOREM", "sum/difference identity", ident),
            step("TABLE_LOOKUP", f"sin {A}°", sA),
            step("TABLE_LOOKUP", f"cos {A}°", cA),
            step("TABLE_LOOKUP", f"sin {B}°", sB),
            step("TABLE_LOOKUP", f"cos {B}°", cB),
            step("REWRITE", expr),
            step("Z", answer),
        ]
        return self._pack("trig_identity_sum_diff",
                          f"Find the exact value of {fn} {angle}° using "
                          f"a sum or difference identity.", steps, answer)

    def _double(self):
        a, b, c = self._random_triple()
        if random.random() < 0.5:
            a, b = b, a
        q = random.randint(1, 4)
        ss, cs, _ = SIGNS[q]
        sin_v = Fraction(ss * a, c)
        cos_v = Fraction(cs * b, c)
        sin2 = 2 * sin_v * cos_v
        cos2 = 1 - 2 * sin_v ** 2
        steps = [
            step("TRIG_SETUP", f"sin θ = {sin_v}, θ in quadrant "
                 f"{ROMAN[q]}", "sin 2θ and cos 2θ"),
            step("THEOREM", "Pythagorean identity",
                 f"cos θ = ±{Fraction(b, c)}"),
            step("SIGN_RULE", f"cos, quadrant {ROMAN[q]}",
                 "positive" if cs > 0 else "negative"),
            step("EVAL", "cos θ", cos_v),
            step("THEOREM", "double angle", "sin 2θ = 2 sin θ cos θ"),
            step("M", 2, sin_v, 2 * sin_v),
            step("M", 2 * sin_v, cos_v, sin2),
            step("EVAL", "sin 2θ", sin2),
            step("THEOREM", "double angle", "cos 2θ = 1 - 2 sin^2 θ"),
            step("E", sin_v, 2, sin_v ** 2),
            step("M", 2, sin_v ** 2, 2 * sin_v ** 2),
            step("S", 1, 2 * sin_v ** 2, cos2),
            step("EVAL", "cos 2θ", cos2),
        ]
        answer = f"sin 2θ = {sin2}; cos 2θ = {cos2}"
        steps.append(step("Z", answer))
        return self._pack("trig_identity_double",
                          f"Given sin θ = {sin_v} with θ in quadrant "
                          f"{ROMAN[q]}, find sin 2θ and cos 2θ.",
                          steps, answer)

    def _half(self):
        a, b, c = self._random_triple()
        if random.random() < 0.5:
            a, b = b, a
        cos_t = Fraction(c * c - 2 * a * a, c * c)  # cos θ = 1 - 2(a/c)²
        sin_half = Fraction(a, c)
        cos_half = Fraction(b, c)
        steps = [
            step("TRIG_SETUP", f"cos θ = {cos_t}, 0° < θ < 180°",
                 "sin(θ/2) and cos(θ/2)"),
            step("THEOREM", "half angle",
                 "sin(θ/2) = √((1 - cos θ)/2), "
                 "cos(θ/2) = √((1 + cos θ)/2)"),
            step("S", 1, cos_t, 1 - cos_t),
            step("D", 1 - cos_t, 2, (1 - cos_t) / 2),
            step("E", sin_half, 2, sin_half ** 2),
            step("EVAL", "sin(θ/2)", sin_half),
            step("A", 1, cos_t, 1 + cos_t),
            step("D", 1 + cos_t, 2, (1 + cos_t) / 2),
            step("E", cos_half, 2, cos_half ** 2),
            step("EVAL", "cos(θ/2)", cos_half),
        ]
        answer = f"sin(θ/2) = {sin_half}; cos(θ/2) = {cos_half}"
        steps.append(step("Z", answer))
        return self._pack("trig_identity_half",
                          f"Given cos θ = {cos_t} with 0° < θ < 180°, "
                          f"find sin(θ/2) and cos(θ/2). (θ/2 is in the "
                          f"first quadrant.)", steps, answer)

    @staticmethod
    def _random_triple():
        m = random.randint(2, 220)
        n = random.randint(1, m - 1)
        a = m * m - n * n
        b = 2 * m * n
        c = m * m + n * n
        if random.random() < 0.5:
            a, b = b, a
        return abs(a), abs(b), c

    @staticmethod
    def _pack(op, problem, steps, answer):
        return dict(
            problem_id=jid(),
            operation=op,
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
