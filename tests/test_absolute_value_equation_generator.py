import unittest
from generators.absolute_value_equation_generator import AbsoluteValueEquationGenerator

class TestAbsoluteValueEquationGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = AbsoluteValueEquationGenerator()

    def test_generate_structure(self):
        for _ in range(20):
            problem = self.gen.generate()
            self.assertIn("problem_id", problem)
            self.assertIn("operation", problem)
            self.assertIn("problem", problem)
            self.assertIn("steps", problem)
            self.assertIn("final_answer", problem)
            self.assertTrue(len(problem['steps']) > 0)
            self.assertTrue(problem['steps'][-1].startswith("Z|"))

    def test_no_solution_logic(self):
        # Force a negative c scenario by monkeypatching or just running enough times?
        # Better to check if logic handles it when it appears.
        # Let's try to mock the random choice
        import random
        from unittest.mock import patch
        
        with patch('random.choices', return_value=['no_sol']):
            problem = self.gen.generate()
            self.assertEqual(problem['final_answer'], "No solution")
            self.assertTrue(any("ABS_CHECK" in s for s in problem['steps']))

    def test_one_solution_logic(self):
        from unittest.mock import patch
        with patch('random.choices', return_value=['one_sol']):
            problem = self.gen.generate()
            self.assertNotEqual(problem['final_answer'], "No solution")
            self.assertTrue(any("ABS_SPLIT|Single case" in s for s in problem['steps']))

    def test_two_solution_logic(self):
        from unittest.mock import patch
        with patch('random.choices', return_value=['two_sol']):
            problem = self.gen.generate()
            # A0: 'x = r1 or x = r2', roots ascending
            self.assertIn(" or ", problem['final_answer'])
            self.assertTrue(any("ABS_SPLIT|Two cases" in s for s in problem['steps']))
            self.assertTrue(any("ABS_CASE|Case 1" in s for s in problem['steps']))
            self.assertTrue(any("ABS_CASE|Case 2" in s for s in problem['steps']))

    def test_oracle_and_pipe_safety(self):
        """A9 oracle: both roots satisfy |ax+b| = c parsed from the problem;
        no step field carries a raw pipe; roots ascend."""
        import re
        from fractions import Fraction
        for _ in range(500):
            res = self.gen.generate()
            eq = res['problem'].replace('Solve: ', '')
            m = re.fullmatch(r'\|(.+)\| = (-?\d+)', eq)
            self.assertIsNotNone(m, eq)
            inner, c = m.group(1), int(m.group(2))
            im = re.fullmatch(r'(?:(\d+))?x(?: ([+-]) (\d+))?', inner)
            a = int(im.group(1)) if im.group(1) else 1
            b = (0 if im.group(2) is None
                 else int(im.group(3)) * (1 if im.group(2) == '+' else -1))
            answer = res['final_answer']
            for raw in res['steps'][:-1]:
                self.assertLessEqual(len(raw.split('|')) - 1, 4, raw)
            if c < 0:
                self.assertEqual(answer, 'No solution')
            else:
                roots = [Fraction(x) for x in re.findall(r'x = (-?\d+(?:/\d+)?)', answer)]
                self.assertEqual(len(roots), 1 if c == 0 else 2)
                self.assertEqual(roots, sorted(roots))
                for root in roots:
                    self.assertEqual(abs(a * root + b), c, answer)

if __name__ == '__main__':
    unittest.main()
