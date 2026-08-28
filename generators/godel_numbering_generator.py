"""Gödel-number encoding, decoding, and symbol-table lookup.

Variants: ``encode``, ``decode``, and ``symbol_lookup``.  Traces use
``SYMBOL_CODE``, ``GODEL_TERM``, ``M``, ``PF_STEP``, ``PF_PRIME``,
``GODEL_DECODE``, ``CHECK``, and ``Z``.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step


FOUNDATIONS = True


SYMBOLS = ("¬", "∨", "(", ")", "p", "q")
CODES = (1, 2, 3, 4, 5, 7)
PRIMES = (2, 3, 5, 7, 11)
MAX_NUMBER = 10_000_000

QUERIES = {
    "encode": (
        "Compute the Gödel number of the symbol sequence.",
        "Encode the displayed sequence by prime powers.",
        "Determine the exact product assigned to the sequence.",
        "Apply the position-prime encoding rule.",
        "Find the integer code for the listed symbols.",
    ),
    "decode": (
        "Recover the encoded symbol sequence.",
        "Decode the integer by its consecutive-prime exponents.",
        "Determine the symbols represented by the Gödel number.",
        "Factor the number and invert the symbol table.",
        "Find the exact sequence encoded by the integer.",
    ),
    "symbol_lookup": (
        "Complete the requested symbol-table lookup.",
        "Determine the matching symbol-code pair.",
        "Use the displayed table in the requested direction.",
        "Find the corresponding code or symbol.",
        "Report the exact entry from the symbol table.",
    ),
}


def random_table():
    assigned = random.sample(CODES, len(CODES))
    return dict(zip(SYMBOLS, assigned))


def table_text(table):
    return "; ".join(f"{symbol} → {table[symbol]}" for symbol in SYMBOLS)


def encode(sequence, table):
    terms = [prime ** table[symbol]
             for prime, symbol in zip(PRIMES, sequence)]
    product = 1
    for term in terms:
        product *= term
    return product, terms


def random_encodable(table):
    while True:
        length = random.randint(3, 5)
        sequence = [random.choice(SYMBOLS) for _ in range(length)]
        number, terms = encode(sequence, table)
        if number <= MAX_NUMBER:
            return sequence, number, terms


def encoding_steps(sequence, table, terms):
    steps = []
    product = 1
    for position, (symbol, prime, term) in enumerate(
            zip(sequence, PRIMES, terms), 1):
        code = table[symbol]
        steps.append(step("SYMBOL_CODE", f"position {position}: {symbol}", code))
        steps.append(step("GODEL_TERM", f"{prime}^{code}", term))
        new_product = product * term
        steps.append(step("M", product, term, new_product))
        product = new_product
    return steps


def decoding_steps(number, sequence, table):
    steps = []
    remaining = number
    exponents = []
    for prime, symbol in zip(PRIMES, sequence):
        steps.append(step("PF_PRIME", prime))
        exponent = 0
        while remaining % prime == 0:
            quotient = remaining // prime
            steps.append(step("PF_STEP", remaining, prime, quotient))
            remaining = quotient
            exponent += 1
        exponents.append(exponent)
        steps.append(step("SYMBOL_CODE", f"exponent {exponent}", symbol))
    rendered = " ".join(sequence)
    steps.append(step("GODEL_DECODE", ", ".join(map(str, exponents)), rendered))
    steps.append(step("CHECK", "unfactored remainder", remaining))
    return steps


class GodelNumberingGenerator(ProblemGenerator):
    """Generate exact finite Gödel-number calculations."""

    VARIANTS = ("encode", "decode", "symbol_lookup")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _encode(self):
        table = random_table()
        sequence, number, terms = random_encodable(table)
        rendered = " ".join(sequence)
        problem = (f"Symbol table: {table_text(table)}. Encoding rule: for "
                   "sequence codes c1,...,ck, use "
                   "2^c1 · 3^c2 · 5^c3 · ... . "
                   f"Sequence: {rendered}. {random.choice(QUERIES['encode'])}")
        steps = encoding_steps(sequence, table, terms)
        steps.append(step("CHECK", f"number ≤ {MAX_NUMBER}", number))
        return problem, steps, str(number)

    def _decode(self):
        table = random_table()
        sequence, number, _ = random_encodable(table)
        problem = (f"Symbol table: {table_text(table)}. Decoding rule: the "
                   "exponents of consecutive primes 2,3,5,7,11 are the "
                   f"symbol codes. Gödel number: {number}. "
                   f"{random.choice(QUERIES['decode'])}")
        steps = decoding_steps(number, sequence, table)
        return problem, steps, " ".join(sequence)

    def _symbol_lookup(self):
        table = random_table()
        symbol = random.choice(SYMBOLS)
        code = table[symbol]
        if random.choice((True, False)):
            request = f"Lookup request: code of symbol {symbol}."
        else:
            request = f"Lookup request: symbol having code {code}."
        problem = (f"Symbol table: {table_text(table)}. {request} "
                   f"{random.choice(QUERIES['symbol_lookup'])}")
        answer = f"{symbol} → {code}"
        steps = [step("SYMBOL_CODE", symbol, code),
                 step("CHECK", request[:-1], answer)]
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "encode":
            problem, steps, answer = self._encode()
        elif variant == "decode":
            problem, steps, answer = self._decode()
        else:
            problem, steps, answer = self._symbol_lookup()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"godel_numbering_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
