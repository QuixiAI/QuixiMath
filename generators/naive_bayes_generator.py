import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


FEATURES = ["offer", "link", "urgent", "known", "long", "money"]
CLASSES = ["Spam", "Ham"]
VARIANTS = ["two_feature", "three_feature"]
ALPHA = 1


def fraction_text(value):
    return str(Fraction(value))


def pairs_text(pairs):
    return ", ".join(f"{name}={value}" for name, value in pairs)


def count_text(class_name, total, counts):
    pieces = [f"N={total}"] + [f"{name}={counts[name]}" for name in counts]
    return f"{class_name} " + ", ".join(pieces)


def score_for_class(total, total_all, counts, query):
    score = Fraction(total, total_all)
    denom = total + 2 * ALPHA
    for feature, value in query:
        ones = counts[feature]
        observed = ones if value == 1 else total - ones
        score *= Fraction(observed + ALPHA, denom)
    return score


def make_case(feature_count):
    features = random.sample(FEATURES, feature_count)
    for _ in range(100):
        totals = {
            "Spam": random.randint(6, 20),
            "Ham": random.randint(6, 20),
        }
        counts = {
            class_name: {
                feature: random.randint(0, totals[class_name])
                for feature in features
            }
            for class_name in CLASSES
        }
        query = [(feature, random.randint(0, 1)) for feature in features]
        total_all = sum(totals.values())
        scores = {
            class_name: score_for_class(
                totals[class_name], total_all, counts[class_name], query
            )
            for class_name in CLASSES
        }
        if scores["Spam"] != scores["Ham"]:
            return features, totals, counts, query, scores
    totals = {"Spam": 10, "Ham": 10}
    counts = {
        "Spam": {feature: 8 for feature in features},
        "Ham": {feature: 2 for feature in features},
    }
    query = [(feature, 1) for feature in features]
    total_all = sum(totals.values())
    scores = {
        class_name: score_for_class(
            totals[class_name], total_all, counts[class_name], query
        )
        for class_name in CLASSES
    }
    return features, totals, counts, query, scores


class NaiveBayesGenerator(ProblemGenerator):
    """
    Naive Bayes classification from binary feature count tables.

    Variants:
    - two_feature: classify a query using two binary feature counts.
    - three_feature: classify a query using three binary feature counts.

    Op-codes used:
    - NB_SETUP / NB_PRIOR / NB_FEATURE_COUNT / NB_LIKELIHOOD / NB_SCORE
    - CHECK (established): compare unnormalized class scores
    - A / S / D / M (established/shared): exact priors, smoothed
      likelihoods, score products, and posterior normalization
    - Z: predicted class and normalized posteriors
    """

    VARIANTS = VARIANTS

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        feature_count = 2 if variant == "two_feature" else 3
        features, totals, counts, query, scores = make_case(feature_count)
        total_all = sum(totals.values())

        steps = [
            step("NB_SETUP", f"query={pairs_text(query)}",
                 f"alpha={ALPHA}", f"classes={','.join(CLASSES)}"),
        ]

        priors = {}
        likelihoods = {}
        for class_name in CLASSES:
            total = totals[class_name]
            prior = Fraction(total, total_all)
            priors[class_name] = prior
            steps.append(step("D", total, total_all, fraction_text(prior)))
            steps.append(step("NB_PRIOR", class_name, fraction_text(prior)))
            class_likelihoods = []
            denom = total + 2 * ALPHA
            for feature, value in query:
                ones = counts[class_name][feature]
                if value == 1:
                    observed = ones
                else:
                    observed = total - ones
                    steps.append(step("S", total, ones, observed))
                numerator = observed + ALPHA
                steps.extend([
                    step("NB_FEATURE_COUNT", class_name,
                         f"{feature}={value}", f"count={observed}"),
                    step("A", observed, ALPHA, numerator),
                    step("A", total, 2 * ALPHA, denom),
                    step("D", numerator, denom,
                         fraction_text(Fraction(numerator, denom))),
                    step("NB_LIKELIHOOD", class_name,
                         f"{feature}={value}",
                         fraction_text(Fraction(numerator, denom))),
                ])
                class_likelihoods.append(Fraction(numerator, denom))
            likelihoods[class_name] = class_likelihoods

        recomputed_scores = {}
        for class_name in CLASSES:
            running = priors[class_name]
            steps.append(step("NB_SCORE", class_name,
                              f"start={fraction_text(running)}"))
            for likelihood in likelihoods[class_name]:
                new_running = running * likelihood
                steps.append(step("M", fraction_text(running),
                                  fraction_text(likelihood),
                                  fraction_text(new_running)))
                running = new_running
            recomputed_scores[class_name] = running
            steps.append(step("NB_SCORE", class_name,
                              f"score={fraction_text(running)}"))

        score_total = recomputed_scores["Spam"] + recomputed_scores["Ham"]
        posteriors = {
            class_name: recomputed_scores[class_name] / score_total
            for class_name in CLASSES
        }
        prediction = (
            "Spam" if recomputed_scores["Spam"] > recomputed_scores["Ham"]
            else "Ham"
        )
        relation = ">" if prediction == "Spam" else "<"
        steps.extend([
            step("A", fraction_text(recomputed_scores["Spam"]),
                 fraction_text(recomputed_scores["Ham"]),
                 fraction_text(score_total)),
            step("D", fraction_text(recomputed_scores["Spam"]),
                 fraction_text(score_total), fraction_text(posteriors["Spam"])),
            step("D", fraction_text(recomputed_scores["Ham"]),
                 fraction_text(score_total), fraction_text(posteriors["Ham"])),
            step("CHECK", "Spam vs Ham",
                 f"{fraction_text(recomputed_scores['Spam'])} {relation} "
                 f"{fraction_text(recomputed_scores['Ham'])}",
                 f"predict={prediction}"),
        ])
        answer = (
            f"class={prediction}; "
            f"P_Spam_given_x={fraction_text(posteriors['Spam'])}; "
            f"P_Ham_given_x={fraction_text(posteriors['Ham'])}"
        )
        steps.append(step("Z", answer))

        problem = (
            f"Classify query {pairs_text(query)} by naive Bayes with Laplace "
            f"smoothing alpha={ALPHA}. Feature-one counts: "
            f"{count_text('Spam', totals['Spam'], counts['Spam'])}; "
            f"{count_text('Ham', totals['Ham'], counts['Ham'])}. "
            "Use class priors from N."
        )
        return dict(
            problem_id=jid(),
            operation=f"naive_bayes_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
