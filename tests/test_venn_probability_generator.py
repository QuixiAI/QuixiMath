"""Independent region-system oracle for VennProbabilityGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.venn_probability_generator import QUERIES, VennProbabilityGenerator
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
    if variant == "from_probabilities":
        match = re.fullmatch(
            r"Events A and B satisfy P\(A\) = (\d+(?:/\d+)?), P\(B\) = "
            r"(\d+(?:/\d+)?), and P\(A ∩ B\) = (\d+(?:/\d+)?)\.", body)
        assert match is not None, body
        p_a, p_b, p_both = map(Fraction, match.groups())
        union = p_a + p_b - p_both
        outside = 1 - union
        answer = (f"P(A ∪ B) = {ptext(union)}; "
                  f"P(Aᶜ ∩ Bᶜ) = {ptext(outside)}")
        data = {"p_a": p_a, "p_b": p_b, "p_both": p_both,
                "union": union, "outside": outside}
    elif variant == "three_set":
        match = re.fullmatch(
            r"A population has (\d+) items with card\(A\) = (\d+), card\(B\) = "
            r"(\d+), card\(C\) = (\d+), card\(A ∩ B\) = (\d+), card\(A ∩ C\) "
            r"= (\d+), card\(B ∩ C\) = (\d+), and card\(A ∩ B ∩ C\) = "
            r"(\d+)\. One item is chosen uniformly\.", body)
        assert match is not None, body
        total, a, b, c, ab, ac, bc, abc = map(int, match.groups())
        union_count = a + b + c - ab - ac - bc + abc
        none = total - union_count
        union, outside = Fraction(union_count, total), Fraction(none, total)
        answer = (f"P(A ∪ B ∪ C) = {ptext(union)}; "
                  f"P(none) = {ptext(outside)}")
        data = {"total": total, "union": union, "outside": outside,
                "none": none}
    else:
        match = re.fullmatch(
            r"Of (\d+) ([a-z]+), (\d+) (.+), (\d+) (.+), and (\d+) do both\. "
            r"Let A mean '([^']+)' and B mean '([^']+)'\. One ([a-z]+) is "
            r"chosen uniformly\.", body)
        assert match is not None, body
        total, count_a, count_b, both = (int(match.group(i))
                                             for i in (1, 3, 5, 7))
        assert match.group(4) == match.group(8)
        assert match.group(6) == match.group(9)
        only_a, only_b = count_a - both, count_b - both
        union_count = count_a + count_b - both
        neither = total - union_count
        assert min(only_a, only_b, both, neither) >= 0
        if variant == "only_A":
            answer = f"{ptext(Fraction(only_a, total))}; {ptext(Fraction(neither, total))}"
        elif variant == "neither":
            answer = ptext(Fraction(neither, total))
        elif variant == "union":
            answer = ptext(Fraction(union_count, total))
        else:
            answer = ptext(Fraction(only_a + only_b, total))
        data = {"total": total, "only_a": only_a, "only_b": only_b,
                "both": both, "union_count": union_count, "neither": neither}
    return {"variant": variant, "query": query, "answer": answer, **data}


class VennProbabilityGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(244949)

    def test_output_contract(self):
        example = VennProbabilityGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = VennProbabilityGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_steps_are_exact(self):
        generator = VennProbabilityGenerator()
        for _ in range(300):
            example = generator.generate()
            oracle_parts(example)
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "F":
                    self.assertEqual(Fraction(fields[1]), Fraction(fields[2]))
                    self.assertEqual(fields[2], ptext(Fraction(fields[2])))
                elif fields[0] == "PROB_SETUP":
                    value = Fraction(int(fields[1]), int(fields[2]))
                    self.assertGreaterEqual(value, 0)
                    self.assertLessEqual(value, 1)

    def test_three_set_overrides_difficulty(self):
        generator = VennProbabilityGenerator("three_set")
        for _ in range(100):
            self.assertEqual(generator.generate()["difficulty"], 4)
        self.assertNotIn("difficulty", VennProbabilityGenerator("union").generate())

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in VennProbabilityGenerator.VARIANTS:
            generator = VennProbabilityGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"], f"probability_venn_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            VennProbabilityGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = VennProbabilityGenerator()
        for _ in range(250):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            rendered = "\n".join([example["problem"], *example["steps"],
                                   example["final_answer"]])
            self.assertNotRegex(rendered, r"1x|\^1\b|\+ 0|--")
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4, raw_step)


if __name__ == "__main__":
    unittest.main()
