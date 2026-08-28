import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.chi_square_generator import (
    CRIT_BY_ALPHA, NONUNIFORM_MODELS, ChiSquareGenerator, exact,
)
from helpers import DELIM


def oracle_chi(problem):
    """Recompute χ² from the counts in the problem text alone."""
    m = re.search(r"model proportions: (.*?); observed counts: (.*?); "
                  r"N = (\d+)", problem)
    if m:
        probabilities = [Fraction(value) for value in
                         re.findall(r"=([\d./]+)", m.group(1))]
        observed = [int(value) for value in
                    re.findall(r"=(\d+)", m.group(2))]
        total = int(m.group(3))
        expected = [total * probability for probability in probabilities]
        return sum(Fraction((obs - exp) ** 2) / exp
                   for obs, exp in zip(observed, expected))
    m = re.search(r"observed counts by category: (.*?); each expected "
                  r"count is (\d+)", problem)
    if m:
        obs = [int(value) for value in re.findall(r"=([0-9]+)", m.group(1))]
        E = int(m.group(2))
        return sum(Fraction((o - E) ** 2, E) for o in obs)
    matrix = parse_matrix(problem)
    if matrix is not None:
        _, _, observed = matrix
        total = sum(map(sum, observed))
        row_totals = list(map(sum, observed))
        column_totals = [sum(row[j] for row in observed)
                         for j in range(len(observed[0]))]
        expected = [[Fraction(row * column, total)
                     for column in column_totals] for row in row_totals]
        return sum(Fraction(observed[i][j] - expected[i][j]) ** 2
                   / expected[i][j]
                   for i in range(len(observed))
                   for j in range(len(observed[0])))
    m = re.search(r"counts: (\d+), (\d+); (\d+), (\d+); N = (\d+)",
                  problem)
    assert m, problem
    o11, o12, o21, o22, N = (int(g) for g in m.groups())
    R1, R2 = o11 + o12, o21 + o22
    C1, C2 = o11 + o21, o12 + o22
    Es = [Fraction(R1 * C1, N), Fraction(R1 * C2, N),
          Fraction(R2 * C1, N), Fraction(R2 * C2, N)]
    Os = [o11, o12, o21, o22]
    return sum(Fraction((o - e) ** 2) / e for o, e in zip(Os, Es))


def parse_matrix(problem):
    match = re.search(r"shape (\d+)x(\d+);.*?counts by row: "
                      r"([\d, /]+); N = (\d+)", problem)
    if not match:
        return None
    rows, columns, body, total = match.groups()
    observed = [[int(value.strip()) for value in row.split(",")]
                for row in body.strip().split("/")]
    assert len(observed) == int(rows)
    assert all(len(row) == int(columns) for row in observed)
    assert sum(map(sum, observed)) == int(total)
    return int(rows), int(columns), observed


def expected_table(problem):
    rows, columns, observed = parse_matrix(problem)
    total = sum(map(sum, observed))
    row_totals = list(map(sum, observed))
    column_totals = [sum(row[j] for row in observed)
                     for j in range(columns)]
    pairs = []
    for i in range(rows):
        for j in range(columns):
            value = Fraction(row_totals[i] * column_totals[j], total)
            pairs.append(f"r{i + 1}c{j + 1}: {exact(value)}")
    return "; ".join(pairs)


def oracle_check(example):
    p = example["problem"]
    ans = example["final_answer"]
    variant = example["operation"].removeprefix("chi_square_")
    if variant == "df_from_shape":
        rows, columns = map(int, re.search(
            r"shape (\d+)x(\d+)", p).groups())
        return ans == f"df = {(rows - 1) * (columns - 1)}; " \
                      f"({rows} - 1)({columns} - 1)"
    if variant == "expected_table":
        return ans == expected_table(p)
    chi = oracle_chi(p)
    crit = Fraction(re.search(r"critical value of ([\d.]+)", p).group(1))
    if variant in ("gof_stat", "gof_nonuniform", "independence_stat",
                   "rxc_stat"):
        return ans == exact(chi)
    want = "reject H0" if chi > crit else "fail to reject H0"
    relation = ">" if chi > crit else "≤"
    verdict = f"{want} ({exact(chi)} {relation} {exact(crit)})"
    if variant == "homogeneity":
        rows, columns, _ = parse_matrix(p)
        df = (rows - 1) * (columns - 1)
        return ans == f"χ² = {exact(chi)}; df = {df}; {verdict}"
    ans = ans.split(" (")[0]
    return ans == want


class TestChiSquareGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ChiSquareGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        """A9 oracle: recompute χ² and the decision from the text."""
        for _ in range(1000):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_critical_value_and_formula(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertRegex(result["problem"], r"critical value of [\d.]+")
            if not result["operation"].endswith("df_from_shape"):
                self.assertTrue(any(s.startswith(f"CHI_FORMULA{DELIM}")
                                    for s in result["steps"]))

    def test_expected_table_for_independence(self):
        for v in ("independence_stat", "independence_decision"):
            gen = ChiSquareGenerator(v)
            for _ in range(50):
                result = gen.generate()
                exp = [s for s in result["steps"]
                       if s.startswith(f"EXP_CELL{DELIM}")]
                self.assertEqual(len(exp), 4, result["steps"])
        for variant in ("expected_table", "rxc_stat", "rxc_decision",
                        "homogeneity"):
            generator = ChiSquareGenerator(variant)
            for _ in range(50):
                result = generator.generate()
                rows, columns, _ = parse_matrix(result["problem"])
                exp = [s for s in result["steps"]
                       if s.startswith(f"EXP_CELL{DELIM}")]
                self.assertEqual(len(exp), rows * columns)

    def test_both_decisions_occur(self):
        for v in ("gof_decision", "independence_decision", "rxc_decision",
                  "homogeneity"):
            gen = ChiSquareGenerator(v)
            verdicts = {gen.generate()["final_answer"] for _ in range(400)}
            heads = {"fail to reject H0" if "fail to reject H0" in answer
                     else "reject H0" for answer in verdicts}
            self.assertIn("reject H0", heads)
            self.assertIn("fail to reject H0", heads)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 10)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            ChiSquareGenerator("bogus")

    def test_step_arithmetic_and_expected_cells(self):
        for _ in range(500):
            result = self.gen.generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "EXP_CELL":
                    formula, answer = ((fields[1], fields[2]) if len(fields) == 3
                                       else (fields[2], fields[3]))
                    match = re.fullmatch(r"\((\d+)·(\d+)\)/(\d+)", formula)
                    self.assertIsNotNone(match, raw)
                    row, column, total = map(int, match.groups())
                    self.assertEqual(Fraction(row * column, total),
                                     Fraction(answer), raw)
                elif fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "CHI_TERM":
                    square = re.fullmatch(r"\(?(-?\d+)\)?\^2 = (\d+)",
                                          fields[2])
                    self.assertIsNotNone(square, raw)
                    base, squared = map(int, square.groups())
                    self.assertEqual(base * base, squared, raw)
                    quotient = re.fullmatch(
                        r"(\d+)/([\d.]+) = ([\d./]+)", fields[3])
                    self.assertIsNotNone(quotient, raw)
                    numerator, denominator, value = quotient.groups()
                    self.assertEqual(Fraction(numerator) / Fraction(denominator),
                                     Fraction(value), raw)
                elif fields[0] == "CHECK":
                    comparison = re.fullmatch(
                        r"([\d./]+) ([>≤]) ([\d.]+)", fields[2])
                    self.assertIsNotNone(comparison, raw)
                    left, relation, right = comparison.groups()
                    holds = (Fraction(left) > Fraction(right)
                             if relation == ">"
                             else Fraction(left) <= Fraction(right))
                    self.assertTrue(holds, raw)
                    self.assertEqual(fields[3],
                                     "reject H0" if relation == ">"
                                     else "fail to reject H0")

    def test_widened_labels_and_phrasings_vary(self):
        problems = {self.gen.generate()["problem"] for _ in range(1000)}
        self.assertGreater(len(problems), 990)
        joined = "\n".join(problems)
        self.assertIn("observed counts by category", joined)
        self.assertIn("Independence table data", joined)

    def test_nonuniform_models_and_integer_expected_counts(self):
        allowed = {value for model in NONUNIFORM_MODELS for value in model}
        generator = ChiSquareGenerator("gof_nonuniform")
        seen_models = set()
        for _ in range(300):
            result = generator.generate()
            match = re.search(r"model proportions: (.*?); observed counts: "
                              r"(.*?); N = (\d+)", result["problem"])
            probabilities = tuple(Fraction(value) for value in
                                  re.findall(r"=([\d./]+)", match.group(1)))
            total = int(match.group(3))
            self.assertEqual(sum(probabilities), 1)
            self.assertTrue(set(probabilities) <= allowed)
            self.assertTrue(all((total * value).denominator == 1
                                for value in probabilities))
            seen_models.add(probabilities)
            self.assertTrue(oracle_check(result))
        self.assertEqual(seen_models, set(NONUNIFORM_MODELS))

    def test_rxc_shapes_margins_df_and_expected_answer(self):
        seen_shapes = set()
        for variant in ("expected_table", "rxc_stat", "rxc_decision",
                        "homogeneity"):
            generator = ChiSquareGenerator(variant)
            for _ in range(250):
                result = generator.generate()
                rows, columns, observed = parse_matrix(result["problem"])
                seen_shapes.add((rows, columns))
                self.assertEqual(sum(map(sum, observed)), 100)
                self.assertTrue(all(sum(row) % 10 == 0 for row in observed))
                self.assertTrue(all(sum(row[j] for row in observed) % 10 == 0
                                    for j in range(columns)))
                df = int(re.search(r"df = (\d+)", result["problem"]).group(1))
                self.assertEqual(df, (rows - 1) * (columns - 1))
                self.assertTrue(oracle_check(result))
        self.assertEqual(seen_shapes, {(2, 3), (3, 2), (3, 3)})

    def test_extension_critical_rows_are_supplied_and_labeled(self):
        for variant in ("gof_nonuniform", "expected_table", "rxc_stat",
                        "rxc_decision", "homogeneity", "df_from_shape"):
            generator = ChiSquareGenerator(variant)
            seen_alpha = set()
            for _ in range(200):
                problem = generator.generate()["problem"]
                crit, df, alpha = re.search(
                    r"critical value of ([\d.]+).*?df = (\d+).*?α = (0\.\d+)",
                    problem).groups()
                self.assertEqual(crit, CRIT_BY_ALPHA[alpha][int(df)])
                seen_alpha.add(alpha)
            self.assertEqual(seen_alpha, set(CRIT_BY_ALPHA))

    def test_df_from_shape_composite_answer(self):
        generator = ChiSquareGenerator("df_from_shape")
        seen = set()
        for _ in range(100):
            result = generator.generate()
            self.assertTrue(oracle_check(result))
            seen.add(result["final_answer"])
        self.assertEqual(len(seen), 3)


if __name__ == "__main__":
    unittest.main()
