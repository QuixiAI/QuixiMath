import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


VARIANTS = ["relu", "sigmoid", "gelu"]


def fraction_text(value):
    return str(Fraction(value))


class ActivationGenerator(ProblemGenerator):
    """
    Activation values, derivatives, and two-layer scalar chain rule.

    Computes y = w2 * a(w1*x + b1) + b2 and dy/dx = w2 * a'(z) * w1 for
    ReLU, sigmoid, or GELU. Sigmoid and GELU use z=0 cases so the provided
    exp/GELU values and derivatives are exact.

    Op-codes used:
    - ACT_SETUP / EXP_VALUE / ACT_VALUE / ACT_DERIV / MODEL_OUTPUT /
      CHAIN_DERIV
    - M / A / S / D (established/shared): affine pass, activation, chain rule
    - Z: preactivation, activation value, derivative, output, dy/dx
    """

    VARIANTS = VARIANTS

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        x = random.choice([value for value in range(-5, 6) if value != 0])
        w1 = random.choice([value for value in range(-5, 6) if value != 0])
        if variant == "relu":
            b1 = random.randint(-8, 8)
            while w1 * x + b1 == 0:
                b1 = random.randint(-8, 8)
        else:
            b1 = -w1 * x
        w2 = random.choice([value for value in range(-5, 6) if value != 0])
        b2 = random.randint(-6, 6)

        z_linear = w1 * x
        z = z_linear + b1
        steps = [
            step("ACT_SETUP", f"activation={variant}", f"x={x}",
                 f"w1={w1},b1={b1},w2={w2},b2={b2}"),
            step("M", w1, x, z_linear),
            step("A", z_linear, b1, z),
        ]
        if variant == "relu":
            activation = Fraction(max(0, z))
            derivative = Fraction(1 if z > 0 else 0)
            problem_extra = ""
        elif variant == "sigmoid":
            exp_value = Fraction(1)
            denom = 1 + exp_value
            activation = Fraction(1, denom)
            one_minus = 1 - activation
            derivative = activation * one_minus
            steps.extend([
                step("EXP_VALUE", "exp(-z)", fraction_text(exp_value)),
                step("A", 1, fraction_text(exp_value), denom),
                step("D", 1, denom, fraction_text(activation)),
                step("S", 1, fraction_text(activation),
                     fraction_text(one_minus)),
                step("M", fraction_text(activation), fraction_text(one_minus),
                     fraction_text(derivative)),
            ])
            problem_extra = " with provided exp(-z)=1"
        else:
            activation = Fraction(0)
            derivative = Fraction(1, 2)
            problem_extra = " with provided GELU(0)=0 and GELU'(0)=1/2"

        steps.extend([
            step("ACT_VALUE", variant, z, fraction_text(activation)),
            step("ACT_DERIV", variant, z, fraction_text(derivative)),
        ])
        hidden = w2 * activation
        output = hidden + b2
        derivative_partial = w2 * derivative
        chain = derivative_partial * w1
        steps.extend([
            step("M", w2, fraction_text(activation), fraction_text(hidden)),
            step("A", fraction_text(hidden), b2, fraction_text(output)),
            step("MODEL_OUTPUT", fraction_text(output)),
            step("M", w2, fraction_text(derivative),
                 fraction_text(derivative_partial)),
            step("M", fraction_text(derivative_partial), w1,
                 fraction_text(chain)),
            step("CHAIN_DERIV", "dy/dx", fraction_text(chain)),
        ])
        answer = (
            f"z={z}; a={fraction_text(activation)}; "
            f"a_prime={fraction_text(derivative)}; "
            f"y={fraction_text(output)}; dy_dx={fraction_text(chain)}"
        )
        steps.append(step("Z", answer))
        name = {"relu": "ReLU", "sigmoid": "sigmoid", "gelu": "GELU"}[variant]
        problem = (
            "For the two-layer scalar model y=w2*a(w1*x+b1)+b2 with "
            f"x={x}, w1={w1}, b1={b1}, w2={w2}, b2={b2}, use {name} "
            f"activation{problem_extra}. Compute activation value, activation "
            "derivative, y, and dy/dx."
        )
        return dict(
            problem_id=jid(),
            operation=f"activation_chain_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
