import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


STATES = ["H", "L"]
START = {"H": Fraction(1, 2), "L": Fraction(1, 2)}
TRANS = {
    ("H", "H"): Fraction(3, 4), ("H", "L"): Fraction(1, 4),
    ("L", "H"): Fraction(1, 3), ("L", "L"): Fraction(2, 3),
}
EMIT = {
    ("H", "A"): Fraction(3, 4), ("H", "B"): Fraction(1, 4),
    ("L", "A"): Fraction(1, 4), ("L", "B"): Fraction(3, 4),
}
OBSERVATIONS = ["AAB", "ABB", "BAA", "BBA"]


def ftxt(value):
    return str(Fraction(value))


def dict_text(table):
    return ", ".join(f"{k}={ftxt(v)}" for k, v in table.items())


class ViterbiGenerator(ProblemGenerator):
    """
    Viterbi decoding for a two-state hidden Markov model.

    Op-codes used:
    - HMM_SETUP / VITERBI_INIT / VITERBI_CAND / VITERBI_PICK
    - VITERBI_BACKTRACE
    - Z: most likely state path and exact probability
    """

    def generate(self) -> dict:
        obs = random.choice(OBSERVATIONS)
        steps = [
            step("HMM_SETUP", "states H,L", f"observations {obs}"),
            step("HMM_START", dict_text(START)),
        ]
        dp = {}
        back = []
        first = obs[0]
        for state in STATES:
            prob = START[state] * EMIT[(state, first)]
            dp[state] = prob
            steps.append(step("VITERBI_INIT", state, f"obs={first}",
                              ftxt(prob)))
        for t, symbol in enumerate(obs[1:], start=2):
            new_dp = {}
            back_row = {}
            for state in STATES:
                candidates = []
                for prev in STATES:
                    prob = dp[prev] * TRANS[(prev, state)] * EMIT[(state, symbol)]
                    candidates.append((prob, prev))
                    steps.append(step("VITERBI_CAND", f"t={t},state={state}",
                                      f"from {prev}", ftxt(prob)))
                best_prob, best_prev = max(candidates,
                                           key=lambda item: (item[0], item[1]))
                new_dp[state] = best_prob
                back_row[state] = best_prev
                steps.append(step("VITERBI_PICK", f"t={t},state={state}",
                                  f"from {best_prev}", ftxt(best_prob)))
            dp = new_dp
            back.append(back_row)
        final_prob, final_state = max((dp[s], s) for s in STATES)
        path = [final_state]
        for row in reversed(back):
            path.append(row[path[-1]])
        path.reverse()
        steps.append(step("VITERBI_BACKTRACE", "->".join(path),
                          ftxt(final_prob)))
        answer = f"path = {'->'.join(path)}; probability = {ftxt(final_prob)}"
        problem = (
            "Decode observations {obs} with Viterbi. States H,L; "
            "start H=1/2,L=1/2; transitions HH=3/4,HL=1/4,LH=1/3,LL=2/3; "
            "emissions H:A=3/4,H:B=1/4,L:A=1/4,L:B=3/4."
        ).format(obs=obs)
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="viterbi_hmm_decode",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
