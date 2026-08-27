import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.euler_method_generator import EulerMethodGenerator
from generators.exponential_model_generator import dec
from helpers import DELIM

NUM = r"-?\d+(?:\.\d+)?"


def parse_problem(text):
    """Parse any phrasing into (a, b, c, h, x0, y0, n, indep, dep).

    Independent of the generator: only the rendered sentence is read.
    """
    ode = re.search(r"d([A-Za-z])/d([A-Za-z]) = (.+?)(?:,|\s+with\s+|\s+from\s+)",
                    text)
    assert ode, text
    dep, indep, rhs = ode.group(1), ode.group(2), ode.group(3)

    hm = re.search(r"h = (\d+(?:\.\d+)?)", text)
    assert hm, text
    h = Fraction(hm.group(1))

    ic = re.search(rf"{re.escape(dep)}\(({NUM})\)\s*=\s*({NUM})", text)
    assert ic, text
    x0, y0 = Fraction(ic.group(1)), Fraction(ic.group(2))

    target = None
    for m in re.finditer(rf"{re.escape(dep)}\(({NUM})\)(\s*=)?", text):
        if m.group(2) is None:
            target = Fraction(m.group(1))
    assert target is not None, text

    a = b = c = Fraction(0)
    parts = re.split(r"\s+([+-])\s+", rhs.strip())
    terms = [parts[0]]
    for i in range(1, len(parts), 2):
        terms.append(parts[i] + parts[i + 1])
    for term in terms:
        m = re.fullmatch(r"([+-]?)\s*(\d*(?:\.\d+)?)\s*([A-Za-z]?)",
                         term.strip())
        assert m, (term, text)
        sign = -1 if m.group(1) == "-" else 1
        num = Fraction(m.group(2)) if m.group(2) else Fraction(1)
        coef = sign * num
        var = m.group(3)
        if var == indep:
            a += coef
        elif var == dep:
            b += coef
        elif var == "":
            c += coef
        else:  # pragma: no cover - would be a rendering bug
            raise AssertionError((term, text))

    n = (target - x0) / h
    assert n.denominator == 1 and n > 0, text
    return a, b, c, h, x0, y0, int(n), indep, dep


def oracle_answer(example):
    """A9 oracle: rerun Euler exactly from the problem text alone."""
    a, b, c, h, x0, y0, n, _, _ = parse_problem(example["problem"])
    x, y = x0, y0
    for _ in range(n):
        y = y + h * (a * x + b * y + c)
        x = x + h
    return dec(y)


class TestEulerMethodGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = EulerMethodGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_exact_recomputation(self):
        """A9 oracle: independent exact Euler run matches the answer."""
        for _ in range(600):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result),
                             result["final_answer"], result["problem"])

    def test_oracle_covers_every_variant(self):
        for variant in EulerMethodGenerator.VARIANTS:
            gen = EulerMethodGenerator(variant)
            for _ in range(120):
                result = gen.generate()
                self.assertEqual(result["operation"], f"euler_method_{variant}")
                self.assertEqual(oracle_answer(result),
                                 result["final_answer"], result["problem"])

    def test_all_phrasings_parse(self):
        """Every phrasing must round-trip through the independent parser."""
        starts = set()
        for _ in range(400):
            result = self.gen.generate()
            parse_problem(result["problem"])
            starts.add(result["problem"].split()[0])
        self.assertGreaterEqual(len(starts), 4)

    def test_step_arithmetic(self):
        """EVAL / M / A / S fields must be internally consistent and match
        an exact Euler run reconstructed from the problem text."""
        for _ in range(300):
            result = self.gen.generate()
            a, b, c, h, x0, y0, n, indep, dep = parse_problem(result["problem"])
            rows = [s.split(DELIM) for s in result["steps"]
                    if s.startswith(f"TABLE_ENTRY{DELIM}")]
            evals = [s.split(DELIM) for s in result["steps"]
                     if s.startswith(f"EVAL{DELIM}")]
            muls = [s.split(DELIM) for s in result["steps"]
                    if s.startswith(f"M{DELIM}")]
            self.assertEqual(len(rows), n + 1)
            self.assertEqual(len(evals), n)
            self.assertEqual(len(muls), n)
            x, y = x0, y0
            self.assertEqual(rows[0][1], f"{indep} = {dec(x0)}")
            self.assertEqual(rows[0][2], f"{dep} = {dec(y0)}")
            for i in range(n):
                k = a * x + b * y + c
                hk = h * k
                # EVAL shows f(x, y) and the substituted value.
                self.assertEqual(evals[i][1], f"f({dec(x)}, {dec(y)})")
                self.assertTrue(evals[i][2].endswith(f"= {dec(k)}"),
                                (evals[i], dec(k)))
                # M multiplies the step size by the slope.
                self.assertEqual(muls[i][1], dec(h))
                self.assertEqual(muls[i][2], dec(k))
                self.assertEqual(muls[i][3], dec(hk))
                self.assertEqual(Fraction(muls[i][1]) * Fraction(muls[i][2]),
                                 Fraction(muls[i][3]))
                y = y + hk
                x = x + h
                self.assertEqual(rows[i + 1][1], f"{indep} = {dec(x)}")
                self.assertEqual(rows[i + 1][2], f"{dep} = {dec(y)}")
            self.assertEqual(dec(y), result["final_answer"])

    def test_update_steps_are_exact(self):
        """The A / S update line must equal the two table rows it joins."""
        for _ in range(200):
            result = self.gen.generate()
            for s in result["steps"]:
                parts = s.split(DELIM)
                if parts[0] == "A":
                    self.assertEqual(Fraction(parts[1]) + Fraction(parts[2]),
                                     Fraction(parts[3]), s)
                elif parts[0] == "S":
                    self.assertEqual(Fraction(parts[1]) - Fraction(parts[2]),
                                     Fraction(parts[3]), s)

    def test_table_rows_match_step_count(self):
        for variant, n in (("two_step", 2), ("three_step", 3),
                           ("four_step", 4)):
            gen = EulerMethodGenerator(variant)
            for _ in range(100):
                result = gen.generate()
                rows = [s for s in result["steps"]
                        if s.startswith(f"TABLE_ENTRY{DELIM}")]
                self.assertEqual(len(rows), n + 1)
                slopes = [s for s in result["steps"]
                          if s.startswith(f"EVAL{DELIM}")]
                self.assertEqual(len(slopes), n)
                # The last table row holds the final answer.
                self.assertEqual(rows[-1].split(DELIM)[2].split(" = ")[1],
                                 result["final_answer"])

    def test_no_degenerate_renders(self):
        for _ in range(300):
            result = self.gen.generate()
            joined = " ".join(result["steps"]) + " " + result["problem"]
            for bad in (r"(?<![\d.])1x", r"(?<![\d.])1y", "--", r"\+ -",
                        r"\d\.\d*0\b", r"\bE\b"):
                self.assertIsNone(re.search(bad, joined),
                                  (bad, result["steps"]))

    def test_pipe_safety_and_field_count(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertNotIn(DELIM, result["problem"])
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)), 5, s)
                for field in s.split(DELIM):
                    self.assertNotIn(DELIM, field)

    def test_hand_friendly_values(self):
        """No table value may run past four decimal places."""
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                for tok in re.findall(r"-?\d+\.(\d+)", s):
                    self.assertLessEqual(len(tok), 4, s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(200):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)

    def test_determinism_under_seed(self):
        random.seed(11)
        first = [EulerMethodGenerator().generate()["problem"]
                 for _ in range(20)]
        random.seed(11)
        second = [EulerMethodGenerator().generate()["problem"]
                  for _ in range(20)]
        self.assertEqual(first, second)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            EulerMethodGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
