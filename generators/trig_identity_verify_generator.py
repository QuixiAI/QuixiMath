import random
from base_generator import ProblemGenerator
from helpers import step, jid

# Each entry: (lhs, rhs, canonical path). 'V' is the variable
# placeholder. The path transforms the LEFT side into the right.
IDENTITIES = [
    ("tan V · cos V", "sin V", [
        ("IDENT_SUB", "tan V = sin V/cos V", ""),
        ("REWRITE", "(sin V/cos V) · cos V", ""),
        ("CANCEL", "cos V", "sin V"),
        ("IDENT_MATCH", "sin V = sin V", ""),
    ]),
    ("cot V · sec V", "csc V", [
        ("IDENT_SUB", "cot V = cos V/sin V", ""),
        ("IDENT_SUB", "sec V = 1/cos V", ""),
        ("REWRITE", "(cos V/sin V) · (1/cos V)", ""),
        ("CANCEL", "cos V", "1/sin V"),
        ("IDENT_SUB", "1/sin V = csc V", ""),
        ("IDENT_MATCH", "csc V = csc V", ""),
    ]),
    ("sec^2 V - tan^2 V", "1", [
        ("IDENT_SUB", "sec^2 V = 1/cos^2 V", ""),
        ("IDENT_SUB", "tan^2 V = sin^2 V/cos^2 V", ""),
        ("REWRITE", "(1 - sin^2 V)/cos^2 V", ""),
        ("IDENT_SUB", "1 - sin^2 V = cos^2 V", ""),
        ("REWRITE", "cos^2 V/cos^2 V", ""),
        ("CANCEL", "cos^2 V", "1"),
        ("IDENT_MATCH", "1 = 1", ""),
    ]),
    ("(1 - cos V)(1 + cos V)", "sin^2 V", [
        ("FOIL_SETUP", "(1 - cos V)(1 + cos V)", ""),
        ("REWRITE", "1 - cos^2 V", ""),
        ("IDENT_SUB", "1 - cos^2 V = sin^2 V", ""),
        ("IDENT_MATCH", "sin^2 V = sin^2 V", ""),
    ]),
    ("sin^4 V - cos^4 V", "sin^2 V - cos^2 V", [
        ("REWRITE", "(sin^2 V + cos^2 V)(sin^2 V - cos^2 V)", ""),
        ("IDENT_SUB", "sin^2 V + cos^2 V = 1", ""),
        ("REWRITE", "(1)(sin^2 V - cos^2 V)", ""),
        ("REWRITE", "sin^2 V - cos^2 V", ""),
        ("IDENT_MATCH", "sin^2 V - cos^2 V = sin^2 V - cos^2 V", ""),
    ]),
    ("(1 + tan^2 V) · cos^2 V", "1", [
        ("IDENT_SUB", "1 + tan^2 V = sec^2 V", ""),
        ("REWRITE", "sec^2 V · cos^2 V", ""),
        ("IDENT_SUB", "sec^2 V = 1/cos^2 V", ""),
        ("REWRITE", "cos^2 V/cos^2 V", ""),
        ("CANCEL", "cos^2 V", "1"),
        ("IDENT_MATCH", "1 = 1", ""),
    ]),
    ("csc V - sin V", "cos V · cot V", [
        ("IDENT_SUB", "csc V = 1/sin V", ""),
        ("REWRITE", "(1 - sin^2 V)/sin V", ""),
        ("IDENT_SUB", "1 - sin^2 V = cos^2 V", ""),
        ("REWRITE", "cos^2 V/sin V", ""),
        ("REWRITE", "cos V · (cos V/sin V)", ""),
        ("IDENT_SUB", "cos V/sin V = cot V", ""),
        ("IDENT_MATCH", "cos V · cot V = cos V · cot V", ""),
    ]),
    ("(sin V + cos V)^2", "1 + 2 sin V cos V", [
        ("REWRITE", "sin^2 V + 2 sin V cos V + cos^2 V", ""),
        ("IDENT_SUB", "sin^2 V + cos^2 V = 1", ""),
        ("REWRITE", "1 + 2 sin V cos V", ""),
        ("IDENT_MATCH", "1 + 2 sin V cos V = 1 + 2 sin V cos V", ""),
    ]),
    ("1/(1 - cos V) + 1/(1 + cos V)", "2/sin^2 V", [
        ("REWRITE",
         "((1 + cos V) + (1 - cos V))/((1 - cos V)(1 + cos V))", ""),
        ("REWRITE", "2/(1 - cos^2 V)", ""),
        ("IDENT_SUB", "1 - cos^2 V = sin^2 V", ""),
        ("REWRITE", "2/sin^2 V", ""),
        ("IDENT_MATCH", "2/sin^2 V = 2/sin^2 V", ""),
    ]),
]

VARS = ["θ", "x", "t", "A", "β"]


class TrigIdentityVerifyGenerator(ProblemGenerator):
    """
    Verifies trig identities along a canonical transformation path:
    start from the more complex side, substitute known identities,
    simplify, and close with an explicit match of both sides. The
    final answer is always 'Identity verified' (A0 for this format).

    Op-codes used:
    - IDENTITY_SETUP: the identity and which side is transformed
    - IDENT_SUB: substitute a known identity (statement)
    - REWRITE / CANCEL / FOIL_SETUP: algebra along the way
      (established)
    - IDENT_MATCH: both sides now identical (statement)
    - Z: 'Identity verified'
    """

    def generate(self) -> dict:
        lhs, rhs, path = random.choice(IDENTITIES)
        var = random.choice(VARS)
        flipped = random.random() < 0.5

        def sub(t):
            return t.replace("V", var)

        if flipped:
            identity = f"{sub(rhs)} = {sub(lhs)}"
            side = "right"
        else:
            identity = f"{sub(lhs)} = {sub(rhs)}"
            side = "left"

        steps = [step("IDENTITY_SETUP", f"verify: {identity}",
                      f"transform the {side} side")]
        for code, f1, f2 in path:
            if f2:
                steps.append(step(code, sub(f1), sub(f2)))
            else:
                steps.append(step(code, sub(f1)))
        answer = "Identity verified"
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="trig_identity_verify",
            problem=f"Verify the identity: {identity}.",
            steps=steps,
            final_answer=answer,
        )
