import random
from base_generator import ProblemGenerator
from helpers import step, jid

# value string -> solutions in [0, 360) per function
SOLUTIONS = {
    "sin": {"0": [0, 180], "1/2": [30, 150], "√2/2": [45, 135],
            "√3/2": [60, 120], "1": [90], "-1/2": [210, 330],
            "-√2/2": [225, 315], "-√3/2": [240, 300], "-1": [270]},
    "cos": {"0": [90, 270], "1/2": [60, 300], "√2/2": [45, 315],
            "√3/2": [30, 330], "1": [0], "-1/2": [120, 240],
            "-√2/2": [135, 225], "-√3/2": [150, 210], "-1": [180]},
    "tan": {"0": [0, 180], "1": [45, 225], "√3": [60, 240],
            "√3/3": [30, 210], "-1": [135, 315], "-√3": [120, 300],
            "-√3/3": [150, 330]},
}

# doubled magnitudes for the '2 fn x - K = 0' rendering
DOUBLE = {"1/2": "1", "√2/2": "√2", "√3/2": "√3", "1": "2", "0": "0"}

# quadratic catalog: (a, b, c, factor text template, root value strings)
QUADS = [
    (2, -1, -1, "(2U + 1)(U - 1)", ["-1/2", "1"]),
    (2, 1, -1, "(2U - 1)(U + 1)", ["1/2", "-1"]),
    (2, -3, 1, "(2U - 1)(U - 1)", ["1/2", "1"]),
    (2, 3, 1, "(2U + 1)(U + 1)", ["-1/2", "-1"]),
    (1, -1, 0, "U(U - 1)", ["0", "1"]),
    (1, 0, -1, "(U - 1)(U + 1)", ["1", "-1"]),
]


class TrigEquationGenerator(ProblemGenerator):
    """
    Trig equations over [0°, 360°).

    Variants:
    - linear:    2 fn(x) - K = 0 -> fn(x) = table value -> reference
      angle plus quadrant placement
    - quadratic: a·fn²(x) + b·fn(x) + c = 0, factored via a stated
      substitution u = fn(x), each root placed on the circle, union of
      solutions ascending

    Op-codes used:
    - EQ_SETUP / EQ_OP_BOTH / REWRITE / ZERO_PRODUCT (established)
    - SUBST: u = fn(x) for the quadratic form (established)
    - EVAL: the isolated ratio value (established)
    - TABLE_LOOKUP: the reference angle (established)
    - SIGN_RULE: which quadrants carry the sign (established)
    - SOLUTIONS: the angles for one ratio value (equation, angles)
    - Z: 'x = a°, b°, ...' ascending
    """

    VARIANTS = ["linear", "quadratic"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _place_steps(steps, fn, v):
        """TABLE_LOOKUP + SIGN_RULE + SOLUTIONS for fn(x) = v."""
        sols = SOLUTIONS[fn][v]
        ref = v.lstrip("-")
        if v not in ("0", "1", "-1") or fn == "tan" and v != "0":
            if ref in ("1", "√3", "√3/3") and fn == "tan" or fn != "tan":
                steps.append(step("TABLE_LOOKUP",
                                  f"{fn} reference for {ref}",
                                  f"{SOLUTIONS[fn][ref][0]}°"))
        negative = v.startswith("-")
        if negative:
            quads = {"sin": "III and IV", "cos": "II and III",
                     "tan": "II and IV"}[fn]
            steps.append(step("SIGN_RULE", f"{fn} negative",
                              f"quadrants {quads}"))
        steps.append(step("SOLUTIONS", f"{fn} x = {v}",
                          ", ".join(f"{d}°" for d in sols)))
        return sols

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "linear":
            fn = random.choice(["sin", "cos", "tan"])
            if fn == "tan":
                v = random.choice(list(SOLUTIONS["tan"]))
                k = v.lstrip("-")
                sign = "+" if v.startswith("-") else "-"
                eq = f"tan x {sign} {k} = 0" if v != "0" \
                    else "tan x = 0"
                steps = [step("EQ_SETUP", eq, "solve on [0°, 360°)")]
                if v != "0":
                    steps.append(step("EQ_OP_BOTH",
                                      "add" if sign == "-" else "subtract",
                                      k, "tan x", v))
                steps.append(step("EVAL", "tan x", v))
            else:
                v = random.choice([w for w in SOLUTIONS[fn] if w != "0"])
                k = DOUBLE[v.lstrip("-")]
                sign = "+" if v.startswith("-") else "-"
                eq = f"2 {fn} x {sign} {k} = 0"
                steps = [
                    step("EQ_SETUP", eq, "solve on [0°, 360°)"),
                    step("EQ_OP_BOTH",
                         "add" if sign == "-" else "subtract", k,
                         f"2 {fn} x",
                         k if sign == "-" else f"-{k}"),
                    step("EQ_OP_BOTH", "divide", 2, f"{fn} x", v),
                    step("EVAL", f"{fn} x", v),
                ]
            sols = self._place_steps(steps, fn, v)
            answer = "x = " + ", ".join(f"{d}°" for d in sorted(sols))
            steps.append(step("Z", answer))
            problem = f"Solve {eq} for 0° ≤ x < 360°."
            return self._pack("trig_equation_linear", problem, steps,
                              answer)

        fn = random.choice(["sin", "cos"])
        a, b, c, ftxt, roots = random.choice(QUADS)
        u = f"{fn} x"

        eq = f"{a if a > 1 else ''}{fn}^2 x"
        if b:
            eq += f" {'+' if b > 0 else '-'} " + \
                (f"{abs(b)} " if abs(b) > 1 else "") + f"{fn} x"
        if c:
            eq += f" {'+' if c > 0 else '-'} {abs(c)}"
        eq += " = 0"

        factored = ftxt.replace("U", f"{fn} x")
        steps = [
            step("EQ_SETUP", eq, "solve on [0°, 360°)"),
            step("SUBST", "u", f"{fn} x",
                 f"{a if a > 1 else ''}u^2 "
                 f"{'+' if b > 0 else '-'} "
                 f"{abs(b) if abs(b) > 1 else ''}u "
                 f"{'+' if c > 0 else '-'} {abs(c)} = 0"
                 if b and c else f"substitute u = {fn} x"),
            step("REWRITE", f"{factored} = 0"),
            step("ZERO_PRODUCT", f"{factored} = 0",
                 " or ".join(f"{fn} x = {r}" for r in roots)),
        ]
        all_sols = []
        for r in roots:
            all_sols.extend(self._place_steps(steps, fn, r))
        answer = "x = " + ", ".join(f"{d}°" for d in sorted(all_sols))
        steps.append(step("Z", answer))
        problem = f"Solve {eq} for 0° ≤ x < 360°."
        return self._pack("trig_equation_quadratic", problem, steps,
                          answer)

    @staticmethod
    def _pack(op, problem, steps, answer):
        return dict(
            problem_id=jid(),
            operation=op,
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
