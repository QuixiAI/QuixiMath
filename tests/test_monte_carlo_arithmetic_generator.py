"""Independent integer and Fraction oracle for MonteCarloArithmeticGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.monte_carlo_arithmetic_generator import (
    QUERIES, MonteCarloArithmeticGenerator,
)
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


def lcg_parameters(body):
    match = re.search(r"x_\(n\+1\)=\((\d+)\*x_n\+(\d+)\) mod (\d+), x_0=(\d+)", body)
    return tuple(map(int, match.groups()))


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant in ("lcg_sequence", "lcg_period"):
        multiplier, increment, modulus, initial = lcg_parameters(body)
        if variant == "lcg_sequence":
            count = int(re.search(r"through x_(\d+)", body).group(1))
            values = []
            current = initial
            for _ in range(count):
                current = (multiplier * current + increment) % modulus
                values.append(current)
            uniforms = [Fraction(value, modulus) for value in values]
            answer = ("x = " + ", ".join(map(str, values)) + "; u = "
                      + ", ".join(ptext(value) for value in uniforms))
        else:
            seen, values = {}, []
            current = initial
            while current not in seen:
                seen[current] = len(values)
                values.append(current)
                current = (multiplier * current + increment) % modulus
            cycle = values[seen[current]:]
            answer = f"period {len(cycle)}; cycle " + ", ".join(map(str, cycle))
    elif variant == "inverse_transform_discrete":
        cdf_text = re.search(r"with cdf (.+?)\. Uniform input", body).group(1)
        cdf = [(int(index), Fraction(value)) for index, value in
               re.findall(r"F\((\d+)\)=(\d+(?:/\d+)?)", cdf_text)]
        u = Fraction(re.search(r"Uniform input u=(\d+(?:\.\d+|/\d+)?)", body).group(1))
        outcome = next(index for index, value in cdf if u <= value)
        answer = f"sampled outcome = {outcome}"
    elif variant == "inverse_transform_linear":
        bound = int(re.search(r"0≤x≤(\d+)", body).group(1))
        u = Fraction(re.search(r"Uniform input u=(\d+(?:/\d+)?)", body).group(1))
        root = next(Fraction(num, den) for den in range(1, 21)
                    for num in range(0, den + 1) if Fraction(num, den) ** 2 == u)
        answer = f"sample x = {ptext(bound * root)}"
    elif variant == "hit_or_miss_pi":
        point_text = re.search(r"sample points (.+?)\. A hit", body).group(1)
        points = [(Fraction(x), Fraction(y)) for x, y in
                  re.findall(r"\((\d+(?:/\d+)?),(\d+(?:/\d+)?)\)", point_text)]
        hits = sum(x * x + y * y <= 1 for x, y in points)
        answer = (f"hits = {hits} of {len(points)}; pi estimate = "
                  f"{ptext(Fraction(4 * hits, len(points)))}")
    else:
        sample_text = re.search(r"sampled outputs are (.+?)\. Target", body).group(1)
        samples = [Fraction(value) for value in sample_text.split(", ")]
        answer = f"estimate = {ptext(sum(samples, Fraction()) / len(samples))}"
    return {"variant": variant, "query": query, "answer": answer}


class MonteCarloArithmeticGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(240768)

    def test_output_contract(self):
        example = MonteCarloArithmeticGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = MonteCarloArithmeticGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_and_lcg_steps_are_exact(self):
        generator = MonteCarloArithmeticGenerator()
        for _ in range(300):
            example = generator.generate()
            oracle_parts(example)
            setup = next((raw for raw in example["steps"]
                          if raw.startswith("LCG_SETUP" + DELIM)), None)
            lcg = None
            if setup:
                match = re.search(r"a=(\d+), c=(\d+), m=(\d+)", setup)
                lcg = tuple(map(int, match.groups()))
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "POW":
                    match = re.fullmatch(r"base (\d+(?:/\d+)?), exponent (\d+)",
                                         fields[1])
                    self.assertIsNotNone(match, raw)
                    self.assertEqual(Fraction(match.group(1)) ** int(match.group(2)),
                                     Fraction(fields[2]))
                elif fields[0] == "ROOT":
                    self.assertEqual(Fraction(fields[2]) ** 2, Fraction(fields[1]))
                elif fields[0] == "LCG_STEP":
                    multiplier, increment, modulus = lcg
                    expression = re.fullmatch(r"\((\d+)\*(\d+)\+(\d+)\) mod (\d+)",
                                              fields[2])
                    self.assertIsNotNone(expression, raw)
                    a, previous, c, m = map(int, expression.groups())
                    self.assertEqual((a, c, m), lcg)
                    self.assertEqual((multiplier * previous + increment) % modulus,
                                     int(fields[3]))

    def test_plan_lcg_example(self):
        multiplier, increment, modulus, current = 5, 3, 16, 7
        values = []
        for _ in range(4):
            current = (multiplier * current + increment) % modulus
            values.append(current)
        self.assertEqual(values, [6, 1, 8, 11])

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in MonteCarloArithmeticGenerator.VARIANTS:
            generator = MonteCarloArithmeticGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_monte_carlo_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            MonteCarloArithmeticGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = MonteCarloArithmeticGenerator()
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
