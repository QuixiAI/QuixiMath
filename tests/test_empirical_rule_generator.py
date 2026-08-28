"""Independent rule-table oracle for EmpiricalRuleGenerator prompts."""
import random
import re
import unittest
from fractions import Fraction

from generators.empirical_rule_generator import QUERIES, EmpiricalRuleGenerator
from helpers import DELIM


RULE = {1: Fraction(68), 2: Fraction(95), 3: Fraction(997, 10)}


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def text_number(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    assert value.denominator in (2, 4, 5, 10, 20, 25, 40, 50, 100)
    places = 1
    while (value * 10 ** places).denominator != 1:
        places += 1
    integer = int(abs(value) * 10 ** places)
    digits = str(integer).rjust(places + 1, "0")
    sign = "-" if value < 0 else ""
    return (sign + digits[:-places] + "." + digits[-places:]).rstrip("0").rstrip(".")


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    mean, sigma = map(int, re.search(r"X ~ N\((\d+), (\d+)\)", body).groups())
    if variant == "percent_within":
        low, high, left_k, right_k = map(int, re.search(
            r"Target region: from (\d+) to (\d+).+μ − (\d+)σ and μ \+ (\d+)σ",
            body,
        ).groups())
        assert left_k == right_k and low == mean - left_k * sigma
        assert high == mean + right_k * sigma
        answer = f"{text_number(RULE[left_k])}%"
    elif variant == "percent_tail":
        side, cutoff, repeated_side, sign, k = re.search(
            r"Target region: (above|below) (\d+), which is (above|below) μ "
            r"([+−]) (\d+)σ", body,
        ).groups()
        k = int(k)
        assert side == repeated_side
        expected_cutoff = (mean + k * sigma if side == "above"
                           else mean - k * sigma)
        assert int(cutoff) == expected_cutoff
        value = (100 - RULE[k]) / 2
        answer = f"{text_number(value)}%"
    elif variant == "interval_for_percent":
        percent = Fraction(re.search(r"Target central percent: ([0-9.]+)%", body)
                           .group(1))
        k = next(k for k, value in RULE.items() if value == percent)
        answer = f"({mean - k * sigma}, {mean + k * sigma})"
    elif variant == "count_of_n":
        size = int(re.search(r"Population size N = (\d+)", body).group(1))
        target = re.search(r"Target region: (.+)\.", body).group(1)
        if "within" in target:
            k = int(re.search(r"within (\d+)σ", target).group(1))
            percent = RULE[k]
        else:
            k = int(re.search(r"[+−] (\d+)σ", target).group(1))
            percent = (100 - RULE[k]) / 2
        count = Fraction(size) * percent / 100
        assert count.denominator == 1
        answer = str(count.numerator)
    else:
        low, left_k, high, right_k = map(int, re.search(
            r"Target region: from (\d+) = μ − (\d+)σ to (\d+) = μ \+ (\d+)σ",
            body,
        ).groups())
        assert low == mean - left_k * sigma and high == mean + right_k * sigma
        percent = RULE[left_k] / 2 + RULE[right_k] / 2
        answer = f"{text_number(percent)}%"
    return {"variant": variant, "query": query, "answer": answer}


class EmpiricalRuleGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(310018)

    def test_output_contract(self):
        example = EmpiricalRuleGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_700_answers_from_problem_text(self):
        generator = EmpiricalRuleGenerator()
        for _ in range(700):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_steps_are_exact(self):
        generator = EmpiricalRuleGenerator()
        for _ in range(450):
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

    def test_every_problem_supplies_all_rule_constants(self):
        generator = EmpiricalRuleGenerator()
        for _ in range(300):
            problem = generator.generate()["problem"]
            for text in ("68% within 1σ", "95% within 2σ",
                         "99.7% within 3σ"):
                self.assertIn(text, problem)

    def test_every_cutoff_is_exactly_mu_plus_or_minus_k_sigma(self):
        generator = EmpiricalRuleGenerator()
        for _ in range(350):
            example = generator.generate()
            oracle_parts(example)
            for raw in example["steps"]:
                if raw.startswith(f"ZSCORE{DELIM}"):
                    fields = raw.split(DELIM)
                    expression = fields[1]
                    cutoff, mean, sigma = map(int, re.fullmatch(
                        r"\((-?\d+) - (-?\d+)\)/(\d+)", expression
                    ).groups())
                    self.assertEqual(Fraction(cutoff - mean, sigma),
                                     Fraction(fields[2]), raw)

    def test_count_variant_always_has_an_integer_answer(self):
        generator = EmpiricalRuleGenerator("count_of_n")
        for _ in range(300):
            self.assertRegex(generator.generate()["final_answer"], r"^\d+$")

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in EmpiricalRuleGenerator.VARIANTS:
            generator = EmpiricalRuleGenerator(variant)
            seen = set()
            for _ in range(300):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"statistics_empirical_rule_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            EmpiricalRuleGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = EmpiricalRuleGenerator()
        for _ in range(350):
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
