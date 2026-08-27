"""Strand-wide conventions for foundations generators.

Phase 0 has no registered ``FOUNDATIONS`` generator yet, so fixtures pin the
notation and rejection rules while a discovery test exercises the module flag.
Generator-specific A9 tests remain responsible for parsing their declared
answer shape with :mod:`tests.foundations_oracle`.
"""
import importlib
import os
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from helpers import DELIM  # noqa: E402
from tests import foundations_oracle as oracle  # noqa: E402
from tests.conventions_common import (  # noqa: E402
    assert_contract, assert_pipe_safe, flagged_generators, sample_examples,
)

ASCII_CONNECTIVES = (
    (re.compile(r"(?<!\w)&&?(?!\w)"), "use ∧, not &/&&"),
    (re.compile(r"<->|<=>"), "use ↔"),
    (re.compile(r"->"), "use →"),
    (re.compile(r"\b(?:AND|OR|NOT|XOR|NAND)\b"),
     "use the canonical connective symbols"),
)


def example_text(example):
    return "\n".join((str(example.get("problem", "")),
                      "\n".join(example.get("steps", [])),
                      str(example.get("final_answer", ""))))


def connective_violations(example):
    """Non-canonical ASCII spellings of logical connectives."""
    text = example_text(example)
    return [message for pattern, message in ASCII_CONNECTIVES
            if pattern.search(text)]


def roster_violations(example):
    """Every non-nested roster is parseable, sorted and duplicate-free."""
    bad = []
    for token in re.findall(r"\{[^{}]*\}", example_text(example)):
        # Set-builder expressions have their own grammar, not roster order.
        if " ∈ " in token and " : " in token:
            try:
                oracle.eval_set_builder(token)
            except Exception as exc:  # noqa: BLE001 - reported as a failure
                bad.append(f"set-builder {token!r} does not parse: {exc}")
            continue
        try:
            items = oracle.parse_roster(token)
        except Exception as exc:  # noqa: BLE001 - reported as a failure
            bad.append(f"roster {token!r} does not parse: {exc}")
            continue
        if len(items) != len(set(items)):
            bad.append(f"roster {token!r} contains duplicates")
        if not oracle.roster_order_ok(items):
            bad.append(f"roster {token!r} is not in canonical order")
    return bad


def formula_violations(formulas):
    """Explicit printed formulas must round-trip through the oracle grammar."""
    bad = []
    for formula in formulas:
        if not oracle.is_canonical_formula(formula):
            bad.append(f"formula {formula!r} is not canonical")
    return bad


def check_example(testcase, example):
    assert_contract(testcase, example)
    assert_pipe_safe(testcase, example)
    testcase.assertFalse(connective_violations(example))
    testcase.assertFalse(roster_violations(example))


class FoundationsConventionsTest(unittest.TestCase):
    SAMPLE = 200

    def test_flagged_generators_obey_the_conventions(self):
        for gen in flagged_generators("FOUNDATIONS"):
            with self.subTest(generator=type(gen).__name__):
                for example in sample_examples(gen, self.SAMPLE, seed=7):
                    check_example(self, example)

    def test_discovery_finds_a_flagged_module(self):
        module = importlib.import_module("generators.set_operations_generator")
        module.FOUNDATIONS = True
        try:
            names = {type(gen).__name__
                     for gen in flagged_generators("FOUNDATIONS")}
            self.assertIn("SetOperationsGenerator", names)
        finally:
            del module.FOUNDATIONS


class CheckerFixtureTest(unittest.TestCase):
    def good(self, **overrides):
        answer = "{1, 2, 3}"
        example = dict(
            problem_id="fixture",
            operation="foundations_set_fixture",
            problem=("Let A = {1, 2, 3} and B = {2, 3}. Find A ∩ B and "
                     "state card(A)."),
            steps=[f"SET_SETUP{DELIM}A = {{1, 2, 3}}{DELIM}B = {{2, 3}}",
                   f"Z{DELIM}{answer}"],
            final_answer=answer,
        )
        example.update(overrides)
        return example

    def test_good_fixture_passes(self):
        check_example(self, self.good())

    def test_ascii_bar_is_rejected(self):
        bad = self.good(problem="Find |A| for A = {1, 2, 3}.")
        with self.assertRaises(AssertionError):
            check_example(self, bad)

    def test_ascii_connective_is_rejected(self):
        bad = self.good(problem="Classify p AND q.")
        self.assertTrue(connective_violations(bad))

    def test_duplicate_roster_is_rejected(self):
        bad = self.good(problem="Let A = {1, 1, 2}.")
        self.assertTrue(roster_violations(bad))

    def test_out_of_order_roster_is_rejected(self):
        bad = self.good(problem="Let A = {3, 1, 2}.")
        self.assertTrue(roster_violations(bad))

    def test_set_builder_uses_colon_and_oracle_grammar(self):
        good = self.good(problem="Let A = {x ∈ ℤ : -3 ≤ x < 4}.")
        self.assertFalse(roster_violations(good))
        bad = self.good(problem="Let A = {x ∈ ℤ : x is blue}.")
        self.assertTrue(roster_violations(bad))

    def test_formula_must_be_canonically_parenthesized(self):
        self.assertFalse(formula_violations(["(p ∧ ¬q) → r"]))
        self.assertTrue(formula_violations(["p ∧ q ∨ r"]))

    def test_truth_rows_are_t_before_f(self):
        rows = oracle.all_assignments(("q", "p"))
        rendered = [oracle.row_text(row) for row in rows]
        self.assertEqual(rendered,
                         ["p=T, q=T", "p=T, q=F",
                          "p=F, q=T", "p=F, q=F"])


if __name__ == "__main__":
    unittest.main()
