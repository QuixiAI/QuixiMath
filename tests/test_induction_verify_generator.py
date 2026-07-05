import random
import unittest

from generators.induction_verify_generator import InductionVerifyGenerator
from tests.new_generator_test_utils import GeneratorTestMixin, oracle_induction


class TestInductionVerifyGenerator(GeneratorTestMixin, unittest.TestCase):
    GEN = InductionVerifyGenerator
    ORACLE = staticmethod(oracle_induction)
    VARIANTS = InductionVerifyGenerator.VARIANTS
    OP_PREFIX = "induction_verify"

    def setUp(self):
        random.seed(42)
        super().setUp()


if __name__ == "__main__":
    unittest.main()
