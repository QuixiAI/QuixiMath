"""Update several competing hypotheses with exact Bayes calculations.

Variants: ``three_hypotheses``, ``four_hypotheses``, ``all_posteriors``,
``sequential_two_observations``, ``posterior_odds``, and
``coin_identification``. Op-codes: ``BAYES_STAGE``, ``BAYES_TERM``,
``BAYES_EVIDENCE``, ``LIKELIHOOD``, ``POSTERIOR``, ``ODDS``, ``E``, ``M``,
``A``, ``D``, ``CHECK``, and ``Z``. Priors are random exact partitions, while urn
inventories and coin biases supply exact likelihoods; random parameters and
five phrasings per variant give an unbounded problem space.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import odds_txt, prob_txt


PROBABILITY = True
COLORS = ("amber", "blue", "green", "orange", "purple", "red", "teal",
          "white", "yellow")
COIN_BIASES = (Fraction(1, 4), Fraction(1, 3), Fraction(1, 2),
               Fraction(2, 3), Fraction(3, 4))
QUERIES = {
    "three_hypotheses": (
        "Find the requested posterior probability.",
        "Use all three prior-times-likelihood terms in Bayes' rule.",
        "Which exact posterior belongs to the stated urn hypothesis?",
        "Compute the evidence across the three urns, then update the target.",
        "Apply Bayes' rule to identify the target urn's probability.",
    ),
    "four_hypotheses": (
        "Find the requested posterior among the four hypotheses.",
        "Use all four urn prior-times-likelihood terms in Bayes' rule.",
        "Which exact posterior belongs to the target in this four-urn model?",
        "Compute the evidence across exactly four urns, then update the target.",
        "Apply Bayes' rule across four alternatives to update the target urn.",
    ),
    "all_posteriors": (
        "Find the posterior probability of every urn.",
        "Normalize all the prior-times-likelihood terms.",
        "Give the complete posterior distribution over the urns.",
        "Update every hypothesis after the observed color.",
        "Compute all posterior probabilities and verify that they sum to one.",
    ),
    "sequential_two_observations": (
        "Update after the first draw, then use that posterior as the next prior.",
        "Find the target posterior after each of the two observations.",
        "Perform the two Bayes updates in sequence.",
        "Report the intermediate and final exact posterior probabilities.",
        "Use the first posterior distribution as the prior for draw two.",
    ),
    "posterior_odds": (
        "Find the requested posterior odds in lowest terms.",
        "Update the prior odds with the observed color's likelihood ratio.",
        "Compare the two posterior hypothesis weights as exact odds.",
        "Normalize the Bayes terms into the stated odds ratio.",
        "What are the posterior odds of the first urn against the second?",
    ),
    "coin_identification": (
        "Find the requested coin's posterior probability.",
        "Use the entire toss sequence to identify the chosen coin.",
        "Compute every sequence likelihood before applying Bayes' rule.",
        "Update the coin hypotheses from the observed heads and tails.",
        "What is the exact posterior probability of the target coin?",
    ),
}


def _partition(count):
    total = random.randint(count + 1, 12)
    cuts = sorted(random.sample(range(1, total), count - 1))
    amounts = [cuts[0]]
    amounts.extend(cuts[index] - cuts[index - 1]
                   for index in range(1, len(cuts)))
    amounts.append(total - cuts[-1])
    return tuple(Fraction(amount, total) for amount in amounts)


def _sum_steps(values):
    steps = []
    running = values[0]
    for value in values[1:]:
        steps.append(step("A", prob_txt(running), prob_txt(value),
                          prob_txt(running + value)))
        running += value
    return steps, running


def _update_steps(labels, priors, likelihoods, stage):
    steps = [step("BAYES_STAGE", stage,
                  "prior × likelihood for every hypothesis")]
    terms = []
    for label, prior, likelihood in zip(labels, priors, likelihoods):
        term = prior * likelihood
        steps.append(step("M", prob_txt(prior), prob_txt(likelihood),
                          prob_txt(term)))
        steps.append(step("BAYES_TERM", label,
                          f"{prob_txt(prior)} × {prob_txt(likelihood)}",
                          prob_txt(term)))
        terms.append(term)
    addition, evidence = _sum_steps(terms)
    steps.extend(addition)
    steps.append(step("BAYES_EVIDENCE", "sum of Bayes terms",
                      prob_txt(evidence)))
    posteriors = []
    for label, term in zip(labels, terms):
        posterior = term / evidence
        steps.append(step("D", prob_txt(term), prob_txt(evidence),
                          prob_txt(posterior)))
        steps.append(step("POSTERIOR", label,
                          f"({prob_txt(term)})/({prob_txt(evidence)})",
                          prob_txt(posterior)))
        posteriors.append(posterior)
    check_steps, total = _sum_steps(posteriors)
    steps.extend(check_steps)
    steps.append(step("CHECK", "posteriors sum",
                      " + ".join(prob_txt(value) for value in posteriors),
                      prob_txt(total)))
    return steps, tuple(posteriors), evidence


def _urn_data(count):
    labels = tuple(f"U{index}" for index in range(1, count + 1))
    first_color, second_color = random.sample(COLORS, 2)
    inventories = []
    for _ in labels:
        base_total = random.randint(3, 10)
        first = random.randint(1, base_total - 1)
        scale = random.randint(1, 50)
        inventories.append((first * scale, (base_total - first) * scale))
    inventories = tuple(inventories)
    priors = _partition(count)
    inventory_text = "; ".join(
        f"{label} has {counts[0]} {first_color} and {counts[1]} {second_color}"
        for label, counts in zip(labels, inventories))
    prior_text = "; ".join(f"{label}={prob_txt(prior)}"
                           for label, prior in zip(labels, priors))
    return labels, (first_color, second_color), inventories, priors, inventory_text, prior_text


def _urn_likelihoods(colors, inventories, observation):
    color_index = colors.index(observation)
    return tuple(Fraction(counts[color_index], sum(counts))
                 for counts in inventories)


def _urn_likelihood_steps(labels, colors, inventories, observation):
    color_index = colors.index(observation)
    steps = []
    for label, counts in zip(labels, inventories):
        total = sum(counts)
        favorable = counts[color_index]
        likelihood = Fraction(favorable, total)
        steps.extend([
            step("A", counts[0], counts[1], total),
            step("D", favorable, total, prob_txt(likelihood)),
            step("LIKELIHOOD", label,
                 f"{observation} count {favorable}/{total}",
                 prob_txt(likelihood)),
        ])
    return steps


def _urn_prefix(inventory_text, prior_text, observations, target):
    return (f"Urns: {inventory_text}. Priors: {prior_text}. One urn is chosen "
            "and retained. Draws are with replacement. Observations: "
            f"{', '.join(observations)}. Target: {target}.")


class BayesMultipleHypothesesGenerator(ProblemGenerator):
    """Generate exact multi-hypothesis and sequential Bayes exercises."""

    VARIANTS = ("three_hypotheses", "four_hypotheses", "all_posteriors",
                "sequential_two_observations", "posterior_odds",
                "coin_identification")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _single(count, all_posteriors=False):
        (labels, colors, inventories, priors, inventory_text,
         prior_text) = _urn_data(count)
        observation = random.choice(colors)
        likelihoods = _urn_likelihoods(colors, inventories, observation)
        target_index = random.randrange(count)
        target = ("all posterior probabilities given " + observation
                  if all_posteriors else
                  f"P({labels[target_index]} given {observation})")
        prefix = _urn_prefix(inventory_text, prior_text, (observation,), target)
        steps, posteriors, _ = _update_steps(labels, priors, likelihoods,
                                             f"observe {observation}")
        steps = _urn_likelihood_steps(labels, colors, inventories,
                                      observation) + steps
        if all_posteriors:
            answer = "; ".join(
                f"P({label} given {observation}) = {prob_txt(value)}"
                for label, value in zip(labels, posteriors))
        else:
            answer = prob_txt(posteriors[target_index])
        return prefix, steps, answer

    @staticmethod
    def _sequential():
        (labels, colors, inventories, priors, inventory_text,
         prior_text) = _urn_data(3)
        observations = (random.choice(colors), random.choice(colors))
        target_index = random.randrange(3)
        first_likelihoods = _urn_likelihoods(colors, inventories,
                                             observations[0])
        first_steps, first_posteriors, _ = _update_steps(
            labels, priors, first_likelihoods, f"observe {observations[0]}")
        first_steps = _urn_likelihood_steps(labels, colors, inventories,
                                            observations[0]) + first_steps
        second_likelihoods = _urn_likelihoods(colors, inventories,
                                              observations[1])
        second_steps, final_posteriors, _ = _update_steps(
            labels, first_posteriors, second_likelihoods,
            f"observe {observations[1]} using previous posteriors as priors")
        second_steps = _urn_likelihood_steps(labels, colors, inventories,
                                             observations[1]) + second_steps
        target = f"P({labels[target_index]} given {', '.join(observations)})"
        prefix = _urn_prefix(inventory_text, prior_text, observations, target)
        direct_weights = tuple(
            prior * first * second for prior, first, second in
            zip(priors, first_likelihoods, second_likelihoods))
        direct_total = sum(direct_weights, Fraction())
        direct = direct_weights[target_index] / direct_total
        steps = first_steps + second_steps
        steps.append(step("CHECK", "two updates equal direct joint update",
                          prob_txt(final_posteriors[target_index]),
                          prob_txt(direct)))
        first_condition = observations[0]
        full_condition = ", ".join(observations)
        answer = (f"P({labels[target_index]} given {first_condition}) = "
                  f"{prob_txt(first_posteriors[target_index])}; "
                  f"P({labels[target_index]} given {full_condition}) = "
                  f"{prob_txt(final_posteriors[target_index])}")
        return prefix, steps, answer

    @staticmethod
    def _odds():
        (labels, colors, inventories, priors, inventory_text,
         prior_text) = _urn_data(2)
        observation = random.choice(colors)
        likelihoods = _urn_likelihoods(colors, inventories, observation)
        target = f"posterior odds {labels[0]}:{labels[1]} given {observation}"
        prefix = _urn_prefix(inventory_text, prior_text, (observation,), target)
        steps, posteriors, _ = _update_steps(labels, priors, likelihoods,
                                             f"observe {observation}")
        steps = _urn_likelihood_steps(labels, colors, inventories,
                                      observation) + steps
        odds = odds_txt(posteriors[0])
        steps.append(step("ODDS", f"{labels[0]}:{labels[1]}", odds))
        answer = f"posterior odds {labels[0]}:{labels[1]} = {odds}"
        return prefix, steps, answer

    @staticmethod
    def _coins():
        labels = ("C1", "C2", "C3")
        heads_probabilities = tuple(sorted(random.sample(COIN_BIASES,
                                                         len(labels))))
        priors = _partition(len(labels))
        length = 3
        heads = random.randint(1, length - 1)
        observations = ["H"] * heads + ["T"] * (length - heads)
        random.shuffle(observations)
        target_index = random.randrange(len(labels))
        coin_text = "; ".join(
            f"{label} has P(H)={prob_txt(probability)}"
            for label, probability in zip(labels, heads_probabilities))
        prior_text = "; ".join(f"{label}={prob_txt(prior)}"
                               for label, prior in zip(labels, priors))
        condition = ", ".join(observations)
        prefix = (f"Coins: {coin_text}. Priors: {prior_text}. One coin is "
                  f"chosen and retained. Tosses: {condition}. Target: "
                  f"P({labels[target_index]} given {condition}).")
        likelihoods = []
        power_steps = []
        tails = length - heads
        for label, probability in zip(labels, heads_probabilities):
            complement = 1 - probability
            head_power = probability ** heads
            tail_power = complement ** tails
            likelihood = head_power * tail_power
            power_steps.extend([
                step("E", prob_txt(probability), heads, prob_txt(head_power)),
                step("E", prob_txt(complement), tails, prob_txt(tail_power)),
                step("M", prob_txt(head_power), prob_txt(tail_power),
                     prob_txt(likelihood)),
                step("CHECK", f"sequence likelihood for {label}",
                     f"{heads} H factors and {tails} T factors",
                     prob_txt(likelihood)),
            ])
            likelihoods.append(likelihood)
        update_steps, posteriors, _ = _update_steps(
            labels, priors, tuple(likelihoods), f"observe {condition}")
        answer = prob_txt(posteriors[target_index])
        return prefix, power_steps + update_steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "three_hypotheses":
            prefix, steps, answer = self._single(3)
        elif variant == "four_hypotheses":
            prefix, steps, answer = self._single(4)
        elif variant == "all_posteriors":
            prefix, steps, answer = self._single(random.choice((3, 4)), True)
        elif variant == "sequential_two_observations":
            prefix, steps, answer = self._sequential()
        elif variant == "posterior_odds":
            prefix, steps, answer = self._odds()
        else:
            prefix, steps, answer = self._coins()
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_bayes_multiple_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
