import random
import unittest

from generators.master_theorem_generator import MasterTheoremGenerator
from tests.new_generator_test_utils import GeneratorTestMixin, oracle_master


class TestMasterTheoremGenerator(GeneratorTestMixin, unittest.TestCase):
    GEN = MasterTheoremGenerator
    ORACLE = staticmethod(oracle_master)
    VARIANTS = MasterTheoremGenerator.VARIANTS
    OP_PREFIX = "master_theorem"

    def setUp(self):
        random.seed(42)
        super().setUp()


if __name__ == "__main__":
    unittest.main()
