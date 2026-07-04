import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.mutual_information_generator import MutualInformationGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"For joint distribution P\(X,Y\) with rows X=0\.\.(\d+) and columns "
    r"Y=0\.\.(\d+): rows=(\[.+\])\. Find (.+)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def list_text(values):
    return "[" + ",".join(fraction_text(value) for value in values) + "]"


def bit_unit(value):
    return "bit" if Fraction(value) == 1 else "bits"


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    if not match:
        raise AssertionError(problem)
    max_row = int(match.group(1))
    max_col = int(match.group(2))
    rows_text = match.group(3)
    task = match.group(4)
    inner = rows_text[1:-1]
    rows = []
    for row_text in inner.split(";"):
        row_inner = row_text[1:-1]
        rows.append([Fraction(piece) for piece in row_inner.split(",")])
    self_check = (len(rows) == max_row + 1 and
                  all(len(row) == max_col + 1 for row in rows))
    if not self_check:
        raise AssertionError(problem)
    return rows, task


def table_text(table):
    return "rows=[" + ";".join(list_text(row) for row in table) + "]"


def add_sum_steps(steps, values):
    running = values[0]
    for value in values[1:]:
        new_running = running + value
        steps.append(make_step("A", fraction_text(running),
                               fraction_text(value),
                               fraction_text(new_running)))
        running = new_running
    return running


def log2_power(probability):
    value = Fraction(probability)
    exponent = 0
    while value < 1:
        value *= 2
        exponent -= 1
    if value != 1:
        raise AssertionError(f"not a power of two: {probability}")
    return exponent


def entropy_steps(steps, label, probabilities):
    steps.append(make_step("ENTROPY_SETUP", label, "-sum p log2(p)"))
    running = Fraction(0)
    for probability in probabilities:
        if probability == 0:
            steps.append(make_step("ENTROPY_SKIP", label, "p=0"))
            continue
        self_information = -log2_power(probability)
        term = probability * self_information
        steps.append(make_step("LOG2", fraction_text(probability),
                               -self_information))
        steps.append(make_step("M", fraction_text(probability),
                               self_information, fraction_text(term)))
        new_running = running + term
        steps.append(make_step("A", fraction_text(running),
                               fraction_text(term),
                               fraction_text(new_running)))
        running = new_running
    return running


def trace(table, task):
    steps = [make_step("MI_SETUP", table_text(table), f"task={task}")]
    rows = len(table)
    cols = len(table[0])
    cells = [value for row in table for value in row]
    px = []
    for row in range(rows):
        values = table[row]
        steps.append(make_step("MARGINAL", f"P(X={row})=row{row} sum"))
        px.append(add_sum_steps(steps, values))
    py = []
    for col in range(cols):
        values = [table[row][col] for row in range(rows)]
        steps.append(make_step("MARGINAL", f"P(Y={col})=col{col} sum"))
        py.append(add_sum_steps(steps, values))
    hx = entropy_steps(steps, "H(X)", px)
    hy = entropy_steps(steps, "H(Y)", py)
    hxy = entropy_steps(steps, "H(X,Y)", cells)
    steps.append(make_step("COND_ENTROPY", "H(Y given X)=H(X,Y)-H(X)"))
    hy_given_x = hxy - hx
    steps.append(make_step("S", fraction_text(hxy), fraction_text(hx),
                           fraction_text(hy_given_x)))
    steps.append(make_step("MI_FORMULA", "I=H(X)+H(Y)-H(X,Y)"))
    hx_plus_hy = hx + hy
    steps.append(make_step("A", fraction_text(hx), fraction_text(hy),
                           fraction_text(hx_plus_hy)))
    mutual_information = hx_plus_hy - hxy
    steps.append(make_step("S", fraction_text(hx_plus_hy), fraction_text(hxy),
                           fraction_text(mutual_information)))
    return steps, {
        "H(X,Y)": hxy,
        "H(Y given X)": hy_given_x,
        "I(X;Y)": mutual_information,
    }


def answer_for(task, values):
    if task == "H(X,Y)":
        value = values["H(X,Y)"]
        return f"H(X,Y)={fraction_text(value)} {bit_unit(value)}"
    if task == "H(Y given X)":
        value = values["H(Y given X)"]
        return f"H(Y given X)={fraction_text(value)} {bit_unit(value)}"
    if task == "I(X;Y)":
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


def expected_flow(example):
    table, task = parse_problem(example["problem"])
    steps, values = trace(table, task)
    answer = answer_for(task, values)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestMutualInformationGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = MutualInformationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(300):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_arithmetic_steps(self):
        for _ in range(200):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in MutualInformationGenerator.VARIANTS:
            result = MutualInformationGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"mutual_information_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            MutualInformationGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(200):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
