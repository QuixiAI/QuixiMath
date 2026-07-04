import random

from base_generator import ProblemGenerator
from helpers import step, jid


BASE_GAMMAS = {
    "gamma0": [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, -1, 0],
        [0, 0, 0, -1],
    ],
    "gamma1": [
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, -1, 0, 0],
        [-1, 0, 0, 0],
    ],
    "gamma3": [
        [0, 0, 1, 0],
        [0, 0, 0, -1],
        [-1, 0, 0, 0],
        [0, 1, 0, 0],
    ],
}
LABELS = ["gamma0", "gamma1", "gamma3"]
METRIC = {"gamma0": 1, "gamma1": -1, "gamma3": -1}


def mat_text(matrix):
    return str(matrix).replace(" ", "")


def permute_matrix(matrix, perm):
    return [[matrix[perm[i]][perm[j]] for j in range(4)] for i in range(4)]


def dot_expr(row, col):
    return " + ".join(f"{a}*{b}" for a, b in zip(row, col))


def dot_value(row, col):
    return sum(a * b for a, b in zip(row, col))


def eta_value(left, right):
    if left != right:
        return 0
    return METRIC[left]


class GammaMatrixGenerator(ProblemGenerator):
    """
    Small Dirac gamma-matrix algebra checks by explicit 4x4 multiplication.

    A real subset gamma0, gamma1, gamma3 is used, with simultaneous basis
    permutations for variety. Problems supply the actual matrices.

    Op-codes used:
    - GAMMA_SETUP: task, gamma labels, entry or trace target
    - MATRIX_PRODUCT: product being formed
    - DOT4: row-by-column 4-term dot product for a matrix entry
    - MATRIX_ENTRY_SUM: anticommutator entry addition
    - TRACE_ADD: cumulative trace from diagonal product entries
    - CLIFFORD_EXPECT / TRACE_EXPECT: metric-side expected value
    - CHECK: compare computed and expected values
    - Z: verified entry or trace value
    """

    VARIANTS = ["anticommutator_entry", "trace"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        left, right, gammas = self._pick_gammas()
        if variant == "anticommutator_entry":
            problem, steps, answer = self._generate_anticommutator_entry(
                left, right, gammas
            )
        else:
            problem, steps, answer = self._generate_trace(left, right, gammas)
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"gamma_matrix_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _pick_gammas(self):
        perm = list(range(4))
        random.shuffle(perm)
        gammas = {
            label: permute_matrix(matrix, perm)
            for label, matrix in BASE_GAMMAS.items()
        }
        return random.choice(LABELS), random.choice(LABELS), gammas

    def _dot_step(self, steps, product_name, left_matrix, right_matrix, row,
                  col):
        row_values = left_matrix[row]
        col_values = [right_matrix[k][col] for k in range(4)]
        value = dot_value(row_values, col_values)
        steps.append(
            step("DOT4", product_name, f"({row + 1},{col + 1})",
                 dot_expr(row_values, col_values), value)
        )
        return value

    def _generate_anticommutator_entry(self, left, right, gammas):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        eta = eta_value(left, right)
        ab_name = f"{left}{right}"
        ba_name = f"{right}{left}"
        steps = [
            step("GAMMA_SETUP", "anticommutator_entry",
                 f"{left},{right}", f"entry=({row + 1},{col + 1})"),
            step("MATRIX_PRODUCT", ab_name, f"{left}*{right}"),
        ]
        ab = self._dot_step(steps, ab_name, gammas[left], gammas[right],
                            row, col)
        steps.append(step("MATRIX_PRODUCT", ba_name, f"{right}*{left}"))
        ba = self._dot_step(steps, ba_name, gammas[right], gammas[left],
                            row, col)
        total = ab + ba
        expected = 2 * eta if row == col else 0
        steps.extend([
            step("MATRIX_ENTRY_SUM", f"({row + 1},{col + 1})",
                 f"{ab} + {ba}", total),
            step("CLIFFORD_EXPECT", f"2*eta={2 * eta}",
                 f"I_entry={1 if row == col else 0}", expected),
            step("CHECK", "anticommutator entry",
                 f"computed={total}", f"expected={expected}"),
        ])
        answer = (
            f"{{{left},{right}}}_({row + 1},{col + 1}) = {total}"
        )
        problem = (
            f"Given {left}={mat_text(gammas[left])} and "
            f"{right}={mat_text(gammas[right])} with "
            f"eta_{left[-1]}{right[-1]}={eta}, compute entry "
            f"({row + 1},{col + 1}) of {{{left},{right}}}="
            f"{left}*{right}+{right}*{left}."
        )
        return problem, steps, answer

    def _generate_trace(self, left, right, gammas):
        eta = eta_value(left, right)
        product_name = f"{left}{right}"
        steps = [
            step("GAMMA_SETUP", "trace", f"{left},{right}", "Tr(product)"),
            step("MATRIX_PRODUCT", product_name, f"{left}*{right}"),
        ]
        trace_total = 0
        for index in range(4):
            entry = self._dot_step(
                steps, product_name, gammas[left], gammas[right],
                index, index
            )
            next_total = trace_total + entry
            steps.append(
                step("TRACE_ADD", product_name, f"({index + 1},{index + 1})",
                     f"{trace_total} + {entry}", next_total)
            )
            trace_total = next_total
        expected = 4 * eta
        steps.extend([
            step("TRACE_EXPECT", f"4*eta_{left[-1]}{right[-1]}",
                 eta, expected),
            step("CHECK", "trace theorem",
                 f"computed={trace_total}", f"expected={expected}"),
        ])
        answer = f"Tr({left}*{right}) = {trace_total}"
        problem = (
            f"Given {left}={mat_text(gammas[left])} and "
            f"{right}={mat_text(gammas[right])} with "
            f"eta_{left[-1]}{right[-1]}={eta}, compute "
            f"Tr({left}*{right})."
        )
        return problem, steps, answer
