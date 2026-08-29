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

from generators.standard_deviation_generator import (
    LEGACY_PROMPTS, LEGACY_VARIANTS, NEW_QUERIES, StandardDeviationGenerator,
)
from helpers import DELIM


def sqrt_val(txt):
    m = re.fullmatch(r"(\d*)(?:√(\d+))?", txt)
    k = int(m.group(1)) if m.group(1) else 1
    return k * math.sqrt(int(m.group(2))) if m.group(2) else float(k)


def oracle_check(example):
    p = example["problem"]
    ans = example["final_answer"]
    if "sample data are:" in p:
        data = [int(v) for v in re.search(
            r"sample data are: ([0-9, -]+)\.", p).group(1).split(", ")]
        mean = Fraction(sum(data), len(data))
        variance = sum((Fraction(v) - mean) ** 2 for v in data) / (len(data) - 1)
        return Fraction(ans) ** 2 == variance
    if "population data are:" in p:
        data = [int(v) for v in re.search(
            r"population data are: ([0-9, -]+)\.", p).group(1).split(", ")]
        mean = Fraction(sum(data), len(data))
        variance = sum((Fraction(v) - mean) ** 2 for v in data) / len(data)
        return Fraction(ans) == variance
    if "frequency table (value: frequency):" in p:
        entries = re.search(r"frequency table \(value: frequency\): "
                            r"(.+?)\.", p).group(1)
        data = []
        for entry in entries.split("; "):
            value, frequency = map(int, entry.split(": "))
            data.extend([value] * frequency)
        mean = Fraction(sum(data), len(data))
        variance = sum((Fraction(v) - mean) ** 2 for v in data) / len(data)
        return Fraction(ans) ** 2 == variance
    if "CV rule:" in p:
        mean, sigma = re.search(r"mean μ = ([0-9./]+) and standard "
                                r"deviation σ = (\d+)", p).groups()
        expected = Fraction(int(sigma), Fraction(mean)) * 100
        return ans == f"{expected.numerator if expected.denominator == 1 else float(expected)}%"
    data = [int(v) for v in
            re.search(r"data set: (.+)\. Give", p).group(1)
            .split(", ")]
    n = len(data)
    mean = Fraction(sum(data), n)
    ss = sum((Fraction(v) - mean) ** 2 for v in data)
    if "population variance" in p:
        return Fraction(ans) == ss / n
    if "sample variance" in p:
        return Fraction(ans) == ss / (n - 1)
    return abs(sqrt_val(ans) - math.sqrt(ss / n)) < 1e-9


class TestStandardDeviationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = StandardDeviationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_recompute_from_problem(self):
        """A9 oracle: exact variance recomputed from the data."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_deviation_table_complete_and_consistent(self):
        for variant in ("population_variance", "sample_variance",
                        "population_std"):
            gen = StandardDeviationGenerator(variant)
            for _ in range(100):
                result = gen.generate()
                data = [int(v) for v in
                        re.search(r"data set: (.+)\. Give",
                                  result["problem"]).group(1).split(", ")]
                rows = [s.split(DELIM)[1:] for s in result["steps"]
                        if s.startswith(f"DEV_ROW{DELIM}")]
                self.assertEqual(sorted(int(r[0]) for r in rows),
                                 sorted(data))
                for x, d, sq in rows:
                    self.assertEqual(int(d) ** 2, int(sq))

    def test_mean_always_integer(self):
        for variant in ("population_variance", "sample_variance",
                        "population_std"):
            gen = StandardDeviationGenerator(variant)
            for _ in range(100):
                result = gen.generate()
                data = [int(v) for v in
                        re.search(r"data set: (.+)\. Give",
                                  result["problem"]).group(1).split(", ")]
                self.assertEqual(sum(data) % len(data), 0)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(600):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 7)

    def test_default_wrapper_preserves_legacy_rng_advancement(self):
        for seed in range(40):
            random.seed(seed)
            legacy_variant = random.choice(LEGACY_VARIANTS)
            StandardDeviationGenerator._generate_legacy(legacy_variant)
            expected_state = random.getstate()
            random.seed(seed)
            StandardDeviationGenerator().generate()
            self.assertEqual(random.getstate(), expected_state)

    def test_new_variants_have_prompt_only_oracles(self):
        for variant in NEW_QUERIES:
            gen = StandardDeviationGenerator(variant)
            for _ in range(250):
                result = gen.generate()
                self.assertTrue(oracle_check(result),
                                (result["problem"], result["final_answer"]))

    def test_new_arithmetic_steps_are_exact(self):
        for variant in NEW_QUERIES:
            gen = StandardDeviationGenerator(variant)
            for _ in range(180):
                result = gen.generate()
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
                    elif fields[0] in ("D", "MEAN_DIV"):
                        self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                         Fraction(fields[3]), raw)
                    elif fields[0] == "E":
                        self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                         Fraction(fields[3]), raw)
                    elif fields[0] == "WEIGHT_ROW":
                        self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                         Fraction(fields[3]), raw)

    def test_shortcut_matches_independent_deviation_route(self):
        gen = StandardDeviationGenerator("shortcut_formula")
        for _ in range(250):
            result = gen.generate()
            self.assertTrue(oracle_check(result))
            checks = [raw for raw in result["steps"]
                      if raw.startswith(f"CHECK{DELIM}shortcut")]
            self.assertEqual(len(checks), 1)

    def test_new_variants_have_four_phrasings(self):
        for variant, queries in NEW_QUERIES.items():
            gen = StandardDeviationGenerator(variant)
            seen = set()
            for _ in range(250):
                problem = gen.generate()["problem"]
                seen.update(query for query in queries
                            if problem.endswith("\n" + query))
            self.assertEqual(seen, set(queries))

    def test_legacy_variants_have_four_phrasings(self):
        for variant, templates in LEGACY_PROMPTS.items():
            gen = StandardDeviationGenerator(variant)
            seen = set()
            for _ in range(250):
                problem = gen.generate()["problem"]
                seen.update(t for t in templates
                            if problem.startswith(t.split("{raw}")[0]))
            self.assertEqual(seen, set(templates))

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            StandardDeviationGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
