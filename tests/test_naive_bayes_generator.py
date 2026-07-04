import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.naive_bayes_generator import NaiveBayesGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Classify query (.+) by naive Bayes with Laplace smoothing alpha=1\. "
    r"Feature-one counts: Spam N=(\d+), (.+); Ham N=(\d+), (.+)\. "
    r"Use class priors from N\."
)

CLASSES = ["Spam", "Ham"]
ALPHA = 1


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def pairs_text(pairs):
    return ", ".join(f"{name}={value}" for name, value in pairs)


def parse_pairs(raw):
    pairs = []
    for piece in raw.split(", "):
        name, value = piece.split("=")
        pairs.append((name, int(value)))
    return pairs


def parse_count_pairs(raw):
    return {name: value for name, value in parse_pairs(raw)}


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    if not match:
        raise AssertionError(problem)
    query = parse_pairs(match.group(1))
    totals = {"Spam": int(match.group(2)), "Ham": int(match.group(4))}
    counts = {
        "Spam": parse_count_pairs(match.group(3)),
        "Ham": parse_count_pairs(match.group(5)),
    }
    return query, totals, counts


def expected_flow(example):
    query, totals, counts = parse_problem(example["problem"])
    total_all = sum(totals.values())
    steps = [
        make_step("NB_SETUP", f"query={pairs_text(query)}",
                  f"alpha={ALPHA}", f"classes={','.join(CLASSES)}"),
    ]

    priors = {}
    likelihoods = {}
    for class_name in CLASSES:
        total = totals[class_name]
        prior = Fraction(total, total_all)
        priors[class_name] = prior
        steps.append(make_step("D", total, total_all, fraction_text(prior)))
        steps.append(make_step("NB_PRIOR", class_name, fraction_text(prior)))
        class_likelihoods = []
        denom = total + 2 * ALPHA
        for feature, value in query:
            ones = counts[class_name][feature]
            if value == 1:
                observed = ones
            else:
                observed = total - ones
                steps.append(make_step("S", total, ones, observed))
            numerator = observed + ALPHA
            probability = Fraction(numerator, denom)
            steps.extend([
                make_step("NB_FEATURE_COUNT", class_name,
                          f"{feature}={value}", f"count={observed}"),
                make_step("A", observed, ALPHA, numerator),
                make_step("A", total, 2 * ALPHA, denom),
                make_step("D", numerator, denom, fraction_text(probability)),
                make_step("NB_LIKELIHOOD", class_name,
                          f"{feature}={value}", fraction_text(probability)),
            ])
            class_likelihoods.append(probability)
        likelihoods[class_name] = class_likelihoods

    scores = {}
    for class_name in CLASSES:
        running = priors[class_name]
        steps.append(make_step("NB_SCORE", class_name,
                               f"start={fraction_text(running)}"))
        for likelihood in likelihoods[class_name]:
            new_running = running * likelihood
            steps.append(make_step("M", fraction_text(running),
                                   fraction_text(likelihood),
                                   fraction_text(new_running)))
            running = new_running
        scores[class_name] = running
        steps.append(make_step("NB_SCORE", class_name,
                               f"score={fraction_text(running)}"))

    score_total = scores["Spam"] + scores["Ham"]
    posteriors = {
        class_name: scores[class_name] / score_total
        for class_name in CLASSES
    }
    prediction = "Spam" if scores["Spam"] > scores["Ham"] else "Ham"
    relation = ">" if prediction == "Spam" else "<"
    steps.extend([
        make_step("A", fraction_text(scores["Spam"]),
                  fraction_text(scores["Ham"]), fraction_text(score_total)),
        make_step("D", fraction_text(scores["Spam"]),
                  fraction_text(score_total),
                  fraction_text(posteriors["Spam"])),
        make_step("D", fraction_text(scores["Ham"]),
                  fraction_text(score_total), fraction_text(posteriors["Ham"])),
        make_step("CHECK", "Spam vs Ham",
                  f"{fraction_text(scores['Spam'])} {relation} "
                  f"{fraction_text(scores['Ham'])}",
                  f"predict={prediction}"),
    ])
    answer = (
        f"class={prediction}; "
        f"P_Spam_given_x={fraction_text(posteriors['Spam'])}; "
        f"P_Ham_given_x={fraction_text(posteriors['Ham'])}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestNaiveBayesGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = NaiveBayesGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_variants_are_available(self):
        for variant in NaiveBayesGenerator.VARIANTS:
            result = NaiveBayesGenerator(variant).generate()
            self.assertEqual(result["operation"], f"naive_bayes_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)
            query, _, _ = parse_problem(result["problem"])
            expected_count = 2 if variant == "two_feature" else 3
            self.assertEqual(len(query), expected_count)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            NaiveBayesGenerator("bogus")

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
