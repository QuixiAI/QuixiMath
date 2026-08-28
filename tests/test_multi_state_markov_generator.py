"""Independent matrix and Gaussian-elimination oracle for three-state chains."""
import random
import re
import unittest
from fractions import Fraction

from generators.multi_state_markov_generator import QUERIES, MultiStateMarkovGenerator
from helpers import DELIM


def ptext(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_row(text):
    return tuple(Fraction(value) for value in text.split(","))


def parse_matrix(body):
    match = re.search(r"P1=\(([^)]+)\); P2=\(([^)]+)\); P3=\(([^)]+)\)", body)
    assert match, body
    matrix = tuple(parse_row(row) for row in match.groups())
    assert all(sum(row, Fraction()) == 1 for row in matrix)
    return matrix


def solve_system(matrix, rhs):
    size = len(rhs)
    rows = [list(map(Fraction, matrix[row])) + [Fraction(rhs[row])]
            for row in range(size)]
    for column in range(size):
        pivot = next(row for row in range(column, size)
                     if rows[row][column] != 0)
        rows[column], rows[pivot] = rows[pivot], rows[column]
        divisor = rows[column][column]
        rows[column] = [value / divisor for value in rows[column]]
        for row in range(size):
            if row == column:
                continue
            factor = rows[row][column]
            rows[row] = [left - factor * right
                         for left, right in zip(rows[row], rows[column])]
    return [rows[row][-1] for row in range(size)]


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    matrix = parse_matrix(body)
    if variant == "two_step":
        match = re.search(r"Target: P\(X_2=(\d) given X_0=(\d)\)", body)
        end, start = (int(value) - 1 for value in match.groups())
        answer = ptext(sum((matrix[start][middle] * matrix[middle][end]
                            for middle in range(3)), Fraction()))
    elif variant == "path_probability":
        path = [int(value) - 1 for value in
                re.search(r"Target: P\(path ([\d→]+)\)", body).group(1).split("→")]
        probability = Fraction(1)
        for left, right in zip(path, path[1:]):
            probability *= matrix[left][right]
        answer = ptext(probability)
    elif variant == "hitting_prob_3state":
        # Boundary values h_1=0 and h_3=1 leave one exact first-step equation.
        answer = ptext(solve_system([[1 - matrix[1][1]]], [matrix[1][2]])[0])
    elif variant == "expected_hitting_time":
        coefficients = [[1 - matrix[0][0], -matrix[0][1]],
                        [-matrix[1][0], 1 - matrix[1][1]]]
        times = solve_system(coefficients, [1, 1])
        answer = f"E_1[T_3] = {ptext(times[0])}; E_2[T_3] = {ptext(times[1])}"
    elif variant == "stationary_3state":
        coefficients = [
            [matrix[0][0] - 1, matrix[1][0], matrix[2][0]],
            [matrix[0][1], matrix[1][1] - 1, matrix[2][1]],
            [1, 1, 1],
        ]
        stationary = solve_system(coefficients, [0, 0, 1])
        answer = "pi = (" + ", ".join(ptext(value) for value in stationary) + ")"
    else:
        initial = parse_row(re.search(r"Initial distribution v=\(([^)]+)\)", body).group(1))
        output = [sum((initial[start] * matrix[start][end]
                       for start in range(3)), Fraction()) for end in range(3)]
        answer = "after one step = (" + ", ".join(ptext(value) for value in output) + ")"
    return {"variant": variant, "query": query, "answer": answer}


class MultiStateMarkovGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(240767)

    def test_output_contract(self):
        example = MultiStateMarkovGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = MultiStateMarkovGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_steps_are_exact(self):
        generator = MultiStateMarkovGenerator()
        for _ in range(300):
            example = generator.generate()
            oracle_parts(example)
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]))

    def test_plan_two_step_example(self):
        matrix = ((Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)),
                  (Fraction(0), Fraction(1, 2), Fraction(1, 2)),
                  (Fraction(1, 3), Fraction(1, 3), Fraction(1, 3)))
        value = sum((matrix[0][middle] * matrix[middle][2]
                     for middle in range(3)), Fraction())
        self.assertEqual(value, Fraction(1, 3))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in MultiStateMarkovGenerator.VARIANTS:
            generator = MultiStateMarkovGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_multi_state_markov_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            MultiStateMarkovGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = MultiStateMarkovGenerator()
        for _ in range(250):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            rendered = "\n".join([example["problem"], *example["steps"],
                                   example["final_answer"]])
            self.assertNotRegex(rendered, r"1x|\^1\b|\+ 0|--|− -")
            for raw in example["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
