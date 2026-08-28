"""Set up hypotheses, parameters, errors, and inference conditions.

Variants: ``state_hypotheses``, ``parameter_identify``,
``type_I_II_describe``, ``np_condition``, ``ten_percent_condition``,
``clt_condition``, and ``min_n_for_np``. Language variants invert explicit
scenario templates; numeric variants show every large-count, 10%, or CLT
calculation. ``min_n_for_np`` solves both inequalities and takes the larger
exact ceiling. Op-codes: ``HYP_STATE``, ``PARAMETER``, ``ERROR_TYPE``,
``RULE``, ``CLT_CHECK``, ``REWRITE``, ``CEIL``, ``MAX``, ``M``, ``D``,
``S``, ``CHECK``, and ``Z``.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt
from stats_common import num_txt


STATISTICS = True
VENUES = (
    "amber study", "birch survey", "cedar trial", "delta project",
    "ember lab", "forest audit", "granite program", "harbor test",
    "indigo review", "jade pilot", "kestrel study", "lunar trial",
)
LOCATIONS = (
    "north campus", "south campus", "east annex", "west annex",
    "river center", "lake center", "hill school", "valley school",
    "maple office", "oak office", "pine clinic", "cedar clinic",
)
SCENARIOS = (
    ("p", "the proportion of all city voters who approve"),
    ("p", "the proportion of all inspected components that pass"),
    ("p", "the proportion of all customers who renew"),
    ("p", "the proportion of all planted seeds that germinate"),
    ("p", "the proportion of all packages that arrive on time"),
    ("p", "the proportion of all devices that connect successfully"),
    ("p", "the proportion of all applicants who qualify"),
    ("p", "the proportion of all lab samples that test positive"),
    ("p", "the proportion of all orders that ship today"),
    ("p", "the proportion of all students who complete the course"),
    ("p", "the proportion of all households that recycle weekly"),
    ("p", "the proportion of all patients who improve"),
    ("μ", "the mean fill volume of all bottles"),
    ("μ", "the mean commute time of all employees"),
    ("μ", "the mean battery life of all devices"),
    ("μ", "the mean package weight of all shipments"),
    ("μ", "the mean exam score of all students"),
    ("μ", "the mean response time of all servers"),
    ("μ", "the mean daily output of all machines"),
    ("μ", "the mean wait time of all customers"),
    ("μ", "the mean water use of all households"),
    ("μ", "the mean delivery time of all orders"),
    ("μ", "the mean recovery time of all patients"),
    ("μ", "the mean weekly mileage of all drivers"),
)
DIRECTIONS = {
    "less": ("less than", "<", "left-tailed"),
    "greater": ("greater than", ">", "right-tailed"),
    "different": ("different from", "≠", "two-tailed"),
}
QUERIES = {
    "state_hypotheses": (
        "Write H0 and Ha and name the tail.",
        "Translate the research suspicion into hypotheses.",
        "State the null, alternative, and test direction.",
        "Give the complete hypothesis setup.",
    ),
    "parameter_identify": (
        "Identify and interpret the population parameter.",
        "Is the target p or μ? Give its full meaning.",
        "Name the parameter represented by the research target.",
        "Report the symbol and population-level interpretation.",
    ),
    "type_I_II_describe": (
        "Classify the described error and restate it.",
        "Is this a Type I or Type II error? Include the consequence.",
        "Name the hypothesis-testing error in composite form.",
        "Use H0 and Ha to identify the stated mistake.",
    ),
    "np_condition": (
        "Check both large-count conditions.",
        "Decide whether np ≥ 10 and n(1 − p) ≥ 10 hold.",
        "Evaluate the success and failure count requirements.",
        "Give a composite pass-or-fail large-count result.",
    ),
    "ten_percent_condition": (
        "Check the 10% condition.",
        "Decide whether n ≤ N/10.",
        "Compare the sample size with one tenth of the population.",
        "Give a composite pass-or-fail independence check.",
    ),
    "clt_condition": (
        "Decide whether the sample mean is approximately normal.",
        "Apply the stated population-shape or n ≥ 30 rule.",
        "Check whether a normal model for x̄ is justified.",
        "Give a composite CLT-condition result.",
    ),
    "min_n_for_np": (
        "Find the smallest integer n satisfying both large-count conditions.",
        "Solve np ≥ 10 and n(1 − p) ≥ 10 for the minimum n.",
        "Take the larger of the two required sample-size ceilings.",
        "What minimum sample size meets both count rules?",
    ),
}


def _site():
    code = f"sample {random.choice('ABCDEFGH')}{random.randint(10, 99)}"
    return (f"{random.choice(LOCATIONS)} during the "
            f"{random.choice(VENUES)} ({code})")


def _null_value(parameter):
    if parameter == "p":
        return Fraction(random.randint(1, 9), 10)
    return Fraction(random.randint(20, 900))


def _ceil(value):
    value = Fraction(value)
    return -(-value.numerator // value.denominator)


class InferenceSetupGenerator(ProblemGenerator):
    """Generate exact, parseable inference-setup procedures."""

    VARIANTS = ("state_hypotheses", "parameter_identify",
                "type_I_II_describe", "np_condition",
                "ten_percent_condition", "clt_condition", "min_n_for_np")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _language(variant):
        parameter, description = random.choice(SCENARIOS)
        if variant == "parameter_identify":
            prefix = (f"At the {_site()}, a study will estimate {description}. "
                      "The target is population-level, not just the observed sample.")
            steps = [step("PARAMETER", description, parameter)]
            answer = f"{parameter}; {description}"
            return prefix, steps, answer

        null = _null_value(parameter)
        null_text = num_txt(null)
        direction = random.choice(tuple(DIRECTIONS))
        phrase, relation, tail = DIRECTIONS[direction]
        hypotheses = (f"H0: {parameter} = {null_text}; "
                      f"Ha: {parameter} {relation} {null_text}")
        if variant == "state_hypotheses":
            prefix = (f"At the {_site()}, the target quantity is {description}. "
                      f"Its historical value is {null_text}. A researcher suspects "
                      f"this population quantity is {phrase} its historical value.")
            steps = [step("HYP_STATE", f"H0: {parameter} = {null_text}",
                          f"Ha: {parameter} {relation} {null_text}", tail)]
            answer = f"{hypotheses}; {tail}"
            return prefix, steps, answer

        error_type = random.choice(("Type I", "Type II"))
        if error_type == "Type I":
            consequence = (f"concluding {parameter} {relation} {null_text} "
                           f"when {parameter} = {null_text}")
        else:
            consequence = (f"failing to conclude {parameter} {relation} {null_text} "
                           f"when {parameter} {relation} {null_text}")
        prefix = (f"At the {_site()}, a test of {description} uses {hypotheses}. "
                  f"Error described: {consequence}.")
        steps = [step("HYP_STATE", f"H0: {parameter} = {null_text}",
                      f"Ha: {parameter} {relation} {null_text}", tail),
                 step("ERROR_TYPE", consequence, error_type)]
        answer = f"{error_type}; {consequence}"
        return prefix, steps, answer

    @staticmethod
    def _np_condition():
        p = Fraction(random.randint(1, 9), 10)
        n = random.randint(10, 250)
        successes, failures = n * p, n * (1 - p)
        ok = successes >= 10 and failures >= 10
        rs = "≥" if successes >= 10 else "<"
        rf = "≥" if failures >= 10 else "<"
        answer = (f"{'ok' if ok else 'fails'}; np = {num_txt(successes)} {rs} 10, "
                  f"n(1 − p) = {num_txt(failures)} {rf} 10")
        prefix = (f"At the {_site()}, a random sample has n = {n} and null "
                  f"proportion p = {prob_txt(p)}. Use the rule np ≥ 10 and "
                  "n(1 − p) ≥ 10.")
        steps = [step("RULE", "large counts", "np ≥ 10 and n(1 − p) ≥ 10"),
                 step("M", n, prob_txt(p), num_txt(successes)),
                 step("S", 1, prob_txt(p), prob_txt(1 - p)),
                 step("M", n, prob_txt(1 - p), num_txt(failures)),
                 step("CHECK", "large counts",
                      f"{num_txt(successes)} {rs} 10, {num_txt(failures)} {rf} 10",
                      "ok" if ok else "fails")]
        return prefix, steps, answer

    @staticmethod
    def _ten_percent():
        limit = random.randint(10, 900)
        population = 10 * limit
        if random.choice((True, False)):
            n = random.randint(1, limit)
        else:
            n = random.randint(limit + 1, min(population, limit + 400))
        ok = n <= limit
        relation = "≤" if ok else ">"
        answer = (f"{'ok' if ok else 'fails'}; n = {n} {relation} "
                  f"N/10 = {limit}")
        prefix = (f"At the {_site()}, a sample of n = {n} is drawn without "
                  f"replacement from a population of N = {population}. Use the "
                  "10% condition n ≤ N/10.")
        steps = [step("RULE", "10% condition", "n ≤ N/10"),
                 step("D", population, 10, limit),
                 step("CHECK", "n vs N/10", f"{n} {relation} {limit}",
                      "ok" if ok else "fails")]
        return prefix, steps, answer

    @staticmethod
    def _clt_condition():
        shape = random.choice(("normal", "right-skewed", "left-skewed", "unknown"))
        n = random.randint(8, 80)
        if shape == "normal":
            ok = True
            evidence = "population normal"
        elif n >= 30:
            ok = True
            evidence = f"n = {n} ≥ 30"
        else:
            ok = False
            evidence = f"population shape {shape} and n = {n} < 30"
        answer = f"{'ok' if ok else 'fails'}; {evidence}"
        prefix = (f"At the {_site()}, the population shape is {shape} and "
                  f"independent random samples have n = {n}. Use this rule: "
                  "x̄ is approximately normal if the population is normal or n ≥ 30.")
        steps = [step("RULE", "CLT shape condition",
                      "population normal or n ≥ 30"),
                 step("CLT_CHECK", evidence,
                      "approximately normal" if ok else "not justified")]
        return prefix, steps, answer

    @staticmethod
    def _minimum_n():
        p = Fraction(random.randint(1, 9), 10)
        q = 1 - p
        need_p, need_q = Fraction(10, 1) / p, Fraction(10, 1) / q
        ceil_p, ceil_q = _ceil(need_p), _ceil(need_q)
        n = max(ceil_p, ceil_q)
        prefix = (f"At the {_site()}, the null proportion is p = {prob_txt(p)}. "
                  "Use both large-count rules np ≥ 10 and n(1 − p) ≥ 10.")
        steps = [step("RULE", "large counts", "np ≥ 10 and n(1 − p) ≥ 10"),
                 step("REWRITE", "n ≥ 10/p and n ≥ 10/(1 − p)"),
                 step("D", 10, prob_txt(p), num_txt(need_p)),
                 step("CEIL", num_txt(need_p), ceil_p),
                 step("S", 1, prob_txt(p), prob_txt(q)),
                 step("D", 10, prob_txt(q), num_txt(need_q)),
                 step("CEIL", num_txt(need_q), ceil_q),
                 step("MAX", ceil_p, ceil_q, n),
                 step("CHECK", "both expected counts at n",
                      f"np = {num_txt(n * p)}, n(1 − p) = {num_txt(n * q)}",
                      "both ≥ 10")]
        return prefix, steps, str(n)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant in ("state_hypotheses", "parameter_identify",
                       "type_I_II_describe"):
            prefix, steps, answer = self._language(variant)
        elif variant == "np_condition":
            prefix, steps, answer = self._np_condition()
        elif variant == "ten_percent_condition":
            prefix, steps, answer = self._ten_percent()
        elif variant == "clt_condition":
            prefix, steps, answer = self._clt_condition()
        else:
            prefix, steps, answer = self._minimum_n()
        problem = f"{prefix}\n{random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_inference_setup_{variant}",
                "problem": problem, "steps": steps,
                "final_answer": answer}
