"""Extended prompt-text oracles for ConditionalProbabilityGenerator."""
import itertools
import random
import re
import unittest
from fractions import Fraction

from generators.conditional_probability_generator import (
    QUERIES, ConditionalProbabilityGenerator, exact,
)
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


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "table":
        match = re.fullmatch(
            r"A two-way table for ([a-z]+) has counts: (.+)\. One ([a-z]+) "
            r"is selected uniformly\. Target: P\(([a-z]+)=([a-z]+) given "
            r"([a-z]+)=([a-z]+)\)\.", body)
        assert match is not None, body
        cells = {}
        row_key = col_key = None
        for item in match.group(2).split("; "):
            cell = re.fullmatch(
                r"([a-z]+)=([a-z]+) and ([a-z]+)=([a-z]+): (\d+)", item)
            assert cell is not None, item
            rkey, row, ckey, col, count = cell.groups()
            row_key, col_key = row_key or rkey, col_key or ckey
            cells[row, col] = int(count)
        target_key, target_value = match.group(4), match.group(5)
        given_key, given_value = match.group(6), match.group(7)
        numerator = denominator = 0
        for (row, col), count in cells.items():
            record = {row_key: row, col_key: col}
            if record[given_key] == given_value:
                denominator += count
                if record[target_key] == target_value:
                    numerator += count
        answer = exact(Fraction(numerator, denominator))
        context = match.group(1)
    elif variant in ("bayes_positive", "bayes_negative"):
        match = re.fullmatch(
            r"A screening test is used for (\d+) people\. Disease=yes count is "
            r"(\d+) and disease=no count is (\d+)\. Sensitivity P\(test positive "
            r"given disease=yes\) = (\d+(?:/\d+)?)\. Specificity P\(test negative "
            r"given disease=no\) = (\d+(?:/\d+)?)\. Target: P\(disease=(yes|no) "
            r"given test (positive|negative)\)\.", body)
        assert match is not None, body
        total, disease, no_disease = map(int, match.groups()[:3])
        assert disease + no_disease == total
        sensitivity, specificity = Fraction(match.group(4)), Fraction(match.group(5))
        tp, fn = disease * sensitivity, disease * (1 - sensitivity)
        tn, fp = no_disease * specificity, no_disease * (1 - specificity)
        value = tp / (tp + fp) if variant == "bayes_positive" else tn / (tn + fn)
        answer, context = exact(value), None
    elif variant == "given_probabilities":
        match = re.fullmatch(
            r"Events A and B have P\(A ∩ B\) = (\d+(?:/\d+)?) and P\(B\) = "
            r"(\d+(?:/\d+)?)\.", body)
        assert match is not None, body
        answer = ptext(Fraction(match.group(1)) / Fraction(match.group(2)))
        context = None
    elif variant == "chain_rule":
        match = re.fullmatch(
            r"A bag has (.+) balls\. Three balls are drawn without replacement "
            r"in this order: ([a-z]+), ([a-z]+), ([a-z]+)\.", body)
        assert match is not None, body
        items = []
        for part in match.group(1).split(", "):
            count, color = part.split()
            items.extend((color, index) for index in range(int(count)))
        wanted = match.groups()[1:4]
        favorable = total = 0
        for outcome in itertools.permutations(items, 3):
            total += 1
            favorable += tuple(item[0] for item in outcome) == wanted
        answer = ptext(Fraction(favorable, total))
        context = None
    else:
        match = re.fullmatch(
            r"Events A and B have P\(A given B\) = (\d+(?:/\d+)?), P\(A\) = "
            r"(\d+(?:/\d+)?), and P\(B\) = (\d+(?:/\d+)?)\.", body)
        assert match is not None, body
        p_a_given_b, p_a, p_b = map(Fraction, match.groups())
        answer = ptext(p_a_given_b * p_b / p_a)
        context = None
    return {"variant": variant, "query": query, "answer": answer,
            "context": context}


class TestConditionalProbabilityGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ConditionalProbabilityGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["steps"][-1], f"Z{DELIM}{result['final_answer']}")

    def test_oracle_all_variants_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_parts(result)["answer"],
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            oracle_parts(result)
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "COND_TOTAL":
                    left, total = fields[2].split(" = ")
                    self.assertEqual(sum(map(int, left.split(" + "))), int(total))
                elif fields[0] == "BAYES_CELL":
                    expression = fields[2]
                    if " × " in expression:
                        left, right = expression.split(" × ")
                        value = int(left) * Fraction(right)
                    else:
                        left, right = expression.split(" − ")
                        value = int(left) - int(right)
                    self.assertEqual(value, int(fields[3]))
                elif fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "FRAC_BUILD":
                    self.assertEqual(fields[2], exact(Fraction(fields[1])))

    def test_probabilities_valid(self):
        for _ in range(300):
            value = float(Fraction(self.gen.generate()["final_answer"]))
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 1)

    def test_formula_present_for_every_variant(self):
        for variant in ConditionalProbabilityGenerator.VARIANTS:
            result = ConditionalProbabilityGenerator(variant).generate()
            codes = {raw.split(DELIM)[0] for raw in result["steps"]}
            self.assertTrue({"COND_FORMULA", "BAYES_FORMULA"} & codes)

    def test_six_table_contexts_are_reachable(self):
        generator = ConditionalProbabilityGenerator("table")
        seen = {oracle_parts(generator.generate())["context"] for _ in range(600)}
        self.assertEqual(len(seen), 6)

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in ConditionalProbabilityGenerator.VARIANTS:
            generator = ConditionalProbabilityGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"conditional_probability_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_pipe_safe_and_render_sane(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            rendered = "\n".join([result["problem"], *result["steps"],
                                   result["final_answer"]])
            self.assertNotRegex(rendered, r"1x|\^1\b|\+ 0|--")
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            ConditionalProbabilityGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
