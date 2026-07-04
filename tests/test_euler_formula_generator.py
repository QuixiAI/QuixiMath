import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.euler_formula_generator import EulerFormulaGenerator
from helpers import DELIM


RECT_RE = re.compile(
    r"Convert z = (.+) to polar and exponential form\."
)
POLAR_RE = re.compile(
    r"Convert z = (\d+) cis\((\d+) deg\) to rectangular and exponential "
    r"form\."
)
IDENTITY = "Use Euler's formula to evaluate e^(i*pi)+1."

ANGLE_DATA = {
    0: ("0", "1", "0"),
    45: ("pi/4", "sqrt2/2", "sqrt2/2"),
    90: ("pi/2", "0", "1"),
    135: ("3pi/4", "-sqrt2/2", "sqrt2/2"),
    180: ("pi", "-1", "0"),
    225: ("5pi/4", "-sqrt2/2", "-sqrt2/2"),
    270: ("3pi/2", "0", "-1"),
    315: ("7pi/4", "sqrt2/2", "-sqrt2/2"),
}


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def parse_cx_int(text):
    text = text.strip()
    match = re.fullmatch(r"(-?\d+) ([+-]) (?:(\d+))?i", text)
    if match:
        imag = int(match.group(3) or 1)
        if match.group(2) == "-":
            imag = -imag
        return int(match.group(1)), imag
    match = re.fullmatch(r"(-?)(?:(\d+))?i", text)
    if match:
        sign = -1 if match.group(1) == "-" else 1
        return 0, sign * int(match.group(2) or 1)
    return int(text), 0


def cx_int(real, imag):
    if imag == 0:
        return str(real)
    if imag == 1:
        imag_text = "i"
    elif imag == -1:
        imag_text = "-i"
    else:
        imag_text = f"{imag}i"
    if real == 0:
        return imag_text
    if imag > 0:
        return f"{real} + {imag_text}"
    return f"{real} - {imag_text.lstrip('-')}"


def cx_exact(real, imag):
    if imag == "0":
        return real
    imag_abs = imag.lstrip("-")
    imag_part = "i" if imag_abs == "1" else f"{imag_abs}i"
    if real == "0":
        return f"-{imag_part}" if imag.startswith("-") else imag_part
    if imag.startswith("-"):
        return f"{real} - {imag_part}"
    return f"{real} + {imag_part}"


def radius_text(real, imag):
    if real == 0:
        return str(abs(imag))
    if imag == 0:
        return str(abs(real))
    scale = abs(real)
    return "sqrt2" if scale == 1 else f"{scale}sqrt2"


def angle_for_point(real, imag):
    if imag == 0 and real > 0:
        return 0
    if real == 0 and imag > 0:
        return 90
    if imag == 0 and real < 0:
        return 180
    if real == 0 and imag < 0:
        return 270
    if real > 0 and imag > 0:
        return 45
    if real < 0 and imag > 0:
        return 135
    if real < 0 and imag < 0:
        return 225
    return 315


def scale_trig(radius, trig_value):
    if trig_value == "0":
        return "0"
    if trig_value == "1":
        return str(radius)
    if trig_value == "-1":
        return str(-radius)
    sign = "-" if trig_value.startswith("-") else ""
    factor = radius // 2
    body = "sqrt2" if factor == 1 else f"{factor}sqrt2"
    return f"{sign}{body}"


def parse_problem(problem):
    if problem == IDENTITY:
        return {"variant": "identity"}
    match = RECT_RE.fullmatch(problem)
    if match:
        real, imag = parse_cx_int(match.group(1))
        return {"variant": "rect_to_forms", "real": real, "imag": imag}
    match = POLAR_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "variant": "polar_to_forms",
        "radius": int(match.group(1)),
        "angle": int(match.group(2)),
    }


def expected_rect(real, imag):
    angle = angle_for_point(real, imag)
    theta_rad = ANGLE_DATA[angle][0]
    r_text = radius_text(real, imag)
    square_sum = real * real + imag * imag
    z_text = cx_int(real, imag)
    steps = [
        make_step("EULER_SETUP", "rectangular to polar/exponential",
                  f"z={z_text}"),
        make_step("E", real, 2, real * real),
        make_step("E", imag, 2, imag * imag),
        make_step("A", real * real, imag * imag, square_sum),
        make_step("ROOT_SIMPLIFY", f"sqrt({square_sum})", r_text),
        make_step("ARGUMENT", f"({real},{imag})", f"{angle} deg"),
        make_step("POLAR_FORM", f"{r_text} cis({angle} deg)"),
        make_step("EXP_FORM", f"{r_text} e^(i*{theta_rad})"),
    ]
    answer = (
        f"polar = {r_text} cis({angle} deg); "
        f"exponential = {r_text} e^(i*{theta_rad})"
    )
    return steps, answer


def expected_polar(radius, angle):
    theta_rad, cos_text, sin_text = ANGLE_DATA[angle]
    real = scale_trig(radius, cos_text)
    imag = scale_trig(radius, sin_text)
    rect = cx_exact(real, imag)
    steps = [
        make_step("EULER_SETUP", "polar to rectangular/exponential",
                  f"r={radius}", f"theta={angle} deg"),
        make_step("EULER_FORMULA", "e^(i theta)=cos theta+i sin theta"),
        make_step("TABLE_LOOKUP", f"cos {angle} deg", cos_text),
        make_step("TABLE_LOOKUP", f"sin {angle} deg", sin_text),
        make_step("SCALE_EXACT", f"{radius}*cos", real),
        make_step("SCALE_EXACT", f"{radius}*sin", imag),
        make_step("RECT_FORM", rect),
        make_step("EXP_FORM", f"{radius} e^(i*{theta_rad})"),
    ]
    answer = (
        f"rectangular = {rect}; "
        f"exponential = {radius} e^(i*{theta_rad})"
    )
    return steps, answer


def expected_identity():
    steps = [
        make_step("EULER_SETUP", "Euler identity", "theta=pi"),
        make_step("EULER_FORMULA", "e^(i theta)=cos theta+i sin theta"),
        make_step("TABLE_LOOKUP", "cos pi", "-1"),
        make_step("TABLE_LOOKUP", "sin pi", "0"),
        make_step("REWRITE", "e^(i*pi)=-1+0i", "-1"),
        make_step("A", -1, 1, 0),
    ]
    return steps, "0"


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "rect_to_forms":
        steps, answer = expected_rect(parts["real"], parts["imag"])
    elif parts["variant"] == "polar_to_forms":
        steps, answer = expected_polar(parts["radius"], parts["angle"])
    else:
        steps, answer = expected_identity()
    steps.append(make_step("Z", answer))
    return steps, answer


class TestEulerFormulaGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = EulerFormulaGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(400):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(int(fields[1]) + int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(int(fields[1]) ** int(fields[2]),
                                     int(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in ("rect_to_forms", "polar_to_forms", "identity"):
            gen = EulerFormulaGenerator(variant)
            for _ in range(40):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"euler_formula_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            EulerFormulaGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
