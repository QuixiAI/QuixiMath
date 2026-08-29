import random
import unittest

from generators.systems_substitution_generator import (
    MODIFIERS, SystemsSubstitutionGenerator,
)
from helpers import DELIM
from tests.linear_system_oracle import solve_system_problem, RENDER_WART_RE


class TestSystemsSubstitutionGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = SystemsSubstitutionGenerator()

    def test_generate_structure(self):
        for _ in range(20):
            problem = self.gen.generate()
            self.assertIn("problem_id", problem)
            self.assertIn("operation", problem)
            self.assertIn("problem", problem)
            self.assertIn("steps", problem)
            self.assertIn("final_answer", problem)
            self.assertTrue(problem['steps'][-1].startswith("Z|"))
            self.assertTrue(any("SYS_SETUP" in s for s in problem['steps']))

    def test_isolated_case(self):
        from unittest.mock import patch
        gen = SystemsSubstitutionGenerator(modifier="plain")
        with patch('random.choice', return_value='isolated'):
             problem = gen.generate()
             # Should involve substitution directly
             self.assertTrue(any("SYS_SUBST" in s for s in problem['steps']))

    def test_easy_isolate_case(self):
        from unittest.mock import patch
        gen = SystemsSubstitutionGenerator(modifier="plain")
        with patch('random.choice', return_value='easy_isolate'):
             problem = gen.generate()
             # Should have ISOLATE step
             self.assertTrue(any("SYS_ISOLATE" in s for s in problem['steps']))

    def test_oracle_solves_system_from_problem_text(self):
        # The system must be nonsingular and its unique solution must
        # match the final answer (solved independently via Cramer's rule)
        for _ in range(500):
            result = self.gen.generate()
            x_sol, y_sol = solve_system_problem(result["problem"])
            self.assertTrue(result["final_answer"].endswith(
                f"x={x_sol}, y={y_sol}"), result["problem"])

    def test_render_sanity(self):
        for _ in range(300):
            result = self.gen.generate()
            blob = result["problem"] + "\n" + "\n".join(result["steps"])
            self.assertNotRegex(blob, RENDER_WART_RE, result["problem"])

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(56)
        for modifier in MODIFIERS:
            result = SystemsSubstitutionGenerator(modifier).generate()
            codes = [raw.split(DELIM)[0] for raw in result["steps"]]
            self.assertEqual(result["operation"], f"systems_substitution_{modifier}")
            if modifier == "distractor":
                self.assertEqual(codes[0], "SELECT_RELEVANT")
            elif modifier == "estimate_first":
                self.assertEqual(codes[0], "ESTIMATE")
                self.assertEqual(codes[-2], "ESTIMATE_CHECK")
            elif modifier == "with_model":
                self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            SystemsSubstitutionGenerator(modifier="bogus")


if __name__ == '__main__':
    unittest.main()
