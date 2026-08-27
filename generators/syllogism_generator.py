"""Classify categorical syllogisms by mood, figure, and finite models.

Variants:
- ``validity`` asks whether the conclusion is forced by the premises.
- ``mood_figure`` emphasizes the three proposition types and term positions.
- ``venn_test`` emphasizes the regions shaded or marked in a Venn test.

The generator ranges over all 256 mood/figure forms under modern Boolean
semantics (universals have no existential import).  It exhausts all subsets
of a three-element universe, so an invalid form has an explicit countermodel.

Op-codes:
- ``MOOD``: record the A/E/I/O mood and standard figure.
- ``VENN_SHADE``: mark a region empty for a universal premise.
- ``VENN_MARK``: place a witness for a particular premise.
- ``CONCLUSION_CHECK``: state whether every premise-model forces the result.
- ``COUNTERMODEL``: give the first finite model refuting the conclusion.
- ``CHECK``: verify the finite-model search result.
- ``Z``: composite validity and mood/figure answer.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step


FOUNDATIONS = True


NOUNS = (
    "artists", "bakers", "climbers", "dancers", "editors", "farmers",
    "gardeners", "historians", "inventors", "jewelers", "kayakers",
    "librarians", "musicians", "nurses", "orators", "painters", "pilots",
    "poets", "researchers", "sailors", "teachers", "travelers", "weavers",
    "writers",
)

QUERIES = {
    "validity": (
        "Decide whether the conclusion follows under modern Boolean semantics.",
        "Classify the argument as valid or invalid and report its form.",
        "Test whether every model of the premises satisfies the conclusion.",
        "Determine validity without assuming that universal classes are nonempty.",
        "Use finite models to decide whether the conclusion is forced.",
    ),
    "mood_figure": (
        "Identify the mood and figure, then determine validity.",
        "Name the A/E/I/O form and its standard figure before classifying it.",
        "Report the categorical form and say whether it is valid.",
        "Determine the mood-figure code and its Boolean validity.",
        "Classify the term arrangement, proposition types, and validity.",
    ),
    "venn_test": (
        "Use a three-circle Venn test to determine validity and form.",
        "Shade universal regions, place particular witnesses, and classify it.",
        "Apply the Venn-diagram test under modern Boolean semantics.",
        "Record the forced empty regions and witnesses before deciding validity.",
        "Test the conclusion from the premise markings and report the form.",
    ),
}


def proposition(letter, subject, predicate):
    if letter == "A":
        return f"All {subject} are {predicate}"
    if letter == "E":
        return f"No {subject} are {predicate}"
    if letter == "I":
        return f"Some {subject} are {predicate}"
    if letter == "O":
        return f"Some {subject} are not {predicate}"
    raise ValueError("categorical proposition must be A, E, I, or O")


def term_positions(figure, subject, middle, predicate):
    """Return ``(major subject/predicate, minor subject/predicate)``."""
    if figure == 1:
        return (middle, predicate), (subject, middle)
    if figure == 2:
        return (predicate, middle), (subject, middle)
    if figure == 3:
        return (middle, predicate), (middle, subject)
    if figure == 4:
        return (predicate, middle), (middle, subject)
    raise ValueError("figure must be 1, 2, 3, or 4")


def holds(letter, subject_mask, predicate_mask):
    universe = 0b111
    if letter == "A":
        return (subject_mask & (universe ^ predicate_mask)) == 0
    if letter == "E":
        return (subject_mask & predicate_mask) == 0
    if letter == "I":
        return (subject_mask & predicate_mask) != 0
    if letter == "O":
        return (subject_mask & (universe ^ predicate_mask)) != 0
    raise ValueError("categorical proposition must be A, E, I, or O")


def first_countermodel(mood, figure):
    major_letter, minor_letter, conclusion_letter = mood
    major_pos, minor_pos = term_positions(figure, "S", "M", "P")
    for subject_mask in range(8):
        for middle_mask in range(8):
            for predicate_mask in range(8):
                model = {"S": subject_mask, "M": middle_mask,
                         "P": predicate_mask}
                if not holds(major_letter, model[major_pos[0]],
                             model[major_pos[1]]):
                    continue
                if not holds(minor_letter, model[minor_pos[0]],
                             model[minor_pos[1]]):
                    continue
                if not holds(conclusion_letter, subject_mask, predicate_mask):
                    return model
    return None


def membership_column(mask):
    return "".join("T" if mask & (1 << index) else "F"
                   for index in range(3))


def venn_step(letter, subject, predicate, witness):
    if letter == "A":
        return step("VENN_SHADE", f"{subject} − {predicate}", "empty")
    if letter == "E":
        return step("VENN_SHADE", f"{subject} ∩ {predicate}", "empty")
    if letter == "I":
        return step("VENN_MARK", f"{subject} ∩ {predicate}", witness)
    return step("VENN_MARK", f"{subject} ∩ ¬{predicate}", witness)


class SyllogismGenerator(ProblemGenerator):
    """Generate all categorical moods and figures with exact model checks."""

    VARIANTS = ("validity", "mood_figure", "venn_test")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        mood = "".join(random.choice("AEIO") for _ in range(3))
        figure = random.randint(1, 4)
        subject, middle, predicate = random.sample(NOUNS, 3)
        major_pos, minor_pos = term_positions(figure, subject, middle, predicate)
        major = proposition(mood[0], *major_pos)
        minor = proposition(mood[1], *minor_pos)
        conclusion = proposition(mood[2], subject, predicate)
        query = random.choice(QUERIES[variant])
        problem = (f"Premises: {major}; {minor}. Conclusion: {conclusion}. "
                   f"{query}")

        countermodel = first_countermodel(mood, figure)
        valid = countermodel is None
        steps = [step("MOOD", mood, f"figure {figure}"),
                 venn_step(mood[0], *major_pos, "x1"),
                 venn_step(mood[1], *minor_pos, "x2"),
                 step("CONCLUSION_CHECK", "forced" if valid else "not forced")]
        if countermodel is not None:
            named = ((subject, countermodel["S"]),
                     (middle, countermodel["M"]),
                     (predicate, countermodel["P"]))
            model_text = ", ".join(
                f"{name}={membership_column(mask)}" for name, mask in named)
            steps.append(step("COUNTERMODEL", model_text))
            steps.append(step("CHECK", "countermodel", "premises=T,T",
                              "conclusion=F"))
        else:
            steps.append(step("CHECK", "all 512 assignments",
                              "no countermodel"))
        answer = f"{'valid' if valid else 'invalid'}; {mood}-{figure}"
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"syllogism_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
