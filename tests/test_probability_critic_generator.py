"""Independent prompt-only oracle for ProbabilityCriticGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.probability_critic_generator import QUERIES, ProbabilityCriticGenerator
from helpers import DELIM


def ptext(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_display(body):
    lines = body.splitlines()
    source_index = next(index for index, line in enumerate(lines)
                        if line.startswith("Source problem: "))
    source = lines[source_index][len("Source problem: "):]
    shown = []
    for line in lines[source_index + 1:]:
        match = re.fullmatch(r"(\d+)\) (.+)", line)
        assert match is not None, line
        assert int(match.group(1)) == len(shown) + 1
        shown.append(match.group(2))
    return source, shown


def tree_truth(source):
    match = re.search(r"success counts (\d+)/(\d+) and (\d+)/(\d+)", source)
    a, b, c, d = map(int, match.groups())
    p, q = Fraction(a, b), Fraction(c, d)
    branches = {"SF": p * (1 - q), "FS": (1 - p) * q}
    return branches, sum(branches.values(), Fraction())


def parse_priors(text):
    result = {}
    for item in text.split("; "):
        label, value = item.split("=")
        result[label] = Fraction(value)
    assert sum(result.values(), Fraction()) == 1
    return result


def bayes_truth(source):
    match = re.search(r"Urns: (.+)\. Priors: (.+)\. One urn.*"
                      r"Observations: ([a-z]+)\. Target: P\((U\d+) given",
                      source)
    inventories, priors_text, observation, target = match.groups()
    priors = parse_priors(priors_text)
    likelihoods = {}
    for item in inventories.split("; "):
        row = re.fullmatch(r"(U\d+) has (\d+) ([a-z]+) and (\d+) ([a-z]+)", item)
        label, n1, color1, n2, color2 = row.groups()
        counts = {color1: int(n1), color2: int(n2)}
        likelihoods[label] = Fraction(counts[observation], sum(counts.values()))
    terms = {label: priors[label] * likelihoods[label] for label in priors}
    evidence = sum(terms.values(), Fraction())
    return terms, target, terms[target] / evidence


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    source, shown = parse_display(body)
    if variant in ("tree_error", "missing_step"):
        branches, total = tree_truth(source)
        if variant == "tree_error":
            bad = None
            for index, label in enumerate(("SF", "FS"), 1):
                row = re.fullmatch(rf"Branch {label}: .+ = (\d+(?:/\d+)?)",
                                   shown[index - 1])
                assert row is not None
                if Fraction(row.group(1)) != branches[label]:
                    assert bad is None
                    bad = index
            assert bad is not None
            shown_values = [Fraction(re.search(r"= (\d+(?:/\d+)?)$", line).group(1))
                            for line in shown[:2]]
            assert shown[2].endswith(f"= {ptext(sum(shown_values, Fraction()))}")
            assert shown[3] == f"Answer: {ptext(sum(shown_values, Fraction()))}"
            answer = f"step {bad}; {ptext(total)}"
        else:
            blanks = [index for index, line in enumerate(shown[:2]) if line == "____"]
            assert len(blanks) == 1
            blank = blanks[0]
            label = ("SF", "FS")[blank]
            answer = (f"step {blank + 1}; branch {label} = {ptext(branches[label])}; "
                      f"answer {ptext(total)}")
    elif variant == "bayes_error":
        terms, target, posterior = bayes_truth(source)
        bad = None
        shown_terms = {}
        for index, label in enumerate(terms, 1):
            row = re.fullmatch(rf"Bayes term {label}: .+ = (\d+(?:/\d+)?)",
                               shown[index - 1])
            assert row is not None
            shown_terms[label] = Fraction(row.group(1))
            if shown_terms[label] != terms[label]:
                assert bad is None
                bad = index
        assert bad is not None
        shown_evidence = sum(shown_terms.values(), Fraction())
        assert shown[3].endswith(f"= {ptext(shown_evidence)}")
        shown_posterior = shown_terms[target] / shown_evidence
        assert shown[4].endswith(f"= {ptext(shown_posterior)}")
        assert shown[5] == f"Answer: {ptext(shown_posterior)}"
        answer = f"step {bad}; {ptext(posterior)}"
    else:
        counts = re.search(r"Stage 1 succeeds in (\d+) of (\d+).*"
                           r"stage 2 succeeds in (\d+) of (\d+)", source)
        a, b, c, d = map(int, counts.groups())
        none = (1 - Fraction(a, b)) * (1 - Fraction(c, d))
        correct = 1 - none
        assert shown[3] == f"Answer for at least one success: {ptext(none)}"
        answer = f"step 4; {ptext(correct)}"
    return {"variant": variant, "query": query, "answer": answer}


class ProbabilityCriticGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(240775)

    def test_output_contract(self):
        example = ProbabilityCriticGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = ProbabilityCriticGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_steps_are_exact(self):
        generator = ProbabilityCriticGenerator()
        for _ in range(350):
            example = generator.generate()
            oracle_parts(example)
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

    def test_verify_sweep_and_flag(self):
        generator = ProbabilityCriticGenerator()
        for _ in range(250):
            example = generator.generate()
            fields = [raw.split(DELIM) for raw in example["steps"]]
            flag_index = next(index for index, row in enumerate(fields)
                              if row[0] == "FLAG")
            line = int(fields[flag_index][1])
            self.assertEqual(fields[:flag_index],
                             [["VERIFY", str(index), "ok"]
                              for index in range(1, line)])

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in ProbabilityCriticGenerator.VARIANTS:
            generator = ProbabilityCriticGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_critic_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ProbabilityCriticGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = ProbabilityCriticGenerator()
        for _ in range(300):
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
