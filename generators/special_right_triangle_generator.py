import random
from base_generator import ProblemGenerator
from helpers import step, jid


class SpecialRightTriangleGenerator(ProblemGenerator):
    """
    30-60-90 and 45-45-90 triangles by their side ratios, every
    direction, with the rationalizing step shown when dividing by √2.

    Variants:
    - 45_from_leg:   leg s -> hypotenuse s√2
    - 45_from_hyp:   even hypotenuse h -> leg h√2/2 via rationalizing
    - 30_from_short: short leg s -> longer leg s√3 and hypotenuse 2s
    - 30_from_hyp:   even hypotenuse -> both legs
    - 30_from_long:  longer leg k√3 -> short leg k and hypotenuse 2k

    Op-codes used:
    - TRI_SETUP: the triangle and the given side (given, goal)
    - THEOREM: the side ratios (established)
    - M / D: doubling and halving (established)
    - REWRITE: radical products (established)
    - RATIONALIZE: multiply by √2/√2 (established)
    - Z: the requested side(s)
    """

    VARIANTS = ["45_from_leg", "45_from_hyp", "30_from_short",
                "30_from_hyp", "30_from_long"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "45_from_leg":
            s = random.randint(2, 14)
            steps = [
                step("TRI_SETUP", f"45-45-90 triangle, leg = {s}",
                     "hypotenuse"),
                step("THEOREM", "45-45-90 ratios",
                     "leg : leg : hypotenuse = 1 : 1 : √2"),
                step("REWRITE", f"hypotenuse = {s}·√2 = {s}√2"),
            ]
            answer = f"{s}√2"
            problem = (f"A 45-45-90 triangle has legs of length {s}. "
                       f"Find the hypotenuse. Give an exact answer.")
        elif variant == "45_from_hyp":
            k = random.randint(2, 10)
            h = 2 * k
            steps = [
                step("TRI_SETUP", f"45-45-90 triangle, hypotenuse = {h}",
                     "leg"),
                step("THEOREM", "45-45-90 ratios",
                     "leg = hypotenuse/√2"),
                step("REWRITE", f"leg = {h}/√2"),
                step("RATIONALIZE", "(√2)/(√2)"),
                step("REWRITE", f"{h}√2/2"),
                step("D", h, 2, k),
            ]
            answer = f"{k}√2"
            steps.append(step("Z", answer))
            problem = (f"A 45-45-90 triangle has hypotenuse {h}. Find "
                       f"the length of each leg. Give an exact answer.")
            return self._pack(variant, problem, steps, answer)
        elif variant == "30_from_short":
            s = random.randint(2, 12)
            steps = [
                step("TRI_SETUP", f"30-60-90 triangle, shorter leg = {s}",
                     "longer leg and hypotenuse"),
                step("THEOREM", "30-60-90 ratios",
                     "short : long : hypotenuse = 1 : √3 : 2"),
                step("REWRITE", f"longer leg = {s}√3"),
                step("M", 2, s, 2 * s),
            ]
            answer = f"longer leg = {s}√3; hypotenuse = {2 * s}"
            problem = (f"The shorter leg of a 30-60-90 triangle is {s}. "
                       f"Find the longer leg and the hypotenuse. Give "
                       f"exact answers.")
        elif variant == "30_from_hyp":
            s = random.randint(2, 12)
            h = 2 * s
            steps = [
                step("TRI_SETUP", f"30-60-90 triangle, hypotenuse = {h}",
                     "both legs"),
                step("THEOREM", "30-60-90 ratios",
                     "short : long : hypotenuse = 1 : √3 : 2"),
                step("D", h, 2, s),
                step("REWRITE", f"longer leg = {s}√3"),
            ]
            answer = f"shorter leg = {s}; longer leg = {s}√3"
            problem = (f"The hypotenuse of a 30-60-90 triangle is {h}. "
                       f"Find both legs. Give exact answers.")
        else:
            k = random.randint(2, 12)
            steps = [
                step("TRI_SETUP",
                     f"30-60-90 triangle, longer leg = {k}√3",
                     "shorter leg and hypotenuse"),
                step("THEOREM", "30-60-90 ratios",
                     "short : long : hypotenuse = 1 : √3 : 2"),
                step("REWRITE", f"{k}√3 = short·√3, so short = {k}"),
                step("M", 2, k, 2 * k),
            ]
            answer = f"shorter leg = {k}; hypotenuse = {2 * k}"
            problem = (f"The longer leg of a 30-60-90 triangle is "
                       f"{k}√3. Find the shorter leg and the "
                       f"hypotenuse. Give exact answers.")
        steps.append(step("Z", answer))
        return self._pack(variant, problem, steps, answer)

    @staticmethod
    def _pack(variant, problem, steps, answer):
        return dict(
            problem_id=jid(),
            operation=f"special_right_triangle_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
