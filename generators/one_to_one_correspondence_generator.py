"""Build finite cardinality comparisons by explicit one-to-one pairing.

Variants:
- ``compare_by_pairing`` pairs rosters A and B and reports the unmatched side.
- ``count_by_pairing`` pairs objects with the counting labels 1 through n.
- ``cardinal_class`` groups four rosters by their cardinal number.

Each variant has five phrasings.  The noun banks, subset choices, sizes, and
cardinality patterns give well over 1,000 distinct problem texts.

Op-codes:
- ``PAIR``: pair one left-hand element with one right-hand element.
- ``UNPAIRED``: report the unmatched side and its canonical roster.
- ``COUNT``: record a roster's cardinal number.
- ``Z``: exact composite answer.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from set_common import roster


FOUNDATIONS = True


A_WORDS = (
    "apple", "apricot", "banana", "cherry", "fig", "grape", "guava",
    "kiwi", "lemon", "lime", "mango", "melon", "orange", "papaya",
    "peach", "pear", "plum", "quince", "tangerine", "watermelon",
)
B_WORDS = (
    "badger", "beaver", "camel", "dolphin", "falcon", "gecko", "heron",
    "ibis", "jaguar", "koala", "lemur", "otter", "panda", "rabbit",
    "seal", "tiger", "viper", "walrus", "yak", "zebra",
)
OBJECT_WORDS = (
    "book", "brush", "button", "chalk", "clip", "coin", "crayon",
    "cup", "eraser", "folder", "key", "marker", "notebook", "pencil",
    "ruler", "spoon", "stamp", "sticker", "ticket", "token",
)
CLASS_POOLS = (
    A_WORDS,
    B_WORDS,
    OBJECT_WORDS,
    (
        "amber", "blue", "bronze", "coral", "cyan", "gold", "gray",
        "green", "indigo", "ivory", "navy", "ochre", "olive", "pink",
        "purple", "red", "silver", "tan", "teal", "violet",
    ),
)


QUERIES = {
    "compare_by_pairing": (
        "Pair the elements in order and compare the set sizes.",
        "Use one-to-one pairing to decide whether either set has more elements.",
        "Match A with B element by element, then report the size comparison.",
        "Compare the cardinal numbers by pairing the two rosters.",
        "Make as many A-to-B pairs as possible and state what remains.",
    ),
    "count_by_pairing": (
        "Pair each object with one counting label and state card(Objects).",
        "Count the objects by one-to-one matching with the labels.",
        "Use the counting labels to establish the cardinal number of Objects.",
        "Match every object to one label, then report the object count.",
        "Demonstrate the count with one-to-one pairs and give card(Objects).",
    ),
    "cardinal_class": (
        "Group the sets that have the same cardinal number.",
        "Identify the cardinal class of each roster.",
        "Count each set and group equal cardinalities.",
        "Decide which sets are equinumerous and report every size group.",
        "Use cardinal number to classify the four sets.",
    ),
}


class OneToOneCorrespondenceGenerator(ProblemGenerator):
    """Generate forced one-to-one pairings over canonically printed rosters."""

    VARIANTS = ("compare_by_pairing", "count_by_pairing", "cardinal_class")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _sample_words(pool, size):
        return sorted(random.sample(pool, size))

    def _compare(self):
        size_a = random.randint(3, 9)
        size_b = random.randint(3, 9)
        values_a = self._sample_words(A_WORDS, size_a)
        values_b = self._sample_words(B_WORDS, size_b)
        problem = (
            f"A = {roster(values_a)}. B = {roster(values_b)}. "
            f"{random.choice(QUERIES['compare_by_pairing'])}"
        )
        steps = [step("PAIR", left, right)
                 for left, right in zip(values_a, values_b)]
        if size_a == size_b:
            steps.append(step("UNPAIRED", "neither", roster([])))
            answer = f"same size ({size_a} each)"
        elif size_a > size_b:
            extra = values_a[size_b:]
            steps.append(step("UNPAIRED", "A", roster(extra)))
            answer = f"A has {size_a - size_b} more ({size_a} vs {size_b})"
        else:
            extra = values_b[size_a:]
            steps.append(step("UNPAIRED", "B", roster(extra)))
            answer = f"B has {size_b - size_a} more ({size_b} vs {size_a})"
        steps.extend((step("COUNT", "A", size_a),
                      step("COUNT", "B", size_b)))
        return problem, steps, answer

    def _count(self):
        size = random.randint(3, 10)
        objects = self._sample_words(OBJECT_WORDS, size)
        labels = list(range(1, size + 1))
        problem = (
            f"Objects = {roster(objects)}. Labels = {roster(labels)}. "
            f"{random.choice(QUERIES['count_by_pairing'])}"
        )
        steps = [step("PAIR", obj, label)
                 for obj, label in zip(objects, labels)]
        steps.append(step("COUNT", "Objects", size))
        answer = f"card(Objects) = {size}; paired all {size} objects"
        return problem, steps, answer

    def _cardinal_class(self):
        repeated_size = random.randint(2, 7)
        repeated = random.sample(range(4), random.choice((2, 2, 3)))
        sizes = []
        unused_sizes = [size for size in range(2, 8) if size != repeated_size]
        random.shuffle(unused_sizes)
        for index in range(4):
            sizes.append(repeated_size if index in repeated else unused_sizes.pop())
        sets = [self._sample_words(pool, size)
                for pool, size in zip(CLASS_POOLS, sizes)]
        assignments = "; ".join(
            f"{chr(65 + index)} = {roster(values)}"
            for index, values in enumerate(sets)
        )
        problem = f"Sets: {assignments}. {random.choice(QUERIES['cardinal_class'])}"
        steps = [step("COUNT", chr(65 + index), len(values))
                 for index, values in enumerate(sets)]
        groups = {}
        for index, size in enumerate(sizes):
            groups.setdefault(size, []).append(chr(65 + index))
        for labels in groups.values():
            if len(labels) < 2:
                continue
            first_index = ord(labels[0]) - 65
            for other in labels[1:]:
                other_index = ord(other) - 65
                for left, right in zip(sets[first_index], sets[other_index]):
                    steps.append(step("PAIR", f"{labels[0]}: {left}",
                                      f"{other}: {right}"))
        answer = "; ".join(
            f"card {size}: {', '.join(groups[size])}"
            for size in sorted(groups)
        )
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "compare_by_pairing":
            problem, steps, answer = self._compare()
        elif variant == "count_by_pairing":
            problem, steps, answer = self._count()
        else:
            problem, steps, answer = self._cardinal_class()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"one_to_one_correspondence_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
