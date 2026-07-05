import random
import unittest

from generators.polynomial_inequality_generator import PolynomialInequalityGenerator
from tests.new_generator_test_utils import GeneratorTestMixin, oracle_polynomial_inequality


class TestPolynomialInequalityGenerator(GeneratorTestMixin, unittest.TestCase):
    GEN = PolynomialInequalityGenerator
    ORACLE = staticmethod(oracle_polynomial_inequality)
    VARIANTS = PolynomialInequalityGenerator.VARIANTS
    OP_PREFIX = "polynomial_inequality"

    def setUp(self):
        random.seed(42)
        super().setUp()


if __name__ == "__main__":
    unittest.main()
