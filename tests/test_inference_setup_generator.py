"""Independent scenario-inversion oracle for InferenceSetupGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.inference_setup_generator import (
    QUERIES, SCENARIOS, InferenceSetupGenerator,
)
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def exact_text(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    denominator = value.denominator
    twos = fives = 0
    while denominator % 2 == 0:
        denominator //= 2
        twos += 1
    while denominator % 5 == 0:
        denominator //= 5
        fives += 1
    if denominator != 1:
        return str(value)
    places = max(twos, fives)
    scaled = value.numerator * 2 ** (places - twos) * 5 ** (places - fives)
    sign = "-" if scaled < 0 else ""
    digits = str(abs(scaled)).rjust(places + 1, "0")
    return (sign + digits[:-places] + "." + digits[-places:]).rstrip("0").rstrip(".")


def ceil_fraction(value):
    value = Fraction(value)
    return -(-value.numerator // value.denominator)


def relation_parts(body):
    relation, tail = next(
        values for phrase, values in {
            "less than": ("<", "left-tailed"),
            "greater than": (">", "right-tailed"),
            "different from": ("≠", "two-tailed"),
        }.items() if phrase in body)
    return relation, tail


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "state_hypotheses":
        description, null_text = re.search(
            r"target quantity is (.+)\. Its historical value is "
            r"(\d+(?:\.\d+)?)\.", body).groups()
        parameter = "p" if description.startswith("the proportion") else "μ"
        relation, tail = relation_parts(body)
        answer = (f"H0: {parameter} = {null_text}; Ha: {parameter} {relation} "
                  f"{null_text}; {tail}")
    elif variant == "parameter_identify":
        description = re.search(r"study will estimate (.+)\. The target", body).group(1)
        parameter = "p" if description.startswith("the proportion") else "μ"
        answer = f"{parameter}; {description}"
    elif variant == "type_I_II_describe":
        parameter, null_text, alt_parameter, relation, alt_null = re.search(
            r"uses H0: ([pμ]) = (\d+(?:\.\d+)?); Ha: ([pμ]) ([<>≠]) "
            r"(\d+(?:\.\d+)?)\. Error described: (.+)\.", body).groups()[:5]
        match = re.search(r"Error described: (.+)\.$", body)
        consequence = match.group(1)
        assert parameter == alt_parameter and null_text == alt_null
        type_i = (f"concluding {parameter} {relation} {null_text} when "
                  f"{parameter} = {null_text}")
        type_ii = (f"failing to conclude {parameter} {relation} {null_text} when "
                   f"{parameter} {relation} {null_text}")
        if consequence == type_i:
            error_type = "Type I"
        else:
            assert consequence == type_ii
            error_type = "Type II"
        answer = f"{error_type}; {consequence}"
    elif variant == "np_condition":
        n, p = re.search(r"sample has n = (\d+) and null proportion p = "
                         r"(\d+(?:/\d+)?)", body).groups()
        n, p = int(n), Fraction(p)
        successes, failures = n * p, n * (1 - p)
        ok = successes >= 10 and failures >= 10
        rs, rf = ("≥" if successes >= 10 else "<",
                  "≥" if failures >= 10 else "<")
        answer = (f"{'ok' if ok else 'fails'}; np = {exact_text(successes)} {rs} 10, "
                  f"n(1 − p) = {exact_text(failures)} {rf} 10")
    elif variant == "ten_percent_condition":
        n, population = map(int, re.search(
            r"sample of n = (\d+) is drawn without replacement from a population "
            r"of N = (\d+)", body).groups())
        limit = Fraction(population, 10)
        ok = n <= limit
        relation = "≤" if ok else ">"
        answer = (f"{'ok' if ok else 'fails'}; n = {n} {relation} "
                  f"N/10 = {exact_text(limit)}")
    elif variant == "clt_condition":
        shape, n = re.search(r"population shape is ([a-z-]+) and independent "
                             r"random samples have n = (\d+)", body).groups()
        n = int(n)
        if shape == "normal":
            answer = "ok; population normal"
        elif n >= 30:
            answer = f"ok; n = {n} ≥ 30"
        else:
            answer = f"fails; population shape {shape} and n = {n} < 30"
    else:
        p = Fraction(re.search(r"null proportion is p = (\d+(?:/\d+)?)", body).group(1))
        needed_success = ceil_fraction(Fraction(10, 1) / p)
        needed_failure = ceil_fraction(Fraction(10, 1) / (1 - p))
        answer = str(max(needed_success, needed_failure))
    return {"variant": variant, "query": query, "answer": answer, "body": body}


class InferenceSetupGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(751309)

    def test_output_contract(self):
        example = InferenceSetupGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_1000_answers_from_problem_text(self):
        generator = InferenceSetupGenerator()
        for _ in range(1000):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_ceilings_and_maxima_are_exact(self):
        generator = InferenceSetupGenerator()
        for _ in range(600):
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
                elif fields[0] == "CEIL":
                    self.assertEqual(ceil_fraction(fields[1]), int(fields[2]), raw)
                elif fields[0] == "MAX":
                    self.assertEqual(max(int(fields[1]), int(fields[2])),
                                     int(fields[3]), raw)

    def test_hypothesis_scenarios_reach_every_template_and_direction(self):
        generator = InferenceSetupGenerator("state_hypotheses")
        descriptions, tails = set(), set()
        for _ in range(1800):
            example = generator.generate()
            parts = oracle_parts(example)
            descriptions.add(re.search(r"target quantity is (.+)\. Its historical",
                                       parts["body"]).group(1))
            tails.add(example["final_answer"].rsplit("; ", 1)[1])
        self.assertEqual(descriptions, {description for _, description in SCENARIOS})
        self.assertEqual(tails, {"left-tailed", "right-tailed", "two-tailed"})

    def test_both_error_types_are_reachable(self):
        generator = InferenceSetupGenerator("type_I_II_describe")
        seen = {generator.generate()["final_answer"].split(";", 1)[0]
                for _ in range(300)}
        self.assertEqual(seen, {"Type I", "Type II"})

    def test_numeric_conditions_reach_pass_and_fail(self):
        for variant in ("np_condition", "ten_percent_condition", "clt_condition"):
            generator = InferenceSetupGenerator(variant)
            seen = {generator.generate()["final_answer"].split(";", 1)[0]
                    for _ in range(500)}
            self.assertEqual(seen, {"ok", "fails"}, variant)

    def test_minimum_n_is_minimal_by_brute_force(self):
        generator = InferenceSetupGenerator("min_n_for_np")
        for _ in range(300):
            example = generator.generate()
            p = Fraction(re.search(r"p = (\d+(?:/\d+)?)",
                                   example["problem"]).group(1))
            n = int(example["final_answer"])
            self.assertGreaterEqual(n * p, 10)
            self.assertGreaterEqual(n * (1 - p), 10)
            self.assertTrue((n - 1) * p < 10 or (n - 1) * (1 - p) < 10)

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in InferenceSetupGenerator.VARIANTS:
            generator = InferenceSetupGenerator(variant)
            seen = set()
            for _ in range(300):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"statistics_inference_setup_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            InferenceSetupGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = InferenceSetupGenerator()
        for _ in range(400):
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
