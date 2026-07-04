import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.cross_section_generator import CrossSectionGenerator
from helpers import DELIM


EVENTS_FB_RE = re.compile(
    r"At a collider with integrated luminosity L=(\d+) fb\^-1 "
    r"and cross section sigma=(\d+) fb, compute expected events "
    r"N=L\*sigma\."
)
EVENTS_PB_RE = re.compile(
    r"At a collider with integrated luminosity L=(\d+) fb\^-1 "
    r"and cross section sigma=(\d+) pb, use 1 pb=1000 fb "
    r"to compute expected events\."
)
CROSS_SECTION_RE = re.compile(
    r"Given N=(\d+) events and integrated luminosity L=(\d+) fb\^-1, "
    r"compute cross section sigma=N/L in fb\."
)
LUMINOSITY_RE = re.compile(
    r"Given target N=(\d+) events and cross section sigma=(\d+) "
    r"fb, compute required integrated luminosity L=N/sigma in fb\^-1\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def parse_problem(problem):
    match = EVENTS_FB_RE.fullmatch(problem)
    if match:
        return {
            "variant": "events_fb",
            "luminosity": int(match.group(1)),
            "sigma": int(match.group(2)),
        }
    match = EVENTS_PB_RE.fullmatch(problem)
    if match:
        return {
            "variant": "events_pb",
            "luminosity": int(match.group(1)),
            "sigma_pb": int(match.group(2)),
        }
    match = CROSS_SECTION_RE.fullmatch(problem)
    if match:
        return {
            "variant": "cross_section",
            "events": int(match.group(1)),
            "luminosity": int(match.group(2)),
        }
    match = LUMINOSITY_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "variant": "luminosity",
        "events": int(match.group(1)),
        "sigma": int(match.group(2)),
    }


def expected_events_fb(parts):
    luminosity = parts["luminosity"]
    sigma = parts["sigma"]
    events = luminosity * sigma
    answer = f"N = {events} events"
    steps = [
        make_step("COLLIDER_SETUP", "events_fb",
                  f"L={luminosity} fb^-1", f"sigma={sigma} fb"),
        make_step("M", luminosity, sigma, events),
        make_step("UNIT_ATTACH", events, "events", answer),
    ]
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_events_pb(parts):
    luminosity = parts["luminosity"]
    sigma_pb = parts["sigma_pb"]
    sigma_fb = sigma_pb * 1000
    events = luminosity * sigma_fb
    answer = f"N = {events} events"
    steps = [
        make_step("COLLIDER_SETUP", "events_pb",
                  f"L={luminosity} fb^-1", f"sigma={sigma_pb} pb"),
        make_step("CONV_FACTOR", "1 pb", "1000 fb"),
        make_step("M", sigma_pb, 1000, sigma_fb),
        make_step("M", luminosity, sigma_fb, events),
        make_step("UNIT_ATTACH", events, "events", answer),
    ]
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_cross_section(parts):
    events = parts["events"]
    luminosity = parts["luminosity"]
    sigma = Fraction(events, luminosity)
    answer = f"sigma = {fraction_text(sigma)} fb"
    steps = [
        make_step("COLLIDER_SETUP", "cross_section",
                  f"N={events} events", f"L={luminosity} fb^-1"),
        make_step("D", events, luminosity, fraction_text(sigma)),
        make_step("UNIT_ATTACH", fraction_text(sigma), "fb", answer),
    ]
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_luminosity(parts):
    events = parts["events"]
    sigma = parts["sigma"]
    luminosity = Fraction(events, sigma)
    answer = f"L = {fraction_text(luminosity)} fb^-1"
    steps = [
        make_step("COLLIDER_SETUP", "luminosity",
                  f"N={events} events", f"sigma={sigma} fb"),
        make_step("D", events, sigma, fraction_text(luminosity)),
        make_step("UNIT_ATTACH", fraction_text(luminosity), "fb^-1", answer),
    ]
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "events_fb":
        return expected_events_fb(parts)
    if parts["variant"] == "events_pb":
        return expected_events_pb(parts)
    if parts["variant"] == "cross_section":
        return expected_cross_section(parts)
    return expected_luminosity(parts)


class TestCrossSectionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = CrossSectionGenerator()

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
                if fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in CrossSectionGenerator.VARIANTS:
            result = CrossSectionGenerator(variant).generate()
            self.assertEqual(result["operation"], f"cross_section_{variant}")
            self.assertEqual(parse_problem(result["problem"])["variant"],
                             variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            CrossSectionGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])

    def test_all_variants_seen_with_random_generator(self):
        seen = {self.gen.generate()["operation"] for _ in range(300)}
        self.assertEqual(
            seen,
            {"cross_section_events_fb", "cross_section_events_pb",
             "cross_section_cross_section", "cross_section_luminosity"},
        )


if __name__ == "__main__":
    unittest.main()
