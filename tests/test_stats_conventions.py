"""Strand-wide conventions for every STATISTICS generator.

``plans/statistics_plan.md`` §4 asks for one mechanical sweep over the strand: for
every generator whose module sets ``STATISTICS = True``, sample 200 examples
and assert

1. the base output contract (``assert_contract``) and that the ``Z`` payload
   is exactly ``final_answer``;
2. pipe safety — no ASCII ``|`` outside the step delimiter
   (``assert_pipe_safe``);
3. every ``TABLE_LOOKUP`` / ``LOOKUP_SUPPLIED`` value appears **verbatim** in
   the problem text (Principle 5: no unstated lookups);
4. every decimal in ``final_answer`` is exact and minimal (A0);
5. every rendered display in the problem parses under the oracle grammar in
   ``tests/stats_oracle.py`` (dot plot, line plot, tally, stem-and-leaf, box
   plot, two-way table, histogram bins, Φ excerpt, inverse-z excerpt).

No generator carries the flag yet (Phase 0 builds the infrastructure, Phase 1
the first generators), so the sweep is exercised here on hand-written
examples instead of being skipped: each checker is shown accepting a
well-formed example and rejecting a violating one. The hand-written fixtures
are typed from ``plans/statistics_plan.md`` §3 rather than produced by
``stats_common``, so they also pin the rendering spec independently.
"""
import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from helpers import DELIM
from tests import stats_oracle as oracle
from tests.conventions_common import (
    assert_contract,
    assert_pipe_safe,
    flagged_generators,
    sample_examples,
)

LOOKUP_OPS = ("TABLE_LOOKUP", "LOOKUP_SUPPLIED")
SAMPLES = 200
SEED = 17

_DECIMAL = re.compile(r"\d+\.\d+")
_ROUNDING = ("≈", "…", "...", "approx")


# ---------------------------------------------------------------------------
# The checkers (module-level so the fixtures below can exercise each one)
# ---------------------------------------------------------------------------


def lookup_violations(example):
    """Every supplied-constant step must quote a value the problem states.

    ``TABLE_LOOKUP|Φ(1.50)|0.9332`` is legal only when ``0.9332`` is in the
    problem text; ``LOOKUP_SUPPLIED|t* (df = 15)|2.131`` only when ``2.131``
    is."""
    problem = str(example.get("problem", ""))
    bad = []
    for raw in example.get("steps", []):
        fields = raw.split(DELIM)
        if fields[0] not in LOOKUP_OPS:
            continue
        if len(fields) < 3:
            bad.append(f"{fields[0]} must name what it read and its value: {raw}")
            continue
        value = fields[-1].strip()
        if not value:
            bad.append(f"{fields[0]} has an empty value: {raw}")
        elif value not in problem:
            bad.append(f"{fields[0]} value {value!r} is not in the problem text")
    return bad


def decimal_violations(example):
    """Decimals in ``final_answer`` are exact and minimal (A0).

    A finite decimal literal always terminates, so what this actually
    enforces is that the answer was not *rounded* into shape: no ``≈`` or
    ellipsis, no scientific notation, and no padding zeros — except the
    4-decimal probability convention (``0.0228``, ``0.9330``), money
    (``$20.00``) and a constant quoted verbatim from the problem (a supplied
    ``11.070`` keeps the problem's digits)."""
    answer = str(example.get("final_answer", ""))
    problem = str(example.get("problem", ""))
    bad = []
    rounding_text = answer.replace("approximately normal", "")
    for marker in _ROUNDING:
        if marker in rounding_text:
            bad.append(f"final_answer is rounded ({marker!r}): {answer!r}")
    for m in _DECIMAL.finditer(answer):
        literal = m.group(0)
        tail = answer[m.end():m.end() + 2]
        if re.match(r"[eE][-+\d]", tail):
            bad.append(f"scientific notation in final_answer: {literal}{tail}")
        frac = literal.split(".")[1]
        if not frac.endswith("0"):
            continue
        if len(frac) == 4:                       # probability convention
            continue
        if answer[m.start() - 1:m.start()] == "$" and len(frac) == 2:
            continue                             # money: cents are exact
        if literal in problem:
            continue                             # quoted supplied constant
        bad.append(f"non-minimal decimal {literal!r} in final_answer")
    return bad


def z_payload_violations(example):
    """``steps[-1]`` must be exactly ``Z|<final_answer>``."""
    steps = example.get("steps") or []
    if not steps:
        return ["steps are empty"]
    want = f"Z{DELIM}{example.get('final_answer')}"
    if steps[-1] != want:
        return [f"last step {steps[-1]!r} is not {want!r}"]
    return []


def display_violations(example):
    """Every rendered display in the problem parses under the oracle
    grammar — a broken box-plot column or a non-alphabetical tally is a
    parse error, not a silent misrender."""
    bad = []
    for kind, block in oracle.find_displays(str(example.get("problem", ""))):
        try:
            oracle.parse_display(kind, block)
        except Exception as exc:                 # noqa: BLE001 - reported
            bad.append(f"{kind} does not parse: {exc}")
    return bad


CHECKERS = (
    ("lookup", lookup_violations),
    ("decimal", decimal_violations),
    ("z_payload", z_payload_violations),
    ("display", display_violations),
)


def all_violations(example):
    out = []
    for name, checker in CHECKERS:
        out += [f"[{name}] {v}" for v in checker(example)]
    return out


# ---------------------------------------------------------------------------
# Fixtures typed from plans/statistics_plan.md §3
# ---------------------------------------------------------------------------

BOX_PLOT_PROBLEM = (
    "The box plot below shows quiz scores. Reading rule: * = min/max, "
    "[ ] = Q1/Q3, : = median, o = outlier, 1 char per unit.\n"
    "Scale: 0    5    10   15   20\n"
    "       +----+----+----+----+\n"
    "Plot:     *-[==:===]--*\n"
    "Read the five-number summary."
)

DOT_PLOT_PROBLEM = (
    "Dot plot of quiz scores (each ● is one student):\n"
    " 6 ∣ ● ●\n"
    " 7 ∣\n"
    " 8 ∣ ● ● ● ●\n"
    " 9 ∣ ●\n"
    "10 ∣ ● ●\n"
    "How many students scored more than 7?"
)

STEM_PROBLEM = (
    "Stem ∣ Leaves\n"
    "   1 ∣ 2 5 7\n"
    "   2 ∣ 0 3 3\n"
    "   3 ∣\n"
    "   4 ∣ 1\n"
    "Key: 2 ∣ 3 means 23\n"
    "Find the median."
)

TALLY_PROBLEM = (
    "Ms. Ortiz recorded each student's favorite color.\n"
    "Blue: ////\\ //\n"
    "Green: //\n"
    "Red: ////\n"
    "How many students chose Blue?"
)

TWO_WAY_PROBLEM = (
    "The two-way table shows the survey results.\n"
    "           Yes   No   Total\n"
    "Grade 9     12    8      20\n"
    "Grade 10    15   15      30\n"
    "Total       27   23      50\n"
    "What percent of Grade 9 students said Yes?"
)

NORMAL_PROBLEM = (
    "Commute times have μ = 50 and σ = 12. For samples of 36, find "
    "P(x̄ > 53). Standard normal table, Φ(z) = P(Z < z): z=1.30: 0.9032; "
    "z=1.50: 0.9332; z=1.80: 0.9641. Use z* = 1.96 if you need it."
)


def example(problem, steps, answer):
    """A minimal generator-shaped example."""
    return {
        "problem_id": "fixture",
        "operation": "fixture",
        "problem": problem,
        "steps": list(steps) + [f"Z{DELIM}{answer}"],
        "final_answer": answer,
    }


GOOD_EXAMPLES = (
    example(
        BOX_PLOT_PROBLEM,
        ["RULE|box plot|* = min/max, [ ] = Q1/Q3, : = median, o = outlier",
         "PLOT_READ|min|column 3|3", "PLOT_READ|Q1|column 5|5"],
        "min = 3, Q1 = 5, median = 8, Q3 = 12, max = 15",
    ),
    example(DOT_PLOT_PROBLEM,
            ["PLOT_READ|row 8|●●●●|4", "A|4|1|5", "A|5|2|7"], "7"),
    example(STEM_PROBLEM,
            ["LEAF_KEY|2 ∣ 3|23", "SORT|12,15,17,20,23,23,41|20"], "20"),
    example(TALLY_PROBLEM, ["TALLY_ROW|Blue|////\\ //|7"], "7"),
    example(TWO_WAY_PROBLEM,
            ["MARGIN_ROW|Grade 9|12 + 8|20", "COND_ROW|Yes given Grade 9|12/20|60%"],
            "60%"),
    example(NORMAL_PROBLEM,
            ["SE_FORMULA|σ/√n", "ROOT|√36|6", "D|12|6|2",
             "ZSCORE|(53 - 50)/2|1.50",
             "TABLE_LOOKUP|Φ(1.50)|0.9332",
             "S|1.0000|0.9332|0.0668"],
            "0.0668"),
    example("Find the sample standard deviation of 9, 11, 11, 13.",
            ["MEAN_DIV|44|4|11", "D|8|3|8/3"], "2"),
    example("A bottler claims bottles hold 500 mL. An inspector suspects the "
            "mean is less. Write the hypotheses and name the tail.",
            ["HYP_STATE|H0: μ = 500|Ha: μ < 500|left-tailed"],
            "H0: μ = 500; Ha: μ < 500; left-tailed"),
)


class TestStatisticsConventions(unittest.TestCase):
    """The sweep every statistics generator must survive."""

    def test_flagged_generators(self):
        """200 examples from every STATISTICS generator obey the strand
        conventions. (No generator carries the flag yet — the fixture tests
        below keep the sweep honest until Phase 1 lands.)"""
        gens = flagged_generators("STATISTICS")
        self.assertIsInstance(gens, list)
        for gen in gens:
            name = type(gen).__name__
            with self.subTest(generator=name):
                for ex in sample_examples(gen, n=SAMPLES, seed=SEED):
                    assert_contract(self, ex)
                    assert_pipe_safe(self, ex)
                    problems = all_violations(ex)
                    self.assertFalse(
                        problems,
                        f"{name} {ex.get('operation')}: {problems}")

    def test_checkers_accept_well_formed_examples(self):
        for i, ex in enumerate(GOOD_EXAMPLES):
            with self.subTest(fixture=i):
                assert_contract(self, ex)
                assert_pipe_safe(self, ex)
                self.assertEqual([], all_violations(ex))

    def test_every_fixture_display_is_recognised(self):
        """The grammar sweep actually finds the displays it must check."""
        kinds = {
            BOX_PLOT_PROBLEM: "box_plot",
            DOT_PLOT_PROBLEM: "dot_plot",
            STEM_PROBLEM: "stem_leaf",
            TALLY_PROBLEM: "tally",
            TWO_WAY_PROBLEM: "two_way",
            NORMAL_PROBLEM: "phi_table",
        }
        for problem, kind in kinds.items():
            with self.subTest(kind=kind):
                found = [k for k, _ in oracle.find_displays(problem)]
                self.assertIn(kind, found)


class TestCheckersRejectViolations(unittest.TestCase):
    """Each checker is shown rejecting a violating synthetic example, so the
    sweep above is not vacuously green."""

    def test_lookup_value_absent_from_problem(self):
        ex = example(NORMAL_PROBLEM, ["TABLE_LOOKUP|Φ(2.00)|0.9772"], "0.0228")
        self.assertTrue(lookup_violations(ex))
        self.assertIn("0.9772", lookup_violations(ex)[0])

    def test_lookup_supplied_value_absent_from_problem(self):
        ex = example("Using t* = 2.131 (df = 15), find the interval.",
                     ["LOOKUP_SUPPLIED|t* (df = 15)|2.262"], "(45.7, 54.3)")
        self.assertTrue(lookup_violations(ex))

    def test_lookup_supplied_value_present_is_accepted(self):
        ex = example("Using t* = 2.131 (df = 15), find the interval.",
                     ["LOOKUP_SUPPLIED|t* (df = 15)|2.131"], "(45.738, 54.262)")
        self.assertEqual([], lookup_violations(ex))

    def test_lookup_step_without_a_value(self):
        ex = example(NORMAL_PROBLEM, ["TABLE_LOOKUP|Φ(1.50)"], "0.0668")
        self.assertTrue(lookup_violations(ex))

    def test_padded_decimal_answer(self):
        ex = example("Find the proportion.", ["D|3|4|0.75"], "0.750")
        self.assertTrue(decimal_violations(ex))

    def test_four_decimal_probability_is_allowed(self):
        ex = example("Find the probability.", ["S|1.0000|0.0670|0.9330"],
                     "0.9330")
        self.assertEqual([], decimal_violations(ex))

    def test_money_answer_is_allowed(self):
        ex = example("Find the mean cost.", ["D|60|3|20.00"], "$20.00")
        self.assertEqual([], decimal_violations(ex))

    def test_supplied_constant_keeps_the_problem_digits(self):
        ex = example("χ² critical value = 11.070 (df = 5). Decide at 0.05.",
                     ["CHECK|χ² vs critical|12.5 > 11.070|reject H0"],
                     "reject H0 (12.5 > 11.070)")
        self.assertEqual([], decimal_violations(ex))

    def test_rounded_answer_is_rejected(self):
        ex = example("Find the mean.", ["D|10|3|3.33"], "≈ 3.33")
        self.assertTrue(decimal_violations(ex))
        worded = example("Find the mean.", ["D|10|3|3.33"],
                         "approximately 3.33")
        self.assertTrue(decimal_violations(worded))

    def test_approximately_normal_label_is_allowed(self):
        ex = example("Describe the CLT shape.",
                     ["CLT_CHECK|n = 36 ≥ 30|approximately normal"],
                     "approximately normal (n = 36 ≥ 30); mean 50; SE 2")
        self.assertEqual([], decimal_violations(ex))

    def test_scientific_notation_is_rejected(self):
        ex = example("Find the probability.", ["D|1|1000|0.001"], "1.0e-3")
        self.assertTrue(decimal_violations(ex))

    def test_z_payload_mismatch(self):
        ex = example("Find the mean.", ["D|20|4|5"], "5")
        ex["steps"][-1] = f"Z{DELIM}6"
        self.assertTrue(z_payload_violations(ex))

    def test_broken_box_plot_whisker(self):
        """The right whisker stops one column short of the '*'."""
        broken = BOX_PLOT_PROBLEM.replace("*-[==:===]--*", "*-[==:===]- *")
        ex = example(broken, ["PLOT_READ|min|column 3|3"],
                     "min = 3, Q1 = 5, median = 8, Q3 = 12, max = 15")
        self.assertTrue(display_violations(ex))

    def test_box_plot_missing_median(self):
        broken = BOX_PLOT_PROBLEM.replace("*-[==:===]--*", "*-[======]--*")
        ex = example(broken, [], "min = 3")
        self.assertTrue(display_violations(ex))

    def test_dot_plot_with_a_missing_row(self):
        """A gap row that is dropped instead of drawn empty."""
        broken = DOT_PLOT_PROBLEM.replace(" 7 ∣\n", "")
        ex = example(broken, [], "7")
        self.assertTrue(display_violations(ex))

    def test_stem_plot_with_unsorted_leaves(self):
        broken = STEM_PROBLEM.replace("2 ∣ 0 3 3", "2 ∣ 3 0 3")
        ex = example(broken, [], "20")
        self.assertTrue(display_violations(ex))

    def test_stem_plot_without_a_key(self):
        broken = STEM_PROBLEM.replace("Key: 2 ∣ 3 means 23\n", "")
        ex = example(broken, [], "20")
        self.assertTrue(display_violations(ex))

    def test_tally_with_a_five_stroke_group(self):
        """Five slashes instead of the four-plus-backslash group."""
        broken = TALLY_PROBLEM.replace("Blue: ////\\ //", "Blue: ///// //")
        ex = example(broken, [], "7")
        self.assertTrue(display_violations(ex))

    def test_tally_out_of_alphabetical_order(self):
        broken = TALLY_PROBLEM.replace(
            "Blue: ////\\ //\nGreen: //\nRed: ////",
            "Red: ////\nBlue: ////\\ //\nGreen: //")
        ex = example(broken, [], "7")
        self.assertTrue(display_violations(ex))

    def test_two_way_table_with_a_missing_cell(self):
        broken = TWO_WAY_PROBLEM.replace("Grade 10    15   15      30",
                                         "Grade 10    15           30")
        ex = example(broken, [], "60%")
        self.assertTrue(display_violations(ex))

    def test_negative_phi_row_is_rejected(self):
        broken = NORMAL_PROBLEM.replace("z=1.50", "z=-1.50")
        ex = example(broken, [], "0.0668")
        self.assertTrue(display_violations(ex))

    def test_pipe_in_the_problem_is_rejected(self):
        ex = example("Find P(A|B).", ["D|1|2|0.5"], "0.5")
        from tests.conventions_common import pipe_violations
        self.assertTrue(pipe_violations(ex))


class TestOracleIsIndependent(unittest.TestCase):
    """A9: the oracle must not lean on the generator-side helpers."""

    def test_oracle_imports_nothing_from_the_strand_helpers(self):
        path = os.path.join(repo_root, "tests", "stats_oracle.py")
        with open(path, encoding="utf-8") as fh:
            source = fh.read()
        for banned in ("stats_common", "prob_common"):
            self.assertNotIn(f"import {banned}", source)
            self.assertNotIn(f"from {banned}", source)
        self.assertNotIn("stats_common", sys.modules.get(
            "tests.stats_oracle").__dict__)

    def test_oracle_routines_are_exact(self):
        """Sanity: the oracle's own arithmetic stays in Fractions."""
        self.assertEqual(Fraction(11), oracle.mean([9, 11, 11, 13]))
        self.assertEqual(Fraction(8, 3), oracle.variance([9, 11, 11, 13],
                                                         sample=True))


if __name__ == "__main__":
    unittest.main()
