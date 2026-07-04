import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


FEATURES = ["color", "shape", "size", "texture", "region", "source"]
TOTAL = 16


def fraction_text(value):
    return str(Fraction(value))


def decimal_text(value):
    value = Fraction(value)
    num, den = value.numerator, value.denominator
    places = 0
    while den % 2 == 0:
        den //= 2
        num *= 5
        places += 1
    while den % 5 == 0:
        den //= 5
        num *= 2
        places += 1
    assert den == 1, value
    if places == 0:
        return str(num)
    sign = "-" if num < 0 else ""
    digits = str(abs(num)).rjust(places + 1, "0")
    return sign + f"{digits[:-places]}.{digits[-places:]}".rstrip("0").rstrip(".")


def info_value(probability):
    probability = Fraction(probability)
    if probability == 0:
        return Fraction(0)
    scaled = int(round((-math.log2(float(probability))) * 1000))
    return Fraction(scaled, 1000)


def split_counts(parent_pos):
    left_pos = random.randint(max(0, parent_pos - 8), min(8, parent_pos))
    right_pos = parent_pos - left_pos
    return {
        "left": {"pos": left_pos, "neg": 8 - left_pos},
        "right": {"pos": right_pos, "neg": 8 - right_pos},
    }


def probabilities_for_counts(counts, total):
    return [Fraction(count, total) for count in counts if count]


def collect_probabilities(parent_pos, splits):
    values = set(probabilities_for_counts([parent_pos, TOTAL - parent_pos], TOTAL))
    for split in splits.values():
        for branch in ("left", "right"):
            values.update(
                probabilities_for_counts(
                    [split[branch]["pos"], split[branch]["neg"]], 8
                )
            )
    return sorted(values)


def entropy_from_counts(counts, total, info_table):
    entropy = Fraction(0)
    for count in counts:
        if count == 0:
            continue
        probability = Fraction(count, total)
        entropy += probability * info_table[probability]
    return entropy


def gain_for_split(parent_entropy, split, info_table):
    child_terms = []
    for branch in ("left", "right"):
        branch_counts = [split[branch]["pos"], split[branch]["neg"]]
        branch_entropy = entropy_from_counts(branch_counts, 8, info_table)
        weight = Fraction(8, TOTAL)
        child_terms.append(weight * branch_entropy)
    child_entropy = sum(child_terms, Fraction(0))
    return parent_entropy - child_entropy


def info_table_text(info_table):
    return ", ".join(
        f"{fraction_text(probability)}={decimal_text(value)}"
        for probability, value in sorted(info_table.items())
    )


def append_entropy_steps(steps, label, counts, total, info_table):
    steps.append(step("ENTROPY_SETUP", label,
                      f"counts={counts[0]},{counts[1]}", f"total={total}"))
    running = Fraction(0)
    for count in counts:
        if count == 0:
            steps.append(step("ENTROPY_ZERO", label, "count=0"))
            continue
        probability = Fraction(count, total)
        info = info_table[probability]
        term = probability * info
        new_running = running + term
        steps.extend([
            step("D", count, total, fraction_text(probability)),
            step("INFO_VALUE", f"p={fraction_text(probability)}",
                 f"I={decimal_text(info)}"),
            step("M", fraction_text(probability), decimal_text(info),
                 decimal_text(term)),
            step("A", decimal_text(running), decimal_text(term),
                 decimal_text(new_running)),
        ])
        running = new_running
    steps.append(step("ENTROPY_VALUE", label, decimal_text(running)))
    return running


class InformationGainGenerator(ProblemGenerator):
    """
    Decision-tree information gain from supplied entropy log constants.

    Two candidate binary splits are evaluated from class-count tables. The
    prompt supplies self-information values I(p)=-log2(p), so all entropy and
    gain arithmetic is exact with the stated constants.

    Op-codes used:
    - IG_SETUP / INFO_TABLE / SPLIT_SETUP / ENTROPY_SETUP / ENTROPY_ZERO
    - INFO_VALUE / ENTROPY_VALUE / INFO_GAIN / CHECK
    - D / M / A / S (established/shared): probabilities, weighted child
      entropies, and gains
    - Z: best split and both gains
    """

    def generate(self) -> dict:
        features = random.sample(FEATURES, 2)
        for _ in range(100):
            parent_pos = random.randint(1, TOTAL - 1)
            splits = {
                features[0]: split_counts(parent_pos),
                features[1]: split_counts(parent_pos),
            }
            probabilities = collect_probabilities(parent_pos, splits)
            info_table = {
                probability: info_value(probability)
                for probability in probabilities
            }
            parent_entropy = entropy_from_counts(
                [parent_pos, TOTAL - parent_pos], TOTAL, info_table
            )
            gains = {
                name: gain_for_split(parent_entropy, split, info_table)
                for name, split in splits.items()
            }
            if gains[features[0]] != gains[features[1]]:
                break
        else:
            parent_pos = 8
            splits = {
                features[0]: {
                    "left": {"pos": 8, "neg": 0},
                    "right": {"pos": 0, "neg": 8},
                },
                features[1]: {
                    "left": {"pos": 4, "neg": 4},
                    "right": {"pos": 4, "neg": 4},
                },
            }
            probabilities = collect_probabilities(parent_pos, splits)
            info_table = {
                probability: info_value(probability)
                for probability in probabilities
            }

        parent_counts = [parent_pos, TOTAL - parent_pos]
        steps = [
            step("IG_SETUP", f"parent pos={parent_counts[0]}, neg={parent_counts[1]}",
                 f"total={TOTAL}", f"splits={features[0]},{features[1]}"),
            step("INFO_TABLE", info_table_text(info_table)),
        ]
        parent_entropy = append_entropy_steps(
            steps, "parent", parent_counts, TOTAL, info_table
        )

        gains = {}
        for feature in features:
            split = splits[feature]
            steps.append(step("SPLIT_SETUP", feature,
                              f"left pos={split['left']['pos']}, "
                              f"neg={split['left']['neg']}",
                              f"right pos={split['right']['pos']}, "
                              f"neg={split['right']['neg']}"))
            weighted_terms = []
            for branch in ("left", "right"):
                branch_counts = [
                    split[branch]["pos"],
                    split[branch]["neg"],
                ]
                entropy = append_entropy_steps(
                    steps, f"{feature}_{branch}", branch_counts, 8, info_table
                )
                weight = Fraction(8, TOTAL)
                weighted = weight * entropy
                steps.extend([
                    step("D", 8, TOTAL, fraction_text(weight)),
                    step("M", fraction_text(weight), decimal_text(entropy),
                         decimal_text(weighted)),
                ])
                weighted_terms.append(weighted)
            child_entropy = weighted_terms[0] + weighted_terms[1]
            gain = parent_entropy - child_entropy
            steps.extend([
                step("A", decimal_text(weighted_terms[0]),
                     decimal_text(weighted_terms[1]), decimal_text(child_entropy)),
                step("S", decimal_text(parent_entropy), decimal_text(child_entropy),
                     decimal_text(gain)),
                step("INFO_GAIN", feature, decimal_text(gain)),
            ])
            gains[feature] = gain

        first, second = features
        best = first if gains[first] > gains[second] else second
        relation = ">" if best == first else "<"
        steps.append(step("CHECK", f"{first} vs {second}",
                          f"{decimal_text(gains[first])} {relation} "
                          f"{decimal_text(gains[second])}",
                          f"choose={best}"))
        answer = (
            f"best={best}; gain_{first}={decimal_text(gains[first])}; "
            f"gain_{second}={decimal_text(gains[second])}"
        )
        steps.append(step("Z", answer))

        split_parts = []
        for feature in features:
            split = splits[feature]
            split_parts.append(
                f"{feature}: left pos={split['left']['pos']}, "
                f"neg={split['left']['neg']}; right pos={split['right']['pos']}, "
                f"neg={split['right']['neg']}"
            )
        problem = (
            f"A dataset has {TOTAL} examples with pos={parent_counts[0]} and "
            f"neg={parent_counts[1]}. Candidate splits are "
            f"{split_parts[0]} and {split_parts[1]}. "
            f"Use self-info values I(p)=-log2(p): {info_table_text(info_table)}. "
            "Compute information gain for each split and choose the better split."
        )
        return dict(
            problem_id=jid(),
            operation="information_gain_best_split",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
