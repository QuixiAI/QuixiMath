import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.de_moivre_generator import DeMoivreGenerator
from helpers import DELIM


POWER_RE = re.compile(
    r"Use De Moivre's theorem to compute "
    r"\((\d+) cis\((\d+) deg\)\)\^(\d+)\."
)
UNITY_RE = re.compile(r"Find all (\d+)-th roots of unity in polar form\.")
ARBITRARY_RE = re.compile(
    r"Find all (\d+)-th roots of z = (\d+) cis\((\d+) deg\)\."
)

TRIG = {
    0: ("1", "0"),
    30: ("sqrt3/2", "1/2"),
    45: ("sqrt2/2", "sqrt2/2"),
    60: ("1/2", "sqrt3/2"),
    90: ("0", "1"),
    120: ("-1/2", "sqrt3/2"),
    135: ("-sqrt2/2", "sqrt2/2"),
    150: ("-sqrt3/2", "1/2"),
    180: ("-1", "0"),
    210: ("-sqrt3/2", "-1/2"),
    225: ("-sqrt2/2", "-sqrt2/2"),
    240: ("-1/2", "-sqrt3/2"),
    270: ("0", "-1"),
    300: ("1/2", "-sqrt3/2"),
    315: ("sqrt2/2", "-sqrt2/2"),
    330: ("sqrt3/2", "-1/2"),
}


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def scale_trig(radius, value):
    if value == "0":
        return "0"
    if value == "1":
        return str(radius)
    if value == "-1":
        return str(-radius)
    sign = "-" if value.startswith("-") else ""
    core = value.lstrip("-")
    if core == "1/2":
        return f"{sign}{radius // 2}" if radius % 2 == 0 else \
            f"{sign}{radius}/2"
    root = "sqrt2" if "sqrt2" in core else "sqrt3"
    if radius == 1:
        body = f"{root}/2"
    elif radius % 2 == 0:
        factor = radius // 2
        body = root if factor == 1 else f"{factor}{root}"
    else:
        body = f"{radius}{root}/2"
    return f"{sign}{body}"


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


def roots_text(radius, angles):
    prefix = "" if radius == 1 else f"{radius} "
    return ", ".join(f"{prefix}cis({angle} deg)" for angle in angles)


def parse_problem(problem):
    match = POWER_RE.fullmatch(problem)
    if match:
        radius, theta, exponent = map(int, match.groups())
        return {
            "variant": "power",
            "radius": radius,
            "theta": theta,
            "exponent": exponent,
        }
    match = UNITY_RE.fullmatch(problem)
    if match:
        return {"variant": "roots_unity", "n": int(match.group(1))}
    match = ARBITRARY_RE.fullmatch(problem)
    assert match is not None, problem
    n, radius, theta = map(int, match.groups())
    return {
        "variant": "arbitrary_roots",
        "n": n,
        "radius": radius,
        "theta": theta,
    }


def expected_power(radius, theta, exponent):
    radius_power = radius ** exponent
    raw_angle = theta * exponent
    angle = raw_angle % 360
    cos_text, sin_text = TRIG[angle]
    real = scale_trig(radius_power, cos_text)
    imag = scale_trig(radius_power, sin_text)
    rect = cx_exact(real, imag)
    steps = [
        make_step("DEMOIVRE_SETUP", "power", f"r={radius}",
                  f"theta={theta} deg", f"n={exponent}"),
        make_step("E", radius, exponent, radius_power),
        make_step("M", theta, exponent, raw_angle),
        make_step("MOD_REDUCE", raw_angle, "mod 360", angle),
        make_step("DEMOIVRE_POWER", f"{radius_power} cis({angle} deg)"),
        make_step("TABLE_LOOKUP", f"cos {angle} deg", cos_text),
        make_step("TABLE_LOOKUP", f"sin {angle} deg", sin_text),
        make_step("SCALE_EXACT", f"{radius_power}*cos", real),
        make_step("SCALE_EXACT", f"{radius_power}*sin", imag),
        make_step("RECT_FORM", rect),
    ]
    answer = (
        f"polar = {radius_power} cis({angle} deg); "
        f"rectangular = {rect}"
    )
    return steps, answer


def expected_roots_unity(n):
    steps = [make_step("DEMOIVRE_SETUP", "roots_of_unity", f"n={n}")]
    angles = []
    for k in range(n):
        raw = 360 * k
        angle = raw // n
        steps.append(make_step("M", 360, k, raw))
        steps.append(make_step("D", raw, n, angle))
        steps.append(make_step("ROOT_ANGLE", f"k={k}", f"{angle} deg"))
        steps.append(make_step("ROOT", f"cis({angle} deg)"))
        angles.append(angle)
    return steps, f"roots = {roots_text(1, angles)}"


def expected_arbitrary_roots(n, radius, theta):
    rho = round(radius ** (1 / n))
    while rho ** n < radius:
        rho += 1
    while rho ** n > radius:
        rho -= 1
    steps = [
        make_step("DEMOIVRE_SETUP", "arbitrary_roots", f"R={radius}",
                  f"theta={theta} deg", f"n={n}"),
        make_step("ROOT", radius, n, rho),
    ]
    angles = []
    for k in range(n):
        turn = 360 * k
        raw = theta + turn
        angle = raw // n
        steps.append(make_step("M", 360, k, turn))
        steps.append(make_step("A", theta, turn, raw))
        steps.append(make_step("D", raw, n, angle))
        steps.append(make_step("ROOT_ANGLE", f"k={k}", f"{angle} deg"))
        steps.append(make_step("ROOT", f"{rho} cis({angle} deg)"))
        angles.append(angle)
    return steps, f"roots = {roots_text(rho, angles)}"


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "power":
        steps, answer = expected_power(parts["radius"], parts["theta"],
                                       parts["exponent"])
    elif parts["variant"] == "roots_unity":
        steps, answer = expected_roots_unity(parts["n"])
    else:
        steps, answer = expected_arbitrary_roots(parts["n"],
                                                 parts["radius"],
                                                 parts["theta"])
    steps.append(make_step("Z", answer))
    return steps, answer


class TestDeMoivreGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = DeMoivreGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
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
                elif fields[0] == "D":
                    self.assertEqual(int(fields[1]) // int(fields[2]),
                                     int(fields[3]), raw_step)
                    self.assertEqual(int(fields[1]) % int(fields[2]), 0,
                                     raw_step)
                elif fields[0] == "E":
                    self.assertEqual(int(fields[1]) ** int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "MOD_REDUCE":
                    modulus = int(fields[2].split()[1])
                    self.assertEqual(int(fields[1]) % modulus,
                                     int(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in ("power", "roots_unity", "arbitrary_roots"):
            gen = DeMoivreGenerator(variant)
            for _ in range(40):
                result = gen.generate()
                self.assertEqual(result["operation"], f"de_moivre_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            DeMoivreGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
