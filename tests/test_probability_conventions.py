"""Strand-wide conventions for the probability generators.

``plans/probability_plan.md`` §3/§4: every module flagged ``PROBABILITY = True``
must render answers in one dialect. This module owns the checkers and runs
them over 200 sampled examples of every flagged generator. The strand is
still empty at Phase 0, so the checkers themselves are pinned by fixtures —
one synthetic example per rule that must be rejected — and the discovery
path is exercised by flagging an existing probability generator for the
duration of a test.
"""
import importlib
import math
import os
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from helpers import DELIM  # noqa: E402
from tests.conventions_common import (  # noqa: E402
    assert_contract, assert_pipe_safe, flagged_generators, pipe_violations,
    sample_examples,
)

#: Bars that must never appear: the ASCII delimiter is checked by
#: ``pipe_violations``; ``∣`` is reserved for divisibility in the
#: foundations strand and ``│``/``｜`` are lookalikes.
BAR_CHARS = ("∣", "│", "｜")

FRACTION_RE = re.compile(r"(?<![\w/.])(-?\d+)/(\d+)(?![\d.])")
P_VALUE_RE = re.compile(r"P\([^)]*\)\s*=\s*(-?\d+(?:\.\d+)?%|-?\d+/\d+"
                        r"|-?\d+(?:\.\d+)?)")
BARE_VALUE_RE = re.compile(r"-?\d+(?:\.\d+)?%|-?\d+/\d+|-?\d+(?:\.\d+)?")
#: Operations whose bare numeric answer is a probability.
PROBABILITY_OP_RE = re.compile(r"prob", re.I)
#: … unless the operation names a quantity that is not a probability.
NON_PROBABILITY_OP_RE = re.compile(
    r"mean|expect|variance|var\b|sd\b|deviation|odds|count|outcomes|"
    r"trials|sample_size|estimate|time|paths|period", re.I)


def _value(text):
    """Exact value of a probability token: '3/8', '0.375', '37.5%'."""
    text = text.strip()
    if text.endswith("%"):
        return float(text[:-1]) / 100
    if "/" in text:
        num, den = text.split("/")
        return float(num) / float(den)
    return float(text)


def example_text(example):
    """Problem, steps and answer as one string."""
    return "\n".join([str(example.get("problem", "")),
                      "\n".join(example.get("steps", [])),
                      str(example.get("final_answer", ""))])


def bar_violations(example):
    """Any bar-like character, anywhere (§3: conditioning uses ``given``)."""
    text = example_text(example)
    out = [f"text contains {char!r}" for char in BAR_CHARS if char in text]
    for raw in example.get("steps", []):
        for field in raw.split(DELIM)[1:]:
            if field.count("(") != field.count(")"):
                out.append(f"unbalanced parentheses in step field: {raw}")
    return out + pipe_violations(example)


def lowest_terms_violations(text):
    """Every ``a/b`` in ``text`` must be reduced, with b > 1."""
    out = []
    for num, den in FRACTION_RE.findall(str(text)):
        n, d = int(num), int(den)
        if d == 0:
            out.append(f"zero denominator in {num}/{den}")
        elif d == 1:
            out.append(f"{num}/{den} should be written as an integer")
        elif math.gcd(abs(n), d) != 1:
            out.append(f"{num}/{den} is not in lowest terms")
    return out


def probability_violations(example):
    """Probability-looking numbers in the answer must lie in [0, 1].

    Those are the values of ``P(...) = v`` phrases, plus a bare numeric
    answer when the operation names a probability (and not a mean, a
    variance, odds or a count).
    """
    answer = str(example.get("final_answer", ""))
    tokens = list(P_VALUE_RE.findall(answer))
    operation = str(example.get("operation", ""))
    if (BARE_VALUE_RE.fullmatch(answer.strip())
            and PROBABILITY_OP_RE.search(operation)
            and not NON_PROBABILITY_OP_RE.search(operation)):
        tokens.append(answer.strip())
    out = []
    for token in tokens:
        value = _value(token)
        if not 0 <= value <= 1:
            out.append(f"probability {token} outside [0, 1]")
    return out


def conditioning_violations(example):
    """Conditioning must read ``P(A given B)`` — never a bar."""
    text = example_text(example)
    out = [f"conditioning bar {char!r} in text" for char in BAR_CHARS
           if char in text]
    # ``P(A) given B`` is conditioning written outside the parentheses;
    # prose such as "P(A) given that P(B) = 1/3" is allowed (§3).
    if re.search(r"P\([^)]*\)\s+given\s+(?!that\b|P\()", text):
        out.append("'given' must sit inside P(...), as P(A given B)")
    return out


def roster_violations(text):
    """Rosters are duplicate-free and in enumeration order (§3)."""
    out = []
    for body in re.findall(r"\{([^{}]*)\}", str(text)):
        body = body.strip()
        items = [] if not body else [i.strip() for i in body.split(",")]
        if len(set(items)) != len(items):
            out.append(f"duplicate item in roster {{{body}}}")
        if all(re.fullmatch(r"-?\d+", i) for i in items) and items:
            values = [int(i) for i in items]
            if values != sorted(values):
                out.append(f"roster {{{body}}} is not ascending")
        if set(items) == {"H", "T"} and items[0] != "H":
            out.append(f"roster {{{body}}} puts T before H")
    return out


def z_payload_violations(example):
    """The final step must be exactly ``Z|<final_answer>``."""
    steps = example.get("steps") or []
    if not steps:
        return ["no steps"]
    expected = f"Z{DELIM}{example.get('final_answer')}"
    if steps[-1] != expected:
        return [f"last step {steps[-1]!r} is not {expected!r}"]
    return []


def check_example(testcase, example):
    """Runs every strand rule against one example."""
    assert_contract(testcase, example)
    assert_pipe_safe(testcase, example)
    for label, violations in (
            ("bars", bar_violations(example)),
            ("lowest terms", lowest_terms_violations(example["final_answer"])),
            ("probability range", probability_violations(example)),
            ("conditioning", conditioning_violations(example)),
            ("roster", roster_violations(example_text(example))),
            ("Z payload", z_payload_violations(example))):
        testcase.assertFalse(violations, f"{label}: {violations}")


class ProbabilityConventionsTest(unittest.TestCase):
    """Every flagged generator obeys the strand conventions."""

    SAMPLE = 200

    def test_flagged_generators_obey_the_conventions(self):
        for gen in flagged_generators("PROBABILITY"):
            with self.subTest(generator=type(gen).__name__):
                for example in sample_examples(gen, self.SAMPLE, seed=7):
                    check_example(self, example)

    def test_discovery_finds_a_flagged_module(self):
        """The PROBABILITY flag is the strand's entry point; prove it works
        (and that the checkers pass on a real probability generator) by
        flagging one for the duration of the test."""
        module = importlib.import_module(
            "generators.simple_probability_generator")
        module.PROBABILITY = True
        try:
            found = flagged_generators("PROBABILITY")
            names = {type(gen).__name__ for gen in found}
            self.assertIn("SimpleProbabilityGenerator", names)
            for gen in found:
                if type(gen).__name__ == "SimpleProbabilityGenerator":
                    for example in sample_examples(gen, self.SAMPLE, seed=3):
                        check_example(self, example)
        finally:
            del module.PROBABILITY
        self.assertNotIn("SimpleProbabilityGenerator",
                         {type(g).__name__
                          for g in flagged_generators("PROBABILITY")})


class CheckerFixtureTest(unittest.TestCase):
    """Each checker rejects a synthetic example that breaks its rule."""

    def good(self, **overrides):
        example = dict(
            problem_id="fixture",
            operation="probability_spinner",
            problem=("A spinner with 4 equal sectors labelled 1, 2, 3, 4 is "
                     "spun. Find P(A given B) for A = even."),
            steps=[f"EVENT{DELIM}A{DELIM}{{2, 4}}{DELIM}2",
                   f"PROB_SETUP{DELIM}2{DELIM}4",
                   f"F{DELIM}2/4{DELIM}1/2",
                   f"Z{DELIM}1/2"],
            final_answer="1/2",
        )
        example.update(overrides)
        return example

    def test_good_fixture_passes_every_checker(self):
        check_example(self, self.good())

    def test_ascii_bar_is_rejected(self):
        example = self.good(problem="Find P(A|B) for the spinner.")
        self.assertTrue(bar_violations(example))
        with self.assertRaises(AssertionError):
            check_example(self, example)

    def test_unicode_bar_is_rejected(self):
        example = self.good(final_answer="1/2", problem="Find P(A ∣ B).")
        self.assertTrue(bar_violations(example))
        self.assertTrue(conditioning_violations(example))

    def test_bar_inside_a_step_field_is_rejected(self):
        example = self.good(steps=[
            f"COND_FORMULA{DELIM}P(A{DELIM}B) = P(A and B)/P(B)",
            f"Z{DELIM}1/2"])
        self.assertTrue(bar_violations(example))

    def test_unreduced_fraction_is_rejected(self):
        example = self.good(final_answer="2/4", steps=[f"Z{DELIM}2/4"])
        self.assertTrue(lowest_terms_violations(example["final_answer"]))
        with self.assertRaises(AssertionError):
            check_example(self, example)

    def test_integer_over_one_is_rejected(self):
        self.assertTrue(lowest_terms_violations("3/1"))

    def test_probability_above_one_is_rejected(self):
        example = self.good(final_answer="5/4", steps=[f"Z{DELIM}5/4"])
        self.assertTrue(probability_violations(example))

    def test_negative_labelled_probability_is_rejected(self):
        example = self.good(operation="probability_axioms_weights",
                            final_answer="P(3) = -1/8; P(4) = 9/8",
                            steps=[f"Z{DELIM}P(3) = -1/8; P(4) = 9/8"])
        self.assertEqual(len(probability_violations(example)), 2)

    def test_percent_answer_inside_range_passes(self):
        example = self.good(operation="probability_simple_as_percent",
                            final_answer="37.5%",
                            steps=[f"Z{DELIM}37.5%"])
        self.assertFalse(probability_violations(example))

    def test_non_probability_operation_is_not_range_checked(self):
        example = self.good(operation="probability_expected_value",
                            final_answer="147/10",
                            steps=[f"Z{DELIM}147/10"])
        self.assertFalse(probability_violations(example))

    def test_duplicate_roster_item_is_rejected(self):
        example = self.good(steps=[f"EVENT{DELIM}A{DELIM}{{2, 2, 4}}{DELIM}3",
                                   f"Z{DELIM}1/2"])
        self.assertTrue(roster_violations(example_text(example)))
        with self.assertRaises(AssertionError):
            check_example(self, example)

    def test_out_of_order_roster_is_rejected(self):
        self.assertTrue(roster_violations("A = {4, 2, 6}"))
        self.assertTrue(roster_violations("S = {T, H}"))
        self.assertFalse(roster_violations("S = {H, T}"))
        self.assertFalse(roster_violations("A = {2, 4, 6}"))
        self.assertFalse(roster_violations("A = ∅"))

    def test_mismatched_z_payload_is_rejected(self):
        example = self.good(steps=[f"Z{DELIM}3/4"])
        self.assertTrue(z_payload_violations(example))
        with self.assertRaises(AssertionError):
            check_example(self, example)

    def test_too_many_step_fields_is_rejected(self):
        example = self.good(steps=[f"A{DELIM}1{DELIM}2{DELIM}3{DELIM}4{DELIM}5",
                                   f"Z{DELIM}1/2"])
        self.assertTrue(pipe_violations(example))

    def test_given_outside_the_probability_is_rejected(self):
        example = self.good(problem="Find P(A) given B for the spinner.")
        self.assertTrue(conditioning_violations(example))


if __name__ == "__main__":
    unittest.main()
