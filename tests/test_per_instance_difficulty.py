import os
import random
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from curriculum import clamp_difficulty, stamp_metadata
from generators.multi_digit_addition_generator import (
    MultiDigitAdditionGenerator,
)
from generators.multi_digit_subtraction_generator import (
    MultiDigitSubtractionGenerator,
)
from generators.multi_digit_multiplication_generator import (
    MultiDigitMultiplicationGenerator,
)
from generators.long_division_generator import LongDivisionGenerator


def carries(a, b):
    count = c = 0
    while a or b:
        c = (a % 10 + b % 10 + c) // 10
        count += c
        a //= 10
        b //= 10
    return count


def borrows(a, b):
    count = c = 0
    while b or c:
        if a % 10 - c < b % 10:
            count += 1
            c = 1
        else:
            c = 0
        a //= 10
        b //= 10
    return count


class TestPerInstanceDifficulty(unittest.TestCase):
    def setUp(self):
        random.seed(42)

    def test_clamp(self):
        self.assertEqual(clamp_difficulty(0), 1)
        self.assertEqual(clamp_difficulty(3), 3)
        self.assertEqual(clamp_difficulty(9), 5)

    def test_addition_matches_operands(self):
        gen = MultiDigitAdditionGenerator()
        for _ in range(300):
            r = gen.generate()
            a, b = (int(v) for v in r["problem"].split(" + "))
            width = max(len(str(a)), len(str(b)))
            want = clamp_difficulty(1 + (width >= 4) + (width >= 5) +
                                    (carries(a, b) >= 3))
            self.assertEqual(r["difficulty"], want, r["problem"])

    def test_subtraction_matches_operands(self):
        gen = MultiDigitSubtractionGenerator()
        for _ in range(300):
            r = gen.generate()
            a, b = (int(v) for v in r["problem"].split(" - "))
            width = max(len(str(a)), len(str(b)))
            want = clamp_difficulty(1 + (width >= 4) + (width >= 5) +
                                    (borrows(a, b) >= 3))
            self.assertEqual(r["difficulty"], want, r["problem"])

    def test_multiplication_matches_operands(self):
        gen = MultiDigitMultiplicationGenerator()
        for _ in range(300):
            r = gen.generate()
            a, b = (int(v) for v in r["problem"].split(" * "))
            load = len(str(a)) + len(str(b))
            want = clamp_difficulty(1 + (load >= 5) + (load >= 7) +
                                    (load >= 9))
            self.assertEqual(r["difficulty"], want, r["problem"])

    def test_long_division_matches_operands(self):
        gen = LongDivisionGenerator()
        for _ in range(300):
            r = gen.generate()
            a, b = (int(v) for v in r["problem"].split(" / "))
            want = clamp_difficulty(1 + (a >= 100) + (a >= 1000) +
                                    (b >= 10))
            self.assertEqual(r["difficulty"], want, r["problem"])

    def test_emitted_difficulty_survives_stamping(self):
        gen = MultiDigitAdditionGenerator()
        for _ in range(50):
            r = gen.generate()
            emitted = r["difficulty"]
            stamped = stamp_metadata(r, gen)
            self.assertEqual(stamped["difficulty"], emitted)
            self.assertEqual(stamped["grade_level"], "elementary")

    def test_difficulty_actually_varies(self):
        # Add/sub/div span several tiers via their size and
        # carry/borrow thresholds. Multiplication operands are almost
        # always 5-digit (randint(10, 99999) skews high), so its
        # faithful difficulty sits at the top tier and only dips when
        # a rare small factor is drawn — 2 distinct values is honest,
        # not a broken constant.
        expected = [
            (MultiDigitAdditionGenerator(), 3),
            (MultiDigitSubtractionGenerator(), 3),
            (MultiDigitMultiplicationGenerator(), 2),
            (LongDivisionGenerator(), 3),
        ]
        for gen, want in expected:
            seen = {gen.generate()["difficulty"] for _ in range(500)}
            self.assertGreaterEqual(len(seen), want,
                                    type(gen).__name__)

    def test_estimate_variants_keep_static_metadata(self):
        for gen, want in ((MultiDigitMultiplicationGenerator(True), 3),
                          (LongDivisionGenerator(True), 3)):
            for _ in range(20):
                r = gen.generate()
                self.assertEqual(r["difficulty"], want)
                self.assertEqual(r["grade_level"], "middle")


if __name__ == "__main__":
    unittest.main()
