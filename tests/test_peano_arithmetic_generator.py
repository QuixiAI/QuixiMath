"""Independent successor-counting oracle for PeanoArithmeticGenerator."""
import random
import re
import unittest

from generators.peano_arithmetic_generator import QUERIES, PeanoArithmeticGenerator
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_numeral(text):
    text = text.strip()
    if text.isdigit():
        return int(text)
    if re.fullmatch(r"S*0", text):
        return len(text) - 1
    count = 0
    while text.startswith("S(") and text.endswith(")"):
        count += 1
        text = text[2:-1]
    assert text == "0", text
    return count


def compact(number):
    return "S" * number + "0"


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "addition":
        match = re.fullmatch(
            r"Expression: (.+)\. Rules: a \+ 0 = a; a \+ S\(b\) = "
            r"S\(a \+ b\)\. Evaluation order: left to right\.", body)
        assert match is not None, body
        operands = [parse_numeral(value) for value in match.group(1).split(" + ")]
        result = sum(operands)
        answer = f"{compact(result)} = {result}"
    elif variant == "multiplication":
        match = re.fullmatch(
            r"Expression: (.+)\. Rules: a · 0 = 0; a · S\(b\) = "
            r"a · b \+ a\. Evaluation order: left to right\.", body)
        assert match is not None, body
        operands = [parse_numeral(value) for value in match.group(1).split(" · ")]
        result = 1
        for value in operands:
            result *= value
        answer = f"{compact(result)} = {result}"
    elif variant == "exponentiation":
        match = re.fullmatch(
            r"Expression: (.+) \^ \((.+) \+ (.+)\)\. Rules: a\^0 = S0; "
            r"a\^S\(b\) = a\^b · a; addition uses a \+ 0 = a and "
            r"a \+ S\(b\) = S\(a \+ b\)\.", body)
        assert match is not None, body
        base, first, second = map(parse_numeral, match.groups())
        operands = [base, first, second]
        result = base ** (first + second)
        answer = f"{compact(result)} = {result}"
    elif variant == "leq_witness":
        match = re.fullmatch(
            r"Comparison: (.+) ≤ (.+)\. Definition: a ≤ b iff there exists "
            r"c with a \+ c = b\.", body)
        assert match is not None, body
        first, second = map(parse_numeral, match.groups())
        operands = [first, second]
        if first <= second:
            witness = second - first
            answer = (f"true; witness c = {compact(witness)} "
                      f"({first} + {witness} = {second})")
        else:
            answer = f"false; no c ({first} > {second})"
        result = first <= second
    else:
        match = re.fullmatch(
            r"Expression: (.+)\. Rules: pred\(0\) = 0; pred\(S\(n\)\) = n; "
            r"a ∸ 0 = a; a ∸ S\(b\) = pred\(a ∸ b\)\. "
            r"Evaluation order: left to right\.", body)
        assert match is not None, body
        operands = [parse_numeral(value) for value in match.group(1).split(" ∸ ")]
        result = operands[0]
        for value in operands[1:]:
            result = max(0, result - value)
        answer = f"{compact(result)} = {result}"
    return {"variant": variant, "query": query, "operands": operands,
            "result": result, "answer": answer}


class PeanoArithmeticGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(318557)

    def test_output_contract(self):
        example = PeanoArithmeticGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = PeanoArithmeticGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_base_unfold_fold_and_decimal_checks_are_consistent(self):
        generator = PeanoArithmeticGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            fields = [raw.split(DELIM) for raw in example["steps"]]
            self.assertTrue(any(item[0] in ("PEANO_BASE", "NO_WITNESS")
                                for item in fields))
            check = next(item for item in fields if item[0] == "CHECK")
            self.assertEqual(check[1], "decimal")
            if parts["variant"] != "leq_witness":
                final_compact, final_decimal = example["final_answer"].split(" = ")
                self.assertEqual(parse_numeral(final_compact), int(final_decimal))
                self.assertEqual(int(final_decimal), parts["result"])
            elif parts["result"]:
                witness = next(item for item in fields if item[0] == "WITNESS")
                value = parse_numeral(witness[1].split("=")[1])
                self.assertEqual(parts["operands"][0] + value,
                                 parts["operands"][1])

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in PeanoArithmeticGenerator.VARIANTS:
            generator = PeanoArithmeticGenerator(variant)
            seen_queries = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"peano_arithmetic_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            PeanoArithmeticGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = PeanoArithmeticGenerator()
        for _ in range(250):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            self.assertNotRegex(example["problem"], r"1x|--")
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()
