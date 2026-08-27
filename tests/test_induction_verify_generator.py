import random
import re
import unittest

from generators.induction_verify_generator import InductionVerifyGenerator
from helpers import DELIM
from tests.new_generator_test_utils import GeneratorTestMixin, oracle_induction


class TestInductionVerifyGenerator(GeneratorTestMixin, unittest.TestCase):
    GEN = InductionVerifyGenerator
    ORACLE = staticmethod(oracle_induction)
    VARIANTS = InductionVerifyGenerator.VARIANTS
    OP_PREFIX = "induction_verify"

    def setUp(self):
        random.seed(42)
        super().setUp()

    def test_all_variants_reachable(self):
        observed = {InductionVerifyGenerator(variant).generate()["operation"]
                    for variant in self.VARIANTS}
        expected = {f"induction_verify_{variant}" for variant in self.VARIANTS}
        self.assertEqual(observed, expected)

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = InductionVerifyGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"], oracle_induction(example),
                             example["problem"])

    def test_strong_induction_bases_step_and_witness(self):
        generator = InductionVerifyGenerator("strong_induction")
        for _ in range(200):
            example = generator.generate()
            steps = [item.split(DELIM) for item in example["steps"]]
            bases = [item for item in steps if item[0] == "INDUCT_BASE"]
            self.assertEqual([item[1] for item in bases],
                             ["n=12", "n=13", "n=14", "n=15"])
            witness = next(item for item in steps if item[0] == "WITNESS")
            number = int(witness[1].split("=")[1])
            first = int(witness[2].split("=")[1])
            second = int(witness[3].split("=")[1])
            self.assertEqual(4 * first + 5 * second, number)
            self.assertEqual(second, next(
                value for value in range(number // 5 + 1)
                if (number - 5 * value) % 4 == 0))

    def test_well_ordering_division_check(self):
        generator = InductionVerifyGenerator("well_ordering")
        for _ in range(200):
            example = generator.generate()
            divmod_step = next(item.split(DELIM) for item in example["steps"]
                               if item.startswith(f"DIVMOD{DELIM}"))
            quotient, remainder = map(int, re.fullmatch(
                r"(\d+) R (\d+)", divmod_step[3]).groups())
            number, divisor = int(divmod_step[1]), int(divmod_step[2])
            self.assertEqual(number, divisor * quotient + remainder)
            self.assertLess(remainder, divisor)


if __name__ == "__main__":
    unittest.main()
