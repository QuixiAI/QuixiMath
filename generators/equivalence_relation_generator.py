"""Construct equivalence relations and their canonical class partitions.

Variants:
- ``check_and_classes`` verifies a relation generated from a random partition.
- ``from_partition`` expands every block into its ordered relation pairs.
- ``congruence_classes`` groups a finite interval modulo ``m``.
- ``same_property`` groups numbers by parity, digit sum, or a remainder.
- ``count_pairs`` evaluates ``Σ card(block)²`` for a stated partition.

Op-codes:
- ``REL_SETUP``: define the finite carrier and relation.
- ``REFLEXIVE_CHECK`` / ``SYMMETRIC_CHECK`` / ``TRANSITIVE_CHECK``: verify
  the three equivalence-relation properties.
- ``CLASS`` / ``PARTITION``: expose each block and the full partition.
- ``REL_PAIR``: add one ordered pair induced by a block.
- ``COUNT`` / ``M`` / ``A``: expose exact relation-cardinality arithmetic.
- ``Z``: canonical partition, pair roster, or integer answer.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from set_common import partition_text, relation_text, roster


FOUNDATIONS = True


QUERIES = {
    "check_and_classes": (
        "Verify that R is an equivalence relation and list its classes.",
        "Check reflexivity, symmetry, and transitivity, then give A/R.",
        "Use the pair roster to recover the equivalence-class partition.",
        "Confirm all three equivalence properties and list the blocks.",
        "Determine the classes induced by this equivalence relation.",
    ),
    "from_partition": (
        "Build the equivalence relation induced by P.",
        "List every ordered pair whose two entries lie in one block.",
        "Convert the partition into its complete relation roster.",
        "Construct R by relating exactly the elements in the same block.",
        "Expand each class square and give the resulting relation.",
    ),
    "congruence_classes": (
        "List the equivalence classes of congruence modulo m on A.",
        "Partition A by equal remainders modulo m.",
        "Find A/R for the stated congruence relation.",
        "Group the elements that are congruent modulo m.",
        "Give the canonical partition into residue classes.",
    ),
    "same_property": (
        "List the equivalence classes determined by this shared property.",
        "Partition A by the stated equality of attributes.",
        "Find all blocks of the same-property relation.",
        "Group exactly those numbers with equal property values.",
        "Give the canonical quotient partition A/R.",
    ),
    "count_pairs": (
        "How many ordered pairs are in the induced equivalence relation?",
        "Compute Σ card(block)² for P.",
        "Count all within-block ordered pairs.",
        "Find card(R) for the equivalence relation induced by P.",
        "Square each block size and add to count the relation pairs.",
    ),
}


def random_partition():
    size = random.randint(3, 8)
    values = sorted(random.sample(range(1, 61), size))
    block_count = random.randint(2, min(4, size))
    shuffled = random.sample(values, size)
    blocks = [[shuffled[index]] for index in range(block_count)]
    for value in shuffled[block_count:]:
        random.choice(blocks).append(value)
    blocks = [sorted(block) for block in blocks]
    blocks.sort(key=lambda block: block[0])
    return values, blocks


def relation_from_blocks(blocks):
    return frozenset((first, second)
                     for block in blocks for first in block for second in block)


def blocks_from_key(values, key):
    grouped = {}
    for value in values:
        grouped.setdefault(key(value), []).append(value)
    blocks = [sorted(block) for block in grouped.values()]
    blocks.sort(key=lambda block: block[0])
    return blocks


def class_steps(blocks, labels=None):
    steps = []
    for index, block in enumerate(blocks):
        label = labels[index] if labels is not None else f"[{block[0]}]"
        steps.append(step("CLASS", label, roster(block)))
    steps.append(step("PARTITION", partition_text(blocks)))
    return steps


class EquivalenceRelationGenerator(ProblemGenerator):
    """Generate finite equivalence relations through their class blocks."""

    VARIANTS = ("check_and_classes", "from_partition", "congruence_classes",
                "same_property", "count_pairs")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _check(self):
        values, blocks = random_partition()
        relation = relation_from_blocks(blocks)
        problem = (f"A = {roster(values)}. R = {relation_text(relation)}. "
                   f"{random.choice(QUERIES['check_and_classes'])}")
        steps = [step("REL_SETUP", f"A = {roster(values)}",
                      f"R = {relation_text(relation)}")]
        for value in values:
            steps.append(step("REFLEXIVE_CHECK", f"({value}, {value})",
                              "present"))
        for first, second in sorted(relation):
            steps.append(step("SYMMETRIC_CHECK", f"({first}, {second})",
                              f"reverse ({second}, {first})", "present"))
        for first, middle in sorted(relation):
            for middle_two, last in sorted(relation):
                if middle == middle_two:
                    steps.append(step(
                        "TRANSITIVE_CHECK",
                        f"({first}, {middle}) and ({middle_two}, {last})",
                        f"need ({first}, {last})", "present"))
        steps.extend(class_steps(blocks))
        return problem, steps, partition_text(blocks)

    def _from_partition(self):
        values, blocks = random_partition()
        relation = relation_from_blocks(blocks)
        problem = (f"A = {roster(values)}. Partition P = {partition_text(blocks)}. "
                   f"{random.choice(QUERIES['from_partition'])}")
        steps = class_steps(blocks)
        for block in blocks:
            for first in block:
                for second in block:
                    steps.append(step("REL_PAIR", f"({first}, {second})",
                                      "same block"))
        steps.append(step("COUNT", "pairs", len(relation)))
        return problem, steps, relation_text(relation)

    def _congruence(self):
        modulus = random.randint(2, 7)
        start = random.randint(0, 30)
        values = list(range(start, start + random.randint(8, 16)))
        blocks = blocks_from_key(values, lambda value: value % modulus)
        labels = [f"remainder {block[0] % modulus}" for block in blocks]
        problem = (f"A = {roster(values)}. m = {modulus}. "
                   f"Relation: xRy iff x ≡ y (mod m). "
                   f"{random.choice(QUERIES['congruence_classes'])}")
        steps = class_steps(blocks, labels)
        count = sum(len(block) ** 2 for block in blocks)
        steps.append(step("COUNT", "pairs", count))
        return problem, steps, partition_text(blocks)

    def _same_property(self):
        property_name = random.choice(("parity", "digit sum", "remainder"))
        values = sorted(random.sample(range(10, 100), random.randint(6, 12)))
        if property_name == "parity":
            key = lambda value: value % 2
            rule = "xRy iff x and y have the same parity"
            label = lambda block: "even" if block[0] % 2 == 0 else "odd"
        elif property_name == "digit sum":
            key = lambda value: sum(int(digit) for digit in str(value))
            rule = "xRy iff x and y have the same digit sum"
            label = lambda block: f"digit sum {key(block[0])}"
        else:
            modulus = random.randint(3, 8)
            key = lambda value: value % modulus
            rule = f"xRy iff x and y have the same remainder modulo {modulus}"
            label = lambda block: f"remainder {key(block[0])}"
        blocks = blocks_from_key(values, key)
        problem = (f"A = {roster(values)}. Rule: {rule}. "
                   f"{random.choice(QUERIES['same_property'])}")
        steps = class_steps(blocks, [label(block) for block in blocks])
        return problem, steps, partition_text(blocks)

    def _count_pairs(self):
        values, blocks = random_partition()
        problem = (f"A = {roster(values)}. Partition P = {partition_text(blocks)}. "
                   f"{random.choice(QUERIES['count_pairs'])}")
        steps = [step("PARTITION", partition_text(blocks))]
        running = 0
        for block in blocks:
            square = len(block) * len(block)
            steps.append(step("M", len(block), len(block), square))
            new_total = running + square
            steps.append(step("A", running, square, new_total))
            running = new_total
        steps.append(step("COUNT", "pairs", running))
        return problem, steps, str(running)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "check_and_classes":
            problem, steps, answer = self._check()
        elif variant == "from_partition":
            problem, steps, answer = self._from_partition()
        elif variant == "congruence_classes":
            problem, steps, answer = self._congruence()
        elif variant == "same_property":
            problem, steps, answer = self._same_property()
        else:
            problem, steps, answer = self._count_pairs()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"equivalence_relation_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
