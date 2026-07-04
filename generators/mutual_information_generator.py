import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def list_text(values):
    return "[" + ",".join(fraction_text(value) for value in values) + "]"


def bit_unit(value):
    return "bit" if Fraction(value) == 1 else "bits"


def split_power_count(count, min_parts, max_parts):
    parts = [count]
    target = random.randint(min_parts, max_parts)
    while len(parts) < target:
        choices = [idx for idx, value in enumerate(parts) if value > 1]
        if not choices:
            break
        idx = random.choice(choices)
        value = parts.pop(idx)
        parts.extend([value // 2, value // 2])
    random.shuffle(parts)
    return parts


def random_profile():
    total = 2 ** random.randint(4, 9)
    row_counts = split_power_count(total, 2, 3)
    row_splits = [
        split_power_count(row_count, 1, min(2, row_count))
        for row_count in row_counts
    ]
    cols = sum(len(row) for row in row_splits)
    counts = [[0 for _ in range(cols)] for _ in row_splits]
    col = 0
    for row, split in enumerate(row_splits):
        for count in split:
            counts[row][col] = count
            col += 1
    col_order = list(range(cols))
    random.shuffle(col_order)
    shuffled = [
        [row[col_idx] for col_idx in col_order]
        for row in counts
    ]
    probabilities = [
        [Fraction(count, total) for count in row]
        for row in shuffled
    ]
    return probabilities


def table_text(table):
    return "rows=[" + ";".join(list_text(row) for row in table) + "]"


def add_sum_steps(steps, values):
    running = values[0]
    for value in values[1:]:
        new_running = running + value
        steps.append(step("A", fraction_text(running),
                          fraction_text(value), fraction_text(new_running)))
        running = new_running
    return running


def entropy_steps(steps, label, probabilities):
    steps.append(step("ENTROPY_SETUP", label, "-sum p log2(p)"))
    running = Fraction(0)
    for probability in probabilities:
        if probability == 0:
            steps.append(step("ENTROPY_SKIP", label, "p=0"))
            continue
        exponent = probability.denominator.bit_length() - 1
        term = probability * exponent
        steps.append(step("LOG2", fraction_text(probability), -exponent))
        steps.append(step("M", fraction_text(probability), exponent,
                          fraction_text(term)))
        new_running = running + term
        steps.append(step("A", fraction_text(running),
                          fraction_text(term), fraction_text(new_running)))
        running = new_running
    return running


class MutualInformationGenerator(ProblemGenerator):
    """
    Joint entropy, conditional entropy, and mutual information from joint tables.

    Every nonzero joint and marginal probability is a power of two, so all
    log2 terms are exact integers.

    Variants:
    - joint_entropy: report H(X,Y).
    - conditional_entropy: report H(Y given X)=H(X,Y)-H(X).
    - mutual_information: report I(X;Y)=H(X)+H(Y)-H(X,Y).
    - all_measures: report all three requested information measures.

    Op-codes used:
    - MI_SETUP / MARGINAL / ENTROPY_SETUP / ENTROPY_SKIP
    - LOG2 / COND_ENTROPY / MI_FORMULA
    - A / S / M (established/shared): exact sums, products, differences
    - Z: requested entropy or mutual-information value
    """

    VARIANTS = [
        "joint_entropy",
        "conditional_entropy",
        "mutual_information",
        "all_measures",
    ]

    TASKS = {
        "joint_entropy": "H(X,Y)",
        "conditional_entropy": "H(Y given X)",
        "mutual_information": "I(X;Y)",
        "all_measures": "H(X,Y), H(Y given X), and I(X;Y)",
    }

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        table = random_profile()
        task = self.TASKS[variant]
        steps, values = self._trace(table, task)
        answer = self._answer(variant, values)
        steps.append(step("Z", answer))
        rows = len(table)
        cols = len(table[0])
        problem = (
            f"For joint distribution P(X,Y) with rows X=0..{rows - 1} "
            f"and columns Y=0..{cols - 1}: {table_text(table)}. "
            f"Find {task}."
        )
        return dict(
            problem_id=jid(),
            operation=f"mutual_information_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _trace(self, table, task):
        steps = [step("MI_SETUP", table_text(table), f"task={task}")]
        rows = len(table)
        cols = len(table[0])
        cells = [value for row in table for value in row]
        px = []
        for row in range(rows):
            values = table[row]
            steps.append(step("MARGINAL", f"P(X={row})=row{row} sum"))
            px.append(add_sum_steps(steps, values))
        py = []
        for col in range(cols):
            values = [table[row][col] for row in range(rows)]
            steps.append(step("MARGINAL", f"P(Y={col})=col{col} sum"))
            py.append(add_sum_steps(steps, values))
        hx = entropy_steps(steps, "H(X)", px)
        hy = entropy_steps(steps, "H(Y)", py)
        hxy = entropy_steps(steps, "H(X,Y)", cells)
        steps.append(step("COND_ENTROPY", "H(Y given X)=H(X,Y)-H(X)"))
        hy_given_x = hxy - hx
        steps.append(step("S", fraction_text(hxy), fraction_text(hx),
                          fraction_text(hy_given_x)))
        steps.append(step("MI_FORMULA", "I=H(X)+H(Y)-H(X,Y)"))
        hx_plus_hy = hx + hy
        steps.append(step("A", fraction_text(hx), fraction_text(hy),
                          fraction_text(hx_plus_hy)))
        mutual_information = hx_plus_hy - hxy
        steps.append(step("S", fraction_text(hx_plus_hy), fraction_text(hxy),
                          fraction_text(mutual_information)))
        return steps, {
            "H(X)": hx,
            "H(Y)": hy,
            "H(X,Y)": hxy,
            "H(Y given X)": hy_given_x,
            "I(X;Y)": mutual_information,
        }

    def _answer(self, variant, values):
        if variant == "joint_entropy":
            value = values["H(X,Y)"]
            return f"H(X,Y)={fraction_text(value)} {bit_unit(value)}"
        if variant == "conditional_entropy":
            value = values["H(Y given X)"]
            return f"H(Y given X)={fraction_text(value)} {bit_unit(value)}"
        if variant == "mutual_information":
            value = values["I(X;Y)"]
            return f"I(X;Y)={fraction_text(value)} {bit_unit(value)}"
        hxy = values["H(X,Y)"]
        hy_given_x = values["H(Y given X)"]
        mutual_information = values["I(X;Y)"]
        return (
            f"H(X,Y)={fraction_text(hxy)} {bit_unit(hxy)}; "
            f"H(Y given X)={fraction_text(hy_given_x)} "
            f"{bit_unit(hy_given_x)}; "
            f"I(X;Y)={fraction_text(mutual_information)} "
            f"{bit_unit(mutual_information)}"
        )
