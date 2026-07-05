import random
import unittest

from generators.qr_decomposition_generator import QRDecompositionGenerator
from tests.new_generator_test_utils import GeneratorTestMixin, verify_qr


class TestQRDecompositionGenerator(GeneratorTestMixin, unittest.TestCase):
    GEN = QRDecompositionGenerator
    ORACLE = staticmethod(verify_qr)
    VARIANTS = QRDecompositionGenerator.VARIANTS
    OP_PREFIX = "qr_decomposition"
    CHECK_BOOLEAN = True

    def setUp(self):
        random.seed(42)
        super().setUp()


if __name__ == "__main__":
    unittest.main()
