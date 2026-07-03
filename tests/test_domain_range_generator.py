import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.domain_range_generator import DomainRangeGenerator
from helpers import DELIM


def parse_lin(txt, var):
    """'2x - 10', '-x + 3', 'x', 't + 4' -> (a, b)."""
    m = re.fullmatch(rf"(-?\d*){var}(?: ([+-]) (\d+))?", txt)
    assert m, txt
    a = int(m.group(1) + "1") if m.group(1) in ("", "-") else int(m.group(1))
    b = int(m.group(3) or 0) * (1 if (m.group(2) or "+") == "+" else -1)
    return a, b


def oracle_answer(example):
    """Independently derives the domain from the problem text alone."""
    m = re.fullmatch(r"Find the domain of [a-z]\(([a-z])\) = (.+)\.",
                     example["problem"])
    assert m, example["problem"]
    var, rule = m.groups()

    m = re.fullmatch(r"√\((.+)\)/\((.+)\)", rule)
    if m:  # combined: sqrt(x + p)/(x - q)
        a, b = parse_lin(m.group(1), var)
        c, d = parse_lin(m.group(2), var)
        assert a == 1 and c == 1
        return f"{var} ≥ {-b}, {var} ≠ {-d}"

    m = re.fullmatch(r"(?:.+/)?√\((.+)\)", rule)
    if m:  # radical, strict when there is a numerator prefix
        a, b = parse_lin(m.group(1), var)
        strict = "/" in rule
        edge = Fraction(-b, a)
        assert edge.denominator == 1
        if a > 0:
            rel = ">" if strict else "≥"
        else:
            rel = "<" if strict else "≤"
        return f"{var} {rel} {edge.numerator}"

    m = re.fullmatch(rf".+/\({var}\^2 \+ (\d+)\)", rule)
    if m:  # x^2 + c, c > 0: never zero
        return "All real numbers"

    m = re.fullmatch(
        rf".+/\({var}\^2(?: ([+-]) (\d*){var})? ([+-]) (\d+)\)", rule)
    if m:  # monic quadratic with integer roots
        B = int(m.group(2) or 1) * (1 if (m.group(1) or "+") == "+" else -1)
        if m.group(1) is None:
            B = 0
        C = int(m.group(4)) * (1 if m.group(3) == "+" else -1)
        roots = sorted(t for t in range(-30, 31) if t * t + B * t + C == 0)
        assert len(roots) == 2, rule
        return f"{var} ≠ {roots[0]}, {var} ≠ {roots[1]}"

    m = re.fullmatch(r".+/\((.+)\)", rule)
    assert m, rule
    a, b = parse_lin(m.group(1), var)
    r = Fraction(-b, a)
    assert r.denominator == 1
    return f"{var} ≠ {r.numerator}"


class TestDomainRangeGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = DomainRangeGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "function_domain")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: derive the domain independently for every variant."""
        for _ in range(600):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_every_record_states_its_conditions(self):
        for _ in range(300):
            result = self.gen.generate()
            conds = [s for s in result["steps"]
                     if s.startswith(f"DOMAIN_COND{DELIM}")]
            self.assertGreaterEqual(len(conds), 1, result["steps"])
            if "√" in result["problem"]:
                self.assertTrue(any("radicand" in c for c in conds),
                                result["steps"])
            if result["final_answer"].count("≠") or \
                    "All real" in result["final_answer"]:
                pass  # denominator condition checked below when present
            if "/" in result["problem"].split("√")[-1] or \
                    ("/" in result["problem"] and "√" not in result["problem"]):
                self.assertTrue(any("denominator" in c for c in conds),
                                result["steps"])

    def test_ineq_results_match_final_answer(self):
        """Every INEQ_RESULT relation/value appears in the answer."""
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "INEQ_RESULT":
                    self.assertIn(f"{f[1]} {f[2]} {f[3]}",
                                  result["final_answer"], s)

    def test_flip_present_iff_negative_leading_coef_radical(self):
        gen = DomainRangeGenerator("radical")
        for _ in range(200):
            result = gen.generate()
            radicand = re.search(r"√\((.+)\)", result["problem"]).group(1)
            negative = radicand.startswith("-")
            flipped = any(s.startswith(f"INEQ_FLIP{DELIM}")
                          for s in result["steps"])
            self.assertEqual(negative, flipped, result["problem"])
            rel = "≤" if negative else "≥"
            self.assertIn(rel, result["final_answer"], result["problem"])

    def test_quadratic_exclusions_ascending_and_zero_product(self):
        gen = DomainRangeGenerator("rational_quadratic")
        for _ in range(200):
            result = gen.generate()
            vals = [int(v) for v in
                    re.findall(r"≠ (-?\d+)", result["final_answer"])]
            self.assertEqual(vals, sorted(vals))
            self.assertEqual(len(vals), 2)
            self.assertTrue(any(s.startswith(f"ZERO_PRODUCT{DELIM}")
                                for s in result["steps"]))
            self.assertTrue(any(s.startswith(f"ACCEPT{DELIM}")
                                for s in result["steps"]))

    def test_none_variant_reasons_before_concluding(self):
        gen = DomainRangeGenerator("rational_none")
        for _ in range(50):
            result = gen.generate()
            self.assertEqual(result["final_answer"], "All real numbers")
            self.assertTrue(any(s.startswith(f"DOMAIN_NOTE{DELIM}")
                                for s in result["steps"]))

    def test_all_variants_reachable(self):
        kinds = set()
        for _ in range(400):
            result = self.gen.generate()
            ans = result["final_answer"]
            p = result["problem"]
            if ans == "All real numbers":
                kinds.add("none")
            elif "≥" in ans and "≠" in ans:
                kinds.add("combined")
            elif "≥" in ans or "≤" in ans:
                kinds.add("radical")
            elif ">" in ans or "<" in ans:
                kinds.add("radical_den")
            elif ans.count("≠") == 2:
                kinds.add("quadratic")
            else:
                kinds.add("linear")
        self.assertEqual(kinds, {"none", "combined", "radical",
                                 "radical_den", "quadratic", "linear"})

    def test_no_unit_coefficient_rendering(self):
        for _ in range(400):
            result = self.gen.generate()
            self.assertNotRegex(result["problem"], r"(?<!\d)1[a-z]",
                                result["problem"])

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            DomainRangeGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
