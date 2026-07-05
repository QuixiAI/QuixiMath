import random
import unittest

from generators.separable_pde_generator import SeparablePDEGenerator
from tests.new_generator_test_utils import GeneratorTestMixin, oracle_pde


class TestSeparablePDEGenerator(GeneratorTestMixin, unittest.TestCase):
    GEN = SeparablePDEGenerator
    ORACLE = staticmethod(oracle_pde)
    VARIANTS = SeparablePDEGenerator.VARIANTS
    OP_PREFIX = "separable_pde"

    def setUp(self):
        random.seed(42)
        super().setUp()


if __name__ == "__main__":
    unittest.main()
