import contextlib
import io
import json
import os
import tempfile
import unittest

from base_generator import ProblemGenerator
from helpers import jid
from generators.multi_digit_addition_generator import MultiDigitAdditionGenerator
from tools.probe_generator_capacity import (estimate_capacity, fmt_capacity,
                                            main, probe_generators)


class TinyCapacityGenerator(ProblemGenerator):
    def __init__(self):
        self.i = 0

    def generate(self):
        self.i += 1
        value = self.i % 3
        return {
            "problem_id": jid(),
            "operation": "tiny_capacity",
            "problem": f"{value} + 0",
            "steps": [f"A|{value}|0|{value}", f"Z|{value}"],
            "final_answer": str(value),
        }


class TestProbeGeneratorCapacity(unittest.TestCase):
    def test_probe_flags_small_space(self):
        rows = probe_generators([TinyCapacityGenerator()], samples=20,
                                threshold=10, seed=1)
        self.assertEqual(rows[0]["distinct_problem_texts"], 3)
        self.assertTrue(rows[0]["below_threshold"])

    def test_probe_accepts_large_enough_sampled_space(self):
        rows = probe_generators([MultiDigitAdditionGenerator()], samples=50,
                                threshold=10, seed=1)
        self.assertGreaterEqual(rows[0]["distinct_problem_texts"], 10)
        self.assertFalse(rows[0]["below_threshold"])

    def test_cli_json_output_and_exit_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "capacity.json")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                status = main([
                    "--samples", "20",
                    "--threshold", "10",
                    "--generators", "MultiDigitAdditionGenerator",
                    "--json", path,
                ])
            self.assertEqual(status, 0)
            self.assertIn("MultiDigitAdditionGenerator", out.getvalue())
            with open(path, encoding="utf-8") as fh:
                rows = json.load(fh)
            self.assertEqual(rows[0]["generator"],
                             "MultiDigitAdditionGenerator")


class TestCapacityEstimate(unittest.TestCase):
    """The estimator inverts E[distinct] = N(1 - exp(-n/N)) for N."""

    def test_recovers_known_space_sizes(self):
        import random

        for true_size in (9, 1000, 100_000, 5_000_000):
            rng = random.Random(0)
            samples = 5000
            seen = {rng.randrange(true_size) for _ in range(samples)}
            estimate = estimate_capacity(samples, len(seen))
            if estimate is None:  # sample was fully distinct
                self.assertGreater(true_size, samples)
                continue
            # within a factor of 1.5 either way
            self.assertLess(estimate, true_size * 1.5, true_size)
            self.assertGreater(estimate, true_size / 1.5, true_size)

    def test_fully_distinct_sample_is_unmeasurable(self):
        self.assertIsNone(estimate_capacity(100, 100))
        self.assertEqual(fmt_capacity(None, 100), ">100*")

    def test_degenerate_inputs(self):
        self.assertEqual(estimate_capacity(0, 0), 0)
        self.assertEqual(estimate_capacity(100, 0), 0)

    def test_fmt_capacity_units(self):
        self.assertEqual(fmt_capacity(500, 5000), "500")
        self.assertEqual(fmt_capacity(12_300, 5000), "12.3k")
        self.assertEqual(fmt_capacity(4_500_000, 5000), "4.5M")
        self.assertEqual(fmt_capacity(2_000_000_000, 5000), "2.0B")

    def test_min_capacity_flags_a_small_space(self):
        rows = probe_generators([TinyCapacityGenerator()], samples=60,
                                threshold=1, seed=1, min_capacity=1000)
        self.assertTrue(rows[0]["below_threshold"])
        self.assertLess(rows[0]["estimated_capacity"], 1000)

    def test_min_capacity_absent_keeps_threshold_only(self):
        rows = probe_generators([TinyCapacityGenerator()], samples=60,
                                threshold=1, seed=1)
        self.assertFalse(rows[0]["below_threshold"])


if __name__ == "__main__":
    unittest.main()
