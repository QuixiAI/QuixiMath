"""Independent cumulative/difference oracle for PmfCdfQuantileGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.pmf_cdf_quantile_generator import QUERIES, PmfCdfQuantileGenerator
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def ptext(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def parse_rows(text, kind):
    pattern = (r"P\(X=(-?\d+)\) = (\d+(?:/\d+)?)" if kind == "pmf"
               else r"F\((-?\d+)\) = (\d+(?:/\d+)?)")
    rows = []
    for item in text.split("; "):
        match = re.fullmatch(pattern, item)
        assert match is not None, item
        rows.append((int(match.group(1)), Fraction(match.group(2))))
    return rows


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "cdf_to_pmf":
        match = re.fullmatch(r"X has cdf rows: (.+)\.", body)
        assert match is not None, body
        cdf_rows = parse_rows(match.group(1), "cdf")
        previous = Fraction()
        pmf_rows = []
        for x, cumulative in cdf_rows:
            pmf_rows.append((x, cumulative - previous))
            previous = cumulative
        answer = "; ".join(f"P(X={x}) = {ptext(weight)}" for x, weight in pmf_rows)
        rows = pmf_rows
    elif variant == "interval_from_cdf":
        match = re.fullmatch(
            r"X has cdf rows: (.+)\. Target: P\((-?\d+) < X ≤ (-?\d+)\)\.", body)
        assert match is not None, body
        cdf_rows = parse_rows(match.group(1), "cdf")
        cdf = dict(cdf_rows)
        left, right = int(match.group(2)), int(match.group(3))
        answer = ptext(cdf[right] - cdf[left])
        rows = cdf_rows
    else:
        if variant == "quantile":
            match = re.fullmatch(r"X has pmf: (.+)\. Quantile level q = (\d+/\d+)\.", body)
            assert match is not None, body
            q = Fraction(match.group(2))
        elif variant == "mode":
            match = re.fullmatch(
                r"X has pmf: (.+)\. If several values tie, choose the first in support order\.", body)
            assert match is not None, body
            q = None
        else:
            match = re.fullmatch(r"X has pmf: (.+)\.", body)
            assert match is not None, body
            q = Fraction(1, 2) if variant == "median" else None
        rows = parse_rows(match.group(1), "pmf")
        cumulative = []
        running = Fraction()
        for x, weight in rows:
            running += weight
            cumulative.append((x, running))
        assert running == 1
        if variant == "pmf_to_cdf":
            answer = "; ".join(f"F({x}) = {ptext(value)}" for x, value in cumulative)
        elif variant in ("median", "quantile"):
            selected = next(x for x, value in cumulative if value >= q)
            answer = (f"median {selected}" if variant == "median"
                      else f"q={ptext(q)} quantile {selected}")
        else:
            maximum = max(weight for _, weight in rows)
            selected = next(x for x, weight in rows if weight == maximum)
            tied = sum(weight == maximum for _, weight in rows) > 1
            tie_text = " (first among ties)" if tied else ""
            answer = f"mode {selected}{tie_text}; P(X={selected}) = {ptext(maximum)}"
    return {"variant": variant, "query": query, "answer": answer, "rows": rows}


class PmfCdfQuantileGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(360555)

    def test_output_contract(self):
        example = PmfCdfQuantileGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = PmfCdfQuantileGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_cumulative_and_difference_steps_are_exact(self):
        generator = PmfCdfQuantileGenerator()
        for _ in range(300):
            example = generator.generate()
            oracle_parts(example)
            cdf_values = []
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "CDF_ROW":
                    cdf_values.append(Fraction(fields[2]))
            self.assertEqual(cdf_values, sorted(cdf_values))
            if cdf_values:
                self.assertEqual(cdf_values[-1], 1)

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in PmfCdfQuantileGenerator.VARIANTS:
            generator = PmfCdfQuantileGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_pmf_cdf_quantile_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            PmfCdfQuantileGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = PmfCdfQuantileGenerator()
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
