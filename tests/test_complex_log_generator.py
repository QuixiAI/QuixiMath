import cmath
import math
import os
import random
import re
import sys
import unittest
from fractions import Fraction
from unittest import mock

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators import complex_log_generator
from generators.complex_log_generator import ComplexLogGenerator
from helpers import DELIM


R = r"(\d+(?:/\d+)?)"
CIS_RE = re.compile(rf"z = {R} cis\((\d+) deg\)")
TRIG_RE = re.compile(rf"z = {R}\(cos (\d+) deg \+ i sin (\d+) deg\)")
EXPO_RE = re.compile(rf"z = {R} e\^\(i\*(\d+) deg\)")

BASE_ALTS = (r"\(e\^\(i\*\d+ deg\)\)|\(cos \d+ deg \+ i sin \d+ deg\)"
             r"|cis\(\d+ deg\)|\(-1\)|\(-i\)|1|i")
POWER_RE = re.compile(rf"({BASE_ALTS})\^(\(-i\)|\(-?\d+i\)|i)")

PI_RE = re.compile(r"(-?)(\d*)pi(?:/(\d+))?")


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def parse_pi(text):
    """Inverse of the generator's pi rendering: '5pi/6' -> Fraction(5, 6)."""
    if text == "0":
        return Fraction(0)
    match = PI_RE.fullmatch(text)
    assert match is not None, text
    sign = -1 if match.group(1) else 1
    num = int(match.group(2)) if match.group(2) else 1
    den = int(match.group(3)) if match.group(3) else 1
    return sign * Fraction(num, den)


def parse_radius(text):
    if "/" in text:
        num, den = text.split("/")
        return Fraction(int(num), int(den))
    return int(text)


def principal_degrees(theta):
    return theta - 360 if theta > 180 else theta


def pi_text(frac):
    frac = Fraction(frac)
    if frac == 0:
        return "0"
    sign = "-" if frac < 0 else ""
    frac = abs(frac)
    num = "" if frac.numerator == 1 else str(frac.numerator)
    if frac.denominator == 1:
        return f"{sign}{num}pi"
    return f"{sign}{num}pi/{frac.denominator}"


def arg_text(principal):
    return pi_text(Fraction(principal, 180))


def radius_text(radius):
    if isinstance(radius, Fraction):
        return f"{radius.numerator}/{radius.denominator}"
    return str(radius)


def ln_text(radius):
    return "0" if radius == 1 else f"ln({radius_text(radius)})"


def principal_log_text(radius, arg):
    ln_part = ln_text(radius)
    if arg == "0":
        return ln_part
    if arg.startswith("-"):
        arg_abs = arg.lstrip("-")
        if ln_part == "0":
            return f"-i*{arg_abs}"
        return f"{ln_part} - i*{arg_abs}"
    if ln_part == "0":
        return f"i*{arg}"
    return f"{ln_part} + i*{arg}"


def multivalued_log_text(radius, arg):
    ln_part = ln_text(radius)
    angle = "2pi*k" if arg == "0" else f"{arg} + 2pi*k"
    if ln_part == "0":
        return f"i*({angle})"
    return f"{ln_part} + i*({angle})"


def parse_problem(problem):
    """Recover the instance from the problem text alone (all phrasings)."""
    match = CIS_RE.search(problem)
    if match:
        return {"variant": "log",
                "radius": parse_radius(match.group(1)),
                "theta": int(match.group(2))}
    match = TRIG_RE.search(problem)
    if match:
        assert match.group(2) == match.group(3), problem
        return {"variant": "log",
                "radius": parse_radius(match.group(1)),
                "theta": int(match.group(2))}
    match = EXPO_RE.search(problem)
    if match:
        return {"variant": "log",
                "radius": parse_radius(match.group(1)),
                "theta": int(match.group(2))}
    match = POWER_RE.search(problem)
    assert match is not None, problem
    base, exponent = match.group(1), match.group(2)
    if base == "1":
        theta = 0
    elif base == "i":
        theta = 90
    elif base == "(-1)":
        theta = 180
    elif base == "(-i)":
        theta = 270
    else:
        theta = int(re.search(r"(\d+) deg", base).group(1))
    if exponent == "i":
        coeff = 1
    elif exponent == "(-i)":
        coeff = -1
    else:
        coeff = int(exponent.strip("()").rstrip("i"))
    return {"variant": "power_ii", "theta": theta, "coeff": coeff,
            "base": base}


def parse_principal_log(text):
    """'ln(5) - i*pi/6' -> (Fraction modulus, Fraction multiple of pi)."""
    angle = Fraction(0)
    modulus = Fraction(1)
    body = text
    match = re.match(r"ln\((\d+(?:/\d+)?)\)", body)
    if match:
        modulus = Fraction(parse_radius(match.group(1)))
        body = body[match.end():]
        if body.startswith(" + i*"):
            angle = parse_pi(body[5:])
        elif body.startswith(" - i*"):
            angle = -parse_pi(body[5:])
        else:
            assert body == "", text
    elif body.startswith("i*"):
        angle = parse_pi(body[2:])
    elif body.startswith("-i*"):
        angle = -parse_pi(body[3:])
    else:
        assert body == "0", text
    return modulus, angle


def expected_log(radius, theta):
    principal = principal_degrees(theta)
    arg = arg_text(principal)
    steps = [
        make_step("LOG_SETUP", f"z={radius_text(radius)} cis({theta} deg)"),
    ]
    if theta > 180:
        steps.append(make_step("S", theta, 360, principal))
        steps.append(make_step("ANGLE_WRAP", f"{theta} deg",
                               f"{principal} deg"))
    else:
        steps.append(make_step("ARGUMENT", f"{theta} deg",
                               f"{principal} deg"))
    principal_text = principal_log_text(radius, arg)
    multivalued_text = multivalued_log_text(radius, arg)
    steps.extend([
        make_step("LOG_FORMULA", "log z = ln r + i(arg + 2pi*k)"),
        make_step("PRINCIPAL_LOG", principal_text),
        make_step("MULTIVALUED_LOG", multivalued_text, "k in Z"),
    ])
    answer = (
        f"Log(z) = {principal_text}; "
        f"log(z) = {multivalued_text}, k in Z"
    )
    return steps, answer


def expected_power(theta, coeff, base):
    principal = principal_degrees(theta)
    arg = arg_text(principal)
    log_text = principal_log_text(1, arg)
    exponent = Fraction(-coeff * principal, 180)
    exp_result = pi_text(exponent)
    answer = "1" if exponent == 0 else f"e^({exp_result})"
    exp_text = {1: "i", -1: "-i"}.get(coeff, f"{coeff}i")
    expr = f"{base}^i" if coeff == 1 else f"{base}^({exp_text})"
    base_plain = base[1:-1] if base.startswith("(") else base
    steps = [make_step("POWER_SETUP", expr, "principal logarithm")]
    if base_plain != f"cis({theta} deg)":
        steps.append(make_step("REWRITE", f"{base_plain} = cis({theta} deg)"))
    if theta > 180:
        steps.append(make_step("S", theta, 360, principal))
        steps.append(make_step("ANGLE_WRAP", f"{theta} deg",
                               f"{principal} deg"))
    else:
        steps.append(make_step("ARGUMENT", f"{theta} deg",
                               f"{principal} deg"))
    steps.append(make_step("PRINCIPAL_LOG", f"Log(z) = {log_text}"))
    log_factor = f"({log_text})" if log_text.startswith("-") else log_text
    steps.append(make_step("REWRITE", f"{expr} = exp({exp_text}*Log(z))",
                           f"exp({exp_text}*{log_factor})"))
    if principal != 0:
        steps.append(make_step("I_SQUARE", "i^2", "-1"))
    steps.append(make_step("M", -coeff, arg, exp_result))
    steps.append(make_step("REWRITE", f"exp({exp_result})", answer))
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "log":
        steps, answer = expected_log(parts["radius"], parts["theta"])
    else:
        steps, answer = expected_power(parts["theta"], parts["coeff"],
                                       parts["base"])
    steps.append(make_step("Z", answer))
    return steps, answer


class TestComplexLogGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ComplexLogGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(800):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_numeric_oracle_exponentiates_the_log_back_to_z(self):
        """Independent route: e^(Log z) must reproduce z itself."""
        gen = ComplexLogGenerator("log")
        for _ in range(500):
            result = gen.generate()
            parts = parse_problem(result["problem"])
            head = result["final_answer"].split("; ")[0]
            self.assertTrue(head.startswith("Log(z) = "), head)
            modulus, angle = parse_principal_log(head[len("Log(z) = "):])
            self.assertGreater(angle, Fraction(-1))
            self.assertLessEqual(angle, Fraction(1))
            recovered = float(modulus) * cmath.exp(1j * float(angle) * math.pi)
            expected = float(parts["radius"]) * cmath.exp(
                1j * math.radians(parts["theta"]))
            self.assertAlmostEqual(recovered.real, expected.real, places=7,
                                   msg=result["problem"])
            self.assertAlmostEqual(recovered.imag, expected.imag, places=7,
                                   msg=result["problem"])

    def test_numeric_oracle_for_imaginary_powers(self):
        """Independent route: compare against cmath's principal exp/log."""
        gen = ComplexLogGenerator("power_ii")
        for _ in range(500):
            result = gen.generate()
            parts = parse_problem(result["problem"])
            z = cmath.exp(1j * math.radians(parts["theta"]))
            reference = cmath.exp(parts["coeff"] * 1j * cmath.log(z))
            answer = result["final_answer"]
            if answer == "1":
                value = 1.0
            else:
                self.assertTrue(answer.startswith("e^(")
                                and answer.endswith(")"), answer)
                value = math.exp(float(parse_pi(answer[3:-1])) * math.pi)
            self.assertAlmostEqual(reference.imag, 0.0,
                                   delta=1e-9 * max(1.0, abs(reference)))
            self.assertTrue(
                math.isclose(value, reference.real, rel_tol=1e-9),
                f"{result['problem']} -> {answer} vs {reference}")

    def test_principal_argument_range(self):
        gen = ComplexLogGenerator("log")
        for _ in range(400):
            result = gen.generate()
            parts = parse_problem(result["problem"])
            principal = principal_degrees(parts["theta"])
            self.assertGreater(principal, -180)
            self.assertLessEqual(principal, 180)
            if principal != 0:
                self.assertIn(arg_text(principal), result["final_answer"])

    def test_arithmetic_steps(self):
        for _ in range(600):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "S":
                    self.assertEqual(int(fields[1]) - int(fields[2]),
                                     int(fields[3]), raw_step)
                if fields[0] == "M":
                    self.assertEqual(int(fields[1]) * parse_pi(fields[2]),
                                     parse_pi(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in ("log", "power_ii"):
            gen = ComplexLogGenerator(variant)
            for _ in range(80):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"complex_log_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_classic_i_to_the_i(self):
        gen = ComplexLogGenerator("power_ii")
        with mock.patch.object(complex_log_generator, "ANGLES", [90]), \
                mock.patch.object(complex_log_generator, "POWER_COEFFS", [1]):
            for _ in range(20):
                result = gen.generate()
                self.assertIn("i^i", result["problem"])
                self.assertEqual(result["final_answer"], "e^(-pi/2)")
                self.assertIn("PRINCIPAL_LOG|Log(z) = i*pi/2", result["steps"])

    def test_phrasing_variety(self):
        problems = {self.gen.generate()["problem"] for _ in range(400)}
        self.assertGreater(len(problems), 380)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ComplexLogGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(400):
            result = self.gen.generate()
            self.assertNotIn(DELIM, result["problem"])
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
