import unittest
import random
import sys
import os

# Ensure repo root on path
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.geometry_area_perimeter_generator import GeometryAreaPerimeterGenerator
from helpers import DELIM


class TestGeometryAreaPerimeterGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.gen = GeometryAreaPerimeterGenerator()

    def test_format_and_z(self):
        res = self.gen.generate()
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertIn("Perimeter=", res["final_answer"])
        self.assertIn("Area=", res["final_answer"])

    def test_rectangle_case(self):
        # Force rectangle for deterministic check
        import unittest.mock as mock

        with mock.patch(
            "generators.geometry_area_perimeter_generator.random.choice",
            return_value="rectangle",
        ), mock.patch(
            "generators.geometry_area_perimeter_generator.random.randint",
            side_effect=[4, 5],  # width, height
        ):
            res = self.gen.generate()
        perim = 2 * (4 + 5)
        area = 4 * 5
        self.assertEqual(res["final_answer"], f"Perimeter={perim}, Area={area}")


    def test_oracle_geometric_consistency(self):
        """A9 oracle: recompute perimeter/area from the problem text and
        verify the stated figure actually exists (Heron height check,
        parallelogram height < side, trapezoid leg triple)."""
        import math
        import re
        gen = GeometryAreaPerimeterGenerator()
        for _ in range(500):
            res = gen.generate()
            p = res["problem"]
            parts = dict(kv.split("=") for kv in res["final_answer"].split(", "))
            perim, area = float(parts["Perimeter"]), float(parts["Area"])
            nums = list(map(int, re.findall(r"\d+", p)))
            if res["operation"] == "geometry_rectangle":
                w, h = nums
                self.assertEqual(perim, 2 * (w + h))
                self.assertEqual(area, w * h)
            elif res["operation"] == "geometry_triangle":
                b, s2, s3, hh, _ = nums
                self.assertEqual(perim, b + s2 + s3)
                self.assertEqual(area, b * hh / 2)
                s = (b + s2 + s3) / 2
                heron = math.sqrt(s * (s - b) * (s - s2) * (s - s3))
                self.assertAlmostEqual(heron, area, places=6, msg=p)
            elif res["operation"] == "geometry_parallelogram":
                b, sd, hh = nums
                self.assertEqual(perim, 2 * (b + sd))
                self.assertEqual(area, b * hh)
                self.assertLess(hh, sd, p)
            else:
                b1, b2, leg, hh = nums
                self.assertEqual(perim, b1 + b2 + 2 * leg)
                self.assertEqual(area, (b1 + b2) / 2 * hh)
                off = (b1 - b2) / 2
                self.assertEqual(leg ** 2, hh ** 2 + off ** 2, p)


if __name__ == "__main__":
    unittest.main()
