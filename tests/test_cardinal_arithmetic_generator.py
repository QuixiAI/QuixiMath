"""Independent rule engine for CardinalArithmeticGenerator."""
import random
import re
import unittest

from generators.cardinal_arithmetic_generator import CardinalArithmeticGenerator, QUERIES
from helpers import DELIM


RANK = {"ℵ0": 1, "c": 2, "2^c": 3}


def parse_cardinal(text):
    return text if text in RANK else int(text)


def independent_combine(left, right, operator):
    if isinstance(left, int) and isinstance(right, int):
        return left + right if operator == "+" else left * right
    infinite = [value for value in (left, right) if isinstance(value, str)]
    return max(infinite, key=RANK.__getitem__)


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def exponent_answer(power, expression):
    base_text, exponent_text = power.split("^")
    base, exponent = parse_cardinal(base_text), parse_cardinal(exponent_text)
    if exponent == "ℵ0":
        if base == "c":
            result = "c"
        elif base == "ℵ0" or isinstance(base, int) and base >= 2:
            result = "c"
        else:
            raise AssertionError(power)
    elif base == "ℵ0" and isinstance(exponent, int) and exponent > 0:
        result = "ℵ0"
    elif base == "c" and exponent == "c":
        result = "2^c"
    else:
        raise AssertionError(power)
    return f"c ({expression})" if result == "c" else result


def set_answer(description):
    match = re.fullmatch(r"ℕ\^(\d+)", description)
    if match:
        assert int(match.group(1)) > 0
        return f"card({description}) = ℵ0", "finite_power"
    match = re.fullmatch(r"([ℤℚ])\^(\d+)", description)
    if match:
        assert int(match.group(2)) > 0
        return f"card({description}) = ℵ0", "countable_power"
    match = re.fullmatch(r"\(ℝ − ℚ\)\^(\d+)", description)
    if match:
        assert int(match.group(1)) > 0
        return f"card({description}) = c", "co_countable_reals"
    match = re.fullmatch(r"P\(ℕ × F_(\d+)\), where card\(F_\1\) = \1", description)
    if match:
        return f"card(P(ℕ × F_{match.group(1)})) = c (2^ℵ0)", "power_set"
    match = re.fullmatch(r"finite sequences over ℕ of length at most (\d+)", description)
    if match:
        return f"card({description}) = ℵ0", "finite_sequences"
    match = re.fullmatch(
        r"functions ℕ → D_(\d+), where card\(D_\1\) = \1", description)
    assert match is not None, description
    return f"card(functions ℕ → D_{match.group(1)}) = c (2^ℵ0)", "functions"


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "add_multiply":
        match = re.fullmatch(
            r"Evaluate cardinal expression: (.+)\. For positive cardinals, "
            r"if at least one operand is infinite, both addition and "
            r"multiplication equal the larger infinite cardinal\.", body)
        assert match is not None, body
        expression = match.group(1)
        operator = " + " if " + " in expression else " · "
        operands = [parse_cardinal(token) for token in expression.split(operator)]
        result = operands[0]
        for operand in operands[1:]:
            result = independent_combine(result, operand, operator.strip())
        answer = str(result)
        case = operator.strip()
    elif variant == "exponent":
        match = re.fullmatch(
            r"Evaluate cardinal exponentiation inside expression: "
            r"(\d+) ([+·]) \(([^)]+)\)\. Identity to use: "
            r"(.+)\.", body)
        assert match is not None, body
        adjustment, operator, power = match.group(1), match.group(2), match.group(3)
        expression = f"{adjustment} {operator} ({power})"
        answer = exponent_answer(power, expression)
        case = power
    else:
        match = re.fullmatch(
            r"Set description: (.+)\. Cardinality rule: (.+)\.", body)
        assert match is not None, body
        answer, case = set_answer(match.group(1))
        expression = match.group(1)
    return {"variant": variant, "query": query, "answer": answer,
            "case": case, "expression": expression}


class CardinalArithmeticGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(141421)

    def test_output_contract(self):
        example = CardinalArithmeticGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = CardinalArithmeticGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_finite_arithmetic_inside_steps(self):
        generator = CardinalArithmeticGenerator()
        for _ in range(350):
            example = generator.generate()
            for fields in (raw.split(DELIM) for raw in example["steps"]):
                if fields[0] == "A":
                    self.assertEqual(int(fields[1]) + int(fields[2]),
                                     int(fields[3]))
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]))

    def test_all_exponent_and_set_families_are_reachable(self):
        exponent = CardinalArithmeticGenerator("exponent")
        exponent_cases = {oracle_parts(exponent.generate())["case"]
                          for _ in range(500)}
        self.assertTrue(any(case.startswith("ℵ0^") for case in exponent_cases))
        self.assertIn("c^ℵ0", exponent_cases)
        self.assertIn("c^c", exponent_cases)
        self.assertIn("2^ℵ0", exponent_cases)
        sets = CardinalArithmeticGenerator("set_cardinality")
        set_cases = {oracle_parts(sets.generate())["case"] for _ in range(500)}
        self.assertEqual(set_cases,
                         {"finite_power", "countable_power",
                          "co_countable_reals", "power_set",
                          "finite_sequences", "functions"})

    def test_addition_and_multiplication_are_reachable(self):
        generator = CardinalArithmeticGenerator("add_multiply")
        cases = {oracle_parts(generator.generate())["case"] for _ in range(100)}
        self.assertEqual(cases, {"+", "·"})

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in CardinalArithmeticGenerator.VARIANTS:
            generator = CardinalArithmeticGenerator(variant)
            seen_queries = set()
            for _ in range(250):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"cardinal_arithmetic_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            CardinalArithmeticGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = CardinalArithmeticGenerator()
        for _ in range(250):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            self.assertNotRegex(example["problem"],
                                r"1x|\^1(?!\d)|\+ 0|--")
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()
