import random
import unittest

from generators.telescoping_generator import TelescopingGenerator
from tests.new_generator_test_utils import GeneratorTestMixin, oracle_telescoping


class TestTelescopingGenerator(GeneratorTestMixin, unittest.TestCase):
    GEN = TelescopingGenerator
    ORACLE = staticmethod(oracle_telescoping)
    VARIANTS = TelescopingGenerator.VARIANTS
    OP_PREFIX = "telescoping"

    def setUp(self):
        random.seed(42)
        super().setUp()


if __name__ == "__main__":
    unittest.main()
