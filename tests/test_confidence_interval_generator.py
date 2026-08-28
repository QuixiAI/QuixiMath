import math
import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.confidence_interval_generator import (
    EXTENSION_QUERIES, ConfidenceIntervalGenerator,
)
from generators.exponential_model_generator import dec
from helpers import DELIM


def num(pattern, text):
    return Fraction(re.search(pattern, text).group(1).rstrip("."))


def exact_root(value):
    value = Fraction(value)
    numerator = math.isqrt(value.numerator)
    denominator = math.isqrt(value.denominator)
    assert numerator * numerator == value.numerator
    assert denominator * denominator == value.denominator
    return Fraction(numerator, denominator)


def oracle_check(example):
    p = example["problem"]
    ans = example["final_answer"]
    variant = example["operation"].removeprefix("confidence_interval_")
    z = num(r"z\* = ([\d.]+)", p)
    if variant == "prop_ci":
        n = int(num(r"sample of size (\d+)", p))
        phat = num(r"p̂ = ([\d.]+)", p)
        se = exact_root(phat * (1 - phat) / n)
        margin = z * se
        return ans == f"({dec(phat - margin)}, {dec(phat + margin)})"
    if variant == "diff_means_ci":
        match = re.search(
            r"x̄1 = (-?\d+), population σ1 = (\d+), n1 = (\d+); "
            r"x̄2 = (-?\d+), population σ2 = (\d+), n2 = (\d+)", p)
        mean1, sigma1, n1, mean2, sigma2, n2 = map(int, match.groups())
        se = exact_root(Fraction(sigma1 * sigma1, n1)
                        + Fraction(sigma2 * sigma2, n2))
        center, margin = Fraction(mean1 - mean2), z * se
        return ans == f"({dec(center - margin)}, {dec(center + margin)})"
    if variant == "diff_props_ci":
        phat1, n1, phat2, n2 = re.search(
            r"p̂1 = ([\d.]+), n1 = (\d+); p̂2 = ([\d.]+), n2 = (\d+)",
            p).groups()
        phat1, phat2, n1, n2 = Fraction(phat1), Fraction(phat2), int(n1), int(n2)
        se = exact_root(phat1 * (1 - phat1) / n1
                        + phat2 * (1 - phat2) / n2)
        center, margin = phat1 - phat2, z * se
        return ans == f"({dec(center - margin)}, {dec(center + margin)})"
    if variant == "width_effect":
        changed_z = re.search(
            r"critical value from z\* = (\d+(?:\.\d+)?) to z\* = "
            r"(\d+(?:\.\d+)?)", p)
        if changed_z:
            return ans == f"wider; z* {changed_z.group(1)} → {changed_z.group(2)}"
        old_n, new_n = map(int, re.search(
            r"sample size from n = (\d+) to n = (\d+)", p).groups())
        return ans == (f"narrower; √n {math.isqrt(old_n)} → "
                       f"{math.isqrt(new_n)} halves E")
    if "minimum sample size" in p:
        E = num(r"margin of error of ([\d.]+)", p)
        if "proportion" in p:
            phat = num(r"p̂ = ([\d.]+)", p)
            n = math.ceil((z / E) ** 2 * phat * (1 - phat))
        else:
            sigma = num(r"σ = (\d+)", p)
            n = math.ceil((z * sigma / E) ** 2)
        return ans == str(n)
    if "proportion" in p and "margin of error" in p:
        n = int(num(r"sample of size (\d+)", p))
        E = z * (Fraction(1, 2) / math.isqrt(n))
        return ans == dec(E)
    if "margin of error" in p and "mean" in p:
        n = int(num(r"sample of size (\d+)", p))
        sigma = num(r"σ = (\d+)", p)
        return ans == dec(z * sigma / math.isqrt(n))
    # confidence interval for the mean
    n = int(num(r"sample of size (\d+)", p))
    xbar = num(r"x̄ = (\d+)", p)
    sigma = num(r"σ = (\d+)", p)
    E = z * sigma / math.isqrt(n)
    return ans == f"({dec(xbar - E)}, {dec(xbar + E)})"


class TestConfidenceIntervalGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ConfidenceIntervalGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        """A9 oracle: recompute each answer from the givens."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_extension_oracle_from_problem_text(self):
        for variant in ("prop_ci", "diff_means_ci", "diff_props_ci",
                        "width_effect"):
            generator = ConfidenceIntervalGenerator(variant)
            for _ in range(300):
                result = generator.generate()
                self.assertTrue(oracle_check(result),
                                (result["problem"], result["final_answer"]))

    def test_critical_value_in_problem(self):
        """Principle 5: z* is always supplied in the text."""
        for _ in range(300):
            result = self.gen.generate()
            self.assertRegex(result["problem"], r"z\* = [\d.]+")

    def test_sample_sizes_are_integers(self):
        for v in ("sample_size_mean", "sample_size_prop"):
            gen = ConfidenceIntervalGenerator(v)
            for _ in range(100):
                result = gen.generate()
                self.assertRegex(result["final_answer"], r"^\d+$")
                self.assertTrue(any(s.startswith(f"CEIL{DELIM}")
                                    for s in result["steps"]))

    def test_pipe_safe_and_exact(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)
                self.assertNotIn("...", s)

    def test_extension_arithmetic_roots_and_lookups(self):
        for variant in ("prop_ci", "diff_means_ci", "diff_props_ci",
                        "width_effect"):
            generator = ConfidenceIntervalGenerator(variant)
            for _ in range(250):
                result = generator.generate()
                for raw in result["steps"]:
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
                    elif fields[0] == "ROOT" and len(fields) == 4:
                        self.assertEqual(Fraction(fields[3]) ** int(fields[2]),
                                         Fraction(fields[1]), raw)
                    elif fields[0] == "LOOKUP_SUPPLIED":
                        self.assertIn(fields[2], result["problem"])

    def test_width_effect_reaches_both_mechanisms(self):
        generator = ConfidenceIntervalGenerator("width_effect")
        seen = {result.split(";", 1)[0] for result in
                (generator.generate()["final_answer"] for _ in range(400))}
        self.assertEqual(seen, {"wider", "narrower"})

    def test_difference_of_proportions_reaches_nonzero_both_signs(self):
        generator = ConfidenceIntervalGenerator("diff_props_ci")
        signs = set()
        for _ in range(500):
            problem = generator.generate()["problem"]
            phat1, phat2 = map(Fraction, re.search(
                r"p̂1 = ([\d.]+), n1 = \d+; p̂2 = ([\d.]+)", problem).groups())
            difference = phat1 - phat2
            if difference:
                signs.add("positive" if difference > 0 else "negative")
        self.assertEqual(signs, {"positive", "negative"})

    def test_extension_four_phrasings_reachable(self):
        for variant, queries in EXTENSION_QUERIES.items():
            generator = ConfidenceIntervalGenerator(variant)
            seen = set()
            for _ in range(300):
                problem = generator.generate()["problem"]
                for query in queries:
                    if problem.endswith("\n" + query):
                        seen.add(query)
                        break
            self.assertEqual(seen, set(queries))

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(200):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 9)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            ConfidenceIntervalGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
