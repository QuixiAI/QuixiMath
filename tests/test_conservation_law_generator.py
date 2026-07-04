import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.conservation_law_generator import ConservationLawGenerator
from helpers import DELIM


QUANTITIES = ["Q", "B", "Le", "Lmu"]
PROBLEM_RE = re.compile(
    r"Audit conservation of Q, B, Le, Lmu for reaction (.+)\. "
    r"Quantum numbers: (.+)\."
)
TABLE_RE = re.compile(
    r"([^();]+)\(Q=(-?\d+),B=(-?\d+),Le=(-?\d+),Lmu=(-?\d+)\)"
)
ADD_RE = re.compile(r"(-?\d+) \+ ([^(]+)\((-?\d+)\)")


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    reaction = match.group(1)
    table = {}
    for entry in match.group(2).split("; "):
        table_match = TABLE_RE.fullmatch(entry)
        assert table_match is not None, entry
        table[table_match.group(1)] = {
            "Q": int(table_match.group(2)),
            "B": int(table_match.group(3)),
            "Le": int(table_match.group(4)),
            "Lmu": int(table_match.group(5)),
        }
    left_text, right_text = reaction.split(" -> ")
    left = left_text.split(" + ")
    right = right_text.split(" + ")
    return {"reaction": reaction, "table": table, "left": left,
            "right": right}


def table_text(particles, table):
    entries = []
    for name in particles:
        qn = table[name]
        entries.append(
            f"{name}(Q={qn['Q']},B={qn['B']},Le={qn['Le']},"
            f"Lmu={qn['Lmu']})"
        )
    return "; ".join(entries)


def unique_in_order(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def signed_change(value):
    return f"+{value}" if value > 0 else str(value)


def add_side_steps(steps, quantity, side_name, particles, table):
    total = 0
    for particle in particles:
        value = table[particle][quantity]
        next_total = total + value
        steps.append(
            make_step("QN_ADD", quantity, side_name,
                      f"{total} + {particle}({value})", next_total)
        )
        total = next_total
    return total


def expected_flow(example):
    parts = parse_problem(example["problem"])
    particles = unique_in_order(parts["left"] + parts["right"])
    steps = [
        make_step("CONSERVATION_SETUP", parts["reaction"],
                  "check=Q,B,Le,Lmu"),
        make_step("PARTICLE_TABLE", table_text(particles, parts["table"])),
    ]
    left_totals = {}
    right_totals = {}
    for quantity in QUANTITIES:
        left_totals[quantity] = add_side_steps(
            steps, quantity, "left", parts["left"], parts["table"]
        )
        right_totals[quantity] = add_side_steps(
            steps, quantity, "right", parts["right"], parts["table"]
        )
        status = (
            "conserved" if left_totals[quantity] == right_totals[quantity]
            else "violated"
        )
        steps.append(
            make_step("CONSERVE_CHECK", quantity,
                      f"left={left_totals[quantity]},right="
                      f"{right_totals[quantity]}", status)
        )
    failures = []
    for quantity in QUANTITIES:
        delta = right_totals[quantity] - left_totals[quantity]
        if delta != 0:
            failures.append(f"{quantity} changes by {signed_change(delta)}")
    if failures:
        answer = f"forbidden - {'; '.join(failures)}"
    else:
        answer = "allowed - Q, B, Le, Lmu conserved"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestConservationLawGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ConservationLawGenerator()

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

    def test_quantum_number_addition_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] != "QN_ADD":
                    continue
                match = ADD_RE.fullmatch(fields[3])
                self.assertIsNotNone(match, raw_step)
                start = int(match.group(1))
                value = int(match.group(3))
                self.assertEqual(start + value, int(fields[4]), raw_step)

    def test_conservation_checks_match_totals(self):
        for _ in range(200):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] != "CONSERVE_CHECK":
                    continue
                left_raw, right_raw = fields[2].split(",")
                left = int(left_raw.removeprefix("left="))
                right = int(right_raw.removeprefix("right="))
                expected = "conserved" if left == right else "violated"
                self.assertEqual(fields[3], expected, raw_step)

    def test_variant_is_available(self):
        result = ConservationLawGenerator("audit").generate()
        self.assertIn(result["operation"], {
            "conservation_law_allowed",
            "conservation_law_forbidden",
        })
        parse_problem(result["problem"])

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ConservationLawGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])

    def test_allowed_and_forbidden_both_seen(self):
        seen = {self.gen.generate()["operation"] for _ in range(300)}
        self.assertIn("conservation_law_allowed", seen)
        self.assertIn("conservation_law_forbidden", seen)


if __name__ == "__main__":
    unittest.main()
