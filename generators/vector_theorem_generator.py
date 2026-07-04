import random

from base_generator import ProblemGenerator
from helpers import step, jid


def fmt_pi(coeff):
    if coeff == 1:
        return "pi"
    if coeff == -1:
        return "-pi"
    return f"{coeff}*pi"


def fmt_term(coeff, var):
    if coeff == 0:
        return "0"
    if coeff == 1:
        return var
    if coeff == -1:
        return f"-{var}"
    return f"{coeff}*{var}"


def fmt_sum(values):
    pieces = []
    for value in values:
        if not pieces:
            pieces.append(str(value))
        else:
            pieces.append(("+ " if value >= 0 else "- ") + str(abs(value)))
    return " ".join(pieces)


def factor_text(value):
    return f"({value})" if value < 0 else str(value)


class VectorTheoremGenerator(ProblemGenerator):
    """
    Green's theorem, divergence theorem, and Stokes' theorem computations
    using the easier side of the theorem.

    Variants:
    - green_rectangle: circulation around a rectangle via double integral
    - divergence_box: outward flux through a box via volume integral
    - stokes_disk: circulation around a disk via curl flux

    Op-codes used:
    - THEOREM_SETUP: theorem, field, and region
    - PARTIAL_RESULT (established): needed divergence/curl partials
    - REGION_MEASURE: area or volume
    - THEOREM_REWRITE: replace boundary integral by area/volume integral
    - FLUX_SUM / CIRCULATION_SUM: multiply density by measure
    - Z: final flux or circulation
    """

    VARIANTS = ["green_rectangle", "divergence_box", "stokes_disk"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "green_rectangle":
            k = random.choice([v for v in range(-8, 9) if v != 0])
            width = random.randint(2, 12)
            height = random.randint(2, 12)
            area = width * height
            value = k * area
            q_txt = fmt_term(k, "x")
            steps = [
                step("THEOREM_SETUP", "Green",
                     f"F=<0, {q_txt}>", f"rectangle {width} by {height}"),
                step("PARTIAL_RESULT", "Q_x", k),
                step("PARTIAL_RESULT", "P_y", 0),
                step("THEOREM_REWRITE", "circulation",
                     "double integral of Q_x - P_y"),
                step("REGION_MEASURE", "area", f"{width}*{height}", area),
                step("CIRCULATION_SUM", f"({k} - 0)*{area}", value),
            ]
            answer = f"circulation {value}"
            problem = (
                f"Use Green's theorem to compute the counterclockwise "
                f"circulation of F=<0, {q_txt}> around the rectangle "
                f"0 <= x <= {width}, 0 <= y <= {height}."
            )
        elif variant == "divergence_box":
            a = random.randint(-5, 5)
            b = random.randint(-5, 5)
            c = random.randint(-5, 5)
            if a == b == c == 0:
                a = 1
            length = random.randint(2, 10)
            width = random.randint(2, 10)
            height = random.randint(2, 10)
            div = a + b + c
            volume = length * width * height
            value = div * volume
            p_txt = fmt_term(a, "x")
            q_txt = fmt_term(b, "y")
            r_txt = fmt_term(c, "z")
            steps = [
                step("THEOREM_SETUP", "divergence theorem",
                     f"F=<{p_txt}, {q_txt}, {r_txt}>",
                     f"box {length} by {width} by {height}"),
                step("PARTIAL_RESULT", "P_x", a),
                step("PARTIAL_RESULT", "Q_y", b),
                step("PARTIAL_RESULT", "R_z", c),
                step("THEOREM_REWRITE", "outward flux",
                     "triple integral of div F"),
                step("REGION_MEASURE", "volume",
                     f"{length}*{width}*{height}", volume),
                step("FLUX_SUM", f"({fmt_sum([a, b, c])})*{volume}",
                     value),
            ]
            answer = f"outward flux {value}"
            problem = (
                f"Use the divergence theorem to compute the outward flux "
                f"of F=<{p_txt}, {q_txt}, {r_txt}> through the box "
                f"0 <= x <= {length}, 0 <= y <= {width}, "
                f"0 <= z <= {height}."
            )
        else:
            k = random.choice([v for v in range(-8, 9) if v != 0])
            radius = random.randint(2, 12)
            value = k * radius * radius
            pi_value = fmt_pi(value)
            p_txt = fmt_term(-k, "y")
            steps = [
                step("THEOREM_SETUP", "Stokes",
                     f"F=<{p_txt}, 0, 0>",
                     f"disk radius {radius} in z=0"),
                step("PARTIAL_RESULT", "Q_x", 0),
                step("PARTIAL_RESULT", "P_y", -k),
                step("THEOREM_REWRITE", "circulation",
                     "surface integral of curl F dot n"),
                step("REGION_MEASURE", "disk area",
                     f"{radius}^2*pi", fmt_pi(radius * radius)),
                step("CIRCULATION_SUM", f"{factor_text(k)}*{radius}^2*pi",
                     pi_value),
            ]
            answer = f"circulation {pi_value}"
            problem = (
                f"Use Stokes' theorem to compute the counterclockwise "
                f"circulation of F=<{p_txt}, 0, 0> around the circle "
                f"x^2 + y^2 = {radius * radius} in the plane z = 0."
            )
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"vector_theorem_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
