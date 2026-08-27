"""Tests for the applied strand's shared infrastructure (plans/applied_plan.md §4).

Everything the engine promises is checked against ``tests/applied_oracle.py``,
which never imports ``applied_common``: the story is inverted from its text by
an independent grammar and re-solved by an independent route (A9).
"""
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
from applied_common import (CONTEXTS, MISSING_PREFIX, METHOD_WORDS, Line,
                            Part, Rendering, Scenario, Slot, Story, Template,
                            estimate_first, frac_txt, inject_distractors,
                            method_word_hits, missing_answer, num_txt,
                            reject_step, render_problem, select_relevant_step,
                            unit, with_model_answer)  # noqa: E402
from tests.applied_oracle import (Interval, hours_text, invert_work_rate,
                            leading_digit_estimate, number_tokens, parse_table,
                            parse_quantity, solve_work_rate_lcm,
                            to_fraction)  # noqa: E402
from helpers import DELIM  # noqa: E402

TEMPLATE = ac.WORK_RATE_TOGETHER


def field(step_text, index):
    """One payload field of a step string."""
    return step_text.split(DELIM)[index]


def opcode(step_text):
    return step_text.split(DELIM)[0]


class RenderingConventionTest(unittest.TestCase):
    """Renderers and answer conventions (plans/applied_plan.md §3)."""

    def test_unit_pluralises_words_but_not_symbols(self):
        self.assertEqual(unit(2, "hour"), "2 hours")
        self.assertEqual(unit(1, "hour"), "1 hour")
        self.assertEqual(unit(Fraction(3, 2), "hour"), "1.5 hours")
        self.assertEqual(unit(48, "km/h"), "48 km/h")
        self.assertEqual(unit(112, "m²"), "112 m²")
        self.assertEqual(unit(53, "tile"), "53 tiles")
        self.assertEqual(unit(2, "box", "boxes"), "2 boxes")

    def test_number_renderings(self):
        self.assertEqual(num_txt(Fraction(21, 2)), "10.5")
        self.assertEqual(num_txt(6), "6")
        self.assertEqual(frac_txt(Fraction(1, 6)), "1/6")
        self.assertEqual(frac_txt(Fraction(4, 2)), "2")
        self.assertEqual(ac.money(Fraction(1425, 2)), "$712.50")
        self.assertEqual(ac.pct(Fraction(2, 5)), "40%")

    def test_missing_and_with_model_answers(self):
        self.assertEqual(missing_answer("the price of a notebook"),
                         "insufficient information; need the price of a notebook")
        self.assertEqual(
            missing_answer("the time the second {device} takes alone",
                           {"device": "hose"}),
            "insufficient information; need the time the second hose takes alone")
        self.assertEqual(with_model_answer("1/6 + 1/3 = 1/t", "t", "2 hours"),
                         "1/6 + 1/3 = 1/t; t = 2 hours")

    def test_reject_step(self):
        self.assertEqual(reject_step("t = -1", "negative time"),
                         "REJECT|t = -1|negative time")


class ContextBankTest(unittest.TestCase):
    """The shared context bank (plans/applied_plan.md §3)."""

    def test_ten_contexts_with_the_expected_shape(self):
        expected = {"people", "shop", "trip", "workshop", "garden", "recipe",
                    "classroom", "sports", "business", "lab"}
        self.assertEqual(set(CONTEXTS), expected)
        for key, ctx in CONTEXTS.items():
            self.assertEqual(ctx.key, key)
            self.assertTrue(ctx.settings and ctx.agents and ctx.items)
            self.assertGreaterEqual(len(ctx.distractors), 3)
            self.assertIn("work", ctx.fragments)
            self.assertIn("opener", ctx.fragments)
            for triple in ctx.fragments["work"]:
                self.assertEqual(len(triple), 3, triple)

    def test_items_have_hand_friendly_prices(self):
        rng = random.Random(4)
        for ctx in CONTEXTS.values():
            for item in ctx.items:
                self.assertLess(item.price_lo, item.price_hi)
                self.assertEqual(item.price_lo % item.price_step, 0)
                for _ in range(20):
                    price = item.price(rng)
                    self.assertEqual((price * 100).denominator, 1)
                    self.assertTrue(
                        Fraction(item.price_lo, 100) <= price
                        <= Fraction(item.price_hi, 100))
                    self.assertEqual(ac.money(price)[0], "$")

    def test_context_text_is_pipe_safe_and_names_no_method(self):
        rng = random.Random(7)
        for ctx in CONTEXTS.values():
            blobs = list(ctx.settings) + list(ctx.agents)
            blobs += [item.singular for item in ctx.items]
            for triple in ctx.fragments["work"]:
                blobs += list(triple)
            for distractor in ctx.distractors:
                for _ in range(10):
                    sentence, label = distractor.draw(rng)
                    blobs += [sentence, label]
            for blob in blobs:
                self.assertNotIn(DELIM, blob)
                self.assertEqual(method_word_hits(blob), [], blob)


class MethodWordsTest(unittest.TestCase):
    """The defining rule: the problem text names no method (§3)."""

    def test_catches_the_plan_examples(self):
        for text in ("Use the quadratic formula to solve it.",
                     "Apply the work formula.",
                     "Set up a proportion and solve.",
                     "By Bayes, what is the chance?",
                     "Find the LCM of 4 and 6.",
                     "Use the Pythagorean theorem.",
                     "This is the distractor variant.",
                     "Use the rule for combinations."):
            self.assertTrue(method_word_hits(text), text)

    def test_does_not_fire_on_plain_story_text(self):
        for text in (
                "One hose fills the pool in 6 hours; a second fills it in 3 hours.",
                "A 20% discount is applied to $80. What is the sale price?",
                "Brand A: 12 oz for $3.60. Brand B: 20 oz for $5.00.",
                "Compute 47 × 99 mentally. Show the strategy.",
                "A scale shows 3.4 kg, rounded to the nearest 0.1 kg.",
                "Estimate the yearly total. Round to 2 significant figures.",
                "At 7% per year, use the rule of 70 to find the doubling time.",
                "Mia buys 3 notebooks and pays with a $20 bill.",
                "The plumber charges $40 to come out plus $25 per hour.",
                "How many 20 cm cartons fit in the box?"):
            self.assertEqual(method_word_hits(text), [], text)

    def test_list_is_lowercase_and_deduplicated(self):
        self.assertEqual(list(METHOD_WORDS), sorted(set(METHOD_WORDS)))
        for phrase in METHOD_WORDS:
            self.assertEqual(phrase, phrase.lower())


class TemplateEngineTest(unittest.TestCase):
    """Rendering, inversion and the canonical route of the worked example."""

    def test_template_declares_five_renderings_and_metadata(self):
        self.assertGreaterEqual(len(TEMPLATE.renderings), 5)
        self.assertEqual(set(TEMPLATE.rendering_keys),
                         {"quantity_first", "question_first", "table",
                          "narrative", "comparison"})
        self.assertEqual(TEMPLATE.answer_unit, "hours")
        self.assertEqual(TEMPLATE.variable, "t")
        self.assertTrue(TEMPLATE.skills)

    def test_every_rendering_renders_and_the_oracle_inverts_it(self):
        rng = random.Random(1)
        seen = set()
        for _ in range(400):
            key = rng.choice(TEMPLATE.rendering_keys)
            ctx = rng.choice(sorted(CONTEXTS))
            story = render_problem(TEMPLATE, ctx=ctx, rendering=key, rng=rng)
            seen.add((key, ctx))
            inverted = invert_work_rate(story.text)
            self.assertIsNotNone(inverted, story.text)
            self.assertEqual(inverted.rendering, key, story.text)
            self.assertEqual(inverted.a_hours, Fraction(story.values["a_hours"]))
            self.assertEqual(inverted.b_hours, Fraction(story.values["b_hours"]))
        self.assertEqual({key for key, _ in seen}, set(TEMPLATE.rendering_keys))
        self.assertEqual({ctx for _, ctx in seen}, set(CONTEXTS))

    def test_stories_are_pipe_safe_and_name_no_method(self):
        rng = random.Random(2)
        for _ in range(300):
            story = render_problem(TEMPLATE, rng=rng)
            self.assertNotIn(DELIM, story.text)
            self.assertEqual(method_word_hits(story.text), [], story.text)
            self.assertEqual(story.text.count("?"), 1)
            if story.rendering != "question_first":
                self.assertTrue(story.text.endswith("?"))

    def test_answer_matches_the_independent_lcm_route(self):
        rng = random.Random(3)
        for _ in range(300):
            story = render_problem(TEMPLATE, rng=rng)
            steps, answer = story.solve()
            inverted = invert_work_rate(story.text)
            expected = solve_work_rate_lcm(inverted.a_hours, inverted.b_hours)
            self.assertEqual(answer, hours_text(expected))
            self.assertEqual(steps[-1], f"Z{DELIM}{answer}")

    def test_step_arithmetic_is_internally_exact(self):
        rng = random.Random(4)
        for _ in range(200):
            story = render_problem(TEMPLATE, rng=rng)
            steps, answer = story.solve()
            a = Fraction(story.values["a_hours"])
            b = Fraction(story.values["b_hours"])
            by_code = {}
            for text in steps:
                by_code.setdefault(opcode(text), []).append(text)
            lcd = to_fraction(field(by_code["L"][0], 3))
            self.assertEqual(lcd % a, 0)
            self.assertEqual(lcd % b, 0)
            for line in by_code["C"]:
                self.assertEqual(to_fraction(field(line, 1)),
                                 to_fraction(field(line, 2)))
            add = by_code["A"][0]
            self.assertEqual(to_fraction(field(add, 1)) + to_fraction(field(add, 2)),
                             to_fraction(field(add, 3)))
            total = to_fraction(field(by_code["RATE_SUM"][0], 2))
            self.assertEqual(total, 1 / a + 1 / b)
            divide = by_code["D"][0]
            self.assertEqual(to_fraction(field(divide, 1)) / to_fraction(field(divide, 2)),
                             to_fraction(field(divide, 3)))
            check = by_code["CHECK"][0]
            left, right = field(check, 2).split(" + ")
            self.assertEqual(to_fraction(left) + to_fraction(right),
                             to_fraction(field(check, 3)))
            self.assertEqual(answer, hours_text(1 / (1 / a + 1 / b)))

    def test_model_string_is_canonical(self):
        story = render_problem(TEMPLATE, values={"a_hours": 6, "b_hours": 3},
                               ctx="garden", rendering="quantity_first",
                               rng=random.Random(5))
        steps, answer = story.solve()
        self.assertEqual(answer, "2 hours")
        self.assertEqual(story.model(), "1/6 + 1/3 = 1/t")
        self.assertEqual(with_model_answer(story.model(), TEMPLATE.variable, answer),
                         "1/6 + 1/3 = 1/t; t = 2 hours")

    def test_table_rendering_is_parseable_as_a_table(self):
        story = render_problem(TEMPLATE, values={"a_hours": 6, "b_hours": 3},
                               ctx="garden", rendering="table",
                               rng=random.Random(6))
        rows = parse_table(story.text)
        self.assertEqual(len(rows), 2)
        self.assertEqual([parse_quantity(value)[0] for _, value in rows],
                         [Fraction(6), Fraction(3)])
        self.assertNotIn(DELIM, story.text)

    def test_pairs_are_hand_friendly(self):
        self.assertGreaterEqual(len(ac.WORK_RATE_PAIRS), 20)
        for slow, fast in ac.WORK_RATE_PAIRS:
            self.assertGreater(slow, fast)
            together = solve_work_rate_lcm(slow, fast)
            self.assertGreaterEqual(together, 1)
            self.assertEqual((together * 2).denominator, 1)

    def test_unknown_rendering_or_slot_raises(self):
        with self.assertRaises(KeyError):
            render_problem(TEMPLATE, rendering="nope")
        with self.assertRaises(KeyError):
            render_problem(TEMPLATE, hide=("c_hours",))


def _linear_template(renderings=None, **overrides):
    """A throwaway two-slot template used to exercise validation."""
    slots = (Slot("p", "the price", kind="money"),
             Slot("n", "the count", unit="notebook"))
    if renderings is None:
        renderings = tuple(
            Rendering(f"r{i}", (
                Line("Each costs {p}.", ("p",)),
                Line("She buys {n}.", ("n",)),
                Line("What is the total?", (), "question"),
            )) for i in range(5))
    kwargs = dict(
        key="linear", slots=slots, renderings=renderings,
        sampler=lambda rng: {"p": Fraction(5, 2), "n": 3},
        scene=lambda ctx, rng: {},
        solver=lambda values, fields: (["Z|$7.50"], "$7.50"),
        model=lambda values, fields: "3 × 2.50 = c",
    )
    kwargs.update(overrides)
    return Template(**kwargs)


class TemplateValidationTest(unittest.TestCase):
    """A template that would break the strand's rules fails at construction."""

    def test_valid_template_builds(self):
        self.assertEqual(len(_linear_template().renderings), 5)

    def test_fewer_than_five_renderings_rejected(self):
        renderings = _linear_template().renderings[:4]
        with self.assertRaisesRegex(ValueError, "at least 5"):
            _linear_template(renderings=renderings)

    def test_undeclared_slot_reference_rejected(self):
        bad = Rendering("bad", (
            Line("Each costs {p} and she buys {n}.", ("p",)),
            Line("What is the total?", (), "question"),
        ))
        with self.assertRaisesRegex(ValueError, "declares"):
            _linear_template(renderings=(bad,) + _linear_template().renderings[1:])

    def test_missing_question_line_rejected(self):
        bad = Rendering("bad", (Line("Each costs {p}.", ("p",)),
                                Line("She buys {n}.", ("n",))))
        with self.assertRaisesRegex(ValueError, "question line"):
            _linear_template(renderings=(bad,) + _linear_template().renderings[1:])

    def test_rendering_that_omits_a_slot_rejected(self):
        bad = Rendering("bad", (Line("Each costs {p}.", ("p",)),
                                Line("What is the total?", (), "question")))
        with self.assertRaisesRegex(ValueError, "omits slots"):
            _linear_template(renderings=(bad,) + _linear_template().renderings[1:])

    def test_hiding_needs_a_rendering_that_can_drop_the_slot(self):
        joint = tuple(
            Rendering(f"joint{i}", (
                Line("Each costs {p} and she buys {n}.", ("p", "n")),
                Line("What is the total?", (), "question"),
            )) for i in range(5))
        template = _linear_template(renderings=joint)
        self.assertFalse(template.supports_hiding(joint[0], ("p",)))
        with self.assertRaisesRegex(ValueError, "no rendering can hide"):
            render_problem(template, hide=("p",), rng=random.Random(0))


class DistractorTest(unittest.TestCase):
    """The ``distractor`` modifier (plans/applied_plan.md §3)."""

    def test_injection_is_flagged_and_leaves_the_answer_alone(self):
        rng = random.Random(8)
        for count in (1, 2):
            for _ in range(120):
                story = render_problem(TEMPLATE, rng=rng)
                _, plain_answer = story.solve()
                planted, sel = inject_distractors(story, count, rng=rng)
                _, answer = planted.solve()
                self.assertEqual(answer, plain_answer)
                self.assertEqual(opcode(sel), "SELECT_RELEVANT")
                self.assertTrue(field(sel, 1).startswith("used: "))
                self.assertTrue(field(sel, 2).startswith("ignored: "))
                self.assertEqual(len(planted.ignored), count)
                self.assertNotIn(DELIM, planted.text)
                self.assertEqual(method_word_hits(planted.text), [], planted.text)
                self.assertEqual(planted.text.count("?"), 1)
                if planted.rendering != "question_first":
                    self.assertTrue(planted.text.endswith("?"))
                # every ignored number is in the story, and is not a used one
                story_numbers = number_tokens(planted.text)
                used_numbers = set()
                for label in field(sel, 1)[len("used: "):].split(", "):
                    used_numbers.update(number_tokens(label))
                ignored_numbers = number_tokens(field(sel, 2))
                self.assertTrue(ignored_numbers)
                for token in ignored_numbers:
                    self.assertIn(token, story_numbers)
                    self.assertNotIn(token, used_numbers)
                # the relevant data is still there for the solver
                inverted = invert_work_rate(planted.text)
                self.assertIsNotNone(inverted, planted.text)
                self.assertEqual(inverted.a_hours, Fraction(story.values["a_hours"]))
                self.assertEqual(inverted.b_hours, Fraction(story.values["b_hours"]))

    def test_used_labels_quote_the_story_values(self):
        story = render_problem(TEMPLATE, values={"a_hours": 6, "b_hours": 3},
                               ctx="garden", rendering="quantity_first",
                               rng=random.Random(9))
        planted, sel = inject_distractors(story, 1, rng=random.Random(9))
        self.assertEqual(field(sel, 1), "used: 6 hours, 3 hours")
        for label in planted.ignored:
            self.assertIn(label.split(" ")[0], planted.text)

    def test_count_out_of_range_rejected(self):
        story = render_problem(TEMPLATE, rng=random.Random(10))
        for count in (0, 3):
            with self.assertRaises(ValueError):
                inject_distractors(story, count)

    def test_select_relevant_supports_used_ignored_and_needed(self):
        self.assertEqual(
            select_relevant_step(["6 h", "3 h"], ignored=["$40 wage"]),
            "SELECT_RELEVANT|used: 6 h, 3 h|ignored: $40 wage")
        self.assertEqual(
            select_relevant_step(["3", "$20"], needed="the price of a notebook"),
            "SELECT_RELEVANT|used: 3, $20|needed: the price of a notebook")
        both = select_relevant_step(["3"], ignored=["7 shelves"],
                                    needed=["the price of a notebook"])
        self.assertEqual(both.split(DELIM)[2], "ignored: 7 shelves")
        self.assertEqual(both.split(DELIM)[3], "needed: the price of a notebook")


class MissingInformationTest(unittest.TestCase):
    """The canonical missing-information record (plans/applied_plan.md §3, §9)."""

    CANONICAL = re.compile(r"insufficient information; need \S.*[^.\s]")

    def test_hidden_slot_disappears_and_the_answer_is_canonical(self):
        rng = random.Random(11)
        renderings = set()
        for _ in range(200):
            hidden = rng.choice([s.name for s in TEMPLATE.slots])
            story = render_problem(TEMPLATE, hide=(hidden,), rng=rng)
            renderings.add(story.rendering)
            answer = story.missing_answer()
            self.assertTrue(answer.startswith(MISSING_PREFIX))
            self.assertRegex(answer, self.CANONICAL)
            self.assertEqual(answer,
                             missing_answer(TEMPLATE.slot(hidden), story.fields))
            self.assertNotIn(DELIM, answer)
            # the story keeps exactly the other time
            partial = invert_work_rate(story.text, partial=True)
            self.assertIsNotNone(partial, story.text)
            present = partial.a_hours if hidden == "b_hours" else partial.b_hours
            absent = partial.b_hours if hidden == "b_hours" else partial.a_hours
            self.assertIsNone(absent, story.text)
            self.assertEqual(present, Fraction(story.values[
                "a_hours" if hidden == "b_hours" else "b_hours"]))
            self.assertEqual(len(story.used_labels()), 1)
        self.assertGreaterEqual(len(renderings), 4)

    def test_slot_phrase_is_resolved_against_the_story(self):
        story = render_problem(TEMPLATE, hide=("b_hours",), ctx="garden",
                               rendering="quantity_first", rng=random.Random(12))
        self.assertIn(story.fields["device"], story.slot_phrase("b_hours"))
        self.assertEqual(story.missing_answer("b_hours"),
                         MISSING_PREFIX + story.slot_phrase("b_hours"))

    def test_naming_the_slot_is_required_when_several_are_hidden(self):
        story = render_problem(TEMPLATE, hide=("a_hours", "b_hours"),
                               rng=random.Random(13))
        with self.assertRaises(ValueError):
            story.missing_answer()


class EstimateFirstTest(unittest.TestCase):
    """The ``estimate_first`` modifier wraps the existing op-codes (§3)."""

    def test_wrapper_positions_and_format(self):
        story = render_problem(TEMPLATE, values={"a_hours": 30, "b_hours": 20},
                               ctx="garden", rendering="table",
                               rng=random.Random(14))
        steps, answer = story.solve()
        wrapped = estimate_first(steps, Fraction(12), "between 20/2 h and 20 h")
        self.assertEqual(opcode(wrapped[0]), "ESTIMATE")
        self.assertEqual(field(wrapped[0], 1), "between 20/2 h and 20 h")
        self.assertEqual(field(wrapped[0], 2), "10")
        self.assertEqual(opcode(wrapped[-2]), "ESTIMATE_CHECK")
        self.assertEqual(wrapped[-1], f"Z{DELIM}{answer}")
        self.assertEqual(field(wrapped[-2], 1), "10")
        self.assertEqual(field(wrapped[-2], 2), "12")
        self.assertIn("≈", field(wrapped[-2], 3))
        self.assertEqual(steps, story.solve()[0])  # input list untouched
        self.assertEqual(wrapped[1:-2], steps[:-1])

    def test_estimate_uses_leading_digit_rounding(self):
        for value in (Fraction(12), Fraction(21, 2), Fraction(4653),
                      Fraction(93, 2500), Fraction(1, 3)):
            wrapped = estimate_first(["Z|x"], value, "work")
            estimate = to_fraction(field(wrapped[0], 2))
            self.assertEqual(estimate, leading_digit_estimate(value))

    def test_money_rendering_and_no_z_step(self):
        wrapped = estimate_first([ac.step("M", 3, "$2.50", "$7.50")],
                                 Fraction(15, 2), "3 × $2.50 ≈ 3 × $3",
                                 render=ac.money)
        self.assertEqual(field(wrapped[0], 2), "$8.00")
        self.assertEqual(opcode(wrapped[-1]), "ESTIMATE_CHECK")
        self.assertEqual(field(wrapped[-1], 2), "$7.50")


class ScenarioTest(unittest.TestCase):
    """The Strand X harness (plans/applied_plan.md §4, §5)."""

    @staticmethod
    def _profit(state):
        state["profit"] = 4000 - 2500
        return [ac.step("S", 4000, 2500, state["profit"])], "$1500"

    @staticmethod
    def _margin(state):
        margin = Fraction(state["profit"], 4000)
        return ([ac.step("D", state["profit"], 4000, num_txt(margin)),
                 ac.step("DEC_TO_PERCENT", num_txt(margin), ac.pct(margin))],
                ac.pct(margin))

    @staticmethod
    def _growth(state):
        state["growth"] = Fraction(1000, 4000)
        return [ac.step("D", 1000, 4000, num_txt(state["growth"]))], "25%"

    def _scenario(self):
        return Scenario([
            Part("january profit", self._profit, key="profit_text",
                 skills=("subtraction",)),
            Part("profit margin", self._margin, skills=("percent_of",)),
            Part("sales growth", self._growth, skills=("percent_change", "subtraction")),
        ])

    def test_part_markers_and_composite_answer(self):
        result = self._scenario().run()
        self.assertEqual(result.answer, "Q1 $1500; Q2 37.5%; Q3 25%")
        markers = [s for s in result.steps if opcode(s) == "PART"]
        self.assertEqual(markers, ["PART|1|january profit",
                                   "PART|2|profit margin",
                                   "PART|3|sales growth"])
        self.assertEqual(result.steps[-1], f"Z{DELIM}{result.answer}")
        self.assertEqual(result.questions,
                         ("january profit", "profit margin", "sales growth"))
        for text in result.steps:
            self.assertNotIn(DELIM, text.split(DELIM)[0])
            self.assertLessEqual(len(text.split(DELIM)) - 1, 4)

    def test_state_is_threaded_between_parts(self):
        result = self._scenario().run({"year": 2026})
        self.assertEqual(result.state["year"], 2026)
        self.assertEqual(result.state["profit"], 1500)
        self.assertEqual(result.state["q1"], "$1500")
        self.assertEqual(result.state["profit_text"], "$1500")

    def test_skills_are_collected_in_order_and_deduplicated(self):
        self.assertEqual(self._scenario().skills,
                         ["subtraction", "percent_of", "percent_change"])
        explicit = Scenario(self._scenario().parts, skills=["composition"])
        self.assertEqual(explicit.skills, ["composition"])
        bare = Scenario([Part("only", lambda state: ([], "7"))])
        self.assertIsNone(bare.skills)
        self.assertIsNone(bare.run().skills)

    def test_empty_scenario_rejected(self):
        with self.assertRaises(ValueError):
            Scenario([])


class OracleSelfTest(unittest.TestCase):
    """The oracle helpers themselves (they are the yardstick, so they get
    their own checks)."""

    def test_leading_digit_estimate(self):
        cases = {Fraction(4653): 5000, Fraction(93, 2500): Fraction(4, 100),
                 Fraction(12): 10, Fraction(21, 2): 10, Fraction(15): 20,
                 Fraction(-4653): -5000, Fraction(0): 0}
        for value, expected in cases.items():
            self.assertEqual(leading_digit_estimate(value), Fraction(expected))

    def test_interval_endpoint_arithmetic(self):
        length = Interval.from_tolerance(Fraction(25, 2), Fraction(1, 5))
        width = Interval.from_tolerance(8, Fraction(1, 10))
        area = length * width
        self.assertEqual(area.lo, Fraction(9717, 100))
        self.assertEqual(area.hi, Fraction(10287, 100))
        self.assertEqual(area.text(), "[97.17, 102.87]")
        self.assertEqual(Interval.from_rounding(Fraction(17, 5), Fraction(1, 10)).text(),
                         "[3.35, 3.45]")
        self.assertIn(Fraction(34, 10), Interval.from_rounding(Fraction(17, 5),
                                                              Fraction(1, 10)))
        with self.assertRaises(ZeroDivisionError):
            Interval(1, 2) / Interval(-1, 1)

    def test_table_and_quantity_parsers(self):
        text = ("Times to fill the pool alone — hose A: 6 hours; hose B: 3 hours. "
                "How long together?")
        self.assertEqual(parse_table(text), [("hose A", "6 hours"),
                                             ("hose B", "3 hours")])
        self.assertEqual(parse_quantity("6 hours"), (Fraction(6), "hours"))
        self.assertEqual(parse_quantity("$2.50"), (Fraction(5, 2), "$"))
        self.assertEqual(parse_quantity("40%"), (Fraction(40), "%"))
        self.assertEqual(number_tokens("The rent is $1,850.00 for 12 years."),
                         ["1850.00", "12"])


if __name__ == "__main__":
    unittest.main()
