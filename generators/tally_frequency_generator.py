"""Construct and read categorical tally-frequency tables.

Variants: ``raw_to_table``, ``tally_to_count``, ``table_total``,
``most_least``, and ``how_many_more``. Op-codes: ``STAT_SETUP``,
``TALLY_ROW``, ``A``, ``S``, ``CHECK``, and ``Z``. Categories are rendered
alphabetically; groups of five use the fixed ``////\\`` tally grammar.
Random category banks, counts, response order, settings, and four phrasings
per variant give an unbounded prompt space.
"""
import random
from collections import Counter

from base_generator import ProblemGenerator
from helpers import jid, step
from stats_common import render_tally, running_sum_steps, tally_marks, text_list


STATISTICS = True
CATEGORY_BANKS = (
    ("favorite colors", ("Blue", "Green", "Orange", "Purple", "Red", "Yellow")),
    ("favorite fruits", ("Apple", "Banana", "Cherry", "Grape", "Melon", "Pear")),
    ("chosen pets", ("Bird", "Cat", "Dog", "Fish", "Hamster", "Rabbit")),
    ("club choices", ("Art", "Chess", "Drama", "Music", "Robotics", "Science")),
    ("transportation choices", ("Bike", "Bus", "Car", "Train", "Walk")),
    ("book genres", ("Fantasy", "History", "Mystery", "Poetry", "Science")),
)
SETTINGS = ("classroom", "community center", "library", "math club",
            "museum workshop", "school fair", "science lab", "study hall",
            "survey office", "training center")
QUERIES = {
    "raw_to_table": (
        "Make the alphabetized tally-frequency table.",
        "Construct a tally table and report every category count.",
        "Turn the raw responses into the required frequency table.",
        "Count each response and give the complete tally summary.",
    ),
    "tally_to_count": (
        "Decode the tally marks and give the count for {target}.",
        "How many observations are recorded for {target}?",
        "Read the {target} row and report its frequency.",
        "Use the groups of five to find the {target} count.",
    ),
    "table_total": (
        "Find the total number of observations in the tally table.",
        "Add all category frequencies to determine the survey size.",
        "How many responses does the complete tally table contain?",
        "Decode and sum every row of the table.",
    ),
    "most_least": (
        "Identify the unique most and least frequent categories with their counts.",
        "Which categories occur most and least often, and how many times?",
        "Read the tally table to report the unique maximum and minimum rows.",
        "Give the most-common and least-common categories with frequencies.",
    ),
    "how_many_more": (
        "How many more observations are recorded for {high} than for {low}?",
        "Find the difference between the {high} and {low} frequencies.",
        "By how much does the {high} count exceed the {low} count?",
        "Subtract the {low} row from the {high} row.",
    ),
}


def _data(unique_extremes=False, raw=False):
    topic, bank = random.choice(CATEGORY_BANKS)
    categories = tuple(sorted(random.sample(bank, random.randint(3, 5))))
    while True:
        upper = 6 if raw else 12
        counts = {category: random.randint(1, upper) for category in categories}
        total = sum(counts.values())
        unique = (list(counts.values()).count(max(counts.values())) == 1
                  and list(counts.values()).count(min(counts.values())) == 1)
        if ((not raw or 8 <= total <= 20)
                and (not unique_extremes or unique)):
            return topic, counts


def _prompt(prefix, query):
    return f"At the {random.choice(SETTINGS)}, {prefix}\n{query}"


class TallyFrequencyGenerator(ProblemGenerator):
    """Generate exact categorical tally construction and reading tasks."""

    VARIANTS = ("raw_to_table", "tally_to_count", "table_total",
                "most_least", "how_many_more")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _raw():
        topic, counts = _data(raw=True)
        responses = [category for category, count in counts.items()
                     for _ in range(count)]
        random.shuffle(responses)
        answer = text_list(counts)
        prefix = (f"a survey records {topic}. Raw responses: "
                  + ", ".join(responses) + ".")
        steps = [step("STAT_SETUP", "raw categorical responses",
                      f"n={len(responses)}")]
        for category, count in sorted(counts.items()):
            steps.append(step("TALLY_ROW", category, tally_marks(count), count))
        steps.append(step("CHECK", "split",
                          " + ".join(map(str, counts.values())), len(responses)))
        return prefix, steps, answer, {}

    @staticmethod
    def _table(variant):
        topic, counts = _data(unique_extremes=variant == "most_least")
        table = render_tally(counts, f"Tally table for {topic}")
        prefix = f"a survey produced this tally table.\n{table}"
        steps = [step("STAT_SETUP", f"tally table for {topic}",
                      f"{len(counts)} categories")]
        if variant == "tally_to_count":
            target = random.choice(sorted(counts))
            count = counts[target]
            steps.extend([
                step("TALLY_ROW", target, tally_marks(count), count),
                step("CHECK", "groups of five plus singles", count),
            ])
            return prefix, steps, str(count), {"target": target}
        if variant == "table_total":
            values = [counts[category] for category in sorted(counts)]
            for category in sorted(counts):
                steps.append(step("TALLY_ROW", category,
                                  tally_marks(counts[category]), counts[category]))
            additions, total = running_sum_steps(values)
            steps.extend(additions)
            steps.append(step("CHECK", "all rows counted", total))
            return prefix, steps, str(total), {}
        if variant == "most_least":
            most = max(counts, key=counts.get)
            least = min(counts, key=counts.get)
            steps.extend([
                step("TALLY_ROW", most, tally_marks(counts[most]), counts[most]),
                step("TALLY_ROW", least, tally_marks(counts[least]), counts[least]),
                step("CHECK", "unique extremes",
                     f"max {counts[most]}, min {counts[least]}"),
            ])
            answer = (f"most: {most} ({counts[most]}); "
                      f"least: {least} ({counts[least]})")
            return prefix, steps, answer, {}
        high, low = random.sample(sorted(counts), 2)
        if counts[high] < counts[low]:
            high, low = low, high
        if counts[high] == counts[low]:
            alternatives = [(a, b) for a in counts for b in counts
                            if counts[a] > counts[b]]
            if not alternatives:
                return TallyFrequencyGenerator._table(variant)
            high, low = random.choice(alternatives)
        difference = counts[high] - counts[low]
        steps.extend([
            step("TALLY_ROW", high, tally_marks(counts[high]), counts[high]),
            step("TALLY_ROW", low, tally_marks(counts[low]), counts[low]),
            step("S", counts[high], counts[low], difference),
            step("CHECK", f"{high} exceeds {low}", difference),
        ])
        return prefix, steps, str(difference), {"high": high, "low": low}

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "raw_to_table":
            prefix, steps, answer, fields = self._raw()
        else:
            prefix, steps, answer, fields = self._table(variant)
        query = random.choice(QUERIES[variant]).format(**fields)
        problem = _prompt(prefix, query)
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_tally_frequency_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
