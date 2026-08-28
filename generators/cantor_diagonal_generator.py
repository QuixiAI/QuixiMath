"""Finite witnesses for Cantor's diagonal construction."""
import random

from base_generator import ProblemGenerator
from helpers import jid, step


FOUNDATIONS = True


QUERIES = {
    "binary_strings": (
        "Construct the diagonal string and a binary string absent from the list.",
        "Flip the diagonal bits to produce a new listed-length string.",
        "Use diagonalization to find a binary string not among the rows.",
        "Determine the diagonal and its bitwise-flipped witness.",
        "Build the anti-diagonal binary string and verify every row differs.",
    ),
    "decimal_digits": (
        "Construct the diagonal and the new decimal string.",
        "Apply the stated replacement rule to every diagonal digit.",
        "Use decimal diagonalization to produce a string absent from the list.",
        "Determine the diagonal digits and their replacements.",
        "Build the anti-diagonal decimal string and verify every row differs.",
    ),
    "function_table": (
        "Construct the diagonal and the new function prefix.",
        "Flip each diagonal table entry to define g on the shown inputs.",
        "Use diagonalization to produce a function prefix unlike every row.",
        "Determine the diagonal values and the corresponding values of g.",
        "Build g on the displayed inputs and verify it differs from every f_k.",
    ),
}


def distinct_rows(size, alphabet):
    rows = []
    seen = set()
    while len(rows) < size:
        row = "".join(random.choice(alphabet) for _ in range(size))
        if row not in seen:
            seen.add(row)
            rows.append(row)
    return rows


def diagonal(rows):
    return "".join(row[index] for index, row in enumerate(rows))


def binary_flip(value):
    return "1" if value == "0" else "0"


def decimal_replace(value):
    return "2" if value == "1" else "1"


class CantorDiagonalGenerator(ProblemGenerator):
    """Generate finite diagonal constructions over strings and functions."""

    VARIANTS = ("binary_strings", "decimal_digits", "function_table")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _binary_strings(self):
        size = random.randint(5, 10)
        rows = distinct_rows(size, "01")
        row_text = "; ".join(
            f"row {index + 1} = {row}" for index, row in enumerate(rows))
        problem = (f"Binary rows of length {size}, indexed 1 through {size}: "
                   f"{row_text}. Replace each diagonal bit by its opposite. "
                   f"{random.choice(QUERIES['binary_strings'])}")
        old = diagonal(rows)
        new = "".join(binary_flip(value) for value in old)
        steps = []
        for index, value in enumerate(old):
            replacement = new[index]
            steps.extend([step("DIAG", f"row {index + 1}", value),
                          step("FLIP", index + 1,
                               f"{value} → {replacement}")])
        steps.append(step("NEW_STRING", new))
        for index in range(size):
            steps.append(step("CHECK",
                              f"differs from row {index + 1} at position {index + 1}"))
        answer = f"diagonal {old}; new string {new}"
        return problem, steps, answer

    def _decimal_digits(self):
        size = random.randint(5, 9)
        rows = distinct_rows(size, "0123456789")
        row_text = "; ".join(
            f"row {index + 1} = {row}" for index, row in enumerate(rows))
        problem = (f"Decimal rows of length {size}, indexed 1 through {size}: "
                   f"{row_text}. Replace a diagonal digit d by 1 unless d = 1, "
                   "in which case replace it by 2. "
                   f"{random.choice(QUERIES['decimal_digits'])}")
        old = diagonal(rows)
        new = "".join(decimal_replace(value) for value in old)
        steps = []
        for index, value in enumerate(old):
            replacement = new[index]
            steps.extend([step("DIAG", f"row {index + 1}", value),
                          step("FLIP", index + 1,
                               f"{value} → {replacement}")])
        steps.append(step("NEW_STRING", new))
        for index in range(size):
            steps.append(step("CHECK",
                              f"differs from row {index + 1} at position {index + 1}"))
        answer = f"diagonal {old}; new string {new}"
        return problem, steps, answer

    def _function_table(self):
        size = random.randint(5, 10)
        rows = distinct_rows(size, "01")
        row_text = "; ".join(
            f"f{index} = {row}" for index, row in enumerate(rows))
        problem = (f"For functions f0 through f{size - 1} from ℕ to "
                   f"{{0, 1}}, the columns shown are inputs 0 through "
                   f"{size - 1}: {row_text}. Define g(k) = 1 − f_k(k) on "
                   "the shown inputs. "
                   f"{random.choice(QUERIES['function_table'])}")
        old = diagonal(rows)
        new = "".join(binary_flip(value) for value in old)
        steps = []
        for index, value in enumerate(old):
            replacement = new[index]
            steps.extend([step("DIAG", f"f{index}({index})", value),
                          step("FLIP", index,
                               f"{value} → {replacement}")])
        steps.append(step("NEW_STRING", new))
        for index in range(size):
            steps.append(step("CHECK", f"g differs from f{index} at input {index}"))
        answer = f"diagonal {old}; new function prefix {new}"
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "binary_strings":
            problem, steps, answer = self._binary_strings()
        elif variant == "decimal_digits":
            problem, steps, answer = self._decimal_digits()
        else:
            problem, steps, answer = self._function_table()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"cantor_diagonal_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
