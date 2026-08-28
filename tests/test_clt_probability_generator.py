"""Problem-text-only oracle for CLTProbabilityGenerator."""
import math
import random
import re
import unittest
from fractions import Fraction

from generators.clt_probability_generator import QUERIES, CLTProbabilityGenerator
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


def exact_root(value):
    value = Fraction(value)
    numerator = math.isqrt(value.numerator)
    denominator = math.isqrt(value.denominator)
    assert numerator * numerator == value.numerator
    assert denominator * denominator == value.denominator
    return Fraction(numerator, denominator)


def parse_case(body):
    lines = body.splitlines()
    prefix = lines[0]
    table = {}
    if len(lines) == 2:
        table = {Fraction(z): Fraction(value) for z, value in re.findall(
            r"z=(\d+\.\d{2}): (0\.\d{4})", lines[1])}
        assert table
    target = re.search(r"Target: (.+)\.$", prefix).group(1)
    n_match = re.search(r"samples of size n = (\d+)", prefix)
    if "population proportion" in prefix:
        p = Fraction(re.search(r"is p = (\d+(?:/\d+)?)", prefix).group(1))
        return {"kind": "prop", "p": p, "n": int(n_match.group(1)),
                "target": target, "table": table}
    mean, sigma = map(int, re.search(
        r"population mean μ = (\d+) units and population standard deviation "
        r"σ = (\d+) units", prefix).groups())
    return {"kind": "mean", "mean": mean, "sigma": sigma,
            "n": int(n_match.group(1)) if n_match else None,
            "target": target, "table": table}


def cdf(z, table):
    magnitude = abs(Fraction(z))
    assert magnitude in table, (magnitude, table)
    return table[magnitude] if z >= 0 else 1 - table[magnitude]


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    case = parse_case(body)
    if case["kind"] == "mean":
        mean, sigma, n = case["mean"], case["sigma"], case["n"]
        if variant == "n_for_target_se":
            target_se = Fraction(re.search(
                r"SE\(x̄\) = (\d+(?:\.\d+)?(?:/\d+)?)", case["target"]
            ).group(1))
            ratio = Fraction(sigma, 1) / target_se
            assert ratio.denominator == 1
            answer = str(ratio.numerator ** 2)
            se = target_se
        else:
            root_n = math.isqrt(n)
            assert root_n * root_n == n
            se = Fraction(sigma, root_n)
            if variant == "se_mean":
                answer = exact_text(se)
            elif variant == "mean_sd_xbar":
                answer = f"mean {mean}; SD {exact_text(se)}"
            elif variant == "shape_and_center":
                assert n >= 30
                answer = (f"approximately normal (n = {n} ≥ 30); mean {mean}; "
                          f"SE {exact_text(se)}")
            elif variant == "mean_above":
                cutoff = Fraction(re.fullmatch(
                    r"find P\(x̄ > (\d+(?:\.\d+)?(?:/\d+)?)\)",
                    case["target"]).group(1))
                z = (cutoff - mean) / se
                answer = f"{float(1 - cdf(z, case['table'])):.4f}"
            elif variant == "mean_between":
                lower, upper = map(Fraction, re.fullmatch(
                    r"find P\((\d+(?:\.\d+)?(?:/\d+)?) < x̄ < "
                    r"(\d+(?:\.\d+)?(?:/\d+)?)\)", case["target"]).groups())
                z_low, z_high = (lower - mean) / se, (upper - mean) / se
                answer = f"{float(cdf(z_high, case['table']) - cdf(z_low, case['table'])):.4f}"
            else:
                observed = Fraction(re.fullmatch(
                    r"classify x̄ = (\d+(?:\.\d+)?(?:/\d+)?) using the rule "
                    r"unusual when abs\(z\) > 2", case["target"]).group(1))
                z = (observed - mean) / se
                label = "unusual" if abs(z) > 2 else "usual"
                answer = f"{label}; z = {exact_text(z)}"
    else:
        p, n = case["p"], case["n"]
        se = exact_root(p * (1 - p) / n)
        if variant == "se_prop":
            answer = exact_text(se)
        elif variant == "prop_below":
            cutoff = Fraction(re.fullmatch(
                r"find P\(p̂ < (\d+(?:\.\d+)?(?:/\d+)?)\)",
                case["target"]).group(1))
            z = (cutoff - p) / se
            answer = f"{float(cdf(z, case['table'])):.4f}"
        else:
            lower, upper = map(Fraction, re.fullmatch(
                r"find P\((\d+(?:\.\d+)?(?:/\d+)?) < p̂ < "
                r"(\d+(?:\.\d+)?(?:/\d+)?)\)", case["target"]).groups())
            z_low, z_high = (lower - p) / se, (upper - p) / se
            answer = f"{float(cdf(z_high, case['table']) - cdf(z_low, case['table'])):.4f}"
    return {"variant": variant, "query": query, "answer": answer,
            "case": case, "se": se}


class CLTProbabilityGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(341207)

    def test_output_contract(self):
        example = CLTProbabilityGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_900_answers_from_problem_text(self):
        generator = CLTProbabilityGenerator()
        for _ in range(900):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_roots_and_lookups_are_exact(self):
        generator = CLTProbabilityGenerator()
        for _ in range(500):
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
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "ROOT":
                    self.assertEqual(Fraction(fields[3]) ** int(fields[2]),
                                     Fraction(fields[1]), raw)
                elif fields[0] == "TABLE_LOOKUP":
                    self.assertIn(fields[2], example["problem"])

    def test_probability_tables_have_needed_rows_and_two_decoys(self):
        variants = ("mean_above", "mean_between", "prop_below",
                    "prob_proportion")
        for variant in variants:
            generator = CLTProbabilityGenerator(variant)
            for _ in range(150):
                example = generator.generate()
                parts = oracle_parts(example)
                lookups = [row for row in example["steps"]
                           if row.startswith(f"TABLE_LOOKUP{DELIM}")]
                expected_rows = len(lookups) + 2
                self.assertEqual(len(parts["case"]["table"]), expected_rows,
                                 example["problem"])

    def test_clt_conditions_are_computed_from_stated_parameters(self):
        mean_variants = ("shape_and_center", "mean_above", "mean_between",
                         "unusual_sample_mean")
        for variant in mean_variants:
            generator = CLTProbabilityGenerator(variant)
            for _ in range(80):
                example = generator.generate()
                parts = oracle_parts(example)
                n = parts["case"]["n"]
                self.assertGreaterEqual(n, 30)
                self.assertTrue(any(
                    raw.startswith(f"CLT_CHECK{DELIM}n = {n} ≥ 30{DELIM}")
                    for raw in example["steps"]), example["steps"])
        for variant in ("prop_below", "prob_proportion"):
            generator = CLTProbabilityGenerator(variant)
            for _ in range(100):
                parts = oracle_parts(generator.generate())
                p, n = parts["case"]["p"], parts["case"]["n"]
                self.assertGreaterEqual(n * p, 10)
                self.assertGreaterEqual(n * (1 - p), 10)

    def test_tail_signs_and_unusual_verdicts_are_reachable(self):
        generator = CLTProbabilityGenerator("prop_below")
        signs = set()
        for _ in range(300):
            parts = oracle_parts(generator.generate())
            target = parts["case"]["target"]
            cutoff = Fraction(re.search(r"p̂ < ([^)]+)", target).group(1))
            signs.add("positive" if cutoff > parts["case"]["p"] else "negative")
        self.assertEqual(signs, {"positive", "negative"})

        generator = CLTProbabilityGenerator("unusual_sample_mean")
        labels = {generator.generate()["final_answer"].split(";", 1)[0]
                  for _ in range(300)}
        self.assertEqual(labels, {"usual", "unusual"})

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in CLTProbabilityGenerator.VARIANTS:
            generator = CLTProbabilityGenerator(variant)
            seen = set()
            for _ in range(300):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"statistics_clt_probability_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            CLTProbabilityGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = CLTProbabilityGenerator()
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
