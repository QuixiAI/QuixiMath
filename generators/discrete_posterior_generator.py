"""Exact Bayesian updating on a finite Bernoulli-parameter grid.

Variants: ``posterior_table``, ``map``, ``posterior_mean``,
``posterior_predictive``, ``credible_set``, and ``bayes_factor``. Grids contain
3--4 tenths from 0.1 through 0.9; priors are uniform or dyadic; data have at
most six trials. Every likelihood, unnormalized weight, normalizer, posterior,
mean, predictive probability, credible mass, and Bayes factor is computed as
an exact ``Fraction``. Credible-set ties are broken by smaller theta, stated
in the problem. Op-codes: ``BAYES_UPDATE_SETUP``, ``BAYES_ROW``,
``POSTERIOR_ROW``, ``BAYES_FACTOR``, ``CREDIBLE_PICK``, ``RULE``, ``CHECK``,
``SUM``, ``S``, ``A``, ``M``, ``D``, ``E``, and ``Z``.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import exact, prob_txt


STATISTICS = True

LOCATIONS = (
    "north lab", "south lab", "river office", "lake office",
    "maple center", "oak center", "pine archive", "cedar archive",
    "amber campus", "birch campus", "granite clinic", "harbor clinic",
)
STUDIES = (
    "posterior study", "Bayes review", "prediction audit", "model trial",
    "sampling review", "prior study", "inference audit",
    "decision review", "quality study", "pilot analysis",
    "calibration review", "reliability study",
)

QUERIES = {
    "posterior_table": (
        "Compute the normalized posterior table on the grid.",
        "Update every grid point and report its exact posterior mass.",
        "Normalize the prior-times-likelihood weights.",
        "List the finite-grid posterior distribution.",
    ),
    "map": (
        "Find the unique MAP grid point and its posterior mass.",
        "Which theta maximizes the exact posterior?",
        "Compute the finite-grid MAP estimate.",
        "Report the most probable theta and its normalized probability.",
    ),
    "posterior_mean": (
        "Compute the exact posterior mean of theta.",
        "Weight each grid point by its posterior probability.",
        "Find E[theta given the data] on this grid.",
        "Report the normalized posterior expectation.",
    ),
    "posterior_predictive": (
        "Find the exact posterior-predictive probability of a success next.",
        "Compute the posterior mixture probability for the next trial.",
        "Evaluate the sum of theta times posterior(theta).",
        "Report P(next trial is a success given the data).",
    ),
    "credible_set": (
        "Find the smallest posterior-mass set reaching at least 0.9.",
        "Build the 90% finite-grid credible set by descending mass.",
        "Select grid points until cumulative posterior mass reaches 0.9.",
        "Report the minimal credible set and its exact mass.",
    ),
    "bayes_factor": (
        "Compute the exact likelihood Bayes factor for thetaA versus thetaB.",
        "Find L(thetaA)/L(thetaB) from the observed data.",
        "Compare the two simple grid hypotheses by likelihood ratio.",
        "Report the reduced-fraction Bayes factor.",
    ),
}


def _site():
    record = f"grid {random.choice('ABCDEFGH')}{random.randint(10, 99)}"
    return (f"{random.choice(LOCATIONS)} during the "
            f"{random.choice(STUDIES)} ({record})")


def _prior(size):
    if random.choice((True, False)):
        return [Fraction(1, size)] * size
    if size == 3:
        weights = [Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)]
    else:
        weights = [Fraction(1, 2), Fraction(1, 4),
                   Fraction(1, 8), Fraction(1, 8)]
    random.shuffle(weights)
    return weights


def _case(require_unique_map=False):
    while True:
        size = random.choice((3, 4))
        grid = tuple(Fraction(value, 10) for value in
                     sorted(random.sample(range(1, 10), size)))
        prior = tuple(_prior(size))
        trials = random.randint(1, 6)
        successes = random.randint(0, trials)
        failures = trials - successes
        likelihoods = tuple(theta ** successes * (1 - theta) ** failures
                            for theta in grid)
        weights = tuple(p * likelihood for p, likelihood in
                        zip(prior, likelihoods))
        evidence = sum(weights, Fraction(0))
        posterior = tuple(weight / evidence for weight in weights)
        if not require_unique_map or posterior.count(max(posterior)) == 1:
            return {"grid": grid, "prior": prior, "trials": trials,
                    "successes": successes, "failures": failures,
                    "likelihoods": likelihoods, "weights": weights,
                    "evidence": evidence, "posterior": posterior}


def _problem_prefix(case):
    cells = "; ".join(
        f"P({exact(theta)}) = {prob_txt(prior)}"
        for theta, prior in zip(case["grid"], case["prior"])
    )
    success_word = "success" if case["successes"] == 1 else "successes"
    trial_word = "trial" if case["trials"] == 1 else "trials"
    failure_word = "failure" if case["failures"] == 1 else "failures"
    return (f"At the {_site()}, prior on θ: {cells}. Observe "
            f"{case['successes']} {success_word} in {case['trials']} Bernoulli "
            f"{trial_word} ({case['failures']} {failure_word}).")


def _posterior_steps(case):
    steps = [step("BAYES_UPDATE_SETUP",
                  "grid " + ", ".join(exact(value) for value in case["grid"]),
                  "prior " + ", ".join(prob_txt(value) for value in case["prior"])
                  + f"; data {case['successes']} of {case['trials']}")]
    for theta, prior, likelihood, weight in zip(
            case["grid"], case["prior"], case["likelihoods"], case["weights"]):
        complement = 1 - theta
        success_power = theta ** case["successes"]
        failure_power = complement ** case["failures"]
        steps.extend([
            step("S", 1, exact(theta), exact(complement)),
            step("E", exact(theta), case["successes"], exact(success_power)),
            step("E", exact(complement), case["failures"], exact(failure_power)),
            step("M", exact(success_power), exact(failure_power),
                 exact(likelihood)),
            step("M", prob_txt(prior), exact(likelihood), exact(weight)),
            step("BAYES_ROW", exact(theta),
                 f"{prob_txt(prior)} · {exact(success_power)} · {exact(failure_power)}",
                 exact(weight)),
        ])
    steps.append(step("SUM", " + ".join(exact(value) for value in case["weights"]),
                      exact(case["evidence"])))
    for theta, weight, posterior in zip(
            case["grid"], case["weights"], case["posterior"]):
        steps.extend([step("D", exact(weight), exact(case["evidence"]),
                           prob_txt(posterior)),
                      step("POSTERIOR_ROW", exact(theta), prob_txt(posterior))])
    steps.append(step("CHECK", "posterior split",
                      " + ".join(prob_txt(value) for value in case["posterior"]),
                      "1"))
    return steps


class DiscretePosteriorGenerator(ProblemGenerator):
    """Generate exact finite-grid posterior and predictive calculations.

    The module docstring lists variants, grid/prior bounds, exactness,
    credible-set ordering, and op-codes.
    """

    VARIANTS = tuple(QUERIES)

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _result(variant, problem, steps, answer):
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_discrete_posterior_{variant}",
                "problem": problem, "steps": steps,
                "final_answer": answer}

    def _posterior_variant(self, variant):
        case = _case(require_unique_map=(variant == "map"))
        steps = _posterior_steps(case)
        extra = ""
        if variant == "posterior_table":
            answer = "; ".join(
                f"{exact(theta)}: {prob_txt(posterior)}"
                for theta, posterior in zip(case["grid"], case["posterior"]))
        elif variant == "map":
            index = case["posterior"].index(max(case["posterior"]))
            theta, posterior = case["grid"][index], case["posterior"][index]
            steps.extend([step("RULE", "MAP", "largest posterior"),
                          step("CHECK", "unique maximum",
                               f"θ = {exact(theta)}", prob_txt(posterior))])
            answer = (f"MAP θ = {exact(theta)}; posterior "
                      f"{prob_txt(posterior)}")
        elif variant in ("posterior_mean", "posterior_predictive"):
            terms = []
            for theta, posterior in zip(case["grid"], case["posterior"]):
                product = theta * posterior
                terms.append(product)
                steps.append(step("M", exact(theta), prob_txt(posterior),
                                  exact(product)))
            result = sum(terms, Fraction(0))
            steps.append(step("SUM", " + ".join(exact(value) for value in terms),
                              exact(result)))
            if variant == "posterior_mean":
                answer = f"posterior mean = {exact(result)}"
            else:
                steps.append(step("CHECK", "Bernoulli posterior predictive",
                                  "Σ θ·posterior(θ)", exact(result)))
                answer = f"P(next success) = {exact(result)}"
        else:
            target = Fraction(9, 10)
            ordering = sorted(range(len(case["grid"])),
                              key=lambda index: (-case["posterior"][index],
                                                 case["grid"][index]))
            steps.append(step("RULE", "credible set",
                              "descending posterior; smaller θ breaks ties; stop at 0.9"))
            selected = []
            mass = Fraction(0)
            for index in ordering:
                previous = mass
                mass += case["posterior"][index]
                steps.append(step("A", prob_txt(previous),
                                  prob_txt(case["posterior"][index]),
                                  prob_txt(mass)))
                steps.append(step("CREDIBLE_PICK", exact(case["grid"][index]),
                                  prob_txt(case["posterior"][index]),
                                  prob_txt(mass)))
                selected.append(case["grid"][index])
                if mass >= target:
                    break
            steps.append(step("CHECK", "minimal mass",
                              f"{prob_txt(previous)} < 0.9 ≤ {prob_txt(mass)}",
                              len(selected)))
            members = ", ".join(exact(value) for value in sorted(selected))
            answer = f"{{{members}}}; mass {prob_txt(mass)}"
            extra = (" Order grid points by descending posterior, break ties "
                     "by smaller θ, and stop when cumulative mass reaches at "
                     "least 0.9.")
        problem = (f"{_problem_prefix(case)}{extra}\n"
                   f"{random.choice(QUERIES[variant])}")
        return self._result(variant, problem, steps, answer)

    def _bayes_factor(self):
        case = _case()
        first_index, second_index = random.sample(range(len(case["grid"])), 2)
        first, second = case["grid"][first_index], case["grid"][second_index]
        first_likelihood = case["likelihoods"][first_index]
        second_likelihood = case["likelihoods"][second_index]
        ratio = first_likelihood / second_likelihood
        first_complement, second_complement = 1 - first, 1 - second
        first_success = first ** case["successes"]
        first_failure = first_complement ** case["failures"]
        second_success = second ** case["successes"]
        second_failure = second_complement ** case["failures"]
        steps = [
            step("BAYES_UPDATE_SETUP", f"θA = {exact(first)}, θB = {exact(second)}",
                 f"data {case['successes']} of {case['trials']}"),
            step("E", exact(first), case["successes"], exact(first_success)),
            step("E", exact(first_complement), case["failures"],
                 exact(first_failure)),
            step("M", exact(first_success), exact(first_failure),
                 exact(first_likelihood)),
            step("E", exact(second), case["successes"], exact(second_success)),
            step("E", exact(second_complement), case["failures"],
                 exact(second_failure)),
            step("M", exact(second_success), exact(second_failure),
                 exact(second_likelihood)),
            step("D", exact(first_likelihood), exact(second_likelihood),
                 prob_txt(ratio)),
            step("BAYES_FACTOR", f"L({exact(first)})/L({exact(second)})",
                 prob_txt(ratio)),
        ]
        answer = f"BF({exact(first)}:{exact(second)}) = {prob_txt(ratio)}"
        problem = (f"{_problem_prefix(case)} Compare θA = {exact(first)} "
                   f"with θB = {exact(second)}.\n"
                   f"{random.choice(QUERIES['bayes_factor'])}")
        return self._result("bayes_factor", problem, steps, answer)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "bayes_factor":
            return self._bayes_factor()
        return self._posterior_variant(variant)
