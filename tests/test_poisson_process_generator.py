"""Problem-text oracle for PoissonProcessGenerator."""
import math
import random
import re
import unittest
from fractions import Fraction

from generators.poisson_process_generator import QUERIES, PoissonProcessGenerator
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


def hour_value(text):
    return Fraction(re.fullmatch(r"(\d+(?:/\d+)?) hours?", text).group(1))


def parse_supplied(body):
    match = re.search(r"Supplied value: (e\^.+?) = (\d+\.\d{4})\.", body)
    assert match, body
    return match.group(1), Fraction(match.group(2))


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant in ("count_in_interval", "no_event_interval",
                   "interarrival_within", "time_to_second"):
        rate = Fraction(re.search(r"rate lambda=(\d+) per hour", body).group(1))
        duration = hour_value(re.search(r"minutes \(([^)]+)\)", body).group(1))
        mu = rate * duration
        label, supplied = parse_supplied(body)
        expected_label = (f"e^-{mu.numerator}" if mu.denominator == 1 and mu != 1
                          else f"e^(-{ptext(mu)})")
        assert label == expected_label
        if variant == "count_in_interval":
            k = int(re.search(r"Target: P\(N\(t\)=(\d+)\)", body).group(1))
            value = supplied * mu ** k / math.factorial(k)
            answer = f"{float(value):.4f}"
        elif variant == "no_event_interval":
            answer = f"{float(supplied):.4f}"
        elif variant == "interarrival_within":
            answer = f"{float(1 - supplied):.4f}"
        else:
            answer = f"{float(1 - supplied * (1 + mu)):.4f}"
    elif variant == "thinning_rate":
        rate = Fraction(re.search(r"base rate lambda=(\d+) per hour", body).group(1))
        probability = Fraction(re.search(r"probability p=(\d+(?:/\d+)?)", body).group(1))
        duration = hour_value(re.search(r"length is t=([^\.]+(?:hours?|hour))\.", body).group(1))
        thinned = rate * probability
        mean = thinned * duration
        answer = (f"type-A rate = {ptext(thinned)} per hour; "
                  f"expected type-A count = {ptext(mean)}")
    elif variant == "superposition_rate":
        match = re.search(r"lambda_1=(\d+(?:/\d+)?) per hour and lambda_2="
                          r"(\d+(?:/\d+)?) per hour", body)
        first, second = map(Fraction, match.groups())
        duration = hour_value(re.search(r"length is t=([^\.]+(?:hours?|hour))\.", body).group(1))
        total = first + second
        answer = (f"combined rate = {ptext(total)} per hour; "
                  f"expected total count = {ptext(total * duration)}")
    elif variant == "which_type_first":
        match = re.search(r"lambda_A=(\d+(?:/\d+)?) per hour and lambda_B="
                          r"(\d+(?:/\d+)?) per hour", body)
        first, second = map(Fraction, match.groups())
        answer = ptext(first / (first + second))
    else:
        rate = Fraction(re.search(r"rate lambda=(\d+(?:/\d+)?) per hour", body).group(1))
        duration = hour_value(re.search(r"length t=([^\.]+(?:hours?|hour))\.", body).group(1))
        mu = rate * duration
        answer = f"E[N(t)] = {ptext(mu)}; Var(N(t)) = {ptext(mu)}"
    return {"variant": variant, "query": query, "answer": answer}


class PoissonProcessGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(240763)

    def test_output_contract(self):
        example = PoissonProcessGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = PoissonProcessGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_factorial_and_power_steps_are_exact(self):
        generator = PoissonProcessGenerator()
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
                elif fields[0] == "FACT":
                    self.assertEqual(math.factorial(int(fields[1])), int(fields[2]))
                elif fields[0] == "POW":
                    match = re.fullmatch(r"base (\d+(?:/\d+)?), exponent (\d+)",
                                         fields[1])
                    self.assertIsNotNone(match, raw)
                    self.assertEqual(Fraction(match.group(1)) ** int(match.group(2)),
                                     Fraction(fields[2]))
                elif fields[0] == "ROUND":
                    self.assertEqual(f"{float(Fraction(fields[1])):.4f}", fields[3])

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in PoissonProcessGenerator.VARIANTS:
            generator = PoissonProcessGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_poisson_process_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            PoissonProcessGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = PoissonProcessGenerator()
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
