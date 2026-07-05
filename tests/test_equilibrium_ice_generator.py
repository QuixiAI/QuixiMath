import random
import unittest

from generators.equilibrium_ice_generator import EquilibriumICEGenerator
from tests.new_generator_test_utils import GeneratorTestMixin, oracle_ice


class TestEquilibriumICEGenerator(GeneratorTestMixin, unittest.TestCase):
    GEN = EquilibriumICEGenerator
    ORACLE = staticmethod(oracle_ice)
    VARIANTS = EquilibriumICEGenerator.VARIANTS
    OP_PREFIX = "equilibrium_ice"

    def setUp(self):
        random.seed(42)
        super().setUp()


if __name__ == "__main__":
    unittest.main()
