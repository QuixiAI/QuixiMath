import os
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from tools.gen_opcode_legend import (
    scan_opcodes, render_markdown, _generator_seed, _harvest_catalog_codes,
)
import ast


class TestGenOpcodeLegend(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.opcodes, cls.dynamic_sites = scan_opcodes()

    def test_universal_and_renamed_codes_present(self):
        for code in ("Z", "EQ_OP_NOTE", "PROB_DESCRIBE", "EQ_OP_BOTH", "PROB_SETUP"):
            self.assertIn(code, self.opcodes, f"Missing op-code {code}")

    def test_prob_setup_is_only_numeric_variant(self):
        # After the PROB_DESCRIBE rename, PROB_SETUP should remain only in
        # the structured favorable|total form of numeric probability flows.
        # New probability generators may legitimately use that same shape.
        self.assertEqual(self.opcodes["PROB_SETUP"].arities, {2})
        self.assertIn("simple_probability_generator.py",
                      self.opcodes["PROB_SETUP"].files)

    def test_ifexp_opcode_resolves_both_branches(self):
        # fraction_op_generator.py:42 uses step("A" if ... else "S", ...);
        # the scanner must record both branches.
        self.assertIn("fraction_op_generator.py", self.opcodes["A"].files)
        self.assertIn("fraction_op_generator.py", self.opcodes["S"].files)

    def test_no_dynamic_sites(self):
        self.assertEqual(self.dynamic_sites, [])

    def test_data_catalog_codes_resolved(self):
        # trig_identity_verify emits codes from a data catalog via a
        # loop variable; the scanner must harvest them (not warn), so
        # a catalog-only code like IDENT_MATCH is in the table.
        self.assertIn("IDENT_MATCH", self.opcodes)
        self.assertIn("trig_identity_verify_generator.py",
                      self.opcodes["IDENT_MATCH"].files)

    def test_harvest_infers_arity_from_tuple(self):
        tree = ast.parse(
            'X = [("FOO", "a", ""), ("BAR", "a", "b"), '
            '("lower", "x", "y")]'
        )
        found = _harvest_catalog_codes(tree)
        self.assertEqual(found["FOO"], {1})   # empty field omitted
        self.assertEqual(found["BAR"], {2})
        self.assertNotIn("lower", found)      # not an op-code token

    def test_generator_seed_is_stable_and_configuration_sensitive(self):
        class ExampleGenerator:
            def __init__(self, variant):
                self.variant = variant

        first = ExampleGenerator("a")
        same = ExampleGenerator("a")
        different = ExampleGenerator("b")
        self.assertEqual(_generator_seed(first, 0), _generator_seed(same, 0))
        self.assertNotEqual(_generator_seed(first, 0),
                            _generator_seed(different, 0))
        self.assertNotEqual(_generator_seed(first, 0),
                            _generator_seed(first, 1))

        wrapper_one = ExampleGenerator("wrapper")
        wrapper_one.children = [ExampleGenerator("a")]
        wrapper_two = ExampleGenerator("wrapper")
        wrapper_two.children = [ExampleGenerator("a")]
        self.assertEqual(_generator_seed(wrapper_one, 0),
                         _generator_seed(wrapper_two, 0))

    def test_z_used_by_all_step_emitting_generators(self):
        # Every generator module that emits steps ends with Z.
        self.assertGreater(len(self.opcodes["Z"].files), 70)

    def test_render_markdown(self):
        examples = {"Z": "Z|42"}
        md = render_markdown(self.opcodes, examples, self.dynamic_sites)
        self.assertIn("| Code | Payload fields | Example | Used by |", md)
        self.assertIn("`Z`", md)
        self.assertIn("Z\\|42", md)  # pipes escaped inside table cells
        self.assertIn("not observed in sampling", md)  # codes without examples
        self.assertNotIn("Warnings", md)  # no dynamic sites today


if __name__ == "__main__":
    unittest.main()
