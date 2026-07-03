import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.factor_trinomial_generator import FactorTrinomialGenerator
from helpers import DELIM


def parse_problem(problem):
    """'Factor: x^2 - 2x - 8' -> (var, b, c)."""
    expr = problem.split(": ", 1)[1]
    m = re.fullmatch(r"([a-z])\^2 ([+-]) (\d*)\1 ([+-]) (\d+)", expr)
    assert m, expr
    var = m.group(1)
    b = int(m.group(3) or 1) * (1 if m.group(2) == "+" else -1)
    c = int(m.group(5)) * (1 if m.group(4) == "+" else -1)
    return var, b, c


def parse_answer(ans, var):
    """'(x - 4)(x + 2)' -> (-4, 2)."""
    pairs = re.findall(rf"\({var} ([+-]) (\d+)\)", ans)
    assert len(pairs) == 2, ans
    return tuple(int(n) * (1 if s == "+" else -1) for s, n in pairs)


class TestFactorTrinomialGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = FactorTrinomialGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "factor_trinomial")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_roots_from_problem_text(self):
        """A9 oracle: the answer's roots must satisfy sum=b, product=c,
        and be ordered ascending (A0)."""
        for _ in range(400):
            result = self.gen.generate()
            var, b, c = parse_problem(result["problem"])
            p, q = parse_answer(result["final_answer"], var)
            self.assertEqual(p + q, b, result["problem"])
            self.assertEqual(p * q, c, result["problem"])
            self.assertLess(p, q, "factors not in ascending order")

    def test_trial_and_error_semantics(self):
        """TRY arithmetic true; REJECT iff sum wrong; ACCEPT is the winner
        and every TRY is resolved by exactly one REJECT or ACCEPT."""
        for _ in range(400):
            result = self.gen.generate()
            var, b, c = parse_problem(result["problem"])
            seq = [s.split(DELIM) for s in result["steps"]
                   if s.split(DELIM)[0] in ("TRY", "REJECT", "ACCEPT")]
            self.assertEqual(seq[-1][0], "ACCEPT")
            pending = None
            accepts = 0
            for f in seq:
                if f[0] == "TRY":
                    self.assertIsNone(pending, "unresolved TRY")
                    m, n = (int(v) for v in f[1].strip("()").split(", "))
                    self.assertEqual(m * n, c, str(f))
                    work_sum = int(f[2].rsplit("=", 1)[1])
                    self.assertEqual(m + n, work_sum, str(f))
                    pending = (m, n, work_sum)
                elif f[0] == "REJECT":
                    self.assertIsNotNone(pending)
                    self.assertNotEqual(pending[2], b, str(f))
                    pending = None
                else:  # ACCEPT
                    self.assertIsNotNone(pending)
                    self.assertEqual(pending[2], b, str(f))
                    p, q = parse_answer(result["final_answer"], var)
                    self.assertEqual({pending[0], pending[1]}, {p, q})
                    pending = None
                    accepts += 1
            self.assertEqual(accepts, 1)

    def test_rejections_occur_and_vary(self):
        counts = set()
        for _ in range(300):
            result = self.gen.generate()
            counts.add(sum(1 for s in result["steps"]
                           if s.startswith(f"REJECT{DELIM}")))
        self.assertIn(0, counts, "winner-first cases should exist")
        self.assertTrue(any(c >= 2 for c in counts),
                        "multi-rejection cases should exist")

    def test_foil_check_matches_original(self):
        for _ in range(200):
            result = self.gen.generate()
            check = next(s for s in result["steps"]
                         if s.startswith(f"CHECK{DELIM}"))
            f = check.split(DELIM)
            var, b, c = parse_problem(result["problem"])
            # lhs middle terms must combine to bx
            mids = re.findall(rf"([+-]) (\d*){var}(?!\^)", f[2])
            total = sum(int(n or 1) * (1 if s == "+" else -1) for s, n in mids)
            self.assertEqual(total, b, check)
            self.assertEqual(f[3], result["problem"].split(": ", 1)[1], check)


if __name__ == "__main__":
    unittest.main()
