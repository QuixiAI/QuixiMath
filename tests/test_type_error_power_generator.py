"""Independent supplied-table oracle for TypeErrorPowerGenerator."""
import math
import random
import re
import unittest
from fractions import Fraction

from generators.type_error_power_generator import (
    QUERIES, STANDARD_ERRORS, TypeErrorPowerGenerator,
)
from helpers import DELIM


def exact_text(value):
    value = Fraction(value)
    denominator = value.denominator
    power = 0
    while denominator % 2 == 0:
        denominator //= 2
        power += 1
    while denominator % 5 == 0:
        denominator //= 5
        power += 1
    if denominator != 1:
        return str(value)
    return str(float(value)).rstrip("0").rstrip(".")


def p4(value):
    return f"{float(value):.4f}"


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_table(lines):
    line = next((line for line in lines
                 if line.startswith("Standard normal table")), None)
    if line is None:
        return {}
    return {Fraction(z): Fraction(value) for z, value in re.findall(
        r"z=(\d+(?:\.\d+)?): (\d\.\d{4})", line)}


def exact_root_n(n):
    root = math.isqrt(n)
    assert root * root == n
    return root


def table_beta(z, table):
    lookup = table[abs(z)]
    return 1 - lookup if z < 0 else lookup


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    lines = body.splitlines()
    prefix = lines[0]
    table = parse_table(lines)
    mu0 = Fraction(re.search(r"H0: μ = (\d+(?:\.\d+)?)", prefix).group(1))
    sigma = Fraction(re.search(r"σ = (\d+(?:\.\d+)?)", prefix).group(1))

    if variant == "effect_of_n":
        critical_z = Fraction(re.search(r"z\* = ([\d.]+)", prefix).group(1))
        true_mean = Fraction(re.search(
            r"true μ = (\d+(?:\.\d+)?)", prefix).group(1))
        old_n, new_n = map(int, re.search(
            r"Compare n = (\d+) with n = (\d+)", prefix).groups())
        powers, ses, zs = [], [], []
        for n in (old_n, new_n):
            se = sigma / exact_root_n(n)
            cutoff = mu0 + critical_z * se
            z = (cutoff - true_mean) / se
            beta = table_beta(z, table)
            powers.append(1 - beta)
            ses.append(se)
            zs.append(z)
        answer = (f"power {p4(powers[0])} → {p4(powers[1])}; SE "
                  f"{exact_text(ses[0])} → {exact_text(ses[1])}")
        return {"answer": answer, "variant": variant, "query": query,
                "table": table, "powers": powers, "ses": ses, "zs": zs,
                "ns": (old_n, new_n), "prefix": prefix}

    n = int(re.search(r"n = (\d+)", prefix).group(1))
    se = sigma / exact_root_n(n)
    if variant == "alpha_from_cutoff":
        cutoff = Fraction(re.search(r"critical x̄ = ([\d.]+)", prefix).group(1))
        supplied_z = Fraction(re.search(
            r"supplied z = (\d+(?:\.\d+)?)", prefix).group(1))
        z = (cutoff - mu0) / se
        assert z == supplied_z
        alpha = 1 - table[z]
        answer = f"α = {p4(alpha)}"
        return {"answer": answer, "variant": variant, "query": query,
                "table": table, "se": se, "z": z, "prefix": prefix}

    critical_z = Fraction(re.search(r"z\* = ([\d.]+)", prefix).group(1))
    cutoff = mu0 + critical_z * se
    if variant == "critical_xbar":
        answer = exact_text(cutoff)
        return {"answer": answer, "variant": variant, "query": query,
                "table": table, "se": se, "prefix": prefix}

    true_mean = Fraction(re.search(r"true mean is μ = (\d+(?:\.\d+)?)",
                                   prefix).group(1))
    z = (cutoff - true_mean) / se
    beta = table_beta(z, table)
    power = 1 - beta
    answer = (f"β = {p4(beta)}" if variant == "beta"
              else f"β = {p4(beta)}; power = {p4(power)}")
    return {"answer": answer, "variant": variant, "query": query,
            "table": table, "se": se, "z": z, "beta": beta,
            "power": power, "prefix": prefix}


class TypeErrorPowerGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(864209)

    def test_output_contract(self):
        example = TypeErrorPowerGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_900_answers_from_problem_text(self):
        generator = TypeErrorPowerGenerator()
        for _ in range(900):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_arithmetic_roots_zscores_checks_and_lookups(self):
        generator = TypeErrorPowerGenerator()
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
                elif fields[0] == "ZSCORE":
                    match = re.fullmatch(
                        r"\(([-\d.]+) − ([-\d.]+)\)/([\d.]+)", fields[1])
                    self.assertIsNotNone(match, raw)
                    left, right, divisor = map(Fraction, match.groups())
                    self.assertEqual((left - right) / divisor,
                                     Fraction(fields[2]), raw)
                elif fields[0] == "TABLE_LOOKUP":
                    self.assertIn(fields[2], example["problem"])
                elif fields[0] == "CHECK":
                    left, right = map(Fraction, re.fullmatch(
                        r"(\d\.\d{4}) < (\d\.\d{4})", fields[2]).groups())
                    self.assertLess(left, right, raw)
                    self.assertEqual(fields[3], "power increases")

    def test_each_phi_excerpt_has_needed_rows_and_two_decoys(self):
        for variant in TypeErrorPowerGenerator.VARIANTS:
            generator = TypeErrorPowerGenerator(variant)
            for _ in range(200):
                parts = oracle_parts(generator.generate())
                if variant == "critical_xbar":
                    self.assertEqual(parts["table"], {})
                    continue
                needed = ({abs(parts["z"])} if variant != "effect_of_n"
                          else {abs(value) for value in parts["zs"]})
                self.assertLessEqual(needed, set(parts["table"]))
                self.assertEqual(len(parts["table"]), len(needed) + 2)

    def test_standard_errors_are_exact_and_from_the_bank(self):
        for variant in ("critical_xbar", "beta", "power",
                        "alpha_from_cutoff"):
            generator = TypeErrorPowerGenerator(variant)
            seen = set()
            for _ in range(500):
                parts = oracle_parts(generator.generate())
                seen.add(parts["se"])
            self.assertEqual(seen, set(STANDARD_ERRORS))

    def test_beta_and_power_cover_both_z_signs_without_rounding(self):
        for variant in ("beta", "power"):
            generator = TypeErrorPowerGenerator(variant)
            seen_signs = set()
            for _ in range(500):
                example = generator.generate()
                z = oracle_parts(example)["z"]
                seen_signs.add("negative" if z < 0 else "positive")
                printed = next(raw.split(DELIM)[2] for raw in example["steps"]
                               if raw.startswith(f"ZSCORE{DELIM}"))
                self.assertEqual(Fraction(printed), z)
            self.assertEqual(seen_signs, {"negative", "positive"})

    def test_larger_n_halves_se_and_increases_power(self):
        generator = TypeErrorPowerGenerator("effect_of_n")
        for _ in range(400):
            parts = oracle_parts(generator.generate())
            self.assertEqual(parts["ns"][1], 4 * parts["ns"][0])
            self.assertEqual(parts["ses"][1], parts["ses"][0] / 2)
            self.assertGreater(parts["powers"][1], parts["powers"][0])

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in TypeErrorPowerGenerator.VARIANTS:
            generator = TypeErrorPowerGenerator(variant)
            seen = set()
            for _ in range(300):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(
                    example["operation"],
                    f"statistics_type_error_power_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            TypeErrorPowerGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = TypeErrorPowerGenerator()
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
