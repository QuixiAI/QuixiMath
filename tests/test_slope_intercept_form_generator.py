import unittest
import re
from generators.slope_intercept_form_generator import SlopeInterceptFormGenerator
from helpers import DELIM


def coefficient(text):
    if text == "":
        return 1
    if text == "-":
        return -1
    return int(text)


def oracle_answer(problem):
    equation = re.search(r"line: (y = .+)$", problem).group(1)
    rhs = equation.removeprefix("y = ")
    if "x" not in rhs:
        m, b = 0, int(rhs)
    else:
        match = re.fullmatch(r"(-?\d*)x ([+-]) (\d+)", rhs)
        if match:
            m = coefficient(match.group(1))
            b = int(match.group(3)) * (1 if match.group(2) == "+" else -1)
        else:
            match = re.fullmatch(r"(-?\d+) ([+-]) (\d*)x", rhs)
            if match:
                b = int(match.group(1))
                m = coefficient(match.group(3))
                if match.group(2) == "-":
                    m = -abs(m)
            else:
                match = re.fullmatch(r"(-?\d*)x", rhs)
                assert match, rhs
                m, b = coefficient(match.group(1)), 0
    return f"m={m}, b={b}"

class TestSlopeInterceptFormGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = SlopeInterceptFormGenerator()

    def test_generate_structure(self):
        for _ in range(20):
            problem = self.gen.generate()
            self.assertIn("problem_id", problem)
            self.assertIn("operation", problem)
            self.assertIn("problem", problem)
            self.assertIn("steps", problem)
            self.assertIn("final_answer", problem)
            self.assertTrue(problem['steps'][-1].startswith("Z|"))

    def test_horizontal_line(self):
        from unittest.mock import patch
        with patch('random.choice', return_value='horizontal'):
            problem = self.gen.generate()
            self.assertIn("m=0", problem['final_answer'])
            self.assertNotIn("x", problem['problem']) # y = b

    def test_no_b(self):
        from unittest.mock import patch
        with patch('random.choice', return_value='no_b'):
            problem = self.gen.generate()
            self.assertIn("b=0", problem['final_answer'])

    def test_oracle_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result["problem"]),
                             result["final_answer"], result["problem"])

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)

if __name__ == '__main__':
    unittest.main()
