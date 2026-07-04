import random

from base_generator import ProblemGenerator
from helpers import step, jid


def seq_text(values):
    return "[" + ",".join(str(value) for value in values) + "]"


def convolution(x_values, h_values):
    output = []
    for index in range(len(x_values) + len(h_values) - 1):
        total = 0
        for j, x_value in enumerate(x_values):
            h_index = index - j
            if 0 <= h_index < len(h_values):
                total += x_value * h_values[h_index]
        output.append(total)
    return output


class ConvolutionGenerator(ProblemGenerator):
    """
    Discrete convolution of short finite sequences.

    Op-codes used:
    - CONV_SETUP: input sequences
    - CONV_WINDOW: terms contributing to one output index
    - CONV_SUM: output value for a one-term window
    - M / A (established/shared): exact product and sum arithmetic
    - Z: full convolution sequence
    """

    def generate(self) -> dict:
        x_len = random.randint(3, 5)
        h_len = random.randint(3, 5)
        x_values = [random.randint(0, 9) for _ in range(x_len)]
        h_values = [random.randint(0, 9) for _ in range(h_len)]
        y_values = convolution(x_values, h_values)

        steps = [
            step("CONV_SETUP", f"x={seq_text(x_values)}",
                 f"h={seq_text(h_values)}"),
        ]
        for index in range(len(y_values)):
            terms = []
            products = []
            for j, x_value in enumerate(x_values):
                h_index = index - j
                if 0 <= h_index < len(h_values):
                    terms.append(f"x{j}*h{h_index}")
                    product = x_value * h_values[h_index]
                    products.append(product)
            steps.append(step("CONV_WINDOW", f"n={index}",
                              " + ".join(terms)))
            for term_index, product in enumerate(products):
                j_terms = terms[term_index]
                x_part, h_part = j_terms.split("*")
                x_index = int(x_part[1:])
                h_index = int(h_part[1:])
                steps.append(step("M", x_values[x_index], h_values[h_index],
                                  product))
            if len(products) == 1:
                steps.append(step("CONV_SUM", f"n={index}", products[0]))
            else:
                running = products[0]
                for product in products[1:]:
                    new_running = running + product
                    steps.append(step("A", running, product, new_running))
                    running = new_running
        answer = f"y={seq_text(y_values)}"
        steps.append(step("Z", answer))
        problem = (
            f"Compute the discrete convolution of x={seq_text(x_values)} "
            f"and h={seq_text(h_values)}."
        )
        return dict(
            problem_id=jid(),
            operation="discrete_convolution",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
