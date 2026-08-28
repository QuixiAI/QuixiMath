"""Strand-wide conventions for the applied-reasoning generators.

``plans/applied_plan.md`` §3/§4: every module flagged ``APPLIED = True`` obeys one
dialect — **the problem text names no method**, quantities carry units, the
four standard modifiers (``plain``, ``distractor``, ``estimate_first``,
``with_model``) have fixed shapes, and missing information has exactly one
answer form. This module owns the checkers and runs them over 200 sampled
examples of every flagged generator.

The strand is still empty at Phase 0, so the checkers are pinned three ways
rather than vacuously passing:

1. ``EngineRecordTest`` runs the whole battery over 200 records built from
   ``applied_common``'s worked template, one per modifier — the shape every
   Phase 1 generator will emit.
2. ``CheckerFixtureTest`` proves each checker *rejects* a synthetic example
   that breaks its rule.
3. ``test_discovery_finds_a_flagged_module`` flags a real applied generator
   for the duration of a test, so the discovery path is exercised too.
"""
import importlib
import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import applied_common as ac  # noqa: E402
from applied_common import (METHOD_WORDS, MISSING_PREFIX, estimate_first,
                            inject_distractors, render_problem,
                            select_relevant_step, strip_allowed,
                            with_model_answer)  # noqa: E402
from helpers import DELIM, step  # noqa: E402
from tests.applied_oracle import number_tokens  # noqa: E402
from tests.conventions_common import (  # noqa: E402
    assert_contract, assert_pipe_safe, flagged_generators, method_word_hits,
    sample_examples,
)

#: ``insufficient information; need <slot phrase>`` and nothing else (§3).
MISSING_RE = re.compile(r"insufficient information; need [^\s].*[^.\s]")

#: A variant may name its method only when it is the scaffolded one (§3).
SCAFFOLDED_SUFFIX = "_scaffolded"


def declared_units(gen):
    """The units a generator promises in its answers: the optional
    ``ANSWER_UNIT`` class attribute (a string or a tuple), else the
    ``answer_unit`` metadata of the templates it declares in ``TEMPLATES``."""
    units = getattr(gen, "ANSWER_UNIT", None)
    if units is None:
        units = [getattr(t, "answer_unit", "") for t in
                 getattr(gen, "TEMPLATES", ()) or ()]
    if isinstance(units, str):
        units = [units]
    return tuple(u for u in (units or ()) if u)


def method_word_violations(example):
    """The defining rule: the problem text names no procedure (§3)."""
    operation = str(example.get("operation", ""))
    if operation.endswith(SCAFFOLDED_SUFFIX):
        return []
    text = strip_allowed(str(example.get("problem", "")))
    hits = method_word_hits(text, METHOD_WORDS)
    return [f"problem text names a method: {sorted(set(hits))}"] if hits else []


def unit_violations(example, units):
    """Quantities carry their unit in the answer (§3), unless the answer is
    the missing-information verdict."""
    if not units:
        return []
    answer = str(example.get("final_answer", ""))
    if answer.startswith(MISSING_PREFIX):
        return []
    stems = [u.rstrip("s") for u in units]
    if any(stem and stem in answer for stem in stems):
        return []
    return [f"final_answer {answer!r} carries none of the declared units "
            f"{list(units)}"]


def distractor_violations(example):
    """``distractor`` variants flag exactly one ``SELECT_RELEVANT`` step whose
    ``ignored`` field quotes numbers that really are in the story (§3)."""
    operation = str(example.get("operation", ""))
    if "distractor" not in operation:
        return []
    steps = list(example.get("steps") or [])
    selects = [s for s in steps if s.split(DELIM)[0] == "SELECT_RELEVANT"]
    if len(selects) != 1:
        return [f"{len(selects)} SELECT_RELEVANT steps; exactly one required"]
    fields = selects[0].split(DELIM)[1:]
    used = [f for f in fields if f.startswith("used: ")]
    ignored = [f for f in fields if f.startswith("ignored: ")]
    out = []
    if not used:
        out.append("SELECT_RELEVANT names no 'used: ' field")
    if not ignored:
        return out + ["SELECT_RELEVANT names no 'ignored: ' field"]
    problem_numbers = set(number_tokens(str(example.get("problem", ""))))
    used_numbers = set(number_tokens(used[0])) if used else set()
    ignored_numbers = number_tokens(ignored[0])
    if not ignored_numbers:
        out.append(f"the ignored field names no number: {ignored[0]!r}")
    for token in ignored_numbers:
        if token not in problem_numbers:
            out.append(f"ignored number {token} is not in the problem text")
        if token in used_numbers:
            out.append(f"number {token} is listed as both used and ignored")
    return out


def estimate_violations(example):
    """``estimate_first`` variants open with ``ESTIMATE`` and close with
    ``ESTIMATE_CHECK`` immediately before ``Z`` (DESIGN.md format)."""
    operation = str(example.get("operation", ""))
    steps = list(example.get("steps") or [])
    codes = [s.split(DELIM)[0] for s in steps]
    out = []
    if "estimate_first" in operation:
        if not codes or codes[0] != "ESTIMATE":
            out.append("estimate_first variant does not open with ESTIMATE")
        if len(codes) < 2 or codes[-2] != "ESTIMATE_CHECK":
            out.append("estimate_first variant has no ESTIMATE_CHECK before Z")
    for index, code in enumerate(codes):
        if code == "ESTIMATE_CHECK":
            if index != len(codes) - 2:
                out.append("ESTIMATE_CHECK must sit immediately before Z")
            if len(steps[index].split(DELIM)) - 1 != 3:
                out.append("ESTIMATE_CHECK takes estimate, exact and verdict")
    return out


def missing_info_violations(example):
    """Missing information has one canonical answer form (§3, §9)."""
    answer = str(example.get("final_answer", ""))
    if "insufficient" not in answer.lower():
        return []
    if not MISSING_RE.fullmatch(answer):
        return [f"missing-information answer {answer!r} is not "
                f"'{MISSING_PREFIX}<slot phrase>'"]
    return []


def check_example(testcase, example, units=()):
    """Runs every strand rule against one example."""
    assert_contract(testcase, example)
    assert_pipe_safe(testcase, example)
    for label, violations in (
            ("method words", method_word_violations(example)),
            ("units", unit_violations(example, units)),
            ("distractor", distractor_violations(example)),
            ("estimate", estimate_violations(example)),
            ("missing information", missing_info_violations(example))):
        testcase.assertFalse(violations, f"{label}: {violations}")


# ---------------------------------------------------------------------------
# Records in the shape Phase 1 will emit, built from the worked template
# ---------------------------------------------------------------------------

TEMPLATE = ac.WORK_RATE_TOGETHER
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model",
             "missing", "scaffolded")


def build_record(modifier, rng):
    """One record from ``applied_common.WORK_RATE_TOGETHER`` in the given
    modifier's shape (what ``WorkRateGenerator`` will emit in Phase 1)."""
    operation = f"work_rate_together_{modifier}"
    if modifier == "missing":
        hidden = rng.choice([s.name for s in TEMPLATE.slots])
        story = render_problem(TEMPLATE, hide=(hidden,), rng=rng)
        answer = story.missing_answer()
        steps = [
            select_relevant_step(story.used_labels(),
                                 needed=story.slot_phrase(hidden)),
            step("MISSING", story.slot_phrase(hidden),
                 "one whole job needs both times"),
            step("Z", answer),
        ]
        return dict(problem_id=f"synthetic-{modifier}", operation=operation,
                    problem=story.text, steps=steps, final_answer=answer)

    story = render_problem(TEMPLATE, rng=rng)
    steps, answer = story.solve()
    problem = story.text
    if modifier == "distractor":
        story, select = inject_distractors(story, rng.choice([1, 2]), rng=rng)
        problem = story.text
        steps = [select] + steps
    elif modifier == "estimate_first":
        faster = min(int(story.values["a_hours"]), int(story.values["b_hours"]))
        together = 1 / (Fraction(1, int(story.values["a_hours"]))
                        + Fraction(1, int(story.values["b_hours"])))
        steps = estimate_first(steps, together,
                               f"between {faster}/2 h and {faster} h")
    elif modifier == "with_model":
        answer = with_model_answer(story.model(), TEMPLATE.variable, answer)
        steps = steps[:-1] + [step("Z", answer)]
    elif modifier == "scaffolded":
        # the one exemption: a scaffolded variant may name its method
        problem = f"{problem} Use the work formula."
    return dict(problem_id=f"synthetic-{modifier}", operation=operation,
                problem=problem, steps=steps, final_answer=answer)


class AppliedConventionsTest(unittest.TestCase):
    """Every flagged generator obeys the strand conventions."""

    SAMPLE = 200

    def test_flagged_generators_obey_the_conventions(self):
        for gen in flagged_generators("APPLIED"):
            with self.subTest(generator=type(gen).__name__):
                units = declared_units(gen)
                for example in sample_examples(gen, self.SAMPLE, seed=7):
                    check_example(self, example, units)

    def test_discovery_finds_a_flagged_module(self):
        """Prove discovery and checkers on a permanently flagged module."""
        module = importlib.import_module("generators.fermi_estimation_generator")
        self.assertIs(module.APPLIED, True)
        found = flagged_generators("APPLIED")
        names = {type(gen).__name__ for gen in found}
        self.assertIn("FermiEstimationGenerator", names)
        for gen in found:
            if type(gen).__name__ == "FermiEstimationGenerator":
                for example in sample_examples(gen, self.SAMPLE, seed=3):
                    check_example(self, example, declared_units(gen))


class EngineRecordTest(unittest.TestCase):
    """The battery accepts the records the engine produces — one per
    modifier, 200 in all."""

    def test_engine_records_pass_every_checker(self):
        rng = random.Random(21)
        seen = set()
        for index in range(200):
            modifier = MODIFIERS[index % len(MODIFIERS)]
            record = build_record(modifier, rng)
            seen.add(modifier)
            with self.subTest(modifier=modifier, index=index):
                check_example(self, record, declared_units(self))
                check_example(self, record, TEMPLATE.answer_unit)
        self.assertEqual(seen, set(MODIFIERS))

    def test_each_modifier_is_recognisably_shaped(self):
        rng = random.Random(22)
        plain = build_record("plain", rng)
        self.assertNotIn("SELECT_RELEVANT", "".join(plain["steps"]))

        distractor = build_record("distractor", rng)
        self.assertTrue(distractor["steps"][0].startswith("SELECT_RELEVANT|"))

        estimated = build_record("estimate_first", rng)
        self.assertTrue(estimated["steps"][0].startswith("ESTIMATE|"))
        self.assertTrue(estimated["steps"][-2].startswith("ESTIMATE_CHECK|"))

        modelled = build_record("with_model", rng)
        self.assertRegex(modelled["final_answer"],
                         r"^1/\d+ \+ 1/\d+ = 1/t; t = .+ hours?$")

        missing = build_record("missing", rng)
        self.assertRegex(missing["final_answer"], MISSING_RE)
        self.assertIn("MISSING", missing["steps"][1])

        scaffolded = build_record("scaffolded", rng)
        self.assertTrue(method_word_hits(scaffolded["problem"], METHOD_WORDS))
        self.assertEqual(method_word_violations(scaffolded), [])

    def test_scaffolded_exemption_is_not_the_default(self):
        rng = random.Random(23)
        leaked = build_record("scaffolded", rng)
        leaked["operation"] = "work_rate_together_plain"
        self.assertTrue(method_word_violations(leaked))


class CheckerFixtureTest(unittest.TestCase):
    """Each checker rejects a synthetic example that breaks its rule."""

    def good(self, **overrides):
        example = dict(
            problem_id="fixture",
            operation="work_rate_together_plain",
            problem=("Hose A alone can fill the pool in 6 hours. Hose B alone "
                     "can fill it in 3 hours. Working together, how long do "
                     "they take to fill the pool?"),
            steps=["RATE|hose A|1/6 pool per hour",
                   "RATE|hose B|1/3 pool per hour",
                   "RATE_SUM|1/6 + 1/3|1/2",
                   "D|1|1/2|2",
                   "Z|2 hours"],
            final_answer="2 hours",
        )
        example.update(overrides)
        return example

    def test_the_fixture_itself_is_clean(self):
        check_example(self, self.good(), ("hours",))

    def test_contract_rejects_a_mismatched_z_step(self):
        with self.assertRaises(AssertionError):
            assert_contract(self, self.good(final_answer="3 hours"))
        with self.assertRaises(AssertionError):
            broken = self.good()
            del broken["final_answer"]
            assert_contract(self, broken)

    def test_pipe_safety_rejects_a_bar_in_the_problem(self):
        with self.assertRaises(AssertionError):
            assert_pipe_safe(self, self.good(
                problem="Hose A takes 6 hours | hose B takes 3 hours."))
        with self.assertRaises(AssertionError):
            assert_pipe_safe(self, self.good(final_answer="2 hours|fast"))

    def test_method_words_rejects_a_named_procedure(self):
        for text in ("Use the work formula to combine the two hoses.",
                     "Set up a proportion for the two fill times.",
                     "Find the LCM of 6 and 3 to size the job.",
                     "This is the distractor variant of the story."):
            self.assertTrue(method_word_violations(self.good(problem=text)), text)

    def test_method_words_exempts_the_scaffolded_variant(self):
        scaffolded = self.good(problem="Use the work formula.",
                               operation="work_rate_together_scaffolded")
        self.assertEqual(method_word_violations(scaffolded), [])

    def test_units_rejects_a_bare_number(self):
        self.assertTrue(unit_violations(
            self.good(final_answer="2", steps=["RATE|hose A|1/6 pool per hour",
                                               "Z|2"]), ("hours",)))
        self.assertEqual(unit_violations(self.good(), ("hours",)), [])
        self.assertEqual(unit_violations(self.good(final_answer="2"), ()), [])

    def test_units_exempts_the_missing_information_answer(self):
        answer = MISSING_PREFIX + "the time the second hose takes alone"
        self.assertEqual(
            unit_violations(self.good(final_answer=answer), ("hours",)), [])

    def test_distractor_rejects_a_missing_or_doubled_marker(self):
        base = self.good(operation="work_rate_together_distractor",
                         problem=self.good()["problem"] + " The garden has 12 "
                                 "rose bushes.")
        self.assertTrue(distractor_violations(base))  # no SELECT_RELEVANT
        select = "SELECT_RELEVANT|used: 6 hours, 3 hours|ignored: 12 rose bushes"
        doubled = dict(base, steps=[select, select] + base["steps"])
        self.assertTrue(distractor_violations(doubled))
        ok = dict(base, steps=[select] + base["steps"])
        self.assertEqual(distractor_violations(ok), [])

    def test_distractor_rejects_an_ignored_number_absent_from_the_story(self):
        base = self.good(operation="work_rate_together_distractor",
                         problem=self.good()["problem"] + " The garden has 12 "
                                 "rose bushes.")
        invented = "SELECT_RELEVANT|used: 6 hours, 3 hours|ignored: 40 rose bushes"
        self.assertTrue(distractor_violations(dict(base, steps=[invented] + base["steps"])))
        relevant = "SELECT_RELEVANT|used: 6 hours, 3 hours|ignored: 6 hours"
        self.assertTrue(distractor_violations(dict(base, steps=[relevant] + base["steps"])))
        wordy = "SELECT_RELEVANT|used: 6 hours, 3 hours|ignored: the rose bushes"
        self.assertTrue(distractor_violations(dict(base, steps=[wordy] + base["steps"])))

    def test_distractor_check_is_skipped_for_other_variants(self):
        self.assertEqual(distractor_violations(self.good()), [])

    def test_estimate_rejects_a_misplaced_estimate_pair(self):
        good_steps = ["ESTIMATE|between 3/2 h and 3 h|2"] + self.good()["steps"][:-1] \
            + ["ESTIMATE_CHECK|2|2|2 ≈ 2 ✓", "Z|2 hours"]
        estimated = self.good(operation="work_rate_together_estimate_first",
                              steps=good_steps)
        self.assertEqual(estimate_violations(estimated), [])
        self.assertTrue(estimate_violations(
            dict(estimated, steps=good_steps[1:])))          # no ESTIMATE first
        misplaced = ["ESTIMATE|between 3/2 h and 3 h|2", "ESTIMATE_CHECK|2|2|2 ≈ 2 ✓"] \
            + self.good()["steps"]
        self.assertTrue(estimate_violations(dict(estimated, steps=misplaced)))
        short = good_steps[:-2] + ["ESTIMATE_CHECK|2|2", "Z|2 hours"]
        self.assertTrue(estimate_violations(dict(estimated, steps=short)))

    def test_estimate_check_position_is_policed_outside_the_modifier(self):
        steps = ["ESTIMATE_CHECK|2|2|2 ≈ 2 ✓"] + self.good()["steps"]
        self.assertTrue(estimate_violations(self.good(steps=steps)))

    def test_missing_information_rejects_a_near_miss(self):
        for answer in ("Insufficient information: need the price",
                       "insufficient information, need the price",
                       "insufficient information; need ",
                       "insufficient information; need the price."):
            self.assertTrue(missing_info_violations(self.good(final_answer=answer)),
                            answer)
        canonical = MISSING_PREFIX + "the price of a notebook"
        self.assertEqual(missing_info_violations(self.good(final_answer=canonical)), [])


if __name__ == "__main__":
    unittest.main()
