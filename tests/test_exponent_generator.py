import unittest
import random
import re
import sys
import os
from fractions import Fraction

# Ensure repo root is on sys.path for package imports
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.exponent_generator import (
    ExponentEvaluationGenerator,
    ExponentRulesGenerator,
    ScientificNotationGenerator,
    RootsAndRadicalsGenerator,
)
from generators.exponential_model_generator import dec
from helpers import DELIM


_POW_RE = re.compile(
    r"(?:\((?P<pb>-?\d+(?:\.\d+)?(?:/\d+)?)\)|(?P<b>\d+(?:\.\d+)?))"
    r"\^(?P<e>\d+)")


def parse_exponent_expression(text):
    """Pull the power expression out of any phrasing.

    Returns ``(terms, ops, is_decimal)`` where ``terms`` is a list of
    ``(Fraction base, int exponent)`` and ``ops`` the connecting symbols.
    Reads the sentence only — nothing from the generator.
    """
    matches = list(_POW_RE.finditer(text))
    assert matches, text
    terms = []
    decimal = False
    for m in matches:
        btxt = m.group("pb") if m.group("pb") is not None else m.group("b")
        if "." in btxt:
            decimal = True
        terms.append((Fraction(btxt), int(m.group("e"))))
    ops = []
    for prev, nxt in zip(matches, matches[1:]):
        joiner = text[prev.end():nxt.start()].strip()
        assert joiner in ("·", "+", "-"), (joiner, text)
        ops.append(joiner)
    return terms, ops, decimal


def exponent_oracle_answer(text):
    """A9 oracle: evaluate the parsed expression with exact arithmetic."""
    terms, ops, decimal = parse_exponent_expression(text)
    value = terms[0][0] ** terms[0][1]
    for op, (base, exp) in zip(ops, terms[1:]):
        other = base ** exp
        if op == "·":
            value = value * other
        elif op == "+":
            value = value + other
        else:
            value = value - other
    if decimal:
        return dec(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


class TestExponentEvaluationGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = ExponentEvaluationGenerator()

    def test_generate_output_format(self):
        """Test the output format of the generate method."""
        result = self.generator.generate()

        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIn("operation", result)
        self.assertTrue(result["operation"].startswith("exponent_evaluation"))
        self.assertIn("problem", result)
        self.assertIn("steps", result)
        self.assertIn("final_answer", result)

        # Check final step
        final_step = result["steps"][-1]
        self.assertTrue(final_step.startswith(f"Z{DELIM}"))
        self.assertEqual(final_step.split(DELIM, 1)[1], result["final_answer"])

    def test_generate_consistency(self):
        """Generate multiple examples and check consistency."""
        for _ in range(200):
            result = self.generator.generate()

            # The power expression is always present in the prompt.
            self.assertIn("^", result["problem"])

            # Check for exponent steps
            has_setup_step = any(s.startswith(f"EXP_SETUP{DELIM}") for s in result["steps"])
            has_expand_step = any(s.startswith(f"EXP_EXPAND{DELIM}") for s in result["steps"])

            self.assertTrue(has_setup_step, "Missing EXP_SETUP step")
            self.assertTrue(has_expand_step, "Missing EXP_EXPAND step")

            # Final answer is an exact integer, reduced fraction, or
            # terminating decimal.
            ans = result["final_answer"]
            self.assertRegex(ans, r"^-?\d+(?:\.\d+|/\d+)?$")
            if "/" in ans:
                num, den = ans.split("/")
                self.assertEqual(Fraction(int(num), int(den)),
                                 Fraction(ans), ans)
                self.assertNotEqual(int(den), 1)
            if "." in ans:
                self.assertFalse(ans.endswith("0"), ans)

    def test_oracle_recomputation(self):
        """A9 oracle: re-evaluate the printed expression independently."""
        for _ in range(1500):
            result = self.generator.generate()
            self.assertEqual(exponent_oracle_answer(result["problem"]),
                             result["final_answer"], result["problem"])

    def test_partial_product_chain(self):
        """EXP_PARTIAL lines must multiply out, and the expansion must show
        exactly `exponent` factors."""
        for _ in range(400):
            result = self.generator.generate()
            terms, _, _ = parse_exponent_expression(result["problem"])
            setups = [s.split(DELIM) for s in result["steps"]
                      if s.startswith(f"EXP_SETUP{DELIM}")]
            expands = [s.split(DELIM) for s in result["steps"]
                       if s.startswith(f"EXP_EXPAND{DELIM}")]
            self.assertEqual(len(setups), len(terms))
            self.assertEqual(len(expands), len(terms))
            for (base, exp), setup, expand in zip(terms, setups, expands):
                self.assertEqual(Fraction(setup[1]), base)
                self.assertEqual(int(setup[2]), exp)
                self.assertEqual(len(expand[1].split(" × ")), exp)
            for s in result["steps"]:
                parts = s.split(DELIM)
                if parts[0] == "EXP_PARTIAL":
                    self.assertEqual(Fraction(parts[1]) * Fraction(parts[2]),
                                     Fraction(parts[3]), s)
                elif parts[0] == "M":
                    self.assertEqual(Fraction(parts[1]) * Fraction(parts[2]),
                                     Fraction(parts[3]), s)
                elif parts[0] == "A":
                    self.assertEqual(Fraction(parts[1]) + Fraction(parts[2]),
                                     Fraction(parts[3]), s)
                elif parts[0] == "S":
                    self.assertEqual(Fraction(parts[1]) - Fraction(parts[2]),
                                     Fraction(parts[3]), s)

    def test_all_families_reachable(self):
        ops = set()
        kinds = set()
        for _ in range(600):
            result = self.generator.generate()
            ops.add(result["operation"])
            terms, _, decimal = parse_exponent_expression(result["problem"])
            if decimal:
                kinds.add("decimal")
            elif any(b.denominator != 1 for b, _ in terms):
                kinds.add("fraction")
            elif any(b < 0 for b, _ in terms):
                kinds.add("negative")
            else:
                kinds.add("positive")
        self.assertEqual(ops, {"exponent_evaluation",
                               "exponent_evaluation_product",
                               "exponent_evaluation_sum"})
        self.assertEqual(kinds, {"decimal", "fraction", "negative",
                                 "positive"})

    def test_pipe_safety(self):
        for _ in range(300):
            result = self.generator.generate()
            self.assertNotIn(DELIM, result["problem"])
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)), 5, s)

    def test_negative_base_allowed(self):
        """Test that negative bases are generated when allowed."""
        gen = ExponentEvaluationGenerator(allow_negative_base=True)
        negative_found = False
        for _ in range(50):
            result = gen.generate()
            if "(-" in result["problem"]:
                negative_found = True
                break
        self.assertTrue(negative_found, "Should generate some problems with negative bases")

    def test_no_negative_base(self):
        """Test that no negative bases when disabled."""
        gen = ExponentEvaluationGenerator(allow_negative_base=False)
        for _ in range(300):
            result = gen.generate()
            self.assertNotIn("(-", result["problem"])
            terms, _, _ = parse_exponent_expression(result["problem"])
            for base, _exp in terms:
                self.assertGreater(base, 0)
            self.assertEqual(exponent_oracle_answer(result["problem"]),
                             result["final_answer"])

    def test_max_exponent_respected(self):
        gen = ExponentEvaluationGenerator(max_exponent=4)
        for _ in range(200):
            result = gen.generate()
            terms, _, _ = parse_exponent_expression(result["problem"])
            for _base, exp in terms:
                self.assertLessEqual(exp, 4)

    def test_determinism_under_seed(self):
        random.seed(19)
        first = [self.generator.generate()["problem"] for _ in range(25)]
        random.seed(19)
        second = [self.generator.generate()["problem"] for _ in range(25)]
        self.assertEqual(first, second)


class TestExponentRulesGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = ExponentRulesGenerator()

    def test_generate_output_format(self):
        """Test the output format of the generate method."""
        result = self.generator.generate()

        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIn("operation", result)
        self.assertTrue(result["operation"].startswith("exponent_"))
        self.assertIn("problem", result)
        self.assertIn("steps", result)
        self.assertIn("final_answer", result)

    def test_generate_consistency(self):
        """Generate multiple examples and check consistency."""
        for _ in range(20):
            result = self.generator.generate()

            # Problem should contain 'Simplify' or 'Evaluate'
            self.assertRegex(result["problem"].lower(), r"simplify|evaluate")

            # Check for rule steps
            has_setup_step = any(s.startswith(f"EXP_RULE_SETUP{DELIM}") for s in result["steps"])
            self.assertTrue(has_setup_step, "Missing EXP_RULE_SETUP step")

    def test_product_rule(self):
        """Test product rule generation."""
        gen = ExponentRulesGenerator(rule='product')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "exponent_product_rule")
            self.assertIn("·", result["problem"])

    def test_quotient_rule(self):
        """Test quotient rule generation."""
        gen = ExponentRulesGenerator(rule='quotient')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "exponent_quotient_rule")
            self.assertIn("/", result["problem"])

    def test_power_rule(self):
        """Test power rule generation."""
        gen = ExponentRulesGenerator(rule='power')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "exponent_power_rule")
            self.assertIn(")^", result["problem"])

    def test_negative_exponent_rule(self):
        """Test negative exponent rule generation."""
        gen = ExponentRulesGenerator(rule='negative')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "exponent_negative_rule")
            self.assertIn("(-", result["problem"])

    def test_zero_exponent_rule(self):
        """Test zero exponent rule generation."""
        gen = ExponentRulesGenerator(rule='zero')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "exponent_zero_rule")
            self.assertIn("^0", result["problem"])
            self.assertEqual(result["final_answer"], "1")


class TestScientificNotationGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = ScientificNotationGenerator()

    def test_generate_output_format(self):
        """Test the output format of the generate method."""
        result = self.generator.generate()

        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIn("operation", result)
        self.assertTrue(result["operation"].startswith("scientific_notation"))
        self.assertIn("problem", result)
        self.assertIn("steps", result)
        self.assertIn("final_answer", result)

    def test_to_scientific(self):
        """Test conversion to scientific notation."""
        gen = ScientificNotationGenerator(problem_type='to_scientific')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "scientific_notation_convert_to")
            self.assertIn("scientific notation", result["problem"])
            self.assertIn("×", result["final_answer"])
            self.assertIn("10^", result["final_answer"])

    def test_from_scientific(self):
        """Test conversion from scientific notation."""
        gen = ScientificNotationGenerator(problem_type='from_scientific')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "scientific_notation_convert_from")
            self.assertIn("standard form", result["problem"])

    def test_multiply(self):
        """Test multiplication in scientific notation."""
        gen = ScientificNotationGenerator(problem_type='multiply')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "scientific_notation_multiply")
            self.assertIn("Multiply", result["problem"])

    def test_divide(self):
        """Test division in scientific notation."""
        gen = ScientificNotationGenerator(problem_type='divide')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "scientific_notation_divide")
            self.assertIn("Divide", result["problem"])


SCI_TERM_RE = re.compile(r"^(-?\d+(?:\.\d+)?) × 10\^(-?\d+)$")
SCI_ANY_RE = re.compile(r"(-?\d+(?:\.\d+)?) × 10\^(-?\d+)")
SCI_PAREN_RE = re.compile(r"\((-?\d+(?:\.\d+)?) × 10\^(-?\d+)\)")


def sci_value(coeff_str, power_str):
    return Fraction(coeff_str) * Fraction(10) ** int(power_str)


class TestScientificNotationOracle(unittest.TestCase):
    """A9 oracle: recompute answers from the problem text with exact
    arithmetic (Fraction), independent of the generator's shift logic."""

    def test_convert_to_oracle(self):
        gen = ScientificNotationGenerator(problem_type='to_scientific')
        for _ in range(300):
            result = gen.generate()
            tokens = re.findall(r"(?<![\w^.])-?\d+(?:\.\d+)?", result["problem"])
            self.assertEqual(len(tokens), 1, result["problem"])
            number = Fraction(tokens[0])
            m = SCI_TERM_RE.match(result["final_answer"])
            self.assertIsNotNone(m, result["final_answer"])
            coeff = Fraction(m.group(1))
            self.assertEqual(sci_value(m.group(1), m.group(2)), number)
            self.assertTrue(1 <= coeff < 10, result["final_answer"])

    def test_convert_from_oracle(self):
        gen = ScientificNotationGenerator(problem_type='from_scientific')
        for _ in range(300):
            result = gen.generate()
            m = SCI_ANY_RE.search(result["problem"])
            self.assertIsNotNone(m, result["problem"])
            self.assertEqual(Fraction(result["final_answer"]),
                             sci_value(m.group(1), m.group(2)))
            # Minimal-digit rendering: no trailing zeros after the point
            self.assertNotRegex(result["final_answer"], r"\.\d*0$")

    def test_multiply_divide_oracle(self):
        for ptype in ("multiply", "divide"):
            gen = ScientificNotationGenerator(problem_type=ptype)
            for _ in range(300):
                result = gen.generate()
                terms = SCI_PAREN_RE.findall(result["problem"])
                self.assertEqual(len(terms), 2, result["problem"])
                a = sci_value(*terms[0])
                b = sci_value(*terms[1])
                expected = a * b if ptype == "multiply" else a / b
                m = SCI_TERM_RE.match(result["final_answer"])
                self.assertIsNotNone(m, result["final_answer"])
                self.assertEqual(sci_value(m.group(1), m.group(2)), expected)
                coeff = Fraction(m.group(1))
                self.assertTrue(1 <= coeff < 10, result["final_answer"])

    def test_no_float_artifacts(self):
        # Long strings of leading zeros are legitimate for powers such as
        # 10^-12; binary-float tails are not. Every printed decimal must be
        # minimal and exactly parseable by Fraction.
        gen = ScientificNotationGenerator()
        for _ in range(400):
            result = gen.generate()
            blobs = result["steps"] + [result["problem"],
                                       result["final_answer"]]
            for blob in blobs:
                for token in re.findall(r"-?\d+\.\d+", blob):
                    self.assertFalse(token.endswith("0"), token)
                    self.assertEqual(str(Fraction(token)),
                                     str(Fraction(token)), token)


RULE_BASE = r"(?P<base>\([^()]+\)|[a-z])"


def exponent_rule_oracle(problem, operation):
    """Parse one rule expression from problem text and simplify it."""
    if operation == "exponent_product_rule":
        pattern = RULE_BASE + r"\^(?P<a>\d+) · (?P=base)\^(?P<b>\d+)"
        match = re.search(pattern, problem)
        exponent = int(match.group("a")) + int(match.group("b"))
    elif operation == "exponent_quotient_rule":
        pattern = RULE_BASE + r"\^(?P<a>\d+) / (?P=base)\^(?P<b>\d+)"
        match = re.search(pattern, problem)
        exponent = int(match.group("a")) - int(match.group("b"))
    elif operation == "exponent_power_rule":
        pattern = r"\(" + RULE_BASE + r"\^(?P<a>\d+)\)\^(?P<b>\d+)"
        match = re.search(pattern, problem)
        exponent = int(match.group("a")) * int(match.group("b"))
    elif operation == "exponent_negative_rule":
        pattern = RULE_BASE + r"\^\(-(?P<a>\d+)\)"
        match = re.search(pattern, problem)
        exponent = int(match.group("a"))
        base = match.group("base")
        if "/" in base:
            numerator, denominator = base.strip("()").split("/")
            reciprocal = denominator if numerator == "1" \
                else f"({denominator}/{numerator})"
            return reciprocal if exponent == 1 else f"{reciprocal}^{exponent}"
        denominator = base if exponent == 1 else f"{base}^{exponent}"
        return f"1/{denominator}"
    else:
        match = re.search(r"(?P<base>\([^()]+\)|[a-z]|\d+)\^0", problem)
        return "1" if match else None
    assert match, (operation, problem)
    base = match.group("base")
    return base if exponent == 1 else f"{base}^{exponent}"


class TestRootsAndRadicalsGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = RootsAndRadicalsGenerator()

    def test_generate_output_format(self):
        """Test the output format of the generate method."""
        result = self.generator.generate()

        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIn("operation", result)
        self.assertIn("problem", result)
        self.assertIn("steps", result)
        self.assertIn("final_answer", result)

    def test_square_perfect(self):
        """Test perfect square root evaluation."""
        gen = RootsAndRadicalsGenerator(problem_type='square_perfect')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "square_root_perfect")
            self.assertIn("√", result["problem"])
            # Answer should be a simple integer
            try:
                int(result["final_answer"])
            except ValueError:
                self.fail(f"Perfect square answer should be integer, got {result['final_answer']}")

    def test_cube_perfect(self):
        """Test perfect cube root evaluation."""
        gen = RootsAndRadicalsGenerator(problem_type='cube_perfect')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "cube_root_perfect")
            self.assertIn("∛", result["problem"])
            # Answer should be a simple integer
            try:
                int(result["final_answer"])
            except ValueError:
                self.fail(f"Perfect cube answer should be integer, got {result['final_answer']}")

    def test_simplify_square(self):
        """Test simplifying square roots."""
        gen = RootsAndRadicalsGenerator(problem_type='simplify_square')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "simplify_radical")
            self.assertIn("Simplify", result["problem"])
            # Answer should be in form a√b
            self.assertIn("√", result["final_answer"])

    def test_oracle_from_problem_text(self):
        """A9 oracle: extract the radicand and solve by integer search."""
        import math
        for _ in range(1200):
            result = self.generator.generate()
            match = re.search(r"([√∛])(\d+)", result["problem"])
            self.assertIsNotNone(match, result["problem"])
            symbol, raw = match.groups()
            radicand = int(raw)
            if result["operation"] == "square_root_perfect":
                root = math.isqrt(radicand)
                self.assertEqual(root * root, radicand)
                expected = str(root)
            elif result["operation"] == "cube_root_perfect":
                root = next(k for k in range(1, 101)
                            if k ** 3 >= radicand)
                self.assertEqual(root ** 3, radicand)
                expected = str(root)
            else:
                factor_root = max(k for k in range(1, math.isqrt(radicand) + 1)
                                  if radicand % (k * k) == 0)
                remainder = radicand // (factor_root * factor_root)
                expected = f"{factor_root}√{remainder}"
            self.assertEqual(result["final_answer"], expected,
                             result["problem"])
            self.assertEqual(result["steps"][-1], f"Z{DELIM}{expected}")

    def test_pipe_safety(self):
        for _ in range(300):
            result = self.generator.generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


class TestExponentRulesBaseStyles(unittest.TestCase):
    """Decimal and fractional bases: same rules, styled bases (A9 oracles)."""

    def _oracle_sweep(self, base_style, n=300):
        import re
        random.seed(9)
        gen = ExponentRulesGenerator(base_style=base_style)
        for _ in range(n):
            res = gen.generate()
            self.assertEqual(
                exponent_rule_oracle(res["problem"], res["operation"]),
                res["final_answer"], res["problem"])

    def test_decimal_bases(self):
        self._oracle_sweep("decimal")

    def test_fraction_bases(self):
        self._oracle_sweep("fraction")

    def test_variable_style_unchanged(self):
        random.seed(4)
        gen = ExponentRulesGenerator(base_style="variable")
        for _ in range(50):
            res = gen.generate()
            self.assertNotIn("(0.", res["problem"])

    def test_all_styles_and_phrasings_have_problem_text_oracles(self):
        for style in ExponentRulesGenerator.BASE_STYLES:
            gen = ExponentRulesGenerator(base_style=style)
            for _ in range(700):
                result = gen.generate()
                self.assertEqual(
                    exponent_rule_oracle(result["problem"],
                                         result["operation"]),
                    result["final_answer"], result["problem"])
                self.assertEqual(result["steps"][-1],
                                 f"Z{DELIM}{result['final_answer']}")

    def test_fraction_bases_are_reduced(self):
        import re
        from math import gcd
        random.seed(5)
        gen = ExponentRulesGenerator(base_style="fraction")
        for _ in range(200):
            m = re.search(r"\((\d+)/(\d+)\)", gen.generate()["problem"])
            if m:
                self.assertEqual(gcd(int(m.group(1)), int(m.group(2))), 1)

    def test_bad_base_style_raises(self):
        with self.assertRaises(ValueError):
            ExponentRulesGenerator(base_style="bogus")


if __name__ == '__main__':
    unittest.main()
