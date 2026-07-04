import random

from base_generator import ProblemGenerator
from helpers import step, jid


def vector_text(values):
    return "(" + ",".join(str(value) for value in values) + ")"


def data_text(data):
    return "[" + ", ".join(f"({x},{y})" for x, y in data) + "]"


def bool_text(value):
    return "true" if value else "false"


class KernelPerceptronGenerator(ProblemGenerator):
    """
    One epoch of kernel perceptron updates in alpha-space.

    Uses a one-dimensional linear kernel K(x,z)=xz over three examples. The
    alpha vector starts at zero and alpha_i increments when y_i score_i <= 0.

    Op-codes used:
    - KP_SETUP / KP_EXAMPLE / KERNEL_VALUE / DECISION / UPDATE
    - CHECK (established): mistake/update criterion
    - M / A (established/shared): kernel terms, scores, alpha increments
    - Z: final alpha vector and update count
    """

    def generate(self) -> dict:
        xs = random.sample([value for value in range(-7, 8) if value != 0], 3)
        ys = [random.choice([-1, 1]) for _ in range(3)]
        data = list(zip(xs, ys))
        alphas = [0, 0, 0]
        updates = 0
        steps = [
            step("KP_SETUP", "kernel=linear", f"data={data_text(data)}",
                 "alpha0=(0,0,0)"),
        ]
        for i, (x_i, y_i) in enumerate(data):
            steps.append(step("KP_EXAMPLE", i + 1, f"x={x_i},y={y_i}",
                              f"alpha={vector_text(alphas)}"))
            terms = []
            for j, (x_j, y_j) in enumerate(data):
                kernel = x_j * x_i
                beta = alphas[j] * y_j
                term = beta * kernel
                steps.extend([
                    step("M", x_j, x_i, kernel),
                    step("KERNEL_VALUE", f"{j + 1},{i + 1}", kernel),
                    step("M", alphas[j], y_j, beta),
                    step("M", beta, kernel, term),
                    step("KP_TERM", f"j={j + 1}", term),
                ])
                terms.append(term)
            partial = terms[0] + terms[1]
            score = partial + terms[2]
            margin = y_i * score
            should_update = margin <= 0
            steps.extend([
                step("A", terms[0], terms[1], partial),
                step("A", partial, terms[2], score),
                step("DECISION", f"score_{i + 1}", score),
                step("M", y_i, score, margin),
                step("CHECK", "y*score <= 0", f"{margin} <= 0",
                     f"update={bool_text(should_update)}"),
            ])
            if should_update:
                new_alpha = alphas[i] + 1
                steps.append(step("A", alphas[i], 1, new_alpha))
                alphas[i] = new_alpha
                updates += 1
            steps.append(step("UPDATE", f"alpha{i + 1}", alphas[i]))
        answer = f"alpha={vector_text(alphas)}; updates={updates}"
        steps.append(step("Z", answer))
        problem = (
            "Run one epoch of the kernel perceptron with linear kernel "
            f"K(x,z)=xz on data {data_text(data)}, starting alpha=(0,0,0). "
            "Use update alpha_i += 1 when y_i score_i <= 0."
        )
        return dict(
            problem_id=jid(),
            operation="kernel_perceptron_one_epoch",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
