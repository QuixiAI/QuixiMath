"""Independent factorization oracle for GodelNumberingGenerator."""
import random
import re
import unittest

from generators.godel_numbering_generator import GodelNumberingGenerator, QUERIES
from helpers import DELIM


PRIMES = (2, 3, 5, 7, 11)


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_table(text):
    table = {}
    for item in text.split("; "):
        symbol, code = item.split(" → ")
        table[symbol] = int(code)
    assert len(table) == 6
    assert len(set(table.values())) == 6
    return table


def independent_encode(sequence, table):
    number = 1
    for prime, symbol in zip(PRIMES, sequence):
        number *= pow(prime, table[symbol])
    return number


def independent_decode(number, table):
    inverse = {code: symbol for symbol, code in table.items()}
    sequence = []
    remaining = number
    for prime in PRIMES:
        exponent = 0
        while remaining % prime == 0:
            remaining //= prime
            exponent += 1
        if exponent == 0:
            break
        assert exponent in inverse
        sequence.append(inverse[exponent])
    assert remaining == 1
    return sequence


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "encode":
        match = re.fullmatch(
            r"Symbol table: (.+)\. Encoding rule: for sequence codes "
            r"c1,\.\.\.,ck, use 2\^c1 · 3\^c2 · 5\^c3 · \.\.\. \. "
            r"Sequence: (.+)\.", body)
        assert match is not None, body
        table = parse_table(match.group(1))
        sequence = match.group(2).split(" ")
        number = independent_encode(sequence, table)
        answer = str(number)
    elif variant == "decode":
        match = re.fullmatch(
            r"Symbol table: (.+)\. Decoding rule: the exponents of "
            r"consecutive primes 2,3,5,7,11 are the symbol codes\. "
            r"Gödel number: (\d+)\.", body)
        assert match is not None, body
        table = parse_table(match.group(1))
        number = int(match.group(2))
        sequence = independent_decode(number, table)
        answer = " ".join(sequence)
    else:
        match = re.fullmatch(
            r"Symbol table: (.+)\. Lookup request: "
            r"(?:(?:code of symbol (.+))|(?:symbol having code (\d+)))\.", body)
        assert match is not None, body
        table = parse_table(match.group(1))
        if match.group(2) is not None:
            symbol = match.group(2)
            code = table[symbol]
            mode = "symbol_to_code"
        else:
            code = int(match.group(3))
            symbol = {value: key for key, value in table.items()}[code]
            mode = "code_to_symbol"
        sequence, number = [symbol], 0
        answer = f"{symbol} → {code}"
        return {"variant": variant, "query": query, "answer": answer,
                "table": table, "sequence": sequence, "number": number,
                "mode": mode}
    return {"variant": variant, "query": query, "answer": answer,
            "table": table, "sequence": sequence, "number": number,
            "mode": variant}


class GodelNumberingGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(223607)

    def test_output_contract(self):
        example = GodelNumberingGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = GodelNumberingGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_prime_power_and_multiplication_steps_are_exact(self):
        generator = GodelNumberingGenerator()
        for _ in range(300):
            example = generator.generate()
            for fields in (raw.split(DELIM) for raw in example["steps"]):
                if fields[0] == "GODEL_TERM":
                    base, exponent = map(int, fields[1].split("^"))
                    self.assertEqual(base ** exponent, int(fields[2]))
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]))
                elif fields[0] == "PF_STEP":
                    dividend, divisor, quotient = map(int, fields[1:])
                    self.assertEqual(dividend, divisor * quotient)

    def test_encoded_numbers_respect_bound(self):
        generator = GodelNumberingGenerator("encode")
        for _ in range(300):
            example = generator.generate()
            self.assertLessEqual(int(example["final_answer"]), 10_000_000)

    def test_both_lookup_directions_are_reachable(self):
        generator = GodelNumberingGenerator("symbol_lookup")
        modes = {oracle_parts(generator.generate())["mode"] for _ in range(100)}
        self.assertEqual(modes, {"symbol_to_code", "code_to_symbol"})

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in GodelNumberingGenerator.VARIANTS:
            generator = GodelNumberingGenerator(variant)
            seen_queries = set()
            for _ in range(250):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"godel_numbering_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            GodelNumberingGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = GodelNumberingGenerator()
        for _ in range(250):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            self.assertNotRegex(example["problem"], r"1x|\+ 0|--")
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()
