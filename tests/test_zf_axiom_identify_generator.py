"""Expansion-table oracle for ZFAxiomIdentifyGenerator."""
import random
import re
import unittest

from generators.zf_axiom_identify_generator import (
    QUERIES, ZFAxiomIdentifyGenerator,
)
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def single_axiom(target):
    if target == "ω":
        return "Infinity", "infinity"
    if target.startswith("∪"):
        return "Union", "union"
    if target.startswith("P("):
        return "Power Set", "power"
    if target.startswith("{x ∈"):
        return "Separation", "separation"
    if re.match(r"^\{f_\d+\(x\) : x ∈ \{[-\d, ]+\}\}$", target):
        return "Replacement", "replacement"
    if re.match(r"^\{A_\d+, B_\d+\}$", target):
        return "Pairing", "pair"
    raise AssertionError(target)


def definition_answer(abbreviation):
    union = re.fullmatch(r"(A_\d+) ∪ (B_\d+)", abbreviation)
    if union:
        left, right = union.groups()
        return f"∪{{{left}, {right}}}; Pairing, Union", "union"
    singleton = re.fullmatch(r"singleton\((A_\d+)\)", abbreviation)
    if singleton:
        return f"{{{singleton.group(1)}}}; Pairing", "singleton"
    intersection = re.fullmatch(r"(\{[-\d, ]+\}) ∩ (B_\d+)", abbreviation)
    if intersection:
        base, right = intersection.groups()
        return f"{{x ∈ {base} : x ∈ {right}}}; Separation", "intersection"
    difference = re.fullmatch(r"(\{[-\d, ]+\}) − (B_\d+)", abbreviation)
    if difference:
        base, right = difference.groups()
        return f"{{x ∈ {base} : x ∉ {right}}}; Separation", "difference"
    image = re.fullmatch(r"(f_\d+)\[(\{[-\d, ]+\})\]", abbreviation)
    assert image is not None, abbreviation
    function, source = image.groups()
    return f"{{{function}(x) : x ∈ {source}}}; Replacement", "image"


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "single_step":
        match = re.fullmatch(r"ZF formation target: (.+)\.", body)
        assert match is not None, body
        target = match.group(1)
        answer, case = single_axiom(target)
        forms = [(target, answer)]
    elif variant == "construction_sequence":
        match = re.fullmatch(
            r"ZF construction target: (.+?)\. .+\. Displayed expansion: "
            r"(.+)\.", body)
        assert match is not None, body
        target, expansion = match.groups()
        if " × " in target:
            answer = "Pairing, Power Set, Power Set, Separation"
            case = "product"
        elif " ∪ " in target:
            answer = "Pairing, Union"
            case = "union"
        else:
            answer = "Pairing"
            case = "singleton"
        forms = None
    else:
        match = re.fullmatch(r"ZF definition: (.+)\.", body)
        assert match is not None, body
        abbreviation = match.group(1)
        answer, case = definition_answer(abbreviation)
        forms = None
    return {"variant": variant, "query": query, "answer": answer,
            "case": case, "forms": forms}


class ZFAxiomIdentifyGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(141421)

    def test_output_contract(self):
        example = ZFAxiomIdentifyGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = ZFAxiomIdentifyGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_single_step_form_is_exact(self):
        generator = ZFAxiomIdentifyGenerator("single_step")
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            form_steps = [raw.split(DELIM)[1:]
                          for raw in example["steps"]
                          if raw.startswith("FORM" + DELIM)]
            self.assertEqual(form_steps, [list(parts["forms"][0])])

    def test_every_case_is_reachable(self):
        expected = {
            "single_step": {"pair", "union", "power", "separation",
                            "replacement", "infinity"},
            "construction_sequence": {"union", "product", "singleton"},
            "definition_expansion": {"union", "singleton", "intersection",
                                     "difference", "image"},
        }
        for variant, cases in expected.items():
            generator = ZFAxiomIdentifyGenerator(variant)
            seen = {oracle_parts(generator.generate())["case"]
                    for _ in range(1200)}
            self.assertEqual(seen, cases)

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in ZFAxiomIdentifyGenerator.VARIANTS:
            generator = ZFAxiomIdentifyGenerator(variant)
            seen_queries = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"zf_axiom_identify_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ZFAxiomIdentifyGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = ZFAxiomIdentifyGenerator()
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
