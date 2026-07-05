import random

from base_generator import ProblemGenerator
from helpers import step, jid


PROBLEM_TEMPLATES = [
    ("Simulate PDA {name} on input {input}. Start with stack $. Report "
     "accept/reject and the final stack."),
    ("Trace the pushdown automaton {name} for input {input}; stack bottom is $."),
    ("Run PDA {name} with input {input}, showing stack changes after each symbol."),
]


def stack_text(stack):
    return "".join(stack)


class PDASimulationGenerator(ProblemGenerator):
    """
    Pushdown-automaton simulation for balanced parentheses and a^n b^n.

    Op-codes used:
    - PDA_SETUP / PDA_STATE / PDA_READ / PDA_PUSH / PDA_POP / PDA_REJECT
    - CHECK
    - Z: accept/reject result and final stack
    """

    VARIANTS = ["balanced_parentheses", "anbn"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "balanced_parentheses":
            input_text = random.choice(["()", "(())", "(()())", "(()", "())"])
            steps, status, final_stack = self._balanced(input_text)
        else:
            input_text = random.choice(["ab", "aabb", "aaabbb", "aab", "abb"])
            steps, status, final_stack = self._anbn(input_text)
        answer = f"{status}; stack={final_stack}"
        problem = random.choice(PROBLEM_TEMPLATES).format(
            name=variant,
            input=input_text,
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"pda_simulation_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _balanced(self, text):
        stack = ["$"]
        state = "q"
        steps = [step("PDA_SETUP", "balanced_parentheses", "stack=$")]
        for pos, ch in enumerate(text, start=1):
            steps.append(step("PDA_STATE", f"pos {pos}", state,
                              f"stack={stack_text(stack)}"))
            steps.append(step("PDA_READ", ch))
            if ch == "(":
                stack.append("(")
                steps.append(step("PDA_PUSH", "(", f"stack={stack_text(stack)}"))
            elif len(stack) > 1:
                popped = stack.pop()
                steps.append(step("PDA_POP", popped, f"stack={stack_text(stack)}"))
            else:
                steps.append(step("PDA_REJECT", "pop from bottom"))
                return steps, "rejected", stack_text(stack)
        status = "accepted" if stack == ["$"] else "rejected"
        steps.append(step("CHECK", f"stack={stack_text(stack)}", status))
        return steps, status, stack_text(stack)

    def _anbn(self, text):
        stack = ["$"]
        state = "push"
        steps = [step("PDA_SETUP", "a^n b^n", "stack=$")]
        for pos, ch in enumerate(text, start=1):
            steps.append(step("PDA_STATE", f"pos {pos}", state,
                              f"stack={stack_text(stack)}"))
            steps.append(step("PDA_READ", ch))
            if state == "push" and ch == "a":
                stack.append("A")
                steps.append(step("PDA_PUSH", "A", f"stack={stack_text(stack)}"))
            elif ch == "b":
                state = "pop"
                if len(stack) > 1:
                    popped = stack.pop()
                    steps.append(step("PDA_POP", popped,
                                      f"stack={stack_text(stack)}"))
                else:
                    steps.append(step("PDA_REJECT", "too many b symbols"))
                    return steps, "rejected", stack_text(stack)
            else:
                steps.append(step("PDA_REJECT", "a after b"))
                return steps, "rejected", stack_text(stack)
        status = "accepted" if state == "pop" and stack == ["$"] else "rejected"
        steps.append(step("CHECK", f"state={state}", f"stack={stack_text(stack)}",
                          status))
        return steps, status, stack_text(stack)
