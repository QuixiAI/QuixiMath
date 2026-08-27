"""Construct uniquely solvable finite logic-grid puzzles backward.

Variants:
- ``three_by_three`` maps three people to three items.
- ``three_by_three_two_categories`` maps people to both pets and drinks.
- ``four_by_four`` maps four people to an ordered item category.

A hidden solution is chosen first.  True direct, negative, relational, and
order clues are added only when they eliminate at least one remaining
candidate, stopping exactly when one solution survives.  Five phrasings and
large name/item banks provide more than 100,000 puzzles.

Op-codes:
- ``CLUE_APPLY``: apply one clue and show the survivor-count change.
- ``ELIMINATE``: remove a concrete candidate that violates that clue.
- ``DEDUCE``: record each mapping forced by the sole survivor.
- ``CHECK``: verify every clue against the final mapping.
- ``Z``: exact composite mapping.
"""
import itertools
import random

from base_generator import ProblemGenerator
from helpers import jid, step


FOUNDATIONS = True


NAMES = (
    "Ada", "Ben", "Cleo", "Dara", "Eli", "Finn", "Gia", "Hugo", "Iris",
    "Jae", "Kira", "Luca", "Mara", "Nico", "Oona", "Pia", "Quin", "Ravi",
)
ITEMS = (
    "bell", "book", "brush", "camera", "compass", "drum", "flute", "globe",
    "kite", "lamp", "map", "mug", "pencil", "shell", "spoon", "stamp",
    "telescope", "ticket",
)
PETS = ("cat", "dog", "fish", "gecko", "hamster", "parrot", "rabbit",
        "turtle", "canary", "ferret")
DRINKS = ("cocoa", "juice", "lemonade", "milk", "tea", "water", "cider",
          "smoothie", "punch", "seltzer")

QUERIES = (
    "Use the clues in order to find the unique mapping.",
    "Solve the grid and report each person's assignment.",
    "Eliminate inconsistent mappings until one solution remains.",
    "Determine the complete assignment that satisfies every clue.",
    "Apply each clue, then give the unique person-to-category mapping.",
)


def mapping_text(names, candidate):
    if isinstance(candidate[0], tuple):
        pets, drinks = candidate
        return "; ".join(f"{name}: {pet}, {drink}"
                         for name, pet, drink in zip(names, pets, drinks))
    return "; ".join(f"{name}: {item}" for name, item in zip(names, candidate))


class LogicGridPuzzleGenerator(ProblemGenerator):
    """Generate clues, enumerate candidates, and retain a unique solution."""

    VARIANTS = ("three_by_three", "three_by_three_two_categories",
                "four_by_four")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _ordered_list(values):
        return "[" + ", ".join(values) + "]"

    @staticmethod
    def _one_category_clues(names, items, solution):
        clues = []
        positions = {item: index for index, item in enumerate(items)}
        for person_index, person in enumerate(names):
            correct = solution[person_index]
            clues.append((f"{person} has {correct}",
                          lambda candidate, i=person_index, value=correct:
                          candidate[i] == value))
            for wrong in items:
                if wrong != correct:
                    clues.append((f"{person} does not have {wrong}",
                                  lambda candidate, i=person_index, value=wrong:
                                  candidate[i] != value))
        for first_index, second_index in itertools.permutations(range(len(names)), 2):
            first_item, second_item = solution[first_index], solution[second_index]
            if positions[first_item] < positions[second_item]:
                first, second = names[first_index], names[second_index]
                clues.append((
                    f"{first}'s item comes before {second}'s item in the listed order",
                    lambda candidate, i=first_index, j=second_index, pos=positions:
                    pos[candidate[i]] < pos[candidate[j]],
                ))
        return clues

    @staticmethod
    def _two_category_clues(names, pets, drinks, solution):
        solution_pets, solution_drinks = solution
        clues = []
        for index, person in enumerate(names):
            pet, drink = solution_pets[index], solution_drinks[index]
            clues.extend((
                (f"{person} has {pet}",
                 lambda candidate, i=index, value=pet: candidate[0][i] == value),
                (f"{person} drinks {drink}",
                 lambda candidate, i=index, value=drink: candidate[1][i] == value),
                (f"the person with {pet} drinks {drink}",
                 lambda candidate, value_pet=pet, value_drink=drink:
                 candidate[1][candidate[0].index(value_pet)] == value_drink),
            ))
            for wrong in pets:
                if wrong != pet:
                    clues.append((f"{person} does not have {wrong}",
                                  lambda candidate, i=index, value=wrong:
                                  candidate[0][i] != value))
            for wrong in drinks:
                if wrong != drink:
                    clues.append((f"{person} does not drink {wrong}",
                                  lambda candidate, i=index, value=wrong:
                                  candidate[1][i] != value))
        return clues

    @staticmethod
    def _select_clues(candidates, solution, clue_bank):
        survivors = list(candidates)
        available = list(clue_bank)
        random.shuffle(available)
        selected = []
        while len(survivors) > 1:
            for index, (text, evaluator) in enumerate(available):
                reduced = [candidate for candidate in survivors if evaluator(candidate)]
                if solution in reduced and len(reduced) < len(survivors):
                    selected.append((text, evaluator, list(survivors), reduced))
                    survivors = reduced
                    available.pop(index)
                    break
            else:
                raise RuntimeError("clue bank could not isolate the chosen solution")
        return selected

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        size = 4 if variant == "four_by_four" else 3
        names = tuple(random.sample(NAMES, size))
        if variant == "three_by_three_two_categories":
            pets = tuple(sorted(random.sample(PETS, size)))
            drinks = tuple(sorted(random.sample(DRINKS, size)))
            pet_perms = list(itertools.permutations(pets))
            drink_perms = list(itertools.permutations(drinks))
            candidates = [(pet_perm, drink_perm) for pet_perm in pet_perms
                          for drink_perm in drink_perms]
            solution = random.choice(candidates)
            clue_bank = self._two_category_clues(names, pets, drinks, solution)
            header = (
                f"People: {self._ordered_list(names)}. Pets: {self._ordered_list(pets)}. "
                f"Drinks: {self._ordered_list(drinks)}."
            )
        else:
            items = tuple(sorted(random.sample(ITEMS, size)))
            candidates = list(itertools.permutations(items))
            solution = random.choice(candidates)
            clue_bank = self._one_category_clues(names, items, solution)
            header = (
                f"People: {self._ordered_list(names)}. Items in order: "
                f"{self._ordered_list(items)}."
            )
        selected = self._select_clues(candidates, solution, clue_bank)
        clue_text = " ".join(f"({index}) {text}."
                             for index, (text, _, _, _) in enumerate(selected, 1))
        problem = (
            f"Puzzle format: {variant.replace('_', ' ')}. {header} Clues: {clue_text} "
            f"{random.choice(QUERIES)}"
        )
        steps = []
        for index, (text, _, before, after) in enumerate(selected, 1):
            steps.append(step("CLUE_APPLY", f"clue {index}", text,
                              f"{len(before)} → {len(after)} candidates"))
            eliminated = [candidate for candidate in before if candidate not in after]
            for candidate in eliminated:
                steps.append(step("ELIMINATE", f"clue {index}",
                                  mapping_text(names, candidate), "violates clue"))
        if variant == "three_by_three_two_categories":
            for name, pet, drink in zip(names, solution[0], solution[1]):
                steps.append(step("DEDUCE", name, f"pet = {pet}",
                                  "only solution left"))
                steps.append(step("DEDUCE", name, f"drink = {drink}",
                                  "only solution left"))
        else:
            for name, item in zip(names, solution):
                steps.append(step("DEDUCE", name, f"item = {item}",
                                  "only solution left"))
        for index, (_, evaluator, _, _) in enumerate(selected, 1):
            steps.append(step("CHECK", f"clue {index}",
                              "holds" if evaluator(solution) else "fails"))
        answer = mapping_text(names, solution)
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"logic_grid_puzzle_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
