import random
from base_generator import ProblemGenerator
from helpers import step, jid


class OptimizationGenerator(ProblemGenerator):
    """
    Optimization word problems built so every critical point is an
    integer: model, expand, differentiate, solve V' = 0 (rejecting the
    degenerate root by name), confirm with the second derivative test,
    and report the optimum.

    Variants:
    - barn_fence: A = x(P - 2x), three-sided fence
    - box:        V = x(W - 2x)², open-top box from a square sheet
    - product:    x + y = S, maximize x·y²

    Op-codes used:
    - OPT_SETUP: the scenario and the objective
    - REWRITE / POWER_RULE / FACTOR_GROUP / FACTOR_PAIR_GOAL / TRY /
      REJECT / ACCEPT / ZERO_PRODUCT (established)
    - SECOND_DERIV_TEST / SUBST / E / M / A / S / D / EVAL
      (established)
    - Z: the optimizer and the optimal value with units
    """

    VARIANTS = ["barn_fence", "box", "product"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "barn_fence":
            P = 4 * random.randint(10, 60)
            x = P // 4
            other = P - 2 * x
            area = x * other
            steps = [
                step("OPT_SETUP",
                     f"{P} m of fence, barn forms the fourth side; "
                     f"sides x, x, and {P} - 2x", "maximize area"),
                step("REWRITE", f"A = x({P} - 2x) = {P}x - 2x^2"),
                step("POWER_RULE", f"{P}x - 2x^2", f"{P} - 4x"),
                step("EQ_OP_BOTH", "add", "4x", f"{P}", "4x"),
                step("D", P, 4, x),
                step("SECOND_DERIV_TEST", "A'' = -4 < 0", "maximum"),
                step("S", P, 2 * x, other),
                step("M", x, other, area),
            ]
            answer = (f"x = {x} m, long side = {other} m; maximum "
                      f"area {area} m²")
            problem = (f"A farmer has {P} m of fence to enclose a "
                       f"rectangular field against a barn (the barn "
                       f"forms one side). What dimensions maximize the "
                       f"area, and what is that area?")
        elif variant == "box":
            W = 6 * random.randint(1, 5)
            xs = W // 6
            side = W - 2 * xs
            vol = xs * side * side
            steps = [
                step("OPT_SETUP",
                     f"square sheet {W} by {W}; cut corners x and fold",
                     "maximize volume"),
                step("REWRITE", f"V = x({W} - 2x)^2"),
                step("REWRITE",
                     f"V = 4x^3 - {4 * W}x^2 + {W * W}x"),
                step("POWER_RULE", f"4x^3 - {4 * W}x^2 + {W * W}x",
                     f"12x^2 - {8 * W}x + {W * W}"),
                # 12x² - 8Wx + W² = (2x - W)(6x - W)
                step("REWRITE", f"V' = (2x - {W})(6x - {W})"),
            ]
            steps.append(step("ZERO_PRODUCT",
                              f"(2x - {W})(6x - {W}) = 0",
                              f"x = {W // 2} or x = {W // 6}"))
            steps.append(step("REJECT", f"x = {W // 2}",
                              f"width {W} - 2({W // 2}) = 0, "
                              f"degenerate box"))
            steps.append(step("ACCEPT", f"x = {xs}",
                              "the only usable critical point"))
            steps.append(step("SUBST", "x", xs,
                              f"V = {xs}({W} - {2 * xs})^2"))
            steps.append(step("S", W, 2 * xs, side))
            steps.append(step("E", side, 2, side * side))
            steps.append(step("M", xs, side * side, vol))
            answer = f"x = {xs}; maximum volume {vol}"
            problem = (f"An open-top box is made from a {W} by {W} "
                       f"sheet by cutting squares of side x from the "
                       f"corners and folding. What x maximizes the "
                       f"volume, and what is that volume?")
        else:
            S = 3 * random.randint(2, 12)
            y = 2 * S // 3
            x = S - y
            best = x * y * y
            steps = [
                step("OPT_SETUP",
                     f"x + y = {S}, x, y > 0", "maximize P = x·y^2"),
                step("SUBST", "x", f"{S} - y",
                     f"P = ({S} - y)y^2 = {S}y^2 - y^3"),
                step("POWER_RULE", f"{S}y^2 - y^3",
                     f"{2 * S}y - 3y^2"),
                step("REWRITE", f"P' = y({2 * S} - 3y)"),
                step("ZERO_PRODUCT", f"y({2 * S} - 3y) = 0",
                     f"y = 0 or y = {y}"),
                step("REJECT", "y = 0", "gives zero product"),
                step("ACCEPT", f"y = {y}",
                     "the interior critical point"),
                step("S", S, y, x),
                step("E", y, 2, y * y),
                step("M", x, y * y, best),
            ]
            answer = f"x = {x}, y = {y}; maximum product {best}"
            problem = (f"Two positive numbers x and y satisfy "
                       f"x + y = {S}. Maximize x·y².")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"optimization_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
