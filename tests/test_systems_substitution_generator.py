import unittest
from generators.systems_substitution_generator import SystemsSubstitutionGenerator
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
        with patch('random.choice', return_value='isolated'):
             problem = self.gen.generate()
             # Should involve substitution directly
             self.assertTrue(any("SYS_SUBST" in s for s in problem['steps']))

    def test_easy_isolate_case(self):
        from unittest.mock import patch
        with patch('random.choice', return_value='easy_isolate'):
             problem = self.gen.generate()
             # Should have ISOLATE step
             self.assertTrue(any("SYS_ISOLATE" in s for s in problem['steps']))

    def test_oracle_solves_system_from_problem_text(self):
        # The system must be nonsingular and its unique solution must
        # match the final answer (solved independently via Cramer's rule)
        for _ in range(500):
            result = self.gen.generate()
            x_sol, y_sol = solve_system_problem(result["problem"])
            self.assertEqual(result["final_answer"],
                             f"x={x_sol}, y={y_sol}", result["problem"])

    def test_render_sanity(self):
        for _ in range(300):
            result = self.gen.generate()
            blob = result["problem"] + "\n" + "\n".join(result["steps"])
            self.assertNotRegex(blob, RENDER_WART_RE, result["problem"])


if __name__ == '__main__':
    unittest.main()
