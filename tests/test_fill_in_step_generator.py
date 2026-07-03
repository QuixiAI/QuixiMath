import os
import random
import re
import sys
import unittest
from math import gcd

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.fill_in_step_generator import FillInStepGenerator
from helpers import DELIM


def money(cents):
    return f"{cents // 100}.{cents % 100:02d}"


def parse_shown(problem):
    """Returns (numbered shown lines, blank index 0-based)."""
    lines = re.findall(r"^\d+\) (.+)$", problem, re.M)
    blanks = [i for i, s in enumerate(lines) if s == "____"]
    assert len(blanks) == 1, problem
    return lines, blanks[0]


def reconstruct_flow(example):
    """Independently rebuilds the full expected scratchpad from the problem
    statement alone."""
    p = example["problem"]
    op = example["operation"]
    if op == "fill_in_step_equation":
        m = re.search(r"Solve for x: (\d+)x ([+-]) (\d+) = (-?\d+)", p)
        a, sign, b, c = (int(m.group(1)), m.group(2), int(m.group(3)),
                         int(m.group(4)))
        rhs = c - b if sign == "+" else c + b
        assert rhs % a == 0
        x = rhs // a
        verb = "subtract" if sign == "+" else "add"
        eq = f"{a}x {sign} {b} = {c}"
        return [f"EQ_SETUP|{eq}",
                f"EQ_OP_BOTH|{verb}|{b}|{a}x|{rhs}",
                f"EQ_SIMPLIFY|{a}x = {rhs}",
                f"EQ_OP_BOTH|divide|{a}|x|{x}",
                f"EQ_RESULT|x|{x}",
                f"Z|{x}"]
    if op == "fill_in_step_ratio":
        m = re.search(
            r"Flour \(cups\): (\d+), \?\nSugar \(cups\): (\d+), (\d+)", p)
        pair1, pair2, known = (int(v) for v in m.groups())
        g = gcd(pair1, pair2)
        a, b = pair1 // g, pair2 // g
        k = known // b
        return [f"RATIO_TABLE|Flour (cups): {pair1}, ?|Sugar (cups): {pair2}, {known}",
                f"RATIO_BASE|{pair1}:{pair2}|{g}|{a}:{b}",
                f"D|{known}|{b}|{k}",
                f"M|{a}|{k}|{a * k}",
                f"Z|{a * k}"]
    # tip
    m = re.search(r"costs \$(\d+\.\d{2})\. Add a (\d+)% tip", p)
    bill = int(m.group(1).replace(".", ""))
    pct = int(m.group(2))
    tip = bill * pct // 100
    rate = f"{pct / 100:.2f}"
    return [f"PERCENT_TO_DEC|{pct}%|{rate}",
            f"M|{money(bill)}|{rate}|{money(tip)}",
            f"A|{money(bill)}|{money(tip)}|{money(bill + tip)}",
            f"Z|${money(bill + tip)}"]


class TestFillInStepGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = FillInStepGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstruction(self):
        """A9 oracle: rebuild the whole flow from the problem statement; the
        blanked line must equal the answer, and every shown line must match
        the reconstruction."""
        for _ in range(400):
            result = self.gen.generate()
            shown, blank = parse_shown(result["problem"])
            expected = reconstruct_flow(result)
            self.assertEqual(len(shown), len(expected), result["problem"])
            self.assertEqual(result["final_answer"], expected[blank],
                             result["problem"])
            for i, line in enumerate(shown):
                if i != blank:
                    self.assertEqual(line, expected[i], result["problem"])

    def test_check_arithmetic_consistent(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "NEED":
                    self.assertEqual(len(f), 3, s)  # pipe-free fields
                elif f[0] == "CHECK":
                    self.assertEqual(f[1], "arithmetic", s)
                    tail = f[2].rsplit("= ", 1)
                    if len(tail) == 2:
                        self.assertEqual(tail[1], f[3], s)

    def test_blank_positions_vary(self):
        positions = set()
        for _ in range(200):
            result = self.gen.generate()
            _, blank = parse_shown(result["problem"])
            positions.add((result["operation"], blank))
        self.assertGreaterEqual(len(positions), 7)

    def test_modes_reachable_and_fixed(self):
        seen = {self.gen.generate()["operation"] for _ in range(80)}
        self.assertEqual(seen, {"fill_in_step_equation", "fill_in_step_ratio",
                                "fill_in_step_tip"})
        with self.assertRaises(ValueError):
            FillInStepGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
