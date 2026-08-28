"""One-step enumeration oracle for MartingaleCheckGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.martingale_check_generator import QUERIES, MartingaleCheckGenerator
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


def first_step_ruin(boundary, p):
    q = 1 - p
    size = boundary - 1
    rows = [[Fraction(int(row == column)) for column in range(size)]
            + [Fraction(0)] for row in range(size)]
    for state in range(1, boundary):
        row = state - 1
        if state > 1:
            rows[row][state - 2] -= q
        if state < boundary - 1:
            rows[row][state] -= p
        else:
            rows[row][-1] += p
    for column in range(size):
        pivot = next(row for row in range(column, size)
                     if rows[row][column])
        rows[column], rows[pivot] = rows[pivot], rows[column]
        divisor = rows[column][column]
        rows[column] = [value / divisor for value in rows[column]]
        for row in range(size):
            if row == column:
                continue
            factor = rows[row][column]
            rows[row] = [left - factor * right
                         for left, right in zip(rows[row], rows[column])]
    return [row[-1] for row in rows]


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant in ("drift_corrected", "quadratic", "exponential",
                   "not_martingale"):
        p = Fraction(re.search(r"probability p=(\d+(?:/\d+)?)", body).group(1))
        q = 1 - p
        match = re.search(r"At time n=(\d+), condition on S_\d+=(-?\d+)", body)
        n, state = map(int, match.groups())
        if variant == "drift_corrected":
            drift = p - q
            conditional = sum((weight * (state + increment - (n + 1) * drift)
                               for increment, weight in ((1, p), (-1, q))),
                              Fraction())
            current = state - n * drift
            assert conditional == current
            answer = (f"martingale; E[M_{n + 1} given S_{n} = {state}] = "
                      f"{ptext(conditional)} = M_{n}")
        elif variant == "quadratic":
            conditional = sum((weight * ((state + increment) ** 2 - (n + 1))
                               for increment, weight in ((1, p), (-1, q))),
                              Fraction())
            current = state ** 2 - n
            assert conditional == current
            answer = (f"martingale; E[M_{n + 1} given S_{n} = {state}] = "
                      f"{ptext(conditional)} = M_{n}")
        elif variant == "exponential":
            process = re.search(r"The process is M_k=\(([^)]+)\)\^S_k/"
                                r"\(([^)]+)\)\^k", body)
            base, normalizer = map(Fraction, process.groups())
            conditional = sum(
                (weight * base ** (state + increment) / normalizer ** (n + 1)
                 for increment, weight in ((1, p), (-1, q))), Fraction())
            current = base ** state / normalizer ** n
            assert conditional == current
            answer = (f"martingale; E[M_{n + 1} given S_{n} = {state}] = "
                      f"{ptext(conditional)} = M_{n}")
        else:
            expected = p * (state + 1) + q * (state - 1)
            kind = "submartingale" if expected > state else "supermartingale"
            relation = ">" if expected > state else "<"
            answer = f"{kind}; {ptext(expected)} {relation} {state}"
    elif variant == "optional_stopping_ruin":
        match = re.search(r"S_0=i=(\d+).*0 or N=(\d+)", body)
        initial, boundary = map(int, match.groups())
        p = Fraction(re.search(r"probability p=(\d+(?:/\d+)?)", body).group(1))
        probability = first_step_ruin(boundary, p)[initial - 1]
        ratio = (1 - p) / p
        answer = (f"P(S_tau=N) = {ptext(probability)}; exponential "
                  f"martingale M_k=({ptext(ratio)})^S_k")
    else:
        law = re.search(r"equal a=(\d+(?:/\d+)?) with probability "
                        r"p=(\d+(?:/\d+)?) and b=(\d+(?:/\d+)?) with "
                        r"probability q=(\d+(?:/\d+)?)", body)
        first, p, second, q = map(Fraction, law.groups())
        match = re.search(r"At time n=(\d+), condition on M_\d+=(\d+(?:/\d+)?)", body)
        n, current_text = match.groups()
        n, current = int(n), Fraction(current_text)
        conditional = p * current * first + q * current * second
        assert p * first + q * second == 1
        assert conditional == current
        answer = (f"martingale; E[M_{n + 1} given M_{n} = {ptext(current)}] "
                  f"= {ptext(conditional)} = M_{n}")
    return {"variant": variant, "query": query, "answer": answer}


class MartingaleCheckGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(240774)

    def test_output_contract(self):
        example = MartingaleCheckGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = MartingaleCheckGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_steps_are_exact(self):
        generator = MartingaleCheckGenerator()
        for _ in range(350):
            example = generator.generate()
            oracle_parts(example)
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "POW":
                    match = re.fullmatch(r"base (-?\d+(?:/\d+)?), exponent (-?\d+)",
                                         fields[1])
                    self.assertIsNotNone(match, raw)
                    self.assertEqual(Fraction(match.group(1)) ** int(match.group(2)),
                                     Fraction(fields[2]), raw)

    def test_plan_drift_example(self):
        p, q, state, n = Fraction(2, 3), Fraction(1, 3), 2, 4
        expected_position = p * 3 + q * 1
        self.assertEqual(expected_position, Fraction(7, 3))
        self.assertEqual(expected_position - Fraction(5, 3), Fraction(2, 3))
        self.assertEqual(state - Fraction(4, 3), Fraction(2, 3))

    def test_optional_stopping_matches_first_step_ruin(self):
        generator = MartingaleCheckGenerator("optional_stopping_ruin")
        for _ in range(120):
            example = generator.generate()
            self.assertEqual(example["final_answer"], oracle_parts(example)["answer"])

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in MartingaleCheckGenerator.VARIANTS:
            generator = MartingaleCheckGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_martingale_check_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            MartingaleCheckGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = MartingaleCheckGenerator()
        for _ in range(300):
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
