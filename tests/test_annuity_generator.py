import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.annuity_generator import AnnuityGenerator
from helpers import DELIM


NAME = r"[A-Z][a-z]+"
WORDS = r"[a-z ]+"


def rx(pattern):
    return re.compile(pattern)


# --- one regex per phrasing; the oracle never imports the templates -------
FV_PATTERNS = [
    rx(r"An ordinary annuity pays \$(?P<pmt>\d+) at the end of each "
       r"(?P<unit>\w+) for (?P<n>\d+) \w+ at (?P<rate>\d+)% per \w+\. "
       r"Find the future value\."),
    rx(r"(?P<name>" + NAME + r") deposits \$(?P<pmt>\d+) into a "
       r"(?P<fund>" + WORDS + r") at the end of each (?P<unit>\w+) for "
       r"(?P<n>\d+) \w+\. The account earns (?P<rate>\d+)% per \w+\. "
       r"What is the future value of the annuity\?"),
    rx(r"At the end of every (?P<unit>\w+), (?P<name>" + NAME + r") adds "
       r"\$(?P<pmt>\d+) to a (?P<fund>" + WORDS + r") that earns "
       r"(?P<rate>\d+)% per \w+\. How much is in the " + WORDS +
       r" right after the (?P<n>\d+)(?:st|nd|rd|th) deposit\?"),
    rx(r"A (?P<fund>" + WORDS + r") receives an end-of-(?P<unit>\w+) "
       r"payment of \$(?P<pmt>\d+) for (?P<n>\d+) \w+ and grows at "
       r"(?P<rate>\d+)% per \w+\. Find the accumulated value of the "
       r"annuity\."),
    rx(r"(?P<name>" + NAME + r") makes (?P<n>\d+) end-of-(?P<unit>\w+) "
       r"deposits of \$(?P<pmt>\d+) each into a (?P<fund>" + WORDS +
       r") paying (?P<rate>\d+)% per \w+\. Find the future value of the "
       r"annuity\."),
]

PV_PATTERNS = [
    rx(r"An ordinary annuity pays \$(?P<pmt>\d+) at the end of each "
       r"(?P<unit>\w+) for (?P<n>\d+) \w+ at (?P<rate>\d+)% per \w+\. "
       r"Find the present value\."),
    rx(r"(?P<name>" + NAME + r") will receive \$(?P<pmt>\d+) at the end "
       r"of each (?P<unit>\w+) for (?P<n>\d+) \w+ from a (?P<fund>" +
       WORDS + r") earning (?P<rate>\d+)% per \w+\. What is the present "
       r"value of the annuity\?"),
    rx(r"How much must be deposited now in a (?P<fund>" + WORDS +
       r") earning (?P<rate>\d+)% per (?P<unit>\w+) so that it can pay "
       r"out \$(?P<pmt>\d+) at the end of each \w+ for (?P<n>\d+) \w+\?"),
    rx(r"A (?P<loan>" + WORDS + r") is repaid with (?P<n>\d+) "
       r"end-of-(?P<unit>\w+) payments of \$(?P<pmt>\d+) at (?P<rate>\d+)% "
       r"per \w+\. Find the present value of the payment stream\."),
    rx(r"(?P<name>" + NAME + r") is offered \$(?P<pmt>\d+) at the end of "
       r"each (?P<unit>\w+) for the next (?P<n>\d+) \w+\. At "
       r"(?P<rate>\d+)% per \w+, what single amount today is worth the "
       r"same\?"),
]

DUE_PATTERNS = [
    rx(r"An annuity due pays \$(?P<pmt>\d+) at the beginning of each "
       r"(?P<unit>\w+) for (?P<n>\d+) \w+ at (?P<rate>\d+)% per \w+\. "
       r"Find the future value\."),
    rx(r"(?P<name>" + NAME + r") deposits \$(?P<pmt>\d+) at the beginning "
       r"of every (?P<unit>\w+) into a (?P<fund>" + WORDS + r") earning "
       r"(?P<rate>\d+)% per \w+\. What is the value of the " + WORDS +
       r" at the end of (?P<n>\d+) \w+\?"),
    rx(r"Each (?P<unit>\w+) opens with a \$(?P<pmt>\d+) deposit into a "
       r"(?P<fund>" + WORDS + r") that pays (?P<rate>\d+)% per \w+\. "
       r"Find the future value of the annuity due after (?P<n>\d+) \w+\."),
    rx(r"(?P<name>" + NAME + r") makes (?P<n>\d+) beginning-of-"
       r"(?P<unit>\w+) payments of \$(?P<pmt>\d+) into a (?P<fund>" +
       WORDS + r") at (?P<rate>\d+)% per \w+\. Find the future value of "
       r"the annuity due\."),
]

PERP_PATTERNS = [
    rx(r"A perpetuity pays \$(?P<pmt>\d+) at the end of each "
       r"(?P<unit>\w+) forever\. At (?P<rate>\d+)% per \w+, find its "
       r"present value\."),
    rx(r"(?P<name>" + NAME + r") wants a (?P<fund>" + WORDS + r") that "
       r"pays \$(?P<pmt>\d+) at the end of each (?P<unit>\w+) forever\. "
       r"If the " + WORDS + r" earns (?P<rate>\d+)% per \w+, how much "
       r"must be deposited today\?"),
    rx(r"The (?P<fund>" + WORDS + r") at (?P<name>" + NAME + r") College "
       r"must pay \$(?P<pmt>\d+) every (?P<unit>\w+) forever out of "
       r"interest alone\. At (?P<rate>\d+)% per \w+, what principal is "
       r"required\?"),
    rx(r"Find the present value of a perpetuity of \$(?P<pmt>\d+) per "
       r"(?P<unit>\w+) at (?P<rate>\d+)% per \w+\."),
    rx(r"(?P<name>" + NAME + r") deposits a lump sum into a (?P<fund>" +
       WORDS + r") paying (?P<rate>\d+)% per (?P<unit>\w+)\. If only the "
       r"interest is withdrawn, the " + WORDS + r" can pay \$(?P<pmt>\d+) "
       r"every \w+ forever\. How large is the lump sum\?"),
]

AMORT_PATTERNS = [
    rx(r"Build a (?P<n>\d+)-payment amortization schedule for a loan with "
       r"starting balance \$(?P<bal>\d+), payment \$(?P<pmt>\d+), and "
       r"period rate (?P<rate>\d+)%\. Find total interest and final "
       r"balance\."),
    rx(r"(?P<name>" + NAME + r") owes \$(?P<bal>\d+) on a (?P<loan>" +
       WORDS + r") charged (?P<rate>\d+)% per (?P<unit>\w+)\. The payment "
       r"is \$(?P<pmt>\d+) per \w+\. After (?P<n>\d+) payments, find the "
       r"total interest paid and the balance that remains\."),
    rx(r"A (?P<loan>" + WORDS + r") of \$(?P<bal>\d+) charges "
       r"(?P<rate>\d+)% interest per (?P<unit>\w+)\. With \$(?P<pmt>\d+) "
       r"paid each \w+, amortize the first (?P<n>\d+) payments and give "
       r"the total interest and the remaining balance\."),
    rx(r"The balance on (?P<name>" + NAME + r")'s (?P<loan>" + WORDS +
       r") is \$(?P<bal>\d+), the rate is (?P<rate>\d+)% per "
       r"(?P<unit>\w+), and the payment due each \w+ is \$(?P<pmt>\d+)\. "
       r"Fill in (?P<n>\d+) rows of the amortization schedule, then "
       r"report the total interest and the ending balance\."),
]

ALL_PATTERNS = [
    ("future_value", FV_PATTERNS),
    ("present_value", PV_PATTERNS),
    ("due", DUE_PATTERNS),
    ("perpetuity", PERP_PATTERNS),
    ("amortization", AMORT_PATTERNS),
]


def parse(problem):
    """(variant, template_index, fields) for a problem text, or raise."""
    hits = []
    for variant, patterns in ALL_PATTERNS:
        for index, pattern in enumerate(patterns):
            match = pattern.fullmatch(problem)
            if match:
                hits.append((variant, index, match.groupdict()))
    if len(hits) != 1:
        raise AssertionError(f"{len(hits)} phrasings matched: {problem!r}")
    return hits[0]


def money(fr):
    cents = fr * 100
    assert cents.denominator == 1, fr
    c = cents.numerator
    return f"${c // 100}.{c % 100:02d}"


# --- independent solvers: simulation, never the closed form --------------
def sim_future_value(pmt, rate, periods):
    """Roll the account forward one period at a time."""
    balance = Fraction(0)
    for _ in range(periods):
        balance = balance * (1 + rate) + pmt
    return balance


def sim_due_value(pmt, rate, periods):
    """Annuity due: the deposit lands before the period's growth."""
    balance = Fraction(0)
    for _ in range(periods):
        balance = (balance + pmt) * (1 + rate)
    return balance


def sim_present_value(pmt, rate, periods):
    """Discount the payment stream back one period at a time."""
    value = Fraction(0)
    for _ in range(periods):
        value = (value + pmt) / (1 + rate)
    return value


def sim_schedule(balance, payment, rate, periods):
    rows = []
    total_interest = Fraction(0)
    for _ in range(periods):
        interest = balance * rate
        principal = payment - interest
        balance = balance - principal
        total_interest += interest
        rows.append((interest, principal, balance))
    return rows, total_interest, balance


def oracle(problem):
    """Recompute the expected final answer from the problem text alone."""
    variant, _, fields = parse(problem)
    rate = Fraction(int(fields["rate"]), 100)
    pmt = Fraction(int(fields["pmt"]))
    if variant == "perpetuity":
        # Interest alone must cover the payment: value * rate == pmt.
        value = pmt * 100 / int(fields["rate"])
        assert value * rate == pmt
        return variant, f"present_value {money(value)}", fields
    if variant == "amortization":
        rows, total_interest, final_balance = sim_schedule(
            Fraction(int(fields["bal"])), pmt, rate, int(fields["n"]))
        return variant, (
            f"total_interest {money(total_interest)}; "
            f"final_balance {money(final_balance)}"), fields
    periods = int(fields["n"])
    if variant == "future_value":
        return variant, (
            f"future_value {money(sim_future_value(pmt, rate, periods))}"
        ), fields
    if variant == "due":
        return variant, (
            f"future_value_due {money(sim_due_value(pmt, rate, periods))}"
        ), fields
    return variant, (
        f"present_value {money(sim_present_value(pmt, rate, periods))}"
    ), fields


def check_step_arithmetic(case, steps):
    for raw_step in steps:
        fields = raw_step.split(DELIM)
        code = fields[0]
        if code == "A":
            case.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                             Fraction(fields[3]), raw_step)
        elif code == "S":
            case.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                             Fraction(fields[3]), raw_step)
        elif code == "M":
            case.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                             Fraction(fields[3]), raw_step)
        elif code == "D":
            case.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                             Fraction(fields[3]), raw_step)
        elif code == "E":
            case.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                             Fraction(fields[3]), raw_step)
        elif code == "CHECK":
            lhs = Fraction(fields[2].rsplit("=", 1)[1])
            rhs = Fraction(fields[3].rsplit("=", 1)[1])
            case.assertEqual(lhs, rhs, raw_step)


SETUP_RE = re.compile(r"PMT=(\d+),r=(\d+)%(?:,n=(\d+))?")
AMORT_SETUP_RE = re.compile(r"balance=(\d+),payment=(\d+),r=(\d+)%")


class TestAnnuityGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = AnnuityGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["operation"].startswith("annuity_"))
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_from_problem_text(self):
        seen = set()
        for _ in range(1500):
            result = self.gen.generate()
            variant, answer, _ = oracle(result["problem"])
            seen.add(variant)
            self.assertEqual(result["operation"], f"annuity_{variant}",
                             result["problem"])
            self.assertEqual(result["final_answer"], answer,
                             result["problem"])
            check_step_arithmetic(self, result["steps"])
        self.assertEqual(seen, set(AnnuityGenerator.VARIANTS))

    def test_every_phrasing_is_reachable_and_unambiguous(self):
        counts = {}
        for _ in range(4000):
            variant, index, _ = parse(self.gen.generate()["problem"])
            counts[(variant, index)] = counts.get((variant, index), 0) + 1
        for variant, patterns in ALL_PATTERNS:
            for index in range(len(patterns)):
                self.assertIn((variant, index), counts,
                              f"phrasing {variant}#{index} never generated")

    def test_setup_step_matches_problem_text(self):
        for _ in range(400):
            result = self.gen.generate()
            variant, _, fields = oracle(result["problem"])
            setup = result["steps"][0].split(DELIM)
            self.assertEqual(setup[0], "ANNUITY_SETUP")
            if variant == "amortization":
                match = AMORT_SETUP_RE.fullmatch(setup[2])
                self.assertIsNotNone(match, setup)
                self.assertEqual(match.group(1), fields["bal"])
                self.assertEqual(match.group(2), fields["pmt"])
                self.assertEqual(match.group(3), fields["rate"])
                self.assertEqual(setup[3], f"periods={fields['n']}")
            else:
                match = SETUP_RE.fullmatch(setup[2])
                self.assertIsNotNone(match, setup)
                self.assertEqual(match.group(1), fields["pmt"])
                self.assertEqual(match.group(2), fields["rate"])
                if variant != "perpetuity":
                    self.assertEqual(match.group(3), fields["n"])

    def test_amortization_rows_match_simulation(self):
        gen = AnnuityGenerator("amortization")
        for _ in range(300):
            result = gen.generate()
            _, _, fields = oracle(result["problem"])
            rows, _, _ = sim_schedule(
                Fraction(int(fields["bal"])), Fraction(int(fields["pmt"])),
                Fraction(int(fields["rate"]), 100), int(fields["n"]))
            emitted = [s.split(DELIM) for s in result["steps"]
                       if s.startswith("AMORT_ROW")]
            self.assertEqual(len(emitted), len(rows), result["problem"])
            for index, (fields_row, (interest, principal, balance)) in \
                    enumerate(zip(emitted, rows), start=1):
                self.assertEqual(fields_row[1], str(index))
                self.assertEqual(fields_row[2],
                                 f"interest={money(interest)}")
                self.assertEqual(
                    fields_row[3],
                    f"principal={money(principal)},"
                    f"balance={money(balance)}")
                self.assertGreater(principal, 0, result["problem"])
                self.assertGreater(balance, 0, result["problem"])

    def test_variants_are_available(self):
        for variant in AnnuityGenerator.VARIANTS:
            for _ in range(30):
                result = AnnuityGenerator(variant).generate()
                self.assertEqual(result["operation"], f"annuity_{variant}")
                parsed_variant, answer, _ = oracle(result["problem"])
                self.assertEqual(parsed_variant, variant)
                self.assertEqual(result["final_answer"], answer)
                check_step_arithmetic(self, result["steps"])

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            AnnuityGenerator("bogus")

    def test_answers_are_exact_money(self):
        money_re = re.compile(r"\$\d+\.\d{2}")
        for _ in range(300):
            result = self.gen.generate()
            amounts = money_re.findall(result["final_answer"])
            self.assertTrue(amounts, result["final_answer"])
            self.assertIsNone(
                re.search(r"\de[+-]?\d", result["final_answer"]),
                result["final_answer"])

    def test_pipe_safe(self):
        for _ in range(400):
            result = self.gen.generate()
            self.assertNotIn(DELIM, result["problem"])
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])

    def test_seeded_determinism(self):
        import random
        random.seed(4242)
        first = [self.gen.generate()["problem"] for _ in range(20)]
        random.seed(4242)
        second = [self.gen.generate()["problem"] for _ in range(20)]
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
