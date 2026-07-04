import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def vector_text(values):
    return "(" + ",".join(str(value) for value in values) + ")"


def fraction_vector_text(values):
    return "(" + ",".join(fraction_text(value) for value in values) + ")"


def log_vector_text(values):
    return "(" + ",".join(f"ln({fraction_text(value)})" for value in values) + ")"


def logits_text(temp, weights):
    return "(" + ",".join(f"{temp}*ln({weight})" for weight in weights) + ")"


class SoftmaxGradientGenerator(ProblemGenerator):
    """
    Exact softmax, log-softmax, cross-entropy, and p-y gradient.

    Logits are generated as z_i = T ln(w_i). After temperature scaling by T,
    exp(z_i / T) = w_i, so probabilities and gradients are exact fractions.

    Op-codes used:
    - SOFTMAX_SETUP / TEMP_SCALE / SOFTMAX_EXP / SOFTMAX_PROB /
      LOG_SOFTMAX / CROSS_ENTROPY / GRAD
    - A / D / S (established/shared): partition sum, probabilities, p-y
    - Z: probabilities, log-softmax, cross-entropy, gradient
    """

    def generate(self) -> dict:
        temp = random.choice([1, 2, 3])
        weights = random.sample(range(1, 10), 3)
        target = random.randint(1, 3)
        total = sum(weights)
        probs = [Fraction(weight, total) for weight in weights]
        log_probs = probs[:]
        ce = Fraction(total, weights[target - 1])
        labels = [1 if index == target - 1 else 0 for index in range(3)]
        grads = [probs[index] - labels[index] for index in range(3)]

        steps = [
            step("SOFTMAX_SETUP", f"z={logits_text(temp, weights)}",
                 f"T={temp}", f"target={target}"),
        ]
        for index, weight in enumerate(weights, start=1):
            steps.extend([
                step("TEMP_SCALE", f"z{index}/T", f"ln({weight})"),
                step("SOFTMAX_EXP", index, weight),
            ])
        running = 0
        for weight in weights:
            new_running = running + weight
            steps.append(step("A", running, weight, new_running))
            running = new_running
        for index, prob in enumerate(probs, start=1):
            steps.extend([
                step("D", weights[index - 1], total, fraction_text(prob)),
                step("SOFTMAX_PROB", index, fraction_text(prob)),
                step("LOG_SOFTMAX", index, f"ln({fraction_text(prob)})"),
            ])
        steps.append(step("CROSS_ENTROPY", f"target={target}",
                          f"ln({fraction_text(ce)})"))
        for index, grad in enumerate(grads, start=1):
            steps.extend([
                step("S", fraction_text(probs[index - 1]),
                     labels[index - 1], fraction_text(grad)),
                step("GRAD", index, fraction_text(grad)),
            ])

        answer = (
            f"p={fraction_vector_text(probs)}; "
            f"log_softmax={log_vector_text(log_probs)}; "
            f"CE=ln({fraction_text(ce)}); "
            f"grad={fraction_vector_text(grads)}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"Given logits z={logits_text(temp, weights)} with temperature "
            f"T={temp} and target class {target}, compute the "
            "temperature-scaled softmax, log-softmax, cross-entropy, and "
            "gradient p-y."
        )
        return dict(
            problem_id=jid(),
            operation="softmax_gradient_exact",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
