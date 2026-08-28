"""Independent prompt-only oracle for LinearTransformEffectGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.linear_transform_effect_generator import (
    QUERIES,
    LinearTransformEffectGenerator,
)
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_number(text):
    return Fraction(text.replace("−", "-"))


def parse_transform(body):
    match = re.search(
        r"(?:y|Fahrenheit|inches) = ([−-]?)(\d+(?:\.\d+)?(?:/\d+)?)·"
        r"(?:x|Celsius|centimeters)(?: ([+−]) (\d+(?:\.\d+)?))?",
        body,
    )
    sign, coefficient, op, shift = match.groups()
    k = parse_number(("-" if sign else "") + coefficient)
    c = parse_number(shift) if shift else Fraction(0)
    if op == "−":
        c = -c
    return k, c


def median(values):
    ordered = sorted(Fraction(value) for value in values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def iqr_five(values):
    ordered = sorted(Fraction(value) for value in values)
    return ((ordered[3] + ordered[4]) / 2 -
            (ordered[0] + ordered[1]) / 2)


def number_text(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    denominator = value.denominator
    while denominator % 2 == 0:
        denominator //= 2
    while denominator % 5 == 0:
        denominator //= 5
    if denominator == 1:
        places = 0
        denominator = value.denominator
        while denominator > 1:
            if denominator % 10 == 0:
                denominator //= 10
            elif denominator % 5 == 0:
                denominator //= 5
            else:
                denominator //= 2
            places += 1
        return f"{float(value):.{places}f}".rstrip("0").rstrip(".")
    return str(value)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant in ("shift", "scale", "affine"):
        mean, sd = map(int, re.search(
            r"have mean (-?\d+) and standard deviation (\d+)", body
        ).groups())
        k, c = parse_transform(body)
        answer = (f"mean {number_text(k * mean + c)}; "
                  f"sd {number_text(abs(k) * sd)}")
    elif variant == "unit_conversion":
        mean, old_unit, sd, repeated_unit = re.search(
            r"mean (-?\d+) (°C|cm) and standard deviation (\d+) (°C|cm)",
            body,
        ).groups()
        assert old_unit == repeated_unit
        k, c = parse_transform(body)
        new_unit = "°F" if old_unit == "°C" else "in"
        answer = (f"mean {number_text(k * int(mean) + c)} {new_unit}; sd "
                  f"{number_text(abs(k) * int(sd))} {new_unit}")
    elif variant == "reverse":
        old_mean, old_sd, new_mean, new_sd = map(int, re.search(
            r"original mean is (-?\d+) and sd is (\d+); the transformed "
            r"mean is (-?\d+) and sd is (\d+)", body,
        ).groups())
        k = Fraction(new_sd, old_sd)
        c = Fraction(new_mean) - k * old_mean
        answer = f"k = {number_text(k)}; c = {number_text(c)}"
    else:
        values = list(map(int, re.search(r"data are: ([0-9, -]+)\.", body)
                          .group(1).split(", ")))
        k, c = parse_transform(body)
        transformed = [k * value + c for value in values]
        old = {"mean": Fraction(sum(values), len(values)),
               "median": median(values), "min": min(values),
               "max": max(values), "IQR": iqr_five(values),
               "range": max(values) - min(values)}
        new = {"mean": Fraction(sum(transformed), len(transformed)),
               "median": median(transformed), "min": min(transformed),
               "max": max(transformed), "IQR": iqr_five(transformed),
               "range": max(transformed) - min(transformed)}
        old_mean = old["mean"]
        old_variance = sum((Fraction(x) - old_mean) ** 2 for x in values) / 5
        new_mean = new["mean"]
        new_variance = sum((x - new_mean) ** 2 for x in transformed) / 5
        old["sd"], new["sd"] = old_variance, new_variance
        changed = [name for name in ("mean", "median", "min", "max", "sd",
                                     "IQR", "range") if old[name] != new[name]]
        unchanged = [name for name in ("mean", "median", "min", "max", "sd",
                                       "IQR", "range") if old[name] == new[name]]
        answer = (f"{', '.join(changed)} change; "
                  f"{', '.join(unchanged)} unchanged")
    return {"variant": variant, "query": query, "answer": answer}


class LinearTransformEffectGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(310014)

    def test_output_contract(self):
        example = LinearTransformEffectGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_800_answers_from_problem_text(self):
        generator = LinearTransformEffectGenerator()
        for _ in range(800):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_steps_are_exact(self):
        generator = LinearTransformEffectGenerator()
        for _ in range(500):
            example = generator.generate()
            oracle_parts(example)
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw)

    def test_linear_identity_on_concrete_data(self):
        data = [3, 7, 8, 14, 18]
        old_mean = Fraction(sum(data), len(data))
        old_variance = sum((Fraction(x) - old_mean) ** 2 for x in data) / 5
        for k, c in ((2, -5), (-3, 7), (Fraction(2, 5), 0),
                     (Fraction(9, 5), 32)):
            transformed = [k * x + c for x in data]
            new_mean = Fraction(sum(transformed), 5)
            new_variance = sum((x - new_mean) ** 2
                               for x in transformed) / 5
            self.assertEqual(new_mean, k * old_mean + c)
            self.assertEqual(new_variance, k * k * old_variance)

    def test_negative_k_reverses_min_and_max_sources(self):
        generator = LinearTransformEffectGenerator("which_change")
        seen_negative = False
        for _ in range(300):
            example = generator.generate()
            body = split_query(example["problem"])[0]
            k, c = parse_transform(body)
            if k >= 0:
                continue
            seen_negative = True
            values = list(map(int, re.search(r"data are: ([0-9, -]+)\.", body)
                              .group(1).split(", ")))
            rows = {fields[1]: fields for fields in
                    (raw.split(DELIM) for raw in example["steps"])
                    if fields[0] == "CHANGE_ROW"}
            self.assertIn(number_text(k * max(values) + c), rows["min"][2])
            self.assertIn(number_text(k * min(values) + c), rows["max"][2])
        self.assertTrue(seen_negative)

    def test_unit_conversion_factor_is_supplied(self):
        generator = LinearTransformEffectGenerator("unit_conversion")
        for _ in range(200):
            example = generator.generate()
            body = split_query(example["problem"])[0]
            k, _ = parse_transform(body)
            self.assertIn(f"supplied scale factor is {number_text(k)}", body)
            factor_step = next(raw for raw in example["steps"]
                               if raw.startswith(f"CONV_FACTOR{DELIM}"))
            self.assertEqual(Fraction(factor_step.split(DELIM)[2]), k)
            if " cm" in body:
                mean, sd = map(int, re.search(
                    r"mean (\d+) cm and standard deviation (\d+) cm", body
                ).groups())
                self.assertLessEqual(sd, mean // 3)

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in LinearTransformEffectGenerator.VARIANTS:
            generator = LinearTransformEffectGenerator(variant)
            seen = set()
            for _ in range(300):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"statistics_linear_transform_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            LinearTransformEffectGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = LinearTransformEffectGenerator()
        for _ in range(400):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            rendered = "\n".join([example["problem"], *example["steps"],
                                    example["final_answer"]])
            self.assertNotRegex(rendered, r"1x|\^1\b|\+ 0|--|− -")
            for raw in example["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
