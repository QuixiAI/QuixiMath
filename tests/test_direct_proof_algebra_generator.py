"""Independent template inversion and algebra checks for direct proofs."""
import random
import re
import unittest

from generators.direct_proof_algebra_generator import QUERIES, DirectProofAlgebraGenerator
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_parity_form(text):
    match = re.fullmatch(r"(\w) = 2(\w)( \+ 1)?", text)
    assert match is not None, text
    return match.group(1), match.group(2), 1 if match.group(3) else 0


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant in ("parity_sum", "parity_product"):
        operator = r" \+ " if variant == "parity_sum" else ""
        match = re.fullmatch(
            rf"Let (\w = 2\w(?: \+ 1)?) and (\w = 2\w(?: \+ 1)?), "
            rf"where the witnesses are integers\. Prove (\w){operator}(\w) "
            rf"is (odd|even)\.", body,
        )
        assert match is not None, body
        first, first_witness, first_bit = parse_parity_form(match.group(1))
        second, second_witness, second_bit = parse_parity_form(match.group(2))
        conclusion = match.group(5)
        if variant == "parity_sum":
            constant = first_bit + second_bit
            inside = f"{first_witness} + {second_witness}"
            if constant == 2:
                inside += " + 1"
            answer = f"2({inside})" + (" + 1" if constant % 2 else "")
        elif first_bit == second_bit == 1:
            answer = (f"2(2{first_witness}{second_witness} + {first_witness} "
                      f"+ {second_witness}) + 1")
        elif first_bit == second_bit == 0:
            answer = f"2(2{first_witness}{second_witness})"
        elif first_bit == 0:
            answer = f"2{first_witness}(2{second_witness} + 1)"
        else:
            answer = f"2{second_witness}(2{first_witness} + 1)"
        return {"variant": variant, "query": query, "first": first,
                "second": second, "u": first_witness, "v": second_witness,
                "bits": (first_bit, second_bit), "conclusion": conclusion,
                "answer": answer}
    if variant == "consecutive_product_even":
        match = re.fullmatch(
            r"Let (\w) be an integer and use integer witness (\w) in the "
            r"parity cases\. Prove \1\(\1 \+ 1\) is even\.", body)
        assert match is not None, body
        number, witness = match.groups()
        first = f"2{witness}(2{witness} + 1)"
        second = f"2({witness} + 1)(2{witness} + 1)"
        return {"variant": variant, "query": query, "number": number,
                "witness": witness, "answer": f"{first}; {second}"}
    if variant == "divisibility_transitive":
        match = re.fullmatch(
            r"Let (\w), (\w), (\w) be integers\. Suppose \1 ∣ \2 and \2 ∣ \3, "
            r"with \2 = \1(\w) and \3 = \2(\w)\. Prove \1 ∣ \3\.", body)
        assert match is not None, body
        first, second, third, one, two = match.groups()
        return {"variant": variant, "query": query,
                "answer": f"{third} = {first}({one}{two})"}
    if variant == "contrapositive_setup":
        match = re.fullmatch(r"Theorem: (.+)\.", body)
        assert match is not None, body
        theorem = match.group(1)
        square_odd = re.fullmatch(r"If (\w)² is odd, then \1 is odd", theorem)
        square_even = re.fullmatch(r"If (\w)² is even, then \1 is even", theorem)
        successor = re.fullmatch(r"If (\w) \+ 1 is odd, then \1 is even", theorem)
        product = re.fullmatch(
            r"If (\w)(\w) is odd, then \1 and \2 are odd", theorem)
        if square_odd:
            number = square_odd.group(1)
            answer = f"assume {number} is even; show {number}² is even"
        elif square_even:
            number = square_even.group(1)
            answer = f"assume {number} is odd; show {number}² is odd"
        elif successor:
            number = successor.group(1)
            answer = f"assume {number} is odd; show {number} + 1 is even"
        else:
            assert product is not None, theorem
            first, second = product.groups()
            answer = (f"assume {first} is even or {second} is even; "
                      f"show {first}{second} is even")
        return {"variant": variant, "query": query, "answer": answer}
    match = re.fullmatch(
        r"Claim: (.+)\. Setup symbols: (\w), (\w), (\w)\.", body)
    assert match is not None, body
    theorem = match.group(1)
    number, first_witness, second_witness = match.group(2, 3, 4)
    both = re.fullmatch(r"No integer (\w) is both even and odd", theorem)
    greatest = theorem == "There is no greatest integer"
    rational = re.fullmatch(
        r"The sum of rational (\w) and irrational (\w) is irrational", theorem)
    radical = re.fullmatch(r"√(\d+) is irrational", theorem)
    if both:
        subject = both.group(1)
        setup = (f"assume {subject} is both even and odd; write {subject} = "
                 f"2{first_witness} = 2{second_witness} + 1")
    elif greatest:
        setup = (f"assume {number} is the greatest integer; "
                 f"consider {number} + 1")
    elif rational:
        first, second = rational.groups()
        setup = (f"assume {first} + {second} is rational; then {second} = "
                 f"({first} + {second}) − {first} would be rational")
    else:
        assert radical is not None
        prime = radical.group(1)
        setup = (f"assume √{prime} = {first_witness}/{second_witness} in "
                 f"lowest terms; derive {prime}{second_witness}² = "
                 f"{first_witness}²")
    return {"variant": variant, "query": query, "answer": setup}


class DirectProofAlgebraGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(271903)

    def test_output_contract(self):
        example = DirectProofAlgebraGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = DirectProofAlgebraGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_parity_algebra_holds_for_independent_integer_substitutions(self):
        for variant in ("parity_sum", "parity_product"):
            generator = DirectProofAlgebraGenerator(variant)
            for _ in range(200):
                example = generator.generate()
                parts = oracle_parts(example)
                first_witness = random.randint(-20, 20)
                second_witness = random.randint(-20, 20)
                first = 2 * first_witness + parts["bits"][0]
                second = 2 * second_witness + parts["bits"][1]
                value = first + second if variant == "parity_sum" else first * second
                expected_parity = "odd" if value % 2 else "even"
                self.assertEqual(expected_parity, parts["conclusion"])
                factors = [item.split(DELIM)[1] for item in example["steps"]
                           if item.startswith("FACTOR" + DELIM)]
                self.assertEqual(factors[-1], example["final_answer"])

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in DirectProofAlgebraGenerator.VARIANTS:
            generator = DirectProofAlgebraGenerator(variant)
            seen_queries = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"direct_proof_algebra_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            DirectProofAlgebraGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = DirectProofAlgebraGenerator()
        for _ in range(250):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            self.assertNotRegex(example["problem"], r"1x|\^1|\+ 0|--")
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()
