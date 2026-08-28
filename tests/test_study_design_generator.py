"""Independent keyword and arithmetic oracles for StudyDesignGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.study_design_generator import QUERIES, StudyDesignGenerator
from helpers import DELIM
from tests import stats_oracle


SAMPLING_FACTS = {
    "numbered every": "frame = complete roster",
    "drew names from a hat": "chance = equal for every name",
    "random number generator": "frame = complete roster",
    "from each grade": "groups = grade level",
    "from each department": "groups = department",
    "within every age group": "groups = age group",
    "every 5th": "interval = 5",
    "every 10th": "interval = 10",
    "every 20th": "interval = 20",
    "picked 4 whole classrooms": "clusters = classrooms",
    "selected 3 entire neighborhoods": "clusters = neighborhoods",
    "all members of the chosen teams": "clusters = teams",
    "the first 30 people she met": "source = first people met",
    "whoever was already in the lobby": "source = lobby occupants",
    "students in her own class": "source = teacher's own class",
    "invited viewers to call in": "respondents chose to participate",
    "posted an online poll": "respondents chose to participate",
    "asked listeners to text": "respondents chose to participate",
}

BIAS_FACTS = {
    "only households with a landline":
        "households without landlines were excluded",
    "left out the night shift": "night-shift workers were excluded",
    "only 12 of the 200 mailed forms came back":
        "188 sampled people did not respond",
    "most people never replied": "many sampled people did not reply",
    "invited viewers to call in": "only viewers who chose to call in",
    "asked listeners to text": "only listeners who chose to text",
    "the first 30 people she met": "only the first people met",
    "Do you agree that the unfair fee should be removed":
        "wording pushes toward yes",
    "Shouldn't the school do more": "wording pushes toward yes",
}

STUDY_FACTS = {
    "the researcher assigned": "the researcher assigned the diets",
    "randomly assigned each plot": "the team assigned the fertilizers",
    "gave half the group": "the investigator assigned the training",
    "recorded what each shopper already":
        "the analyst recorded existing choices",
    "observed without intervening": "the field team assigned no treatment",
    "compared existing records": "the researcher used existing records",
}


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def cue_hit(text, bank):
    hits = [(cue, label) for cue, label in bank.items()
            if cue.lower() in text.lower()]
    if len(hits) != 1:
        raise AssertionError(f"expected one cue, got {hits}: {text}")
    return hits[0]


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    parts = {"body": body, "variant": variant, "query": query}
    if variant == "sampling_method":
        cue, label = cue_hit(body, stats_oracle.SAMPLING_CUES)
        answer = f"{label}; {SAMPLING_FACTS[cue]}"
        parts.update(cue=cue, label=label, fact=SAMPLING_FACTS[cue],
                     answer=answer)
    elif variant == "bias_identify":
        cue, label = cue_hit(body, stats_oracle.BIAS_CUES)
        answer = f"{label}; {BIAS_FACTS[cue]}"
        parts.update(cue=cue, label=label, fact=BIAS_FACTS[cue],
                     answer=answer)
    elif variant == "experiment_vs_observational":
        cue, label = cue_hit(body, stats_oracle.DESIGN_CUES)
        answer = f"{label}; {STUDY_FACTS[cue]}"
        parts.update(cue=cue, label=label, fact=STUDY_FACTS[cue],
                     answer=answer)
    elif variant == "design_elements":
        explanatory, response, count, unit = re.search(
            r"varies (.+) and records (.+) for each of (\d+) (.+)\.",
            body).groups()
        answer = (f"explanatory: {explanatory}; response: {response}; "
                  f"units: {count} {unit}")
        parts.update(explanatory=explanatory, response=response,
                     count=int(count), unit=unit, answer=answer)
    elif variant == "systematic_select":
        population, interval, start = map(int, re.search(
            r"N = (\d+)\. Select every (\d+)(?:st|nd|rd|th) ID "
            r"beginning at (\d+)\.", body).groups())
        selected = list(range(start, population + 1, interval))
        parts.update(population=population, interval=interval, start=start,
                     selected=selected,
                     answer=", ".join(map(str, selected)))
    elif variant == "stratified_allocate":
        roster, sample_size = re.search(
            r"stratum populations are (.+)\. Choose a proportional "
            r"stratified sample of n = (\d+)\.", body).groups()
        groups = []
        for cell in roster.split("; "):
            name, size = cell.rsplit(" = ", 1)
            groups.append((name, int(size)))
        sample_size = int(sample_size)
        total = sum(size for _, size in groups)
        allocations = []
        for name, size in groups:
            allocation = Fraction(size * sample_size, total)
            if allocation.denominator != 1:
                raise AssertionError((groups, sample_size))
            allocations.append((name, int(allocation)))
        parts.update(groups=groups, sample_size=sample_size, total=total,
                     allocations=allocations,
                     answer="; ".join(f"{name} {count}"
                                      for name, count in allocations))
    else:
        upper, sample_size = map(int, re.search(
            r"labeled 01-(\d+)\..+stop after choosing (\d+)\.",
            body, re.DOTALL).groups())
        digits = re.search(r"Digits: (\d+)", body).group(1)
        tokens = [int(digits[index:index + 2])
                  for index in range(0, len(digits), 2)]
        chosen = []
        trace = []
        for value in tokens:
            label = f"{value:02d}"
            if value < 1 or value > upper:
                reason = f"> {upper}" if value > upper else f"outside 01-{upper:02d}"
                trace.append((label, "reject", reason))
            elif value in chosen:
                trace.append((label, "reject", "repeat"))
            else:
                chosen.append(value)
                trace.append((label, "accept"))
                if len(chosen) == sample_size:
                    break
        parts.update(upper=upper, sample_size=sample_size, digits=digits,
                     chosen=chosen, trace=trace,
                     answer=", ".join(f"{value:02d}" for value in chosen))
    return parts


def wrapper_kind(text):
    if text.startswith("At "):
        return "at"
    if text.startswith("During the "):
        return "during"
    if " reported this procedure for " in text:
        return "reported"
    if text.startswith("For the "):
        return "for"
    if text.startswith("A protocol used by "):
        return "protocol"
    if " followed this method at " in text:
        return "followed"
    raise AssertionError(text)


class StudyDesignGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(725903)

    def test_output_contract(self):
        example = StudyDesignGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_1000_answers_from_problem_text(self):
        generator = StudyDesignGenerator()
        for _ in range(1000):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_classification_has_exactly_one_independent_oracle_cue(self):
        cases = (
            ("sampling_method", stats_oracle.SAMPLING_CUES),
            ("bias_identify", stats_oracle.BIAS_CUES),
            ("experiment_vs_observational", stats_oracle.DESIGN_CUES),
        )
        for variant, bank in cases:
            generator = StudyDesignGenerator(variant)
            for _ in range(500):
                example = generator.generate()
                parts = oracle_parts(example)
                hits = [(cue, label) for cue, label in bank.items()
                        if cue.lower() in parts["body"].lower()]
                self.assertEqual(hits, [(parts["cue"], parts["label"])])
                cue_step = next(raw.split(DELIM) for raw in example["steps"]
                                if raw.startswith(f"DESIGN_CUE{DELIM}"))
                self.assertEqual(cue_step[1], f'"{parts["cue"]}"')
                self.assertEqual(cue_step[2], parts["label"])

    def test_every_classification_label_reaches_all_six_templates(self):
        cases = (
            ("sampling_method", set(stats_oracle.SAMPLING_CUES.values())),
            ("bias_identify", set(stats_oracle.BIAS_CUES.values())),
            ("experiment_vs_observational", set(stats_oracle.DESIGN_CUES.values())),
        )
        expected = {"at", "during", "reported", "for", "protocol", "followed"}
        for variant, labels in cases:
            seen = {label: set() for label in labels}
            generator = StudyDesignGenerator(variant)
            for _ in range(2400):
                parts = oracle_parts(generator.generate())
                seen[parts["label"]].add(wrapper_kind(parts["body"]))
            self.assertEqual({label: expected for label in labels}, seen)

    def test_design_element_labels_match_printed_scenario(self):
        generator = StudyDesignGenerator("design_elements")
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            labels = {fields[1]: fields[2] for fields in
                      (raw.split(DELIM) for raw in example["steps"])
                      if fields[0] == "LABEL"}
            self.assertEqual(labels, {
                "explanatory": parts["explanatory"],
                "response": parts["response"],
                "units": f"{parts['count']} {parts['unit']}",
            })

    def test_systematic_additions_and_selected_ids_are_exact(self):
        generator = StudyDesignGenerator("systematic_select")
        seen_intervals = set()
        for _ in range(400):
            example = generator.generate()
            parts = oracle_parts(example)
            seen_intervals.add(parts["interval"])
            picks = [int(raw.split(DELIM)[2]) for raw in example["steps"]
                     if raw.startswith(f"SYSTEMATIC_PICK{DELIM}")]
            self.assertEqual(picks, parts["selected"])
            additions = [raw.split(DELIM) for raw in example["steps"]
                         if raw.startswith(f"A{DELIM}")]
            self.assertEqual(len(additions), len(picks) - 1)
            for fields in additions:
                self.assertEqual(int(fields[1]) + int(fields[2]),
                                 int(fields[3]), DELIM.join(fields))
        self.assertEqual(seen_intervals, {3, 4, 5, 6, 8, 10, 12})

    def test_stratified_allocation_recomputes_all_arithmetic(self):
        generator = StudyDesignGenerator("stratified_allocate")
        seen_group_counts = set()
        for _ in range(400):
            example = generator.generate()
            parts = oracle_parts(example)
            seen_group_counts.add(len(parts["groups"]))
            sum_step = next(raw.split(DELIM) for raw in example["steps"]
                            if raw.startswith(f"SUM{DELIM}"))
            self.assertEqual(sum(map(int, sum_step[1].split(" + "))),
                             int(sum_step[2]))
            rows = [raw.split(DELIM) for raw in example["steps"]
                    if raw.startswith(f"ALLOCATE{DELIM}")]
            self.assertEqual([(row[1], int(row[3])) for row in rows],
                             parts["allocations"])
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
        self.assertEqual(seen_group_counts, {2, 3, 4})

    def test_random_digit_trace_rejects_invalid_and_repeats(self):
        generator = StudyDesignGenerator("random_digit_select")
        seen_sizes = set()
        for _ in range(400):
            example = generator.generate()
            parts = oracle_parts(example)
            seen_sizes.add(parts["sample_size"])
            trace = []
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "DIGIT_PICK":
                    trace.append(tuple(fields[1:]))
            self.assertEqual(trace, parts["trace"])
            self.assertTrue(any(row[1:] == ("reject", "repeat")
                                for row in trace))
            self.assertTrue(any(row[0] == "00" and row[1] == "reject"
                                for row in trace))
            self.assertTrue(any(row[1:] == ("reject", "> 40")
                                for row in trace))
            self.assertEqual(len(parts["chosen"]), parts["sample_size"])
            self.assertEqual(len(parts["chosen"]), len(set(parts["chosen"])))
        self.assertEqual(seen_sizes, {3, 4, 5, 6})

    def test_all_variants_and_four_queries_are_reachable(self):
        for variant in StudyDesignGenerator.VARIANTS:
            generator = StudyDesignGenerator(variant)
            seen = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"statistics_study_design_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            StudyDesignGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = StudyDesignGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            rendered = "\n".join([example["problem"], *example["steps"],
                                    example["final_answer"]])
            self.assertNotRegex(rendered, r"1x|\^1\b|\+ 0|--|− -|\b3th ID\b")
            for raw in example["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
