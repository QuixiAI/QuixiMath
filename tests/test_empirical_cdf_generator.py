"""Independent exact oracles for EmpiricalCDFGenerator."""
import random
import re
import unittest
from collections import Counter
from fractions import Fraction

from generators.empirical_cdf_generator import (
    QUERIES, EmpiricalCDFGenerator,
)
from helpers import DELIM


def exact(value):
    """Render a Fraction without using the generator's numeric helpers."""
    value = Fraction(value)
    denominator = value.denominator
    while denominator % 2 == 0:
        denominator //= 2
    while denominator % 5 == 0:
        denominator //= 5
    if denominator != 1:
        return str(value)
    sign = "-" if value < 0 else ""
    numerator = abs(value.numerator)
    denominator = value.denominator
    whole, remainder = divmod(numerator, denominator)
    if remainder == 0:
        return f"{sign}{whole}"
    digits = []
    while remainder:
        remainder *= 10
        digit, remainder = divmod(remainder, denominator)
        digits.append(str(digit))
    return f"{sign}{whole}.{''.join(digits)}"


def probability(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def ecdf_rows(values):
    counts = Counter(values)
    cumulative = 0
    rows = []
    for value in sorted(counts):
        cumulative += counts[value]
        rows.append((value, Fraction(cumulative, len(values))))
    return rows


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    sample_text = re.search(r"the sample is ([\d, ]+)\.", body).group(1)
    values = tuple(map(int, sample_text.split(", ")))
    rows = ecdf_rows(values)
    parts = {"body": body, "variant": variant, "query": query,
             "values": values, "rows": rows}

    if variant == "ecdf_value":
        target = int(re.search(r"Evaluate at x = (\d+)\.", body).group(1))
        count = sum(value <= target for value in values)
        parts.update(target=target, count=count,
                     answer=probability(Fraction(count, len(values))))
    elif variant == "ecdf_table":
        answer = "; ".join(
            f"{value}: {probability(cdf)}" for value, cdf in rows)
        parts.update(answer=answer)
    elif variant == "ecdf_quantile":
        target = Fraction(re.search(r"Use p = ([\d/]+)\.", body).group(1))
        answer = next(value for value, cdf in rows if cdf >= target)
        parts.update(target=target, answer=str(answer), answer_value=answer)
    elif variant == "jump_size":
        target = int(re.search(r"jump at x = (\d+)\.", body).group(1))
        count = values.count(target)
        parts.update(target=target, count=count,
                     answer=probability(Fraction(count, len(values))))
    else:
        bound = int(re.search(r"F0\(x\) = x/(\d+)", body).group(1))
        previous = Fraction(0)
        gaps = []
        row_gaps = []
        for value, cdf in rows:
            model = Fraction(value, bound)
            before = abs(previous - model)
            at = abs(cdf - model)
            gaps.extend(((before, value), (at, value)))
            row_gaps.extend(((value, "before", previous, model, before),
                             (value, "at", cdf, model, at)))
            previous = cdf
        distance = max(gap for gap, _ in gaps)
        location = min(value for gap, value in gaps if gap == distance)
        parts.update(bound=bound, distance=distance, location=location,
                     row_gaps=row_gaps,
                     answer=f"D = {exact(distance)} at x = {location}")
    return parts


class EmpiricalCDFGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(394715)

    def test_output_contract(self):
        example = EmpiricalCDFGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_900_answers_from_problem_text(self):
        generator = EmpiricalCDFGenerator()
        for _ in range(900):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_sort_setup_and_ecdf_rows_match_raw_sample(self):
        generator = EmpiricalCDFGenerator()
        for _ in range(500):
            example = generator.generate()
            parts = oracle_parts(example)
            setup = next(raw.split(DELIM) for raw in example["steps"]
                         if raw.startswith(f"ECDF_SETUP{DELIM}"))
            self.assertEqual(setup[1], f"n = {len(parts['values'])}")
            sort = next(raw.split(DELIM) for raw in example["steps"]
                        if raw.startswith(f"SORT{DELIM}"))
            self.assertEqual(tuple(map(int, sort[1].split(", "))),
                             parts["values"])
            self.assertEqual(tuple(map(int, sort[2].split(", "))),
                             tuple(sorted(parts["values"])))

            expected = dict(parts["rows"])
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] != "ECDF_ROW" or not fields[1].isdigit():
                    continue
                value = int(fields[1])
                if parts["variant"] == "ecdf_value":
                    expected_cdf = Fraction(
                        sum(item <= value for item in parts["values"]),
                        len(parts["values"]))
                else:
                    expected_cdf = expected[value]
                self.assertEqual(Fraction(fields[2]), expected_cdf, raw)

    def test_count_and_division_steps_are_exact(self):
        for variant in ("ecdf_value", "jump_size"):
            generator = EmpiricalCDFGenerator(variant)
            for _ in range(250):
                example = generator.generate()
                parts = oracle_parts(example)
                count = next(raw.split(DELIM) for raw in example["steps"]
                             if raw.startswith(f"COUNT{DELIM}"))
                self.assertEqual(int(count[2]), parts["count"])
                for raw in example["steps"]:
                    fields = raw.split(DELIM)
                    if fields[0] == "D":
                        self.assertEqual(Fraction(fields[1]) /
                                         Fraction(fields[2]),
                                         Fraction(fields[3]), raw)

    def test_table_rows_are_unique_sorted_and_complete(self):
        generator = EmpiricalCDFGenerator("ecdf_table")
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            values = [int(cell.split(": ")[0])
                      for cell in example["final_answer"].split("; ")]
            self.assertEqual(values, sorted(set(parts["values"])))
            self.assertEqual(len(values), len(parts["rows"]))

    def test_quantile_uses_smallest_x_reaching_p(self):
        generator = EmpiricalCDFGenerator("ecdf_quantile")
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            answer = parts["answer_value"]
            self.assertGreaterEqual(dict(parts["rows"])[answer],
                                    parts["target"])
            earlier = [cdf for value, cdf in parts["rows"] if value < answer]
            self.assertTrue(all(cdf < parts["target"] for cdf in earlier))
            self.assertIn("smallest x with F̂(x) ≥ p",
                          DELIM.join(example["steps"]))

    def test_jump_is_multiplicity_over_sample_size(self):
        generator = EmpiricalCDFGenerator("jump_size")
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            self.assertIn(parts["target"], parts["values"])
            self.assertEqual(Fraction(example["final_answer"]),
                             Fraction(parts["count"], len(parts["values"])))

    def test_ks_rows_check_every_before_and_at_gap(self):
        generator = EmpiricalCDFGenerator("ks_distance_uniform")
        seen_bounds = set()
        for _ in range(400):
            example = generator.generate()
            parts = oracle_parts(example)
            seen_bounds.add(parts["bound"])
            rows = [raw.split(DELIM) for raw in example["steps"]
                    if raw.startswith(f"KS_ROW{DELIM}")]
            self.assertEqual(len(rows), 2 * len(parts["rows"]))
            actual = []
            for fields in rows:
                value, side = re.fullmatch(
                    r"x = (\d+), (before|at)", fields[1]).groups()
                left, model = re.fullmatch(
                    r"abs\(([-\d./]+) − ([-\d./]+)\)", fields[2]).groups()
                gap = abs(Fraction(left) - Fraction(model))
                self.assertEqual(gap, Fraction(fields[3]), DELIM.join(fields))
                actual.append((int(value), side, Fraction(left),
                               Fraction(model), gap))
            self.assertEqual(actual, parts["row_gaps"])
        self.assertEqual(seen_bounds, {10, 20, 50})

    def test_ks_check_uses_global_max_and_smallest_x_tie_break(self):
        generator = EmpiricalCDFGenerator("ks_distance_uniform")
        for _ in range(400):
            example = generator.generate()
            parts = oracle_parts(example)
            check = next(raw.split(DELIM) for raw in example["steps"]
                         if raw.startswith(f"CHECK{DELIM}"))
            self.assertEqual(Fraction(check[2]), parts["distance"])
            self.assertEqual(check[3], f"at x = {parts['location']}")
            self.assertIn("smallest x", example["problem"])
            self.assertIn("smallest x wins ties", DELIM.join(example["steps"]))

    def test_n_bank_all_variants_and_four_phrasings_are_reachable(self):
        seen_n = set()
        for variant in EmpiricalCDFGenerator.VARIANTS:
            generator = EmpiricalCDFGenerator(variant)
            seen_queries = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                seen_n.add(len(parts["values"]))
                seen_queries.add(parts["query"])
                self.assertEqual(example["operation"],
                                 f"statistics_empirical_cdf_{variant}")
            self.assertEqual(seen_queries, set(QUERIES[variant]))
        self.assertEqual(seen_n, set(range(4, 9)))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            EmpiricalCDFGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = EmpiricalCDFGenerator()
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
