"""Classify finite Markov states from the positive-transition graph.

Variants: ``communicating_classes``, ``transient_recurrent``, ``period``,
``absorbing_states``, ``irreducible_check``, and ``reachability_matrix``.
Op-codes: ``MARKOV_GRAPH``, ``REACH_PASS``, ``CLASS``, ``CLASS_TYPE``,
``CHAIN_PERIOD``, ``ABSORBING_CHECK``, ``CHECK``, and ``Z``. Graphs use
4–6 states and every state has at least one positive outgoing transition.
"""
import math
import random

from base_generator import ProblemGenerator
from helpers import jid, step


PROBABILITY = True
VENUES = ("amber study", "birch survey", "cedar trial", "delta project",
          "ember lab", "forest audit", "granite program", "harbor test",
          "indigo review", "jade pilot", "kestrel study", "lunar trial",
          "maple project", "nova lab", "onyx survey", "pearl audit",
          "quartz program", "river test", "solar review", "topaz pilot",
          "umber study", "violet trial", "willow project", "zephyr lab")
CITIES = ("Albany", "Boston", "Cedarville", "Dover", "Erie", "Fresno",
          "Galveston", "Hartford", "Ithaca", "Juneau", "Kingston", "Lowell",
          "Madison", "Norfolk", "Olympia", "Portland", "Quincy", "Raleigh",
          "Salem", "Trenton", "Utica", "Ventura", "Wichita", "Yonkers")
NAMES = ("Aiko", "Ben", "Chidi", "Daria", "Elena", "Farah", "Gita", "Hugo",
         "Imani", "Jae", "Kira", "Luca", "Mina", "Noah", "Omar", "Priya",
         "Quinn", "Ravi", "Sofia", "Tariq", "Uma", "Vera", "Wen", "Zola")
QUERIES = {
    "communicating_classes": (
        "Find all communicating classes.",
        "Use mutual reachability to partition the states.",
        "Compute the strongly connected state classes.",
        "Group exactly those states that communicate.",
        "Determine the communication-class decomposition.",
    ),
    "transient_recurrent": (
        "Classify every communicating class as transient or recurrent.",
        "Find which classes are closed and which can be left.",
        "Compute the finite-chain recurrence classification.",
        "Identify transient and recurrent state classes.",
        "Use outgoing edges from each class to classify it.",
    ),
    "period": (
        "Find the period of this irreducible chain.",
        "Take the gcd of the possible return lengths.",
        "Compute the common state period exactly.",
        "Use Boolean matrix powers to find return times.",
        "Determine whether the chain is aperiodic or cyclic.",
    ),
    "absorbing_states": (
        "Find all absorbing and nonabsorbing states.",
        "Identify states whose only positive transition is to themselves.",
        "Classify every state by the absorbing-state criterion.",
        "Compute the absorbing-state set and its complement.",
        "Inspect each outgoing neighborhood for absorption.",
    ),
    "irreducible_check": (
        "Decide whether the chain is irreducible and give the class witness.",
        "Check whether every state communicates with every other state.",
        "Classify irreducibility from the reachability relation.",
        "Find whether there is one communicating class or several.",
        "Report an exact irreducibility verdict with supporting classes.",
    ),
    "reachability_matrix": (
        "Compute the reflexive reachability matrix.",
        "Apply Warshall closure to the positive-transition graph.",
        "Find which states can reach which other states.",
        "Compute all rows of the Boolean transitive closure.",
        "Determine the exact state reachability relation.",
    ),
}


def _context():
    return (f"At the {random.choice(VENUES)} in {random.choice(CITIES)}, "
            f"{random.choice(NAMES)} studies a finite Markov chain.")


def _cycle_edges(nodes):
    return {(nodes[index], nodes[(index + 1) % len(nodes)])
            for index in range(len(nodes))}


def _structured_graph():
    n = random.randint(4, 6)
    split = random.randint(2, n - 2)
    first = list(range(1, split + 1))
    second = list(range(split + 1, n + 1))
    edges = _cycle_edges(first) | _cycle_edges(second)
    edges.add((random.choice(first), random.choice(second)))
    for nodes in (first, second):
        if random.choice((True, False)):
            node = random.choice(nodes)
            edges.add((node, node))
    return n, edges


def _irreducible_graph(period_kind=None):
    if period_kind == 2:
        n = random.choice((4, 6))
        left = list(range(1, n + 1, 2))
        right = list(range(2, n + 1, 2))
        edges = {(a, b) for a in left for b in right}
        edges |= {(b, a) for b in right for a in left}
        return n, edges
    n = random.randint(4, 6)
    nodes = list(range(1, n + 1))
    edges = _cycle_edges(nodes)
    if period_kind == 1:
        node = random.choice(nodes)
        edges.add((node, node))
    elif period_kind is None:
        for _ in range(random.randint(0, n)):
            edges.add((random.choice(nodes), random.choice(nodes)))
    return n, edges


def _absorbing_graph():
    n = random.randint(4, 6)
    absorbing = set(random.sample(range(1, n + 1), random.randint(1, n - 2)))
    edges = {(state, state) for state in absorbing}
    for state in range(1, n + 1):
        if state in absorbing:
            continue
        choices = list(range(1, n + 1))
        outgoing = set(random.sample(choices, random.randint(1, min(3, n))))
        if outgoing == {state}:
            outgoing.add(random.choice(sorted(absorbing)))
        edges |= {(state, target) for target in outgoing}
    return n, edges


def _general_graph():
    n = random.randint(4, 6)
    edges = set()
    for state in range(1, n + 1):
        outgoing = random.sample(range(1, n + 1), random.randint(1, min(3, n)))
        edges |= {(state, target) for target in outgoing}
    return n, edges


def _edge_text(edges):
    return ", ".join(f"{left}→{right}" for left, right in sorted(edges))


def _set_text(values):
    return "{" + ", ".join(map(str, sorted(values))) + "}"


def _rows_text(reach):
    return "; ".join(f"R{row + 1}=(" + ",".join(
        "1" if value else "0" for value in reach[row]) + ")"
        for row in range(len(reach)))


def _warshall(n, edges):
    reach = [[row == column or (row + 1, column + 1) in edges
              for column in range(n)] for row in range(n)]
    snapshots = [[line[:] for line in reach]]
    for middle in range(n):
        reach = [[reach[row][column]
                  or (reach[row][middle] and reach[middle][column])
                  for column in range(n)] for row in range(n)]
        snapshots.append([line[:] for line in reach])
    return reach, snapshots


def _classes(reach):
    remaining = set(range(len(reach)))
    classes = []
    while remaining:
        state = min(remaining)
        component = {other for other in remaining
                     if reach[state][other] and reach[other][state]}
        classes.append({value + 1 for value in component})
        remaining -= component
    return classes


def _closed(component, edges):
    return all(target in component for source, target in edges if source in component)


def _reach_steps(n, edges):
    reach, snapshots = _warshall(n, edges)
    steps = [step("REACH_PASS", f"k={index}", _rows_text(snapshot))
             for index, snapshot in enumerate(snapshots)]
    return reach, steps


def _return_lengths(n, edges):
    adjacency = [[int((row + 1, column + 1) in edges) for column in range(n)]
                 for row in range(n)]
    current = [[int(row == column) for column in range(n)] for row in range(n)]
    lengths = []
    for length in range(1, 2 * n + 1):
        current = [[int(any(current[row][middle] and adjacency[middle][column]
                            for middle in range(n)))
                    for column in range(n)] for row in range(n)]
        if current[0][0]:
            lengths.append(length)
    return lengths


class MarkovStateClassificationGenerator(ProblemGenerator):
    """Generate graph-theoretic finite Markov-state classification tasks."""

    VARIANTS = ("communicating_classes", "transient_recurrent", "period",
                "absorbing_states", "irreducible_check", "reachability_matrix")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _problem(n, edges, target):
        return (f"{_context()} The states are {_set_text(range(1, n + 1))}. "
                f"Positive transitions are {_edge_text(edges)}. Every listed "
                f"edge has positive probability and no other edge does. "
                f"Target: {target}.")

    @staticmethod
    def _communicating(transience):
        n, edges = _structured_graph()
        reach, steps = _reach_steps(n, edges)
        classes = _classes(reach)
        steps.insert(0, step("MARKOV_GRAPH", f"states 1 through {n}",
                             _edge_text(edges)))
        for component in classes:
            steps.append(step("CLASS", _set_text(component), "mutual reachability"))
        if transience:
            transient, recurrent = [], []
            for component in classes:
                is_closed = _closed(component, edges)
                kind = "recurrent" if is_closed else "transient"
                steps.append(step("CLASS_TYPE", _set_text(component),
                                  "closed" if is_closed else "an edge leaves",
                                  kind))
                (recurrent if is_closed else transient).append(component)
            answer = ("transient classes " + ", ".join(_set_text(c) for c in transient)
                      + "; recurrent classes "
                      + ", ".join(_set_text(c) for c in recurrent))
            target = "transient and recurrent communicating classes"
        else:
            answer = "classes " + ", ".join(_set_text(c) for c in classes)
            target = "communicating classes"
        return MarkovStateClassificationGenerator._problem(n, edges, target), steps, answer

    @staticmethod
    def _period():
        kind = random.choice((1, 2, "cycle"))
        n, edges = _irreducible_graph(kind)
        lengths = _return_lengths(n, edges)
        period = 0
        for length in lengths:
            period = math.gcd(period, length)
        target = "the common period of this irreducible chain"
        steps = [
            step("MARKOV_GRAPH", f"states 1 through {n}", _edge_text(edges)),
            step("CHAIN_PERIOD", _set_text(range(1, n + 1)),
                 "return lengths " + _set_text(lengths), period),
            step("CHECK", "irreducible class", _set_text(range(1, n + 1))),
        ]
        answer = f"period {period}; class {_set_text(range(1, n + 1))}"
        return MarkovStateClassificationGenerator._problem(n, edges, target), steps, answer

    @staticmethod
    def _absorbing():
        n, edges = _absorbing_graph()
        absorbing, nonabsorbing = [], []
        steps = [step("MARKOV_GRAPH", f"states 1 through {n}", _edge_text(edges))]
        for state in range(1, n + 1):
            outgoing = {target for source, target in edges if source == state}
            is_absorbing = outgoing == {state}
            steps.append(step("ABSORBING_CHECK", f"state {state}",
                              "outgoing " + _set_text(outgoing),
                              "yes" if is_absorbing else "no"))
            (absorbing if is_absorbing else nonabsorbing).append(state)
        answer = (f"absorbing states {_set_text(absorbing)}; nonabsorbing states "
                  f"{_set_text(nonabsorbing)}")
        target = "absorbing and nonabsorbing states"
        return MarkovStateClassificationGenerator._problem(n, edges, target), steps, answer

    @staticmethod
    def _irreducible():
        expected = random.choice((True, False))
        n, edges = _irreducible_graph() if expected else _structured_graph()
        reach, steps = _reach_steps(n, edges)
        classes = _classes(reach)
        steps.insert(0, step("MARKOV_GRAPH", f"states 1 through {n}",
                             _edge_text(edges)))
        for component in classes:
            steps.append(step("CLASS", _set_text(component), "mutual reachability"))
        irreducible = len(classes) == 1
        steps.append(step("CHECK", "one communicating class",
                          "yes" if irreducible else "no"))
        if irreducible:
            answer = "irreducible yes; all states communicate"
        else:
            answer = ("irreducible no; classes "
                      + ", ".join(_set_text(component) for component in classes))
        target = "whether the chain is irreducible"
        return MarkovStateClassificationGenerator._problem(n, edges, target), steps, answer

    @staticmethod
    def _reachability():
        n, edges = _general_graph()
        reach, steps = _reach_steps(n, edges)
        steps.insert(0, step("MARKOV_GRAPH", f"states 1 through {n}",
                             _edge_text(edges)))
        answer = _rows_text(reach)
        steps.append(step("CHECK", "diagonal reachability", "all ones"))
        target = "the reflexive reachability matrix"
        return MarkovStateClassificationGenerator._problem(n, edges, target), steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "communicating_classes":
            problem, steps, answer = self._communicating(False)
        elif variant == "transient_recurrent":
            problem, steps, answer = self._communicating(True)
        elif variant == "period":
            problem, steps, answer = self._period()
        elif variant == "absorbing_states":
            problem, steps, answer = self._absorbing()
        elif variant == "irreducible_check":
            problem, steps, answer = self._irreducible()
        else:
            problem, steps, answer = self._reachability()
        problem = f"{problem} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_markov_state_classification_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
