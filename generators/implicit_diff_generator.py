import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid

TRIPLES = [(3, 4, 5), (4, 3, 5), (6, 8, 10), (8, 6, 10),
           (5, 12, 13), (12, 5, 13), (8, 15, 17), (15, 8, 17)]


class ImplicitDiffGenerator(ProblemGenerator):
    """
    Implicit differentiation with every term differentiated by name -
    y-terms carry the chain factor y', product terms use the product
    rule - then y' is isolated.

    Variants:
    - circle:    x² + y² = r² -> dy/dx = -x/y, sometimes evaluated at
                 a Pythagorean lattice point
    - cubes:     x³ + y³ = c -> dy/dx = -x²/y²
    - product:   xy = c -> dy/dx = -y/x
    - full_quad: x² + xy + y² = c -> dy/dx = -(2x + y)/(x + 2y)

    Op-codes used:
    - IMPLICIT_SETUP: the curve and the goal (equation, goal)
    - IMPLICIT_DIFF: one term differentiated (term, derivative)
    - REWRITE / EQ_OP_BOTH: assemble and solve for y' (established)
    - SUBST / FRAC_REDUCE: the at-point evaluation (established)
    - Z: dy/dx
    """

    VARIANTS = ["circle", "cubes", "product", "full_quad"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "circle":
            at_point = random.random() < 0.5
            if at_point:
                x0, y0, r = random.choice(TRIPLES)
                if random.random() < 0.5:
                    x0 = -x0
                if random.random() < 0.5:
                    y0 = -y0
            else:
                r = random.choice([2, 3, 5, 6, 7])
            eq = f"x^2 + y^2 = {r * r}"
            steps = [
                step("IMPLICIT_SETUP", eq,
                     f"dy/dx at ({x0}, {y0})" if at_point else "dy/dx"),
                step("IMPLICIT_DIFF", "d/dx of x^2", "2x"),
                step("IMPLICIT_DIFF", "d/dx of y^2",
                     "2y·y' (chain rule: y depends on x)"),
                step("REWRITE", "2x + 2y·y' = 0"),
                step("EQ_OP_BOTH", "subtract", "2x", "2y·y'", "-2x"),
                step("EQ_OP_BOTH", "divide", "2y", "y'", "-x/y"),
                step("REWRITE", "dy/dx = -x/y"),
            ]
            if at_point:
                val = Fraction(-x0, y0)
                steps.append(step("SUBST", "(x, y)", f"({x0}, {y0})",
                                  f"-({x0})/({y0})"))
                steps.append(step("FRAC_REDUCE", f"{-x0}/{y0}", val))
                answer = f"dy/dx = {val}"
                problem = (f"Find dy/dx for {eq} at the point "
                           f"({x0}, {y0}).")
            else:
                answer = "dy/dx = -x/y"
                problem = f"Find dy/dx for {eq}."
        elif variant == "cubes":
            c = random.choice([9, 16, 28, 35, 65, 91, 126, 133])
            eq = f"x^3 + y^3 = {c}"
            steps = [
                step("IMPLICIT_SETUP", eq, "dy/dx"),
                step("IMPLICIT_DIFF", "d/dx of x^3", "3x^2"),
                step("IMPLICIT_DIFF", "d/dx of y^3", "3y^2·y'"),
                step("REWRITE", "3x^2 + 3y^2·y' = 0"),
                step("EQ_OP_BOTH", "subtract", "3x^2", "3y^2·y'",
                     "-3x^2"),
                step("EQ_OP_BOTH", "divide", "3y^2", "y'", "-x^2/y^2"),
            ]
            answer = "dy/dx = -x^2/y^2"
            steps.append(step("REWRITE", answer))
            problem = f"Find dy/dx for {eq}."
        elif variant == "product":
            c = random.choice([v for v in range(-12, 13) if v != 0])
            eq = f"xy = {c}"
            steps = [
                step("IMPLICIT_SETUP", eq, "dy/dx"),
                step("IMPLICIT_DIFF", "d/dx of xy",
                     "y + x·y' (product rule)"),
                step("REWRITE", "y + x·y' = 0"),
                step("EQ_OP_BOTH", "subtract", "y", "x·y'", "-y"),
                step("EQ_OP_BOTH", "divide", "x", "y'", "-y/x"),
            ]
            answer = "dy/dx = -y/x"
            steps.append(step("REWRITE", answer))
            problem = f"Find dy/dx for {eq}."
        else:
            c = random.choice([3, 7, 12, 13, 19, 21, 27])
            eq = f"x^2 + xy + y^2 = {c}"
            steps = [
                step("IMPLICIT_SETUP", eq, "dy/dx"),
                step("IMPLICIT_DIFF", "d/dx of x^2", "2x"),
                step("IMPLICIT_DIFF", "d/dx of xy",
                     "y + x·y' (product rule)"),
                step("IMPLICIT_DIFF", "d/dx of y^2", "2y·y'"),
                step("REWRITE", "2x + y + x·y' + 2y·y' = 0"),
                step("REWRITE", "(x + 2y)·y' = -(2x + y)"),
                step("EQ_OP_BOTH", "divide", "x + 2y", "y'",
                     "-(2x + y)/(x + 2y)"),
            ]
            answer = "dy/dx = -(2x + y)/(x + 2y)"
            steps.append(step("REWRITE", answer))
            problem = f"Find dy/dx for {eq}."
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"implicit_diff_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
