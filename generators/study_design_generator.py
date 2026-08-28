"""Study-design classification and exact mechanical selection procedures.

Variants: ``sampling_method``, ``bias_identify``,
``experiment_vs_observational``, ``design_elements``,
``systematic_select``, ``stratified_allocate``, and
``random_digit_select``. Classification scenarios are exact by construction:
each contains one cue from a disjoint label bank and six wrapper templates
provide phrasing diversity. Numeric procedures use integer systematic lists,
backward-built proportional allocations, and a supplied two-digit stream
whose accept/reject trace is recomputable from the problem alone.
Op-codes: ``DESIGN_CUE``, ``LABEL``, ``RULE``, ``SYSTEMATIC_PICK``,
``DIGIT_PICK``, ``ALLOCATE``, ``SUM``, ``A``, ``D``, ``M``, and ``Z``.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt


STATISTICS = True

SETTINGS = (
    "north campus", "south campus", "river center", "lake center",
    "maple school", "oak school", "pine clinic", "cedar clinic",
    "amber office", "birch office", "granite plant", "harbor station",
)
PROJECTS = (
    "attendance review", "community survey", "health study",
    "service audit", "transportation study", "nutrition review",
    "workplace survey", "education study", "housing review",
    "recreation survey", "environment study", "consumer study",
)
ACTORS = (
    "the coordinator", "the analyst", "the principal", "the director",
    "the nurse", "the planner", "the researcher", "the supervisor",
    "the survey team", "the review board", "the field team", "the office",
)

# Six genuinely different sentence structures. Combined with every cue and
# the subject/setting banks, each classification label has far more than the
# plan's six-template minimum.
SCENARIO_WRAPPERS = (
    "At {setting} ({record}), {clause}.",
    "During the {project} ({record}), {clause}.",
    "{actor} reported this procedure for {record}: {clause}.",
    "For the {project} at {setting} ({record}), {clause}.",
    "A protocol used by {actor} for {record} says that {clause}.",
    "The {project} followed this method at {setting} ({record}): {clause}.",
)


SAMPLING_SCENARIOS = {
    "SRS": (
        ("numbered every", "the team numbered every person on the complete "
         "roster and drew labels fairly", "frame = complete roster"),
        ("drew names from a hat", "the team drew names from a hat after "
         "mixing the complete roster", "chance = equal for every name"),
        ("random number generator", "the team used a random number generator "
         "on the complete numbered roster", "frame = complete roster"),
    ),
    "stratified": (
        ("from each grade", "the team selected students from each grade",
         "groups = grade level"),
        ("from each department", "the team selected employees from each "
         "department", "groups = department"),
        ("within every age group", "the team sampled separately within every "
         "age group", "groups = age group"),
    ),
    "systematic": (
        ("every 5th", "after a random start, the team selected every 5th "
         "name", "interval = 5"),
        ("every 10th", "after a random start, the team selected every 10th "
         "name", "interval = 10"),
        ("every 20th", "after a random start, the team selected every 20th "
         "name", "interval = 20"),
    ),
    "cluster": (
        ("picked 4 whole classrooms", "the team picked 4 whole classrooms "
         "and surveyed everyone in them", "clusters = classrooms"),
        ("selected 3 entire neighborhoods", "the team selected 3 entire "
         "neighborhoods and surveyed every household there",
         "clusters = neighborhoods"),
        ("all members of the chosen teams", "the team surveyed all members "
         "of the chosen teams", "clusters = teams"),
    ),
    "convenience": (
        ("the first 30 people she met", "the interviewer used the first 30 "
         "people she met", "source = first people met"),
        ("whoever was already in the lobby", "the interviewer surveyed "
         "whoever was already in the lobby", "source = lobby occupants"),
        ("students in her own class", "the teacher surveyed students in her "
         "own class", "source = teacher's own class"),
    ),
    "voluntary response": (
        ("invited viewers to call in", "the station invited viewers to call "
         "in with an opinion", "respondents chose to participate"),
        ("posted an online poll", "the organization posted an online poll "
         "that anyone could answer", "respondents chose to participate"),
        ("asked listeners to text", "the host asked listeners to text their "
         "opinions", "respondents chose to participate"),
    ),
}


BIAS_SCENARIOS = {
    "undercoverage": (
        ("only households with a landline", "the calling list included only "
         "households with a landline", "households without landlines were excluded"),
        ("left out the night shift", "the employee list left out the night "
         "shift", "night-shift workers were excluded"),
    ),
    "nonresponse": (
        ("only 12 of the 200 mailed forms came back", "only 12 of the 200 "
         "mailed forms came back", "188 sampled people did not respond"),
        ("most people never replied", "the team contacted a random sample, "
         "but most people never replied", "many sampled people did not reply"),
    ),
    "voluntary response": (
        ("invited viewers to call in", "a television host invited viewers to "
         "call in", "only viewers who chose to call in"),
        ("asked listeners to text", "a radio host asked listeners to text "
         "their answer", "only listeners who chose to text"),
    ),
    "convenience": (
        ("the first 30 people she met", "an interviewer questioned the first "
         "30 people she met", "only the first people met"),
    ),
    "leading question": (
        ("Do you agree that the unfair fee should be removed",
         "the survey asked, “Do you agree that the unfair fee should be "
         "removed?”", "wording pushes toward yes"),
        ("Shouldn't the school do more", "the survey asked, “Shouldn't the "
         "school do more?”", "wording pushes toward yes"),
    ),
}


STUDY_SCENARIOS = {
    "experiment": (
        ("the researcher assigned", "the researcher assigned the diets to "
         "the volunteers", "the researcher assigned the diets"),
        ("randomly assigned each plot", "the team randomly assigned each plot "
         "to a fertilizer", "the team assigned the fertilizers"),
        ("gave half the group", "the investigator gave half the group a "
         "training program", "the investigator assigned the training"),
    ),
    "observational": (
        ("recorded what each shopper already", "the analyst recorded what each "
         "shopper already purchased", "the analyst recorded existing choices"),
        ("observed without intervening", "the field team observed without "
         "intervening", "the field team assigned no treatment"),
        ("compared existing records", "the researcher compared existing "
         "records from two clinics", "the researcher used existing records"),
    ),
}


ELEMENT_BANK = (
    ("fertilizer", "yield", "plots"),
    ("sleep duration", "reaction time", "volunteers"),
    ("tutoring method", "test score", "students"),
    ("water temperature", "growth rate", "dishes"),
    ("feed type", "weight gain", "calves"),
    ("exercise program", "resting pulse", "adults"),
    ("paint formula", "drying time", "boards"),
    ("irrigation amount", "crop height", "rows"),
    ("screen brightness", "battery life", "phones"),
    ("packaging type", "breakage rate", "boxes"),
    ("music condition", "recall score", "participants"),
    ("storage temperature", "shelf life", "samples"),
)

STRATA_BANK = (
    ("freshmen", "sophomores"),
    ("grade 9", "grade 10", "grade 11"),
    ("sales", "service", "engineering"),
    ("north", "central", "south", "west"),
    ("morning", "afternoon", "evening"),
    ("urban", "suburban", "rural"),
    ("small firms", "medium firms", "large firms"),
    ("ages 18-29", "ages 30-49", "ages 50+"),
)

QUERIES = {
    "sampling_method": (
        "Identify the sampling method and give the defining feature.",
        "Classify how the sample was selected.",
        "Name the sampling design and report its grouping, interval, or source.",
        "Which sampling method does this procedure use?",
    ),
    "bias_identify": (
        "Identify the main source of bias and the checkable reason.",
        "Classify the survey bias shown here.",
        "Name the bias mechanism and state who or what caused it.",
        "Which type of bias is most directly present?",
    ),
    "experiment_vs_observational": (
        "Classify the study and state the evidence about treatment assignment.",
        "Is this an experiment or an observational study?",
        "Name the study type and give its defining cue.",
        "Determine whether a treatment was assigned.",
    ),
    "design_elements": (
        "Identify the explanatory variable, response variable, and units.",
        "Label the three core design elements.",
        "State what is varied, what is measured, and on what objects.",
        "Report the explanatory variable, response, and experimental units.",
    ),
    "systematic_select": (
        "List every ID selected by the systematic rule.",
        "Carry out the systematic sample.",
        "Starting at the stated ID, add the interval until the frame ends.",
        "Which population IDs enter the sample?",
    ),
    "stratified_allocate": (
        "Allocate the sample proportionally across the strata.",
        "Find the integer sample count for every group.",
        "Use each stratum's population share to divide the sample.",
        "Report the proportional stratified allocation.",
    ),
    "random_digit_select": (
        "Read the digit line and list the accepted labels in order.",
        "Carry out the random-digit selection trace.",
        "Reject invalid or repeated pairs and stop at the requested size.",
        "Which two-digit labels form the sample?",
    ),
}


def _context():
    return {"setting": random.choice(SETTINGS),
            "project": random.choice(PROJECTS),
            "actor": random.choice(ACTORS),
            "record": f"design {random.choice('ABCDEFGH')}{random.randint(10, 99)}"}


def _site():
    record = f"design {random.choice('ABCDEFGH')}{random.randint(10, 99)}"
    return (f"{random.choice(SETTINGS)} during the "
            f"{random.choice(PROJECTS)} ({record})")


def _wrap(clause):
    return random.choice(SCENARIO_WRAPPERS).format(clause=clause, **_context())


def _ordinal(value):
    if 10 <= value % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(value % 10, "th")
    return f"{value}{suffix}"


class StudyDesignGenerator(ProblemGenerator):
    """Generate study-design labels and exact sample-selection traces.

    Variants, construction guarantees, and op-codes are listed in the module
    docstring. Every classification answer is composite and every numeric
    answer can be reconstructed solely from the printed frame or digit line.
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
                "operation": f"statistics_study_design_{variant}",
                "problem": problem, "steps": steps,
                "final_answer": answer}

    @staticmethod
    def _classification(variant, bank, label_name):
        label = random.choice(tuple(bank))
        cue, clause, fact = random.choice(bank[label])
        scenario = _wrap(clause)
        answer = f"{label}; {fact}"
        steps = [step("DESIGN_CUE", f'"{cue}"', label),
                 step("LABEL", label_name, fact)]
        problem = f"{scenario}\n{random.choice(QUERIES[variant])}"
        return StudyDesignGenerator._result(
            variant, problem, steps, answer)

    def _design_elements(self):
        explanatory, response, unit = random.choice(ELEMENT_BANK)
        count = random.randint(12, 60)
        scenario = (f"At the {_site()}, a researcher varies "
                    f"{explanatory} and records {response} for each of "
                    f"{count} {unit}.")
        answer = (f"explanatory: {explanatory}; response: {response}; "
                  f"units: {count} {unit}")
        steps = [step("LABEL", "explanatory", explanatory),
                 step("LABEL", "response", response),
                 step("LABEL", "units", f"{count} {unit}")]
        problem = f"{scenario}\n{random.choice(QUERIES['design_elements'])}"
        return self._result("design_elements", problem, steps, answer)

    def _systematic_select(self):
        interval = random.choice((3, 4, 5, 6, 8, 10, 12))
        sample_size = random.randint(6, 12)
        population = interval * sample_size
        start = random.randint(1, interval)
        selected = list(range(start, population + 1, interval))
        steps = [step("RULE", "systematic sample",
                      f"start at {start}; add {interval}; stop after {population}"),
                 step("SYSTEMATIC_PICK", 1, start)]
        for index, (previous, current) in enumerate(
                zip(selected, selected[1:]), 2):
            steps.extend([step("A", previous, interval, current),
                          step("SYSTEMATIC_PICK", index, current)])
        answer = ", ".join(map(str, selected))
        problem = (f"At the {_site()}, population IDs are 1 "
                   f"through N = {population}. Select every {_ordinal(interval)} ID "
                   f"beginning at {start}.\n"
                   f"{random.choice(QUERIES['systematic_select'])}")
        return self._result("systematic_select", problem, steps, answer)

    def _stratified_allocate(self):
        names = random.choice(STRATA_BANK)
        allocations = [random.randint(4, 20) for _ in names]
        multiplier = random.randint(2, 8)
        populations = [value * multiplier for value in allocations]
        total_population = sum(populations)
        sample_size = sum(allocations)
        steps = [step("SUM", " + ".join(map(str, populations)),
                      total_population)]
        for name, population, allocation in zip(
                names, populations, allocations):
            proportion = prob_txt(Fraction(population, total_population))
            steps.extend([
                step("D", population, total_population, proportion),
                step("M", proportion, sample_size, allocation),
                step("ALLOCATE", name,
                     f"{population}/{total_population} × {sample_size}",
                     allocation),
            ])
        roster = "; ".join(f"{name} = {size}" for name, size in
                           zip(names, populations))
        answer = "; ".join(f"{name} {count}" for name, count in
                           zip(names, allocations))
        problem = (f"At the {_site()}, the stratum populations "
                   f"are {roster}. Choose a proportional stratified sample "
                   f"of n = {sample_size}.\n"
                   f"{random.choice(QUERIES['stratified_allocate'])}")
        return self._result("stratified_allocate", problem, steps, answer)

    def _random_digit_select(self):
        upper = 40
        sample_size = random.randint(3, 6)
        accepted = random.sample(range(1, upper + 1), sample_size)
        invalid_one = random.randint(41, 99)
        invalid_two = random.randint(41, 99)
        tokens = [invalid_one, accepted[0], accepted[0], 0, accepted[1],
                  invalid_two, *accepted[2:]]
        tokens.extend(random.randint(0, 99) for _ in range(4))
        digits = "".join(f"{value:02d}" for value in tokens)
        chosen = []
        steps = [step("RULE", "random-digit sample",
                      f"read pairs; accept 01-{upper:02d} once; stop after {sample_size}")]
        for value in tokens:
            label = f"{value:02d}"
            if value < 1 or value > upper:
                reason = (f"> {upper}" if value > upper else
                          f"outside 01-{upper:02d}")
                steps.append(step("DIGIT_PICK", label, "reject", reason))
            elif value in chosen:
                steps.append(step("DIGIT_PICK", label, "reject", "repeat"))
            else:
                chosen.append(value)
                steps.append(step("DIGIT_PICK", label, "accept"))
                if len(chosen) == sample_size:
                    break
        answer = ", ".join(f"{value:02d}" for value in chosen)
        problem = (f"At the {_site()}, people are labeled "
                   f"01-{upper:02d}. Read the supplied digit line left to "
                   f"right in nonoverlapping two-digit pairs, accept valid "
                   f"labels only once, and stop after choosing {sample_size}.\n"
                   f"Digits: {digits}\n"
                   f"{random.choice(QUERIES['random_digit_select'])}")
        return self._result("random_digit_select", problem, steps, answer)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "sampling_method":
            return self._classification(
                variant, SAMPLING_SCENARIOS, "sampling feature")
        if variant == "bias_identify":
            return self._classification(
                variant, BIAS_SCENARIOS, "bias mechanism")
        if variant == "experiment_vs_observational":
            return self._classification(
                variant, STUDY_SCENARIOS, "study evidence")
        if variant == "design_elements":
            return self._design_elements()
        if variant == "systematic_select":
            return self._systematic_select()
        if variant == "stratified_allocate":
            return self._stratified_allocate()
        return self._random_digit_select()
