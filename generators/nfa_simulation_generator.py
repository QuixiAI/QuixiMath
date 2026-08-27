import random

from base_generator import ProblemGenerator
from helpers import step, jid


ALPHABET = ["a", "b"]
ALPHABETS = [["a", "b"], ["a", "b", "c"]]
STATE_PREFIXES = ["q", "s", "p", "r", "t", "u"]
STATE_INDEX_POOL = list(range(9))


def set_text(values):
    ordered = sorted(values)
    return "{" + ",".join(ordered) + "}" if ordered else "{}"


def list_text(values):
    return ", ".join(values) if values else "none"


def transition_text(states, alphabet, transitions, epsilons):
    clauses = []
    for state in states:
        entries = []
        for symbol in alphabet:
            targets = transitions.get((state, symbol), set())
            entries.append(f"{symbol}->{set_text(targets)}")
        if epsilons.get(state):
            entries.append(f"epsilon->{set_text(epsilons[state])}")
        clauses.append(f"{state}:{','.join(entries)}")
    return "; ".join(clauses)


def epsilon_closure(states, epsilons):
    closure = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        for target in epsilons.get(state, set()):
            if target not in closure:
                closure.add(target)
                stack.append(target)
    return closure


PROBLEM_TEMPLATES = [
    ("Run the NFA with states {states}; alphabet {alphabet}; start {start}; "
     "accepting states {accept}; transitions {transitions}; input {input}. "
     "List the active-state sets after each symbol and give the result."),
    ("Trace active states for this NFA: states {states}; alphabet {alphabet}; "
     "start {start}; accepting states {accept}; transitions {transitions}; "
     "input {input}. Decide accept or reject."),
    ("For the NFA described by states {states}; alphabet {alphabet}; start "
     "{start}; accepting states {accept}; transitions {transitions}; input "
     "{input}, compute each active set and the final decision."),
    ("A nondeterministic machine has states {states}; alphabet {alphabet}; "
     "start {start}; accepting states {accept}; transitions {transitions}; "
     "input {input}. Follow every branch at once and report the trace."),
    ("Simulate the subset construction on the fly: states {states}; alphabet "
     "{alphabet}; start {start}; accepting states {accept}; transitions "
     "{transitions}; input {input}. Give each active set and the verdict."),
    ("Given states {states}; alphabet {alphabet}; start {start}; accepting "
     "states {accept}; transitions {transitions}; input {input}, work out "
     "the sequence of active-state sets for this NFA and whether it accepts."),
]


def state_names(count):
    """Random distinct state labels, e.g. ['p1', 'p4', 'p7']."""
    prefix = random.choice(STATE_PREFIXES)
    indices = sorted(random.sample(STATE_INDEX_POOL, count))
    return [f"{prefix}{i}" for i in indices]


def random_word(alphabet, lo, hi):
    return "".join(random.choice(alphabet)
                   for _ in range(random.randint(lo, hi)))


def suffix_machine(alphabet, states, pattern, looping_tail):
    """Guess-the-pattern NFA: start loops on everything and branches in."""
    transitions = {}
    for symbol in alphabet:
        transitions[(states[0], symbol)] = {states[0]}
    transitions[(states[0], pattern[0])] = {states[0], states[1]}
    for i in range(1, len(pattern)):
        transitions[(states[i], pattern[i])] = {states[i + 1]}
    if looping_tail:
        for symbol in alphabet:
            transitions[(states[len(pattern)], symbol)] = {
                states[len(pattern)]}
    return transitions


def build_spec(variant):
    """Return (alphabet, states, start, accept, transitions, epsilons, word)."""
    alphabet = random.choice(ALPHABETS)

    if variant in ("ends_with_ab", "contains_ab", "ends_with_pattern",
                   "contains_pattern"):
        if variant in ("ends_with_ab", "contains_ab"):
            pattern = "ab"
        else:
            pattern = random_word(alphabet, 2, 3)
        contains = variant in ("contains_ab", "contains_pattern")
        states = state_names(len(pattern) + 1)
        transitions = suffix_machine(alphabet, states, pattern, contains)
        epsilons = {}
        accept = [states[len(pattern)]]
        if random.random() < 0.5:
            head = random_word(alphabet, 1, 4)
            tail = random_word(alphabet, 0, 3) if contains else ""
            word = head + pattern + tail
        else:
            word = random_word(alphabet, 3, 8)
        return alphabet, states, states[0], accept, transitions, epsilons, word

    if variant == "epsilon_optional_a":
        states = state_names(3)
        transitions = {
            (states[0], "a"): {states[1]},
            (states[1], "b"): {states[2]},
            (states[2], "b"): {states[2]},
        }
        epsilons = {states[0]: {states[1]}}
        accept = [states[2]]
        word = random_word(alphabet, 2, 7)
        return alphabet, states, states[0], accept, transitions, epsilons, word

    if variant == "epsilon_chain":
        pattern = random_word(alphabet, 2, 3)
        states = state_names(len(pattern) + 1)
        transitions = {}
        for i, symbol in enumerate(pattern):
            transitions[(states[i], symbol)] = {states[i + 1]}
        epsilons = {}
        skips = random.sample(range(len(pattern)),
                              random.randint(1, len(pattern)))
        for i in skips:
            epsilons[states[i]] = {states[i + 1]}
        if random.random() < 0.5:
            tail = random.choice(alphabet)
            transitions[(states[-1], tail)] = {states[-1]}
        accept = [states[-1]]
        word = random_word(alphabet, 2, 7)
        return alphabet, states, states[0], accept, transitions, epsilons, word

    # random_nfa / random_epsilon_nfa
    count = random.randint(3, 5)
    states = state_names(count)
    transitions = {}
    for state in states:
        for symbol in alphabet:
            width = random.choices([0, 1, 2], weights=[3, 5, 2])[0]
            if width:
                transitions[(state, symbol)] = set(
                    random.sample(states, width))
    epsilons = {}
    if variant == "random_epsilon_nfa":
        for index, state in enumerate(states[:-1]):
            if random.random() < 0.4:
                epsilons[state] = {random.choice(states[index + 1:])}
    accept = sorted(random.sample(states, random.randint(1, count - 1)))
    word = random_word(alphabet, 3, 7)
    return alphabet, states, states[0], accept, transitions, epsilons, word


def simulate(start, accept, transitions, epsilons, word):
    active = epsilon_closure({start}, epsilons)
    trace = [active]
    for symbol in word:
        moved = set()
        for state in active:
            moved.update(transitions.get((state, symbol), set()))
        active = epsilon_closure(moved, epsilons)
        trace.append(active)
    accepted = bool(active & set(accept))
    return trace, accepted


def interesting(trace):
    """Reject runs that die immediately or never branch."""
    if max(len(s) for s in trace) < 2:
        return False
    return sum(1 for s in trace if s) >= max(2, len(trace) // 2)


class NFASimulationGenerator(ProblemGenerator):
    """
    NFA and epsilon-NFA simulation with active-state-set traces.

    Variants:
    - ends_with_ab: nondeterministically guesses the final "ab" suffix
    - contains_ab: keeps an accepting state once "ab" has appeared
    - epsilon_optional_a: uses an epsilon edge to make the initial "a" optional
    - ends_with_pattern / contains_pattern: the same guessing machines for a
      random 2-3 symbol pattern over the chosen alphabet
    - epsilon_chain: a pattern chain whose symbols are made optional by
      epsilon edges
    - random_nfa / random_epsilon_nfa: randomly wired 3-5 state machines,
      solved by subset simulation

    Machines, alphabets ({a,b} or {a,b,c}), state names and input words are
    all drawn at random; the answer is computed by simulating the machine, so
    accept and reject both occur and neither can be guessed from the shape.

    Op-codes used:
    - NFA_SETUP / NFA_ACCEPT / NFA_TRANSITION / NFA_EPSILON / NFA_INPUT
    - EPS_CLOSURE / NFA_ACTIVE / NFA_READ / NFA_MOVE
    - CHECK: final active-set intersection with accepting states
    - Z: deterministic active-set trace and accept/reject result
    """

    VARIANTS = [
        "ends_with_ab",
        "contains_ab",
        "epsilon_optional_a",
        "ends_with_pattern",
        "contains_pattern",
        "epsilon_chain",
        "random_nfa",
        "random_epsilon_nfa",
    ]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        for attempt in range(60):
            (alphabet, states, start, accept, transitions, epsilons,
             input_string) = build_spec(variant)
            trace, _ = simulate(start, accept, transitions, epsilons,
                                input_string)
            if interesting(trace) or attempt == 59:
                break

        steps = [
            step("NFA_SETUP", f"states {list_text(states)}",
                 f"alphabet {list_text(alphabet)}", f"start {start}"),
            step("NFA_ACCEPT", list_text(accept)),
        ]
        for state in states:
            for symbol in alphabet:
                targets = transitions.get((state, symbol), set())
                steps.append(step("NFA_TRANSITION", state, symbol,
                                  set_text(targets)))
            if epsilons.get(state):
                steps.append(step("NFA_EPSILON", state,
                                  set_text(epsilons[state])))

        active = epsilon_closure({start}, epsilons)
        active_sets = [set_text(active)]
        steps.extend([
            step("NFA_INPUT", input_string),
            step("EPS_CLOSURE", set_text({start}), set_text(active)),
            step("NFA_ACTIVE", "start", set_text(active)),
        ])

        for pos, symbol in enumerate(input_string, start=1):
            moved = set()
            pieces = []
            for state in sorted(active):
                targets = transitions.get((state, symbol), set())
                moved.update(targets)
                pieces.append(f"{state}->{set_text(targets)}")
            move_text = "; ".join(pieces) if pieces else "none"
            closed = epsilon_closure(moved, epsilons)
            steps.append(step("NFA_READ", f"pos {pos}", symbol))
            steps.append(step("NFA_MOVE", set_text(active), symbol,
                              move_text, set_text(moved)))
            steps.append(step("EPS_CLOSURE", set_text(moved),
                              set_text(closed)))
            active = closed
            active_sets.append(set_text(active))
            steps.append(step("NFA_ACTIVE", f"after {pos}",
                              set_text(active)))

        accepting_seen = sorted(set(active) & set(accept))
        status = "accepted" if accepting_seen else "rejected"
        steps.append(step("CHECK",
                          f"active ∩ accept = {list_text(accepting_seen)}",
                          status))
        answer = f"{status}; sets = {' -> '.join(active_sets)}"
        problem = random.choice(PROBLEM_TEMPLATES).format(
            states=list_text(states),
            alphabet=list_text(alphabet),
            start=start,
            accept=list_text(accept),
            transitions=transition_text(states, alphabet, transitions,
                                        epsilons),
            input=input_string,
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"nfa_simulation_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
