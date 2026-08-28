"""Independent finite-grid Bayesian oracles for DiscretePosteriorGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.discrete_posterior_generator import (
    QUERIES, DiscretePosteriorGenerator,
)
from helpers import DELIM


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


def probability(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_case(body):
    prior_text, successes, trials, failures = re.search(
        r"prior on θ: (.+)\. Observe (\d+) success(?:es)? in (\d+) "
        r"Bernoulli trial(?:s)? \((\d+) failure(?:s)?\)\.", body).groups()
    cells = [re.fullmatch(r"P\(([\d.]+)\) = ([\d/]+)", cell).groups()
             for cell in prior_text.split("; ")]
    grid = tuple(Fraction(theta) for theta, _ in cells)
    prior = tuple(Fraction(weight) for _, weight in cells)
    successes, trials, failures = int(successes), int(trials), int(failures)
    assert successes + failures == trials
    likelihoods = tuple(theta ** successes * (1 - theta) ** failures
                        for theta in grid)
    weights = tuple(p * likelihood for p, likelihood in zip(prior, likelihoods))
    evidence = sum(weights, Fraction(0))
    posterior = tuple(weight / evidence for weight in weights)
    return {"grid": grid, "prior": prior, "successes": successes,
            "trials": trials, "failures": failures,
            "likelihoods": likelihoods, "weights": weights,
            "evidence": evidence, "posterior": posterior}


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    case = parse_case(body)
    case.update(body=body, variant=variant, query=query)
    if variant == "posterior_table":
        case["answer"] = "; ".join(
            f"{exact(theta)}: {probability(posterior)}"
            for theta, posterior in zip(case["grid"], case["posterior"]))
    elif variant == "map":
        maximum = max(case["posterior"])
        assert case["posterior"].count(maximum) == 1
        index = case["posterior"].index(maximum)
        case.update(map_index=index,
                    answer=f"MAP θ = {exact(case['grid'][index])}; "
                           f"posterior {probability(maximum)}")
    elif variant in ("posterior_mean", "posterior_predictive"):
        result = sum((theta * posterior for theta, posterior in
                      zip(case["grid"], case["posterior"])), Fraction(0))
        case["mean"] = result
        if variant == "posterior_mean":
            case["answer"] = f"posterior mean = {exact(result)}"
        else:
            case["answer"] = f"P(next success) = {exact(result)}"
    elif variant == "credible_set":
        order = sorted(range(len(case["grid"])),
                       key=lambda index: (-case["posterior"][index],
                                          case["grid"][index]))
        selected = []
        mass = Fraction(0)
        previous = Fraction(0)
        for index in order:
            previous = mass
            mass += case["posterior"][index]
            selected.append(index)
            if mass >= Fraction(9, 10):
                break
        members = ", ".join(exact(case["grid"][index])
                            for index in sorted(selected,
                                                key=lambda i: case["grid"][i]))
        case.update(order=order, selected=selected, mass=mass,
                    previous_mass=previous,
                    answer=f"{{{members}}}; mass {probability(mass)}")
    else:
        first, second = re.search(
            r"Compare θA = ([\d.]+) with θB = ([\d.]+)\.", body).groups()
        first, second = Fraction(first), Fraction(second)
        first_index, second_index = case["grid"].index(first), case["grid"].index(second)
        ratio = case["likelihoods"][first_index] / case["likelihoods"][second_index]
        case.update(first=first, second=second, ratio=ratio,
                    answer=f"BF({exact(first)}:{exact(second)}) = "
                           f"{probability(ratio)}")
    return case


class DiscretePosteriorGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(974203)

    def test_output_contract(self):
        example = DiscretePosteriorGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_900_answers_from_problem_text(self):
        generator = DiscretePosteriorGenerator()
        for _ in range(900):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_grid_prior_and_trial_construction(self):
        generator = DiscretePosteriorGenerator()
        seen_sizes = set()
        seen_prior_kinds = set()
        for _ in range(600):
            parts = oracle_parts(generator.generate())
            seen_sizes.add(len(parts["grid"]))
            self.assertEqual(tuple(sorted(parts["grid"])), parts["grid"])
            self.assertEqual(len(parts["grid"]), len(set(parts["grid"])))
            self.assertTrue(all(Fraction(1, 10) <= value <= Fraction(9, 10)
                                for value in parts["grid"]))
            self.assertEqual(sum(parts["prior"], Fraction(0)), 1)
            self.assertLessEqual(parts["trials"], 6)
            seen_prior_kinds.add("uniform" if len(set(parts["prior"])) == 1
                                 else "dyadic")
        self.assertEqual(seen_sizes, {3, 4})
        self.assertEqual(seen_prior_kinds, {"uniform", "dyadic"})

    def test_posterior_rows_match_prior_times_likelihood(self):
        for variant in DiscretePosteriorGenerator.VARIANTS[:-1]:
            generator = DiscretePosteriorGenerator(variant)
            for _ in range(160):
                example = generator.generate()
                parts = oracle_parts(example)
                bayes_rows = [raw.split(DELIM) for raw in example["steps"]
                              if raw.startswith(f"BAYES_ROW{DELIM}")]
                posterior_rows = [raw.split(DELIM) for raw in example["steps"]
                                  if raw.startswith(f"POSTERIOR_ROW{DELIM}")]
                self.assertEqual(len(bayes_rows), len(parts["grid"]))
                self.assertEqual(len(posterior_rows), len(parts["grid"]))
                for row, theta, weight in zip(
                        bayes_rows, parts["grid"], parts["weights"]):
                    self.assertEqual(Fraction(row[1]), theta)
                    self.assertEqual(Fraction(row[3]), weight)
                for row, theta, posterior in zip(
                        posterior_rows, parts["grid"], parts["posterior"]):
                    self.assertEqual(Fraction(row[1]), theta)
                    self.assertEqual(Fraction(row[2]), posterior)
                self.assertEqual(sum(parts["posterior"], Fraction(0)), 1)

    def test_map_is_unique_and_matches_largest_posterior(self):
        generator = DiscretePosteriorGenerator("map")
        for _ in range(350):
            example = generator.generate()
            parts = oracle_parts(example)
            maximum = max(parts["posterior"])
            self.assertEqual(parts["posterior"].count(maximum), 1)
            check = next(raw.split(DELIM) for raw in example["steps"]
                         if raw.startswith(f"CHECK{DELIM}unique maximum"))
            self.assertEqual(Fraction(check[3]), maximum)

    def test_posterior_mean_and_predictive_are_same_mixture(self):
        results = {}
        for variant in ("posterior_mean", "posterior_predictive"):
            generator = DiscretePosteriorGenerator(variant)
            for _ in range(300):
                parts = oracle_parts(generator.generate())
                expected = sum((theta * posterior for theta, posterior in
                                zip(parts["grid"], parts["posterior"])),
                               Fraction(0))
                self.assertEqual(parts["mean"], expected)
                self.assertGreaterEqual(expected, 0)
                self.assertLessEqual(expected, 1)
            results[variant] = True
        self.assertEqual(set(results), {"posterior_mean", "posterior_predictive"})

    def test_credible_set_is_minimal_and_uses_stated_tie_rule(self):
        generator = DiscretePosteriorGenerator("credible_set")
        for _ in range(400):
            example = generator.generate()
            parts = oracle_parts(example)
            self.assertLess(parts["previous_mass"], Fraction(9, 10))
            self.assertGreaterEqual(parts["mass"], Fraction(9, 10))
            expected_order = sorted(
                range(len(parts["grid"])),
                key=lambda index: (-parts["posterior"][index],
                                   parts["grid"][index]))
            self.assertEqual(parts["order"], expected_order)
            picks = [raw.split(DELIM) for raw in example["steps"]
                     if raw.startswith(f"CREDIBLE_PICK{DELIM}")]
            self.assertEqual([Fraction(row[1]) for row in picks],
                             [parts["grid"][index] for index in parts["selected"]])
            self.assertIn("break ties by smaller θ", example["problem"])

    def test_bayes_factor_uses_likelihood_not_prior(self):
        generator = DiscretePosteriorGenerator("bayes_factor")
        for _ in range(350):
            example = generator.generate()
            parts = oracle_parts(example)
            first = (parts["first"] ** parts["successes"] *
                     (1 - parts["first"]) ** parts["failures"])
            second = (parts["second"] ** parts["successes"] *
                      (1 - parts["second"]) ** parts["failures"])
            self.assertEqual(parts["ratio"], first / second)
            row = next(raw.split(DELIM) for raw in example["steps"]
                       if raw.startswith(f"BAYES_FACTOR{DELIM}"))
            self.assertEqual(Fraction(row[2]), parts["ratio"])

    def test_generic_arithmetic_steps_are_exact(self):
        generator = DiscretePosteriorGenerator()
        for _ in range(700):
            example = generator.generate()
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "SUM":
                    terms = [Fraction(value) for value in fields[1].split(" + ")]
                    self.assertEqual(sum(terms, Fraction(0)),
                                     Fraction(fields[2]), raw)
                elif fields[0] == "A":
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

    def test_all_variants_and_four_queries_are_reachable(self):
        for variant in DiscretePosteriorGenerator.VARIANTS:
            generator = DiscretePosteriorGenerator(variant)
            seen = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(example["operation"],
                                 f"statistics_discrete_posterior_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            DiscretePosteriorGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = DiscretePosteriorGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            rendered = "\n".join([example["problem"], *example["steps"],
                                    example["final_answer"]])
            self.assertNotRegex(rendered,
                                r"1x|\^1\b|\+ 0(?= \+|\||\n|$)|--|− -")
            for raw in example["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
