"""Independent score-variance oracles for FisherInformationGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.fisher_information_generator import (
    QUERIES, FisherInformationGenerator,
)
from helpers import DELIM
from tests import stats_oracle


def exact(value):
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


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def family_parts(body, variant):
    n = int(re.search(r"n = (\d+) independent", body).group(1))
    if "Bernoulli(p)" in body:
        family, symbol = "bernoulli", "p"
        parameter = Fraction(re.search(r"p = ([\d/]+)", body).group(1))
    elif "Poisson(λ)" in body:
        family, symbol = "poisson", "λ"
        parameter = Fraction(re.search(r"λ = ([\d/]+)", body).group(1))
    elif "Exponential(rate λ)" in body:
        family, symbol = "exponential", "λ"
        parameter = Fraction(re.search(r"λ = ([\d/]+)", body).group(1))
    elif "Normal(μ, σ²)" in body:
        family, symbol = "normal_mu", "μ"
        parameter = Fraction(re.search(r"known σ² = (\d+)", body).group(1))
    else:
        family, symbol = "geometric", "p"
        parameter = Fraction(re.search(r"and p = ([\d/]+)", body).group(1))
    information = stats_oracle.fisher_from_score(family, parameter)
    total = n * information
    bound = 1 / total
    return {"family": family, "symbol": symbol, "parameter": parameter,
            "n": n, "information": information, "total": total,
            "bound": bound}


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    values = family_parts(body, variant)
    if variant == "crlb_check":
        family = values["family"]
        if family == "bernoulli":
            estimator = "p̂"
            estimator_variance = (values["parameter"] *
                                  (1 - values["parameter"]) / values["n"])
        elif family == "poisson":
            estimator = "λ̂"
            estimator_variance = values["parameter"] / values["n"]
        else:
            estimator = "x̄"
            estimator_variance = values["parameter"] / values["n"]
        answer = (f"CRLB = {exact(values['bound'])}; Var({estimator}) = "
                  f"{exact(estimator_variance)}; attains the bound")
        values.update(estimator=estimator,
                      estimator_variance=estimator_variance, answer=answer)
    else:
        symbol = values["symbol"]
        values["answer"] = (
            f"I({symbol}) = {exact(values['information'])}; "
            f"I_n({symbol}) = {exact(values['total'])}; "
            f"CRLB = {exact(values['bound'])}")
    values.update(body=body, variant=variant, query=query)
    return values


class FisherInformationGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(590237)

    def test_output_contract(self):
        example = FisherInformationGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_900_answers_from_problem_text(self):
        generator = FisherInformationGenerator()
        for _ in range(900):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_information_uses_independent_score_variance_identities(self):
        for variant in FisherInformationGenerator.VARIANTS[:-1]:
            generator = FisherInformationGenerator(variant)
            for _ in range(220):
                example = generator.generate()
                parts = oracle_parts(example)
                crlb = next(raw.split(DELIM) for raw in example["steps"]
                            if raw.startswith(f"CRLB{DELIM}"))
                self.assertEqual(Fraction(crlb[2]), parts["bound"])
                self.assertEqual(parts["total"],
                                 parts["n"] * parts["information"])
                self.assertEqual(parts["bound"], 1 / parts["total"])

    def test_bernoulli_score_is_enumerated_over_both_outcomes(self):
        generator = FisherInformationGenerator("bernoulli")
        for _ in range(300):
            parts = oracle_parts(generator.generate())
            p = parts["parameter"]
            score_one = 1 / p
            score_zero = -1 / (1 - p)
            enumerated = p * score_one ** 2 + (1 - p) * score_zero ** 2
            self.assertEqual(parts["information"], enumerated)

    def test_geometric_convention_and_score_variance(self):
        generator = FisherInformationGenerator("geometric")
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            p = parts["parameter"]
            variance_failures = (1 - p) / p ** 2
            information = variance_failures / (1 - p) ** 2
            self.assertEqual(parts["information"], information)
            self.assertIn("on 1, 2, ... with pmf p(1-p)^(x-1)",
                          example["problem"])

    def test_generic_arithmetic_steps_are_exact(self):
        generator = FisherInformationGenerator()
        for _ in range(700):
            example = generator.generate()
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw)

    def test_crlb_check_covers_three_efficient_estimators(self):
        generator = FisherInformationGenerator("crlb_check")
        seen = set()
        for _ in range(500):
            example = generator.generate()
            parts = oracle_parts(example)
            seen.add((parts["family"], parts["estimator"]))
            self.assertEqual(parts["estimator_variance"], parts["bound"])
            check = next(raw.split(DELIM) for raw in example["steps"]
                         if raw.startswith(f"CHECK{DELIM}"))
            left, right = map(Fraction, check[2].split(" = "))
            self.assertEqual(left, right)
            self.assertEqual(check[3], "attains the bound")
        self.assertEqual(seen, {("bernoulli", "p̂"),
                                ("poisson", "λ̂"),
                                ("normal_mu", "x̄")})

    def test_symbolic_derivation_steps_present_for_every_family(self):
        for variant in FisherInformationGenerator.VARIANTS[:-1]:
            example = FisherInformationGenerator(variant).generate()
            codes = [raw.split(DELIM)[0] for raw in example["steps"]]
            self.assertIn("LOG_LIKELIHOOD", codes)
            self.assertGreaterEqual(codes.count("DERIVATIVE"), 2)
            self.assertIn("FISHER_INFO", codes)
            self.assertIn("CRLB", codes)

    def test_all_variants_and_four_queries_are_reachable(self):
        for variant in FisherInformationGenerator.VARIANTS:
            generator = FisherInformationGenerator(variant)
            seen = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(example["operation"],
                                 f"statistics_fisher_information_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            FisherInformationGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = FisherInformationGenerator()
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
