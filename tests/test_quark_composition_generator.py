import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.quark_composition_generator import QuarkCompositionGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Given quark charges u=([^,]+), d=([^,]+), s=([^,]+), c=([^,]+), "
    r"b=([^ ]+) and antiquarks have opposite charge, compute the "
    r"electric charge of (?:a|an) (baryon|antibaryon|meson) with constituents "
    r"([^.]+)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def signed_fraction(value):
    fr = Fraction(value)
    if fr > 0:
        return f"+{fraction_text(fr)}"
    return fraction_text(fr)


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    table = {
        "u": Fraction(match.group(1)),
        "d": Fraction(match.group(2)),
        "s": Fraction(match.group(3)),
        "c": Fraction(match.group(4)),
        "b": Fraction(match.group(5)),
    }
    return {
        "table": table,
        "variant": match.group(6),
        "constituents": match.group(7).split(" "),
    }


def charge_of(name, table):
    if name.startswith("anti_"):
        return -table[name.removeprefix("anti_")]
    return table[name]


def expected_flow(example):
    parts = parse_problem(example["problem"])
    constituents = parts["constituents"]
    table = "u=2/3,d=-1/3,s=-1/3,c=2/3,b=-1/3; anti=-charge"
    steps = [
        make_step("QUARK_SETUP", parts["variant"], " ".join(constituents),
                  table),
    ]
    total = Fraction(0)
    for name in constituents:
        charge = charge_of(name, parts["table"])
        next_total = total + charge
        steps.append(make_step("QUARK_CHARGE", name, fraction_text(charge)))
        steps.append(
            make_step("A", fraction_text(total), fraction_text(charge),
                      fraction_text(next_total))
        )
        total = next_total
    answer = f"Q = {signed_fraction(total)}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestQuarkCompositionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = QuarkCompositionGenerator()

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

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_quark_charge_steps_match_prompt_table(self):
        for _ in range(300):
            result = self.gen.generate()
            parts = parse_problem(result["problem"])
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "QUARK_CHARGE":
                    self.assertEqual(charge_of(fields[1], parts["table"]),
                                     Fraction(fields[2]), raw_step)

    def test_variants_are_available(self):
        for variant in QuarkCompositionGenerator.VARIANTS:
            result = QuarkCompositionGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"quark_composition_{variant}")
            self.assertEqual(parse_problem(result["problem"])["variant"],
                             variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            QuarkCompositionGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])

    def test_positive_negative_and_neutral_charges_occur(self):
        answers = {self.gen.generate()["final_answer"] for _ in range(500)}
        self.assertTrue(any(answer.startswith("Q = +") for answer in answers))
        self.assertTrue(any(answer.startswith("Q = -") for answer in answers))
        self.assertIn("Q = 0", answers)


if __name__ == "__main__":
    unittest.main()
