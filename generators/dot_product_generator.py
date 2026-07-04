import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.vector_ops_generator import vec


class DotProductGenerator(ProblemGenerator):
    """
    Dot products and angles between vectors.

    Variants:
    - dot:   u·v componentwise
    - perp:  is u ⊥ v? Compute the dot product, half are zero by
             construction
    - angle: vector pairs built so the angle is exact (0°, 45°, 90°,
             135°, 180°); magnitudes computed, the cosine simplified
             (rationalizing 1/√2 when it appears), then matched

    Op-codes used:
    - VEC_SETUP / DOT_FORMULA: setup and the formula used
    - M / A / E / D: the arithmetic (established)
    - EVAL / ROOT_SIMPLIFY / RATIONALIZE / REWRITE / TABLE_LOOKUP
      (established)
    - Z: number, Yes/No, or angle
    """

    VARIANTS = ["dot", "perp", "angle"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _dot_steps(steps, u, v):
        p1, p2 = u[0] * v[0], u[1] * v[1]
        steps.append(step("M", u[0], v[0], p1))
        steps.append(step("M", u[1], v[1], p2))
        steps.append(step("A", p1, p2, p1 + p2))
        return p1 + p2

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "dot":
            u = [random.randint(-7, 7) for _ in range(2)]
            v = [random.randint(-7, 7) for _ in range(2)]
            steps = [step("VEC_SETUP", f"u = {vec(u)}, v = {vec(v)}",
                          "u·v"),
                     step("DOT_FORMULA", "u·v = x1·x2 + y1·y2")]
            d = self._dot_steps(steps, u, v)
            answer = str(d)
            steps.append(step("Z", answer))
            problem = (f"Given u = {vec(u)} and v = {vec(v)}, compute "
                       f"the dot product u·v.")
        elif variant == "perp":
            u = [random.choice([x for x in range(-6, 7) if x != 0])
                 for _ in range(2)]
            if random.random() < 0.5:
                k = random.choice([1, 2, -1])
                v = [-u[1] * k, u[0] * k]
            else:
                v = [random.randint(-6, 6) for _ in range(2)]
                if u[0] * v[0] + u[1] * v[1] == 0:
                    return self.generate()
            steps = [step("VEC_SETUP", f"u = {vec(u)}, v = {vec(v)}",
                          "perpendicular?"),
                     step("DOT_FORMULA",
                          "u ⊥ v exactly when u·v = 0")]
            d = self._dot_steps(steps, u, v)
            answer = "Yes" if d == 0 else "No"
            steps.append(step("EVAL", "u·v", d))
            steps.append(step("Z", answer))
            problem = (f"Are u = {vec(u)} and v = {vec(v)} "
                       f"perpendicular?")
        else:
            a = random.randint(2, 7)
            b = random.randint(2, 7)
            kind = random.choice(["45", "135", "90", "0", "180"])
            if kind == "45":
                u, v, theta = [a, 0], [b, b], 45
            elif kind == "135":
                u, v, theta = [a, 0], [-b, b], 135
            elif kind == "90":
                u, v, theta = [a, 0], [0, b], 90
            elif kind == "0":
                u, v, theta = [a, a], [b, b], 0
            else:
                u, v, theta = [a, a], [-b, -b], 180
            steps = [step("VEC_SETUP", f"u = {vec(u)}, v = {vec(v)}",
                          "angle between u and v"),
                     step("DOT_FORMULA",
                          "cos θ = (u·v)/(‖u‖ · ‖v‖)")]
            d = self._dot_steps(steps, u, v)
            steps.append(step("EVAL", "u·v", d))
            if kind in ("45", "135", "90"):
                mag_u, mag_v = str(a), f"{b}√2"
                cos_txt = {"45": "√2/2", "135": "-√2/2",
                           "90": "0"}[kind]
                steps.append(step("EVAL", "magnitude of u", a))
                steps.append(step("ROOT_SIMPLIFY",
                                  f"√{2 * b * b} = {b}√2"))
                steps.append(step("EVAL", "magnitude of v", f"{b}√2"))
                if kind == "90":
                    steps.append(step("REWRITE", "cos θ = 0"))
                else:
                    sign = "-" if kind == "135" else ""
                    steps.append(step("REWRITE",
                                      f"cos θ = {d}/({a} · {b}√2) = "
                                      f"{sign}1/√2"))
                    steps.append(step("RATIONALIZE", "(√2)/(√2)"))
                    steps.append(step("REWRITE", f"cos θ = {cos_txt}"))
            else:
                steps.append(step("ROOT_SIMPLIFY",
                                  f"√{2 * a * a} = {a}√2"))
                steps.append(step("ROOT_SIMPLIFY",
                                  f"√{2 * b * b} = {b}√2"))
                cos_txt = "1" if kind == "0" else "-1"
                steps.append(step("REWRITE",
                                  f"cos θ = {d}/({a}√2 · {b}√2) = "
                                  f"{cos_txt}"))
            steps.append(step("TABLE_LOOKUP",
                              f"cos {theta}° = "
                              f"{cos_txt if kind != '90' else '0'}",
                              f"θ = {theta}°"))
            answer = f"{theta}°"
            steps.append(step("Z", answer))
            problem = (f"Find the angle between u = {vec(u)} and "
                       f"v = {vec(v)}.")

        return dict(
            problem_id=jid(),
            operation=f"dot_product_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
