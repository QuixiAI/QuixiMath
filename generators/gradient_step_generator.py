import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


VARIANTS = ["two_sample", "three_sample"]


def fraction_text(value):
    return str(Fraction(value))


def pair_text(left, right):
    return f"({fraction_text(left)},{fraction_text(right)})"


def samples_text(samples):
    return "[" + ", ".join(f"({x},{y})" for x, y in samples) + "]"


class GradientStepGenerator(ProblemGenerator):
    """
    One gradient-descent step on linear-regression MSE loss.

    Variants:
    - two_sample: compute the MSE gradient from two training examples.
    - three_sample: compute the MSE gradient from three training examples.

    Op-codes used:
    - MSE_SETUP / MSE_FORMULA / MSE_SAMPLE / MSE_GRADIENT / GD_UPDATE
    - A / S / M / D / E (established/shared): exact prediction, loss,
      gradient, and update arithmetic
    - Z: loss, gradient, and updated weights
    """

    VARIANTS = VARIANTS

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        count = 2 if variant == "two_sample" else 3
        xs = random.sample(range(-3, 4), count)
        true_w0 = random.randint(-3, 3)
        true_w1 = random.choice([-3, -2, -1, 1, 2, 3])
        samples = []
        for x_value in xs:
            noise = random.choice([-2, -1, 0, 1, 2])
            y_value = true_w0 + true_w1 * x_value + noise
            samples.append((x_value, y_value))
        w0 = Fraction(random.randint(-3, 3))
        w1 = Fraction(random.randint(-3, 3))
        eta = Fraction(1, random.randint(3, 8))

        steps = [
            step("MSE_SETUP", "model y_hat=w0+w1*x",
                 f"samples={samples_text(samples)}",
                 f"w={pair_text(w0, w1)}, eta={fraction_text(eta)}"),
            step("MSE_FORMULA", "L=(1/n) sum r_i^2",
                 "grad=(2/n) sum r_i*[1,x_i]"),
        ]

        sum_squared = Fraction(0)
        sum_residual = Fraction(0)
        sum_residual_x = Fraction(0)
        for index, (x_value, y_value) in enumerate(samples, start=1):
            x_frac = Fraction(x_value)
            y_frac = Fraction(y_value)
            linear_term = w1 * x_frac
            prediction = w0 + linear_term
            residual = prediction - y_frac
            squared = residual ** 2
            new_sum_squared = sum_squared + squared
            new_sum_residual = sum_residual + residual
            residual_x = residual * x_frac
            new_sum_residual_x = sum_residual_x + residual_x
            steps.extend([
                step("M", fraction_text(w1), x_value,
                     fraction_text(linear_term)),
                step("A", fraction_text(w0), fraction_text(linear_term),
                     fraction_text(prediction)),
                step("S", fraction_text(prediction), y_value,
                     fraction_text(residual)),
                step("E", fraction_text(residual), 2,
                     fraction_text(squared)),
                step("A", fraction_text(sum_squared),
                     fraction_text(squared), fraction_text(new_sum_squared)),
                step("A", fraction_text(sum_residual),
                     fraction_text(residual), fraction_text(new_sum_residual)),
                step("M", fraction_text(residual), x_value,
                     fraction_text(residual_x)),
                step("A", fraction_text(sum_residual_x),
                     fraction_text(residual_x),
                     fraction_text(new_sum_residual_x)),
                step("MSE_SAMPLE", f"i={index}",
                     f"pred={fraction_text(prediction)}",
                     f"r={fraction_text(residual)}"),
            ])
            sum_squared = new_sum_squared
            sum_residual = new_sum_residual
            sum_residual_x = new_sum_residual_x

        n = len(samples)
        loss = sum_squared / n
        double_residual = 2 * sum_residual
        grad_w0 = double_residual / n
        double_residual_x = 2 * sum_residual_x
        grad_w1 = double_residual_x / n
        delta_w0 = eta * grad_w0
        new_w0 = w0 - delta_w0
        delta_w1 = eta * grad_w1
        new_w1 = w1 - delta_w1
        steps.extend([
            step("D", fraction_text(sum_squared), n, fraction_text(loss)),
            step("M", 2, fraction_text(sum_residual),
                 fraction_text(double_residual)),
            step("D", fraction_text(double_residual), n,
                 fraction_text(grad_w0)),
            step("M", 2, fraction_text(sum_residual_x),
                 fraction_text(double_residual_x)),
            step("D", fraction_text(double_residual_x), n,
                 fraction_text(grad_w1)),
            step("MSE_GRADIENT", f"g0={fraction_text(grad_w0)}",
                 f"g1={fraction_text(grad_w1)}"),
            step("M", fraction_text(eta), fraction_text(grad_w0),
                 fraction_text(delta_w0)),
            step("S", fraction_text(w0), fraction_text(delta_w0),
                 fraction_text(new_w0)),
            step("M", fraction_text(eta), fraction_text(grad_w1),
                 fraction_text(delta_w1)),
            step("S", fraction_text(w1), fraction_text(delta_w1),
                 fraction_text(new_w1)),
            step("GD_UPDATE", f"w_old={pair_text(w0, w1)}",
                 f"eta={fraction_text(eta)}",
                 f"w_new={pair_text(new_w0, new_w1)}"),
        ])
        answer = (
            f"loss={fraction_text(loss)}; "
            f"gradient={pair_text(grad_w0, grad_w1)}; "
            f"w_new={pair_text(new_w0, new_w1)}"
        )
        steps.append(step("Z", answer))
        problem = (
            "For linear model y_hat = w0 + w1*x with samples "
            f"{samples_text(samples)}, start at w={pair_text(w0, w1)}. "
            "Use MSE L=(1/n) sum (y_hat-y)^2 and learning rate "
            f"eta={fraction_text(eta)}. Compute one gradient-descent update."
        )
        return dict(
            problem_id=jid(),
            operation=f"gradient_step_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
