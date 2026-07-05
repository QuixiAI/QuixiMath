import random
import unittest

from generators.two_sample_test_generator import TwoSampleTestGenerator
from tests.new_generator_test_utils import GeneratorTestMixin, oracle_two_sample


class TestTwoSampleTestGenerator(GeneratorTestMixin, unittest.TestCase):
    GEN = TwoSampleTestGenerator
    ORACLE = staticmethod(oracle_two_sample)
    VARIANTS = TwoSampleTestGenerator.VARIANTS
    OP_PREFIX = "two_sample_test"

    def setUp(self):
        random.seed(42)
        super().setUp()


if __name__ == "__main__":
    unittest.main()
