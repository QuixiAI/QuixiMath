"""Independent problem-text oracle for SlopeInferenceGenerator."""
import math
import random
import re
import unittest
from fractions import Fraction

from generators.slope_inference_generator import (
    QUERIES, RAW_X_PATTERNS, SlopeInferenceGenerator,
)
from helpers import DELIM


def number(value):
    value = Fraction(value)
    denominator = value.denominator
    while denominator % 2 == 0:
        denominator //= 2
    while denominator % 5 == 0:
        denominator //= 5
    if denominator != 1:
        return str(value)
    return str(float(value)).rstrip("0").rstrip(".")


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def exact_root(value):
    root = math.isqrt(value)
    assert root * root == value
    return root


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "from_output":
        slope, se = map(Fraction, re.search(
            r"\nx\s+(-?[\d./]+)\s+([\d./]+)$", body).groups())
        statistic = slope / se
        return {"answer": number(statistic), "variant": variant,
                "query": query, "slope": slope, "se": se, "body": body}
    if variant == "sxx_from_data":
        values = [Fraction(value) for value in re.search(
            r"predictor values are x = ([\d, ]+)\.", body).group(1).split(", ")]
        mean = sum(values) / len(values)
        sxx = sum((value - mean) ** 2 for value in values)
        return {"answer": number(sxx), "variant": variant,
                "query": query, "values": values, "mean": mean,
                "sxx": sxx, "body": body}

    n, slope, residual_sd, sxx = re.search(
        r"n = (\d+) points gives slope b = (-?[\d.]+), residual sd s = "
        r"([\d.]+), and Sxx = (\d+)", body).groups()
    n, slope, residual_sd, sxx = (int(n), Fraction(slope),
                                  Fraction(residual_sd), int(sxx))
    se = residual_sd / exact_root(sxx)
    statistic = slope / se
    if variant == "se_slope":
        answer = number(se)
        critical = None
    elif variant == "t_stat":
        answer = number(statistic)
        critical = None
    else:
        critical_text, df = re.search(
            r"(?:t\*|t critical value) = ([\d.]+) \(df = (\d+)\)", body).groups()
        assert int(df) == n - 2
        critical = Fraction(critical_text)
        if variant == "ci_slope":
            margin = critical * se
            answer = f"({number(slope - margin)}, {number(slope + margin)})"
        else:
            reject = abs(statistic) > critical
            label = "reject H0" if reject else "fail to reject H0"
            relation = ">" if reject else "≤"
            answer = (f"{label} ({number(abs(statistic))} {relation} "
                      f"{critical_text})")
    return {"answer": answer, "variant": variant, "query": query,
            "n": n, "slope": slope, "residual_sd": residual_sd,
            "sxx": sxx, "se": se, "statistic": statistic,
            "critical": critical, "body": body}


class SlopeInferenceGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(517204)

    def test_output_contract(self):
        example = SlopeInferenceGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_900_answers_from_problem_text(self):
        generator = SlopeInferenceGenerator()
        for _ in range(900):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_roots_and_supplied_lookups(self):
        generator = SlopeInferenceGenerator()
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
                elif fields[0] == "ROOT":
                    self.assertEqual(Fraction(fields[3]) ** int(fields[2]),
                                     Fraction(fields[1]), raw)
                elif fields[0] == "MEAN_DIV":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "DEV_ROW":
                    self.assertEqual(Fraction(fields[2]) ** 2,
                                     Fraction(fields[3]), raw)
                elif fields[0] == "LOOKUP_SUPPLIED":
                    self.assertIn(fields[2], example["problem"])

    def test_critical_values_always_carry_n_minus_two_df(self):
        for variant in ("ci_slope", "decision"):
            generator = SlopeInferenceGenerator(variant)
            for _ in range(300):
                parts = oracle_parts(generator.generate())
                self.assertIsNotNone(parts["critical"])
                self.assertIn(f"df = {parts['n'] - 2}", parts["body"])

    def test_decision_reaches_both_outcomes(self):
        generator = SlopeInferenceGenerator("decision")
        labels = {generator.generate()["final_answer"].split(" (")[0]
                  for _ in range(600)}
        self.assertEqual(labels, {"reject H0", "fail to reject H0"})

    def test_computer_output_is_three_lines_and_self_sufficient(self):
        generator = SlopeInferenceGenerator("from_output")
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            block = parts["body"].split("Computer output:\n", 1)[1]
            self.assertEqual(len(block.splitlines()), 2)
            self.assertTrue(block.startswith("Predictor  Coef  SE Coef\n"))
            self.assertEqual(example["final_answer"],
                             number(parts["slope"] / parts["se"]))

    def test_raw_x_patterns_have_exact_square_sxx(self):
        expected = {Fraction(sxx) for _, sxx in RAW_X_PATTERNS}
        generator = SlopeInferenceGenerator("sxx_from_data")
        seen = set()
        for _ in range(500):
            parts = oracle_parts(generator.generate())
            self.assertIn(parts["sxx"], expected)
            self.assertEqual(math.isqrt(int(parts["sxx"])) ** 2, parts["sxx"])
            seen.add(parts["sxx"])
        self.assertEqual(seen, expected)

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in SlopeInferenceGenerator.VARIANTS:
            generator = SlopeInferenceGenerator(variant)
            seen = set()
            for _ in range(300):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"statistics_slope_inference_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            SlopeInferenceGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = SlopeInferenceGenerator()
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
