"""Independent dict-polynomial and definitional oracle for PGFGenerator."""
import math
import random
import re
import unittest
from fractions import Fraction

from generators.pgf_generator import QUERIES, PGFGenerator
from helpers import DELIM


def ptext(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_pmf(body, label):
    rows = [(int(k), Fraction(p)) for k, p in
            re.findall(rf"P\({label}=(\d+)\)=(-?\d+(?:/\d+)?)", body)]
    assert rows and sum((p for _, p in rows), Fraction()) == 1
    return dict(rows)


def term_text(coefficient, exponent):
    coefficient = Fraction(coefficient)
    if exponent == 0:
        return ptext(coefficient)
    variable = "s" if exponent == 1 else f"s^{exponent}"
    return variable if coefficient == 1 else f"({ptext(coefficient)}){variable}"


def poly_text(polynomial):
    return " + ".join(term_text(c, e)
                      for e, c in sorted(polynomial.items(), reverse=True) if c) or "0"


def parse_polynomial(text):
    output = {}
    for term in text.split(" + "):
        if "s" not in term:
            output[0] = Fraction(term)
            continue
        match = re.fullmatch(r"(?:\((\d+(?:/\d+)?)\))?s(?:\^(\d+))?", term)
        assert match is not None, term
        coefficient = Fraction(match.group(1)) if match.group(1) else Fraction(1)
        exponent = int(match.group(2)) if match.group(2) else 1
        output[exponent] = coefficient
    return output


def multiply(first, second):
    output = {}
    for e1, c1 in first.items():
        for e2, c2 in second.items():
            output[e1 + e2] = output.get(e1 + e2, Fraction()) + c1 * c2
    return output


def mean_variance(pmf):
    mean = sum((k * p for k, p in pmf.items()), Fraction())
    variance = sum(((Fraction(k) - mean) ** 2 * p for k, p in pmf.items()), Fraction())
    return mean, variance


def answer_pmf(label, pmf):
    return "; ".join(f"P({label}={k}) = {ptext(p)}" for k, p in sorted(pmf.items()))


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "extract_pmf":
        match = re.search(r"G_X\(s\) = (.+)\. Target: P\(X=(\d+)\)", body)
        polynomial, target = parse_polynomial(match.group(1)), int(match.group(2))
        answer = f"P(X={target}) = {ptext(polynomial.get(target, 0))}"
    elif variant == "sum_independent_product":
        first, second = parse_pmf(body, "X"), parse_pmf(body, "Y")
        product = multiply(first, second)
        answer = f"G_S(s) = {poly_text(product)}; {answer_pmf('S', product)}"
    elif variant == "binomial_pgf":
        match = re.search(r"X~Binomial\((\d+),(\d+(?:/\d+)?)\)", body)
        n, p = int(match.group(1)), Fraction(match.group(2))
        pmf = {k: Fraction(math.comb(n, k)) * p ** k * (1-p) ** (n-k)
               for k in range(n + 1)}
        answer = f"G(s) = {poly_text(pmf)}; E[X] = {ptext(n*p)}"
    else:
        pmf = parse_pmf(body, "X")
        mean, variance = mean_variance(pmf)
        if variant == "build":
            answer = f"G(s) = {poly_text(pmf)}"
        elif variant == "mean_from_pgf":
            answer = f"E[X] = {ptext(mean)}"
        elif variant == "variance_from_pgf":
            answer = f"Var(X) = {ptext(variance)}"
        else:
            answer = ptext(sum((p for k, p in pmf.items() if k % 2 == 0),
                               Fraction()))
    return {"variant": variant, "query": query, "answer": answer}


class PGFGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(684219)

    def test_output_contract(self):
        example = PGFGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = PGFGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_power_and_combination_steps_are_exact(self):
        generator = PGFGenerator()
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
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "NCR":
                    match = re.fullmatch(r"C\((\d+), (\d+)\)", fields[1])
                    self.assertIsNotNone(match, raw)
                    self.assertEqual(math.comb(int(match.group(1)),
                                               int(match.group(2))), int(fields[2]))

    def test_rendered_polynomials_parse_and_have_unit_coefficient_sum(self):
        generator = PGFGenerator()
        for _ in range(250):
            example = generator.generate()
            for polynomial in re.findall(r"G(?:_X|_S)?\(s\) = ([^.;]+)",
                                         example["problem"] + "; "
                                         + example["final_answer"]):
                parsed = parse_polynomial(polynomial)
                self.assertEqual(sum(parsed.values(), Fraction()), 1)

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in PGFGenerator.VARIANTS:
            generator = PGFGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"], f"probability_pgf_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            PGFGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = PGFGenerator()
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
