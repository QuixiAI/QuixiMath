import random

from base_generator import ProblemGenerator
from helpers import step, jid


CASES = {
    "identity": {
        "term": "((lambda x. x) a)",
        "steps": [("BETA", "(lambda x. x) applied to a"),
                  ("SUBSTITUTE", "x:=a in x", "a")],
        "answer": "normal form = a",
    },
    "constant": {
        "term": "(((lambda x. (lambda y. x)) a) b)",
        "steps": [("BETA", "(lambda x. lambda y. x) applied to a"),
                  ("SUBSTITUTE", "x:=a in lambda y. x", "lambda y. a"),
                  ("BETA", "(lambda y. a) applied to b"),
                  ("SUBSTITUTE", "y:=b in a", "a")],
        "answer": "normal form = a",
    },
    "alpha": {
        "term": "((lambda x. (lambda y. x)) y)",
        "steps": [("ALPHA_RENAME", "lambda y. x", "lambda z. x"),
                  ("BETA", "(lambda x. lambda z. x) applied to y"),
                  ("SUBSTITUTE", "x:=y in lambda z. x", "lambda z. y")],
        "answer": "normal form = lambda z. y",
    },
}


PROBLEM_TEMPLATES = [
    "Reduce the lambda term {term} by leftmost-outermost beta reduction.",
    "Normalize {term} using leftmost-outermost beta reduction; alpha-rename when needed.",
    "Find the normal form of {term}, using capture-avoiding substitution.",
]


class LambdaReductionGenerator(ProblemGenerator):
    """
    Small lambda-calculus beta-reduction traces with capture avoidance.

    Op-codes used:
    - LAMBDA_SETUP / BETA / ALPHA_RENAME / SUBSTITUTE / REWRITE
    - Z: normal form under the stated strategy
    """

    VARIANTS = ["identity", "constant", "alpha"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        spec = CASES[variant]
        steps = [step("LAMBDA_SETUP", spec["term"],
                      "leftmost-outermost")]
        for item in spec["steps"]:
            if item[0] == "BETA":
                steps.append(step("BETA", item[1]))
            elif item[0] == "ALPHA_RENAME":
                steps.append(step("ALPHA_RENAME", item[1], item[2]))
                steps.append(step("REWRITE", item[2]))
            elif item[0] == "SUBSTITUTE":
                steps.append(step("SUBSTITUTE", item[1], item[2]))
                steps.append(step("REWRITE", item[-1]))
            else:
                raise ValueError(f"unknown lambda step {item[0]}")
        answer = spec["answer"]
        problem = random.choice(PROBLEM_TEMPLATES).format(term=spec["term"])
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"lambda_reduction_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
