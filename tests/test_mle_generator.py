"""Independent problem-text oracles for all MLEGenerator variants."""
import random
import re
import unittest
from fractions import Fraction

from generators.mle_generator import MLEGenerator, PROMPTS
from helpers import DELIM


def values_from(text):
    return [int(value) for value in re.search(r"\[([-\d,]+)\]", text).group(1).split(",")]


def fraction(value):
    return str(Fraction(value))


def oracle_parts(example):
    problem = example["problem"]
    values = values_from(problem)
    n = len(values)
    total = sum(values)
    if "Bernoulli" in problem and "Binomial(" not in problem:
        successes = total
        failures = n - successes
        estimate = Fraction(successes, n)
        loglik = f"ell(p)={successes}*log(p)+{failures}*log(1-p)"
        score = f"score={successes}/p-{failures}/(1-p)"
        return {"variant": "bernoulli", "values": values,
                "answer": f"{loglik}; {score}; p_hat={fraction(estimate)}",
                "estimate": estimate}
    if "exponential" in problem.lower():
        estimate = Fraction(n, total)
        loglik = f"ell(lambda)={n}*log(lambda)-{total}*lambda"
        score = f"score={n}/lambda-{total}"
        return {"variant": "exponential", "values": values,
                "answer": f"{loglik}; {score}; lambda_hat={fraction(estimate)}",
                "estimate": estimate}
    if "known sigma^2=" in problem:
        sigma2 = int(re.search(r"known sigma\^2=(\d+)", problem).group(1))
        estimate = Fraction(total, n)
        loglik = f"ell(mu)=-(1/(2*{sigma2}))*sum((x_i-mu)^2)+C"
        score = f"score=({total}-{n}*mu)/{sigma2}"
        return {"variant": "normal_mu", "values": values,
                "answer": f"{loglik}; {score}; mu_hat={fraction(estimate)}",
                "estimate": estimate}
    if "both mu and sigma^2 unknown" in problem:
        mean = Fraction(total, n)
        squares = [(Fraction(value) - mean) ** 2 for value in values]
        ss = sum(squares, Fraction(0))
        variance = ss / n
        return {"variant": "normal_sigma2", "values": values,
                "mean": mean, "squares": squares, "ss": ss,
                "variance": variance,
                "answer": f"mu_hat={fraction(mean)}; SS={fraction(ss)}; "
                          f"sigma2_hat={fraction(variance)}"}
    if "Poisson" in problem:
        estimate = Fraction(total, n)
        loglik = f"ell(lambda)={total}*log(lambda)-{n}*lambda+C"
        score = f"score={total}/lambda-{n}"
        return {"variant": "poisson", "values": values,
                "answer": f"{loglik}; {score}; lambda_hat={fraction(estimate)}",
                "estimate": estimate}
    if "Uniform(0,theta)" in problem:
        maximum = max(values)
        return {"variant": "uniform_theta", "values": values,
                "maximum": maximum,
                "answer": f"theta_hat = max = {maximum}; "
                          "score equation has no root"}
    if "geometric" in problem.lower():
        failures = total - n
        mean = Fraction(total, n)
        estimate = Fraction(n, total)
        score = f"score={n}/p-{failures}/(1-p)"
        return {"variant": "geometric", "values": values,
                "mean": mean, "estimate": estimate,
                "answer": f"xbar={fraction(mean)}; {score}; "
                          f"p_hat={fraction(estimate)}"}
    trials_each = int(re.search(r"Binomial\(N=(\d+),p\)", problem).group(1))
    total_trials = n * trials_each
    failures = total_trials - total
    estimate = Fraction(total, total_trials)
    loglik = f"ell(p)={total}*log(p)+{failures}*log(1-p)+C"
    score = f"score={total}/p-{failures}/(1-p)"
    return {"variant": "binomial_n_known", "values": values,
            "trials_each": trials_each, "total_trials": total_trials,
            "estimate": estimate,
            "answer": f"{loglik}; {score}; p_hat={fraction(estimate)}"}


class MLEGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(625184)

    def test_output_contract(self):
        result = MLEGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["steps"][-1],
                         f"Z{DELIM}{result['final_answer']}")

    def test_oracle_recomputes_1000_answers_from_problem_text(self):
        generator = MLEGenerator()
        for _ in range(1000):
            result = generator.generate()
            self.assertEqual(result["final_answer"],
                             oracle_parts(result)["answer"], result["problem"])

    def test_all_arithmetic_steps(self):
        generator = MLEGenerator()
        for _ in range(900):
            result = generator.generate()
            for raw in result["steps"]:
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
                elif fields[0] == "SUM":
                    terms = [int(value) for value in
                             re.findall(r"(?<!\^)-?\d+", fields[2])]
                    self.assertEqual(sum(terms), int(fields[3]), raw)

    def test_normal_sigma2_deviation_rows_and_integer_variance(self):
        generator = MLEGenerator("normal_sigma2")
        seen_n = set()
        for _ in range(400):
            result = generator.generate()
            parts = oracle_parts(result)
            seen_n.add(len(parts["values"]))
            rows = [raw.split(DELIM) for raw in result["steps"]
                    if raw.startswith(f"DEV_ROW{DELIM}")]
            self.assertEqual(len(rows), len(parts["values"]))
            for row, value, square in zip(rows, parts["values"], parts["squares"]):
                self.assertEqual(int(row[1]), value)
                self.assertEqual(Fraction(row[2]), Fraction(value) - parts["mean"])
                self.assertEqual(Fraction(row[3]), square)
            self.assertEqual(parts["variance"].denominator, 1)
            self.assertGreater(parts["variance"], 0)
        self.assertEqual(seen_n, {4, 5, 6, 7, 8})

    def test_poisson_and_geometric_estimators_are_sample_mean_routes(self):
        poisson = MLEGenerator("poisson")
        geometric = MLEGenerator("geometric")
        for _ in range(300):
            p_parts = oracle_parts(poisson.generate())
            self.assertEqual(p_parts["estimate"],
                             Fraction(sum(p_parts["values"]), len(p_parts["values"])))
            g_parts = oracle_parts(geometric.generate())
            self.assertEqual(g_parts["estimate"], 1 / g_parts["mean"])
            self.assertTrue(all(value >= 1 for value in g_parts["values"]))

    def test_uniform_uses_boundary_not_score_root(self):
        generator = MLEGenerator("uniform_theta")
        for _ in range(300):
            result = generator.generate()
            parts = oracle_parts(result)
            boundary = next(raw.split(DELIM) for raw in result["steps"]
                            if raw.startswith(f"BOUNDARY_MLE{DELIM}"))
            self.assertEqual(int(boundary[2]), parts["maximum"])
            check = next(raw for raw in result["steps"]
                         if raw.startswith(f"CHECK{DELIM}likelihood decreasing"))
            self.assertIn(f"θ ≥ {parts['maximum']}", check)

    def test_known_binomial_total_trials_and_interior_estimate(self):
        generator = MLEGenerator("binomial_n_known")
        for _ in range(300):
            result = generator.generate()
            parts = oracle_parts(result)
            self.assertEqual(parts["total_trials"],
                             len(parts["values"]) * parts["trials_each"])
            self.assertTrue(all(0 <= value <= parts["trials_each"]
                                for value in parts["values"]))
            self.assertGreater(parts["estimate"], 0)
            self.assertLess(parts["estimate"], 1)

    def test_all_variants_are_available(self):
        for variant in MLEGenerator.VARIANTS:
            result = MLEGenerator(variant).generate()
            self.assertEqual(result["operation"], f"mle_{variant}")
            self.assertEqual(result["final_answer"],
                             oracle_parts(result)["answer"])

    def test_every_variant_has_four_parseable_phrasings(self):
        fields = {"data": "[1,2,3,4]", "sigma2": 4,
                  "trials_each": 5}
        for variant in MLEGenerator.VARIANTS:
            templates = PROMPTS[variant]
            self.assertEqual(len(templates), 4)
            self.assertEqual(len(set(templates)), 4)
            for template in templates:
                problem = template.format(**fields)
                with self.subTest(variant=variant, problem=problem):
                    self.assertEqual(oracle_parts({"problem": problem})["variant"],
                                     variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            MLEGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = MLEGenerator()
        for _ in range(500):
            result = generator.generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            rendered = "\n".join([result["problem"], *result["steps"],
                                    result["final_answer"]])
            self.assertNotRegex(rendered, r"1x|\^1\b|--|− -")
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
