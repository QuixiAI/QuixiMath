import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.lr_schedule_generator import LRScheduleGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Evaluate a learning-rate schedule with base_lr=([-0-9/]+), "
    r"min_lr=([-0-9/]+), warmup_steps=([0-9]+), total_steps=([0-9]+), "
    r"at step t=([0-9]+)\. Use linear warmup, then cosine decay "
    r"lr=min\+1/2\*\(base-min\)\*\(1\+cos\(pi\*progress\)\)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_flow(example):
    match = PROBLEM_RE.fullmatch(example["problem"])
    if not match:
        raise AssertionError(example["problem"])
    base_lr = Fraction(match.group(1))
    min_lr = Fraction(match.group(2))
    warmup = int(match.group(3))
    total = int(match.group(4))
    t = int(match.group(5))
    steps = [
        make_step("LR_SETUP", f"base={fraction_text(base_lr)}",
                  f"min={fraction_text(min_lr)}",
                  f"warmup={warmup},total={total},t={t}"),
    ]
    if t <= warmup:
        phase = "warmup"
        ratio = Fraction(t, warmup)
        lr = base_lr * ratio
        steps.extend([
            make_step("D", t, warmup, fraction_text(ratio)),
            make_step("M", fraction_text(base_lr), fraction_text(ratio),
                      fraction_text(lr)),
            make_step("LR_PHASE", "warmup"),
        ])
    else:
        phase = "decay"
        elapsed = t - warmup
        decay_span = total - warmup
        progress = Fraction(elapsed, decay_span)
        cos_value = Fraction(0) if progress == Fraction(1, 2) else Fraction(-1)
        diff = base_lr - min_lr
        one_plus = 1 + cos_value
        product = diff * one_plus
        half = product / 2
        lr = min_lr + half
        steps.extend([
            make_step("S", t, warmup, elapsed),
            make_step("S", total, warmup, decay_span),
            make_step("D", elapsed, decay_span, fraction_text(progress)),
            make_step("COSINE", f"pi*{fraction_text(progress)}",
                      fraction_text(cos_value)),
            make_step("S", fraction_text(base_lr), fraction_text(min_lr),
                      fraction_text(diff)),
            make_step("A", 1, fraction_text(cos_value),
                      fraction_text(one_plus)),
            make_step("M", fraction_text(diff), fraction_text(one_plus),
                      fraction_text(product)),
            make_step("D", fraction_text(product), 2, fraction_text(half)),
            make_step("A", fraction_text(min_lr), fraction_text(half),
                      fraction_text(lr)),
            make_step("LR_PHASE", "decay"),
        ])
    steps.append(make_step("LR_VALUE", fraction_text(lr)))
    answer = f"phase={phase}; lr={fraction_text(lr)}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestLRScheduleGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = LRScheduleGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "lr_schedule_warmup_cosine")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
