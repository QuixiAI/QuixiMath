"""Problem-text-only brute-force oracles for SimpsonsParadoxGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.simpsons_paradox_generator import (
    APPLIED, FRAMES, MODIFIERS, VARIANTS, SimpsonsParadoxGenerator,
)
from helpers import DELIM

MODELS = {
    "compute_and_state_reversal": "pooled = (subgroup 1 count + subgroup 2 count)/100",
    "which_is_better_overall": "pooled = (subgroup 1 count + subgroup 2 count)/100",
    "which_is_better_in_each_group": "rate = count/subgroup size",
    "weights_explain": "composition = subgroup size/total",
    "no_reversal_control": "pooled = (subgroup 1 count + subgroup 2 count)/total",
}

METRIC_ALT = r"(?:recovered|were admitted|were hits|closed)"
ENTITY_RE = re.compile(
    rf"[A-Za-z][\w ]*? ([AB]): (\d+) of (\d+) ([\w -]+?) {METRIC_ALT}, "
    rf"(\d+) of (\d+) ([\w -]+?) {METRIC_ALT}\.")


def dec(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    scaled, places = value, 0
    while scaled.denominator != 1 and places < 12:
        scaled *= 10
        places += 1
    if scaled.denominator != 1:
        raise AssertionError(f"does not terminate: {value}")
    digits = str(abs(scaled.numerator)).rjust(places + 1, "0")
    text = (digits[:-places] + "." + digits[-places:]).rstrip("0").rstrip(".")
    return ("-" if value < 0 else "") + text


def pct(fr):
    return dec(Fraction(fr) * 100)


def clean(problem):
    return re.sub(r"^An unrelated memo lists \d+ filed reports\. ", "", problem)


def _parse(text):
    matches = list(ENTITY_RE.finditer(text))
    assert len(matches) == 2, text
    data, sub1, sub2 = {}, None, None
    for m in matches:
        letter, a1, size1, s1, a2, size2, s2 = m.groups()
        data[letter] = (int(a1), int(size1), int(a2), int(size2))
        sub1, sub2 = s1.strip(), s2.strip()
    assert set(data) == {"A", "B"}, text
    return data["A"], data["B"], sub1, sub2


def solve(problem):
    """A9 oracle: recompute every subgroup and pooled rate from the problem
    text alone, then build whichever answer shape the question asks for —
    generically, from the numbers, not from which variant produced the
    text (``compute_and_state_reversal`` and ``no_reversal_control`` ask an
    identical question and are told apart only by their numbers)."""
    text = clean(problem)
    (a1, asize1, a2, asize2), (b1, bsize1, b2, bsize2), sub1, sub2 = _parse(text)
    short1, short2 = sub1.rsplit(" ", 1)[0], sub2.rsplit(" ", 1)[0]
    rate_a1, rate_a2 = Fraction(a1, asize1), Fraction(a2, asize2)
    rate_b1, rate_b2 = Fraction(b1, bsize1), Fraction(b2, bsize2)
    pooled_a = Fraction(a1 + a2, asize1 + asize2)
    pooled_b = Fraction(b1 + b2, bsize1 + bsize2)

    if "and what are the two overall rates" in text:
        if pooled_b > pooled_a:
            return f"B; {pct(pooled_b)}% vs {pct(pooled_a)}%"
        return f"A; {pct(pooled_a)}% vs {pct(pooled_b)}%"

    if "group sizes show" in text:
        a_total, b_total = asize1 + asize2, bsize1 + bsize2
        a_share2 = Fraction(asize2, a_total) * 100
        b_share1 = Fraction(bsize1, b_total) * 100
        return f"A's cases are {dec(a_share2)}% {short2}; B's cases are {dec(b_share1)}% {short1}"

    if "has the better rate in" in text:
        w1, w2 = ("A" if rate_a1 > rate_b1 else "B"), ("A" if rate_a2 > rate_b2 else "B")
        hi1, lo1 = (rate_a1, rate_b1) if w1 == "A" else (rate_b1, rate_a1)
        hi2, lo2 = (rate_a2, rate_b2) if w2 == "A" else (rate_b2, rate_a2)
        return (f"{sub1}: {w1} ({pct(hi1)}% > {pct(lo1)}%); "
               f"{sub2}: {w2} ({pct(hi2)}% > {pct(lo2)}%)")

    # The shared "compare within each group, and overall" shape.
    assert rate_a1 > rate_b1 and rate_a2 > rate_b2, text
    base = (f"A better in both groups ({pct(rate_a1)}% > {pct(rate_b1)}%, "
           f"{pct(rate_a2)}% > {pct(rate_b2)}%)")
    if pooled_b > pooled_a:
        return f"{base}; B better overall ({pct(pooled_b)}% > {pct(pooled_a)}%)"
    assert pooled_a > pooled_b, text
    return f"{base} and overall ({pct(pooled_a)}% > {pct(pooled_b)}%); no reversal"


def expected(problem, variant, modifier):
    answer = solve(problem)
    model = MODELS[variant]
    return (f"{model}; {answer}" if modifier == "with_model" else answer), model


class TestSimpsonsParadoxGenerator(unittest.TestCase):
    def test_marker_contract_and_full_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(370)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(20):
                    result = SimpsonsParadoxGenerator(variant, modifier).generate()
                    self.assertEqual(result["steps"][-1], f"Z{DELIM}{result['final_answer']}")
                    answer, model = expected(result["problem"], variant, modifier)
                    self.assertEqual(result["final_answer"], answer, result["problem"])
                    if modifier == "with_model":
                        self.assertEqual(result["steps"][0].split(DELIM)[1], model)
                    seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})

    def test_plans_worked_example(self):
        problem = ("Hospital A: 8 of 10 easy cases recovered, 18 of 90 hard "
                  "cases recovered. Hospital B: 63 of 90 easy cases recovered, "
                  "1 of 10 hard cases recovered. Compare the recovery rates "
                  "within easy cases and hard cases, and overall.")
        self.assertEqual(
            solve(problem),
            "A better in both groups (80% > 70%, 20% > 10%); "
            "B better overall (64% > 26%)")

    def test_all_five_renderings_invert_every_variant(self):
        facts = ("Hospital A: 8 of 10 easy cases recovered, 18 of 90 hard "
                "cases recovered. Hospital B: 63 of 90 easy cases recovered, "
                "1 of 10 hard cases recovered.")
        question = "Compare the recovery rates within easy cases and hard cases, and overall."
        for frame in FRAMES:
            problem = frame.format(place="the market stand", name="Ari",
                                   facts=facts, question=question)
            self.assertEqual(solve(problem),
                             "A better in both groups (80% > 70%, 20% > 10%); "
                             "B better overall (64% > 26%)", problem)

    def test_no_reversal_control_never_reverses(self):
        random.seed(371)
        for _ in range(200):
            result = SimpsonsParadoxGenerator("no_reversal_control").generate()
            self.assertIn("no reversal", result["final_answer"])

    def test_reversal_variants_always_show_a_reversal(self):
        random.seed(372)
        for _ in range(200):
            result = SimpsonsParadoxGenerator("compute_and_state_reversal").generate()
            self.assertIn("B better overall", result["final_answer"])
            self.assertNotIn("no reversal", result["final_answer"])

    def test_arithmetic_inside_emitted_steps(self):
        random.seed(373)
        for _ in range(700):
            result = SimpsonsParadoxGenerator().generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "CMP":
                    x, y = Fraction(fields[1]), Fraction(fields[2])
                    self.assertEqual(fields[3], ">" if x > y else "<", raw)
                elif fields[0] in ("SUBGROUP_RATE", "POOLED_RATE"):
                    frac_txt, pct_txt = fields[-1].split(" = ")
                    num, den = frac_txt.split("/")
                    self.assertEqual(Fraction(int(num), int(den)) * 100,
                                     Fraction(pct_txt.rstrip("%")), raw)

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(374)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = SimpsonsParadoxGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["operation"],
                                 f"applied_simpsons_paradox_{variant}_{modifier}")
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            SimpsonsParadoxGenerator("bogus")
        with self.assertRaises(ValueError):
            SimpsonsParadoxGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(375)
        banned = ("1x", "-1x", "^1", "+ 0", "--", "the the", "e+")
        for _ in range(700):
            result = SimpsonsParadoxGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            joined = " ".join((result["problem"], result["final_answer"], *result["steps"]))
            for fragment in banned:
                self.assertNotIn(fragment, joined.lower())
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)

    def test_determinism_under_seed(self):
        random.seed(23)
        gen = SimpsonsParadoxGenerator()
        first = [gen.generate()["problem"] for _ in range(30)]
        random.seed(23)
        second = [gen.generate()["problem"] for _ in range(30)]
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
