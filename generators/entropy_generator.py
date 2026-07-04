import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def list_text(values):
    return "[" + ",".join(str(value) for value in values) + "]"


def bit_unit(value):
    return "bit" if Fraction(value) == 1 else "bits"


def power_counts():
    depth = random.randint(3, 8)
    counts = [2 ** depth]
    splits = random.randint(1, depth + 5)
    for _ in range(splits):
        choices = [idx for idx, count in enumerate(counts) if count > 1]
        if not choices:
            break
        idx = random.choice(choices)
        count = counts.pop(idx)
        counts.extend([count // 2, count // 2])
    random.shuffle(counts)
    return counts, 2 ** depth


def entropy_terms(probabilities):
    rows = []
    running = Fraction(0)
    for probability in probabilities:
        exponent = probability.denominator.bit_length() - 1
        term = probability * exponent
        new_running = running + term
        rows.append((probability, exponent, term, running, new_running))
        running = new_running
    return rows, running


class EntropyGenerator(ProblemGenerator):
    """
    Shannon entropy and information content for dyadic distributions.

    Variants:
    - distribution_entropy: H=-sum p log2(p) from listed probabilities.
    - event_information: I(x)=-log2(p(x)) for one dyadic event.
    - counts_entropy: convert power-of-two counts to probabilities, then H.

    Op-codes used:
    - ENTROPY_SETUP / INFO_SETUP / LOG2
    - D / M / A / S (established/shared): exact probability and bit arithmetic
    - Z: entropy or information content in bits
    """

    VARIANTS = ["distribution_entropy", "event_information", "counts_entropy"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "distribution_entropy":
            problem, steps, answer = self._generate_distribution_entropy()
        elif variant == "event_information":
            problem, steps, answer = self._generate_event_information()
        else:
            problem, steps, answer = self._generate_counts_entropy()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"entropy_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_distribution_entropy(self):
        counts, total = power_counts()
        probabilities = [Fraction(count, total) for count in counts]
        rows, entropy = entropy_terms(probabilities)
        steps = [
            step("ENTROPY_SETUP", f"P={list_text([fraction_text(p) for p in probabilities])}",
                 "H=-sum p log2(p)"),
        ]
        for probability, exponent, term, running, new_running in rows:
            steps.append(step("LOG2", fraction_text(probability), -exponent))
            steps.append(step("M", fraction_text(probability), exponent,
                              fraction_text(term)))
            steps.append(step("A", fraction_text(running),
                              fraction_text(term), fraction_text(new_running)))
        answer = f"H={fraction_text(entropy)} {bit_unit(entropy)}"
        problem = (
            f"Compute Shannon entropy in bits for distribution "
            f"P={list_text([fraction_text(p) for p in probabilities])}."
        )
        return problem, steps, answer

    def _generate_event_information(self):
        exponent = random.randint(1, 16)
        probability = Fraction(1, 2 ** exponent)
        steps = [
            step("INFO_SETUP", f"p={fraction_text(probability)}",
                 "I=-log2(p)"),
            step("LOG2", fraction_text(probability), -exponent),
            step("S", 0, -exponent, exponent),
        ]
        answer = f"I={exponent} {bit_unit(exponent)}"
        problem = (
            f"An event has probability p={fraction_text(probability)}. "
            "Find its information content in bits."
        )
        return problem, steps, answer

    def _generate_counts_entropy(self):
        counts, total = power_counts()
        probabilities = [Fraction(count, total) for count in counts]
        rows, entropy = entropy_terms(probabilities)
        steps = [
            step("ENTROPY_SETUP", f"counts={list_text(counts)}, total={total}",
                 "H=-sum p log2(p)"),
        ]
        for count, row in zip(counts, rows):
            probability, exponent, term, running, new_running = row
            steps.append(step("D", count, total, fraction_text(probability)))
            steps.append(step("LOG2", fraction_text(probability), -exponent))
            steps.append(step("M", fraction_text(probability), exponent,
                              fraction_text(term)))
            steps.append(step("A", fraction_text(running),
                              fraction_text(term), fraction_text(new_running)))
        answer = f"H={fraction_text(entropy)} {bit_unit(entropy)}"
        problem = (
            f"A source emits symbols with counts {list_text(counts)} out of "
            f"total {total}. Find entropy in bits."
        )
        return problem, steps, answer
