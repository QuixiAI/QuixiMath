import random
from base_generator import ProblemGenerator
from helpers import step, jid


NOUNS = [
    "beads", "buttons", "cards", "counters", "crayons", "cubes",
    "dominoes", "flags", "folders", "gears", "labels", "marbles",
    "markers", "notebooks", "paper clips", "patches", "pencils",
    "pins", "puzzle pieces", "ribbons", "stickers", "tiles",
    "tokens", "washers",
]

PLACES = [
    "art room", "classroom", "clubhouse", "community center",
    "craft table", "game room", "library", "makerspace", "museum",
    "school store", "science lab", "supply closet", "team room",
    "toy shop", "workshop",
]

PROBLEM_TEMPLATES = [
    ("The {place} has {n} {noun}. Write {n} as a product of primes "
     "using repeated division."),
    ("For a grouping plan at the {place}, prime factorize the count "
     "of {n} {noun}."),
    ("A shipment of {n} {noun} arrives at the {place}. Find the prime "
     "factorization of {n}."),
    ("The {place} needs the prime factorization of its {n} {noun}. "
     "Use repeated division."),
]


def is_prime(value):
    if value < 2:
        return False
    trial = 2
    while trial * trial <= value:
        if value % trial == 0:
            return False
        trial += 1
    return True


def next_prime(value):
    candidate = value + 1
    while not is_prime(candidate):
        candidate += 1
    return candidate


class PrimeFactorizationGenerator(ProblemGenerator):
    """Generates prime factorization using repeated division (factor tree style)."""

    def generate(self) -> dict:
        n = random.randint(24, 2000)
        original = n
        steps = []
        factors = []
        divisor = 2

        while n > 1:
            if divisor * divisor > n:
                # Remaining n is prime
                steps.append(step("PF_PRIME", n))
                factors.append(n)
                break
            if n % divisor == 0:
                n_next = n // divisor
                steps.append(step("PF_STEP", n, divisor, n_next))
                factors.append(divisor)
                n = n_next
            else:
                steps.append(step("CHECK", f"{n} mod {divisor}",
                                  n % divisor, "not divisible"))
                divisor = next_prime(divisor)

        final_answer = " × ".join(str(f) for f in factors)
        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="prime_factorization",
            problem=random.choice(PROBLEM_TEMPLATES).format(
                n=original,
                noun=random.choice(NOUNS),
                place=random.choice(PLACES),
            ),
            steps=steps,
            final_answer=final_answer,
        )
