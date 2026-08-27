import math
import random

from base_generator import ProblemGenerator
from helpers import step, jid


OBJECTS = [
    "hats", "keys", "books", "badges", "tickets", "coats", "folders",
    "cards", "gifts", "laptops", "notebooks", "packages", "labels",
    "forms", "passes", "tokens", "umbrellas", "phones", "envelopes",
    "receipts", "scarves", "gloves", "helmets", "clipboards", "binders",
    "lanyards", "backpacks", "mugs", "aprons", "jackets", "wallets",
    "cameras", "tablets", "charters", "posters", "trophies", "flasks",
    "toolkits", "portfolios", "briefcases", "sketchbooks", "raincoats",
    "instruments", "canteens",
]

NAMES = [
    "Ama", "Bruno", "Camila", "Dilip", "Esme", "Farid", "Greta", "Hiro",
    "Imani", "Jonas", "Kavya", "Lucia", "Malik", "Nadia", "Oskar", "Priya",
    "Quentin", "Rosa", "Samir", "Tessa", "Ulises", "Vera", "Wren", "Xiomara",
    "Yusuf", "Zola", "Aiko", "Bertrand", "Chidi", "Delphine", "Ewan",
    "Fatima", "Gustav", "Halima", "Ivar", "Junko", "Kwame", "Leena",
    "Mateo", "Noor",
]

PLACES = [
    "opera house", "chess club", "science fair", "ferry terminal",
    "county museum", "rowing club", "language institute", "bird sanctuary",
    "puppet theatre", "planetarium", "climbing gym", "botanical garden",
    "town archive", "film society", "pottery studio", "trail lodge",
    "radio station", "observatory", "youth orchestra", "seed library",
    "fencing salle", "print shop", "harbour office", "glass workshop",
]

ROLES = [
    "runs the coat check", "manages the lost-and-found",
    "staffs the front desk", "sorts the returns bin",
    "oversees the check-in table", "keeps the sign-out ledger",
    "minds the cloakroom", "runs the equipment cage",
    "handles the pickup window", "tends the storage lockers",
]


def _derangements(n):
    """Derangement values D_0..D_n by the standard recurrence."""
    values = [1, 0]
    for m in range(2, n + 1):
        values.append((m - 1) * (values[m - 1] + values[m - 2]))
    return values[:max(2, n + 1)]


class DerangementGenerator(ProblemGenerator):
    """
    Derangement counting built on the recurrence D_n=(n-1)(D_(n-1)+D_(n-2)).

    Variants:
    - recurrence: plain derangement count D_n
    - exactly_k: permutations of n items with exactly k fixed points,
      C(n,k)*D_(n-k)
    - at_least_one: permutations with at least one fixed point, n! - D_n
    - probability: probability a uniform random permutation is a
      derangement, D_n/n! as a reduced fraction

    Op-codes used:
    - DERANGE_SETUP: number of items and the fixed-point condition
    - RECURRENCE: derangement recurrence
    - INITIAL: D_0 and D_1
    - A / M / S (established): recurrence and combination arithmetic
    - DERANGE_VALUE: computed D_m
    - NCR (established): binomial coefficient for the fixed positions
    - FACT_FORMULA / FACT (established): factorial expansion and value
    - COMPLEMENT: complement identity for the at-least-one count
    - DERANGE_PROB: derangement probability as D_n over n!
    - GCD (established): gcd used to reduce the probability
    - F (established): reduced fraction
    - Z: exact final answer
    """

    VARIANTS = ["recurrence", "exactly_k", "at_least_one", "probability"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    # ---------------- problem text ----------------

    @staticmethod
    def _context():
        return {
            "name": random.choice(NAMES),
            "place": random.choice(PLACES),
            "obj": random.choice(OBJECTS),
            "role": random.choice(ROLES),
        }

    @staticmethod
    def _lead(ctx):
        return f"{ctx['name']} {ctx['role']} at the {ctx['place']}."

    @classmethod
    def _phrase_recurrence(cls, ctx, n, idx):
        lead = cls._lead(ctx)
        obj = ctx["obj"]
        if idx == 0:
            return (f"{lead} How many derangements are there of {n} "
                    f"distinct {obj}?")
        if idx == 1:
            return (f"{lead} Tonight {n} visitors each left one of their "
                    f"{obj}, and the {obj} are handed back in a random "
                    f"order. In how many of the orders does every visitor "
                    f"get someone else's item?")
        if idx == 2:
            return (f"{lead} Count the permutations of {n} labelled {obj} "
                    f"in which no item stays in its own position.")
        if idx == 3:
            return (f"{lead} A shuffle of the {n} numbered {obj} is called "
                    f"a derangement when no item returns to the slot it "
                    f"came from. How many derangements of the {n} {obj} "
                    f"are there?")
        return (f"{lead} There are {n} owners and {n} matching {obj}. In "
                f"how many ways can the {obj} be returned so that nobody "
                f"receives their own?")

    @classmethod
    def _phrase_exactly_k(cls, ctx, n, k, idx):
        lead = cls._lead(ctx)
        obj = ctx["obj"]
        if idx == 0:
            return (f"{lead} The {n} {obj} are handed back at random. In "
                    f"how many of the orders do exactly {k} owners get "
                    f"their own item?")
        if idx == 1:
            return (f"{lead} How many permutations of {n} labelled {obj} "
                    f"have exactly {k} fixed points?")
        if idx == 2:
            return (f"{lead} Of all the ways to return {n} {obj} to their "
                    f"{n} owners, count those in which exactly {k} of the "
                    f"{obj} reach the right owner.")
        if idx == 3:
            return (f"{lead} A random shuffle of {n} numbered {obj} is "
                    f"recorded. How many shuffles leave exactly {k} of the "
                    f"{obj} in their original positions?")
        return (f"{lead} Among the arrangements of {n} {obj} across {n} "
                f"labelled slots, how many put exactly {k} items in their "
                f"matching slot?")

    @classmethod
    def _phrase_at_least_one(cls, ctx, n, idx):
        lead = cls._lead(ctx)
        obj = ctx["obj"]
        if idx == 0:
            return (f"{lead} The {n} {obj} are handed back at random. In "
                    f"how many of the orders does at least one owner get "
                    f"their own item?")
        if idx == 1:
            return (f"{lead} How many permutations of {n} labelled {obj} "
                    f"have at least one fixed point?")
        if idx == 2:
            return (f"{lead} Count the ways to return {n} {obj} to their "
                    f"{n} owners so that the return is not a complete "
                    f"mismatch, that is, at least one owner is matched "
                    f"correctly.")
        if idx == 3:
            return (f"{lead} A shuffle of {n} numbered {obj} is called "
                    f"lucky when some item lands back in its own slot. How "
                    f"many of the shuffles of the {n} {obj} are lucky?")
        return (f"{lead} Out of every arrangement of {n} {obj} in {n} "
                f"labelled slots, how many have one or more items sitting "
                f"in their matching slot?")

    @classmethod
    def _phrase_probability(cls, ctx, n, idx):
        lead = cls._lead(ctx)
        obj = ctx["obj"]
        tail = " Give the answer as a fraction in lowest terms."
        if idx == 0:
            return (f"{lead} The {n} {obj} are handed back in a uniformly "
                    f"random order. What is the probability that no owner "
                    f"gets their own item?" + tail)
        if idx == 1:
            return (f"{lead} A permutation of {n} labelled {obj} is chosen "
                    f"uniformly at random. What is the probability that it "
                    f"has no fixed point?" + tail)
        if idx == 2:
            return (f"{lead} All arrangements of {n} {obj} in {n} labelled "
                    f"slots are equally likely. Find the probability that "
                    f"the arrangement is a derangement." + tail)
        if idx == 3:
            return (f"{lead} If the {n} numbered {obj} are shuffled at "
                    f"random, how likely is it that not a single item "
                    f"returns to its own slot?" + tail)
        return (f"{lead} A random matching sends the {n} {obj} back to the "
                f"{n} owners. What is the probability that every owner "
                f"receives the wrong item?" + tail)

    # ---------------- steps ----------------

    @staticmethod
    def _recurrence_table(n, steps):
        values = [1, 0]
        steps.append(step("RECURRENCE", "D_n", "(n-1)(D_(n-1)+D_(n-2))"))
        steps.append(step("INITIAL", "D_0 = 1", "D_1 = 0"))
        for m in range(2, n + 1):
            subtotal = values[m - 1] + values[m - 2]
            value = (m - 1) * subtotal
            steps.extend([
                step("A", values[m - 1], values[m - 2], subtotal),
                step("M", m - 1, subtotal, value),
                step("DERANGE_VALUE", f"D_{m}", value),
            ])
            values.append(value)
        return values

    @staticmethod
    def _factorial_steps(n, steps):
        expansion = "·".join(str(i) for i in range(1, n + 1))
        total = math.factorial(n)
        steps.append(step("FACT_FORMULA", f"{n}! = {expansion}"))
        steps.append(step("FACT", n, total))
        return total

    # ---------------- generate ----------------

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        ctx = self._context()
        idx = random.randrange(5)

        if variant == "recurrence":
            n = random.randint(4, 13)
            problem = self._phrase_recurrence(ctx, n, idx)
            steps = [step("DERANGE_SETUP", f"n = {n}", "no item fixed")]
            values = self._recurrence_table(n, steps)
            answer = f"D_{n} = {values[n]}"
            operation = "derangement_recurrence"

        elif variant == "exactly_k":
            n = random.randint(6, 13)
            k = random.randint(1, 3)
            problem = self._phrase_exactly_k(ctx, n, k, idx)
            choose = math.comb(n, k)
            steps = [
                step("DERANGE_SETUP", f"n = {n}", f"exactly {k} fixed"),
                step("NCR", f"C({n},{k})", choose),
                step("DERANGE_SETUP", f"n = {n - k}", "no item fixed"),
            ]
            values = self._recurrence_table(n - k, steps)
            deranged = values[n - k]
            total = choose * deranged
            steps.append(step("M", choose, deranged, total))
            answer = str(total)
            operation = "derangement_exactly_k"

        elif variant == "at_least_one":
            n = random.randint(4, 10)
            problem = self._phrase_at_least_one(ctx, n, idx)
            steps = [
                step("DERANGE_SETUP", f"n = {n}", "at least one fixed"),
                step("COMPLEMENT", "at least one fixed", f"{n}! - D_{n}"),
            ]
            total = self._factorial_steps(n, steps)
            steps.append(step("DERANGE_SETUP", f"n = {n}", "no item fixed"))
            values = self._recurrence_table(n, steps)
            deranged = values[n]
            result = total - deranged
            steps.append(step("S", total, deranged, result))
            answer = str(result)
            operation = "derangement_at_least_one"

        else:  # probability
            n = random.randint(4, 10)
            problem = self._phrase_probability(ctx, n, idx)
            steps = [step("DERANGE_SETUP", f"n = {n}", "no item fixed")]
            values = self._recurrence_table(n, steps)
            deranged = values[n]
            total = self._factorial_steps(n, steps)
            g = math.gcd(deranged, total)
            steps.append(step("DERANGE_PROB", f"D_{n}/{n}!",
                              f"{deranged}/{total}"))
            steps.append(step("GCD", f"gcd({deranged},{total})", g))
            answer = f"{deranged // g}/{total // g}"
            steps.append(step("F", f"{deranged}/{total}", answer))
            operation = "derangement_probability"

        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
