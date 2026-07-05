import random
import unittest

from generators.counting_classics_generator import CountingClassicsGenerator
from tests.new_generator_test_utils import GeneratorTestMixin, oracle_counting


class TestCountingClassicsGenerator(GeneratorTestMixin, unittest.TestCase):
    GEN = CountingClassicsGenerator
    ORACLE = staticmethod(oracle_counting)
    VARIANTS = CountingClassicsGenerator.VARIANTS
    OP_PREFIX = "counting_classics"

    def setUp(self):
        random.seed(42)
        super().setUp()


if __name__ == "__main__":
    unittest.main()
