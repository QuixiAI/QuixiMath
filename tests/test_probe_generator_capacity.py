import contextlib
import io
import json
import os
import tempfile
import unittest

from base_generator import ProblemGenerator
from helpers import jid
from generators.multi_digit_addition_generator import MultiDigitAdditionGenerator
from tools.probe_generator_capacity import main, probe_generators


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


if __name__ == "__main__":
    unittest.main()
