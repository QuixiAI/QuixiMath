import re
import unittest
from fractions import Fraction

from generators.systems_elimination_generator import SystemsEliminationGenerator
from tests.linear_system_oracle import solve_system_problem, RENDER_WART_RE


class TestSystemsEliminationGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = SystemsEliminationGenerator()

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

    def test_oracle_solves_system_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            x_sol, y_sol = solve_system_problem(result["problem"])
            self.assertEqual(result["final_answer"],
                             f"x={x_sol}, y={y_sol}", result["problem"])

    def test_check_step_arithmetic(self):
        # CHECK|substitute|<work> = <value>|<expected>: the two sides agree
        for _ in range(300):
            result = self.gen.generate()
            for raw in result["steps"]:
                if not raw.startswith("CHECK|"):
                    continue
                fields = raw.split("|")
                work, expected = fields[2], fields[3]
                self.assertEqual(work.rsplit("= ", 1)[1], expected, raw)

    def test_render_sanity(self):
        for _ in range(300):
            result = self.gen.generate()
            blob = result["problem"] + "\n" + "\n".join(result["steps"])
            self.assertNotRegex(blob, RENDER_WART_RE, result["problem"])


if __name__ == '__main__':
    unittest.main()
