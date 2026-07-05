import random

from base_generator import ProblemGenerator
from helpers import step, jid


SAMPLES = [
    "abababa",
    "aababa",
    "abcabca",
    "bananaban",
    "abcabcab",
]

PROBLEM_TEMPLATES = [
    ("Compress the string {text} with {method}. Use the exact greedy rule "
     "stated by the method and list the emitted tokens."),
    ("Run {method} on input {text}. Show each dictionary or match step and "
     "give the token stream."),
    ("For text {text}, perform {method} compression and report the emitted "
     "tokens."),
]


def lz77_tokens(text):
    tokens = []
    pos = 0
    while pos < len(text):
        best_offset = 0
        best_length = 0
        for start in range(pos):
            length = 0
            while (pos + length < len(text) and start + length < pos and
                   text[start + length] == text[pos + length]):
                length += 1
            offset = pos - start
            if length > best_length or (
                length == best_length and length > 0 and offset < best_offset
            ):
                best_offset = offset
                best_length = length
        next_char = text[pos + best_length] if pos + best_length < len(text) else "$"
        tokens.append((best_offset, best_length, next_char))
        pos += best_length + (0 if next_char == "$" else 1)
        if next_char == "$":
            break
    return tokens


def lz78_tokens(text):
    dictionary = {}
    tokens = []
    pos = 0
    next_index = 1
    while pos < len(text):
        phrase = ""
        idx = 0
        end = pos
        while end < len(text) and phrase + text[end] in dictionary:
            phrase += text[end]
            idx = dictionary[phrase]
            end += 1
        next_char = text[end] if end < len(text) else "$"
        tokens.append((idx, next_char))
        if next_char != "$":
            dictionary[phrase + next_char] = next_index
            next_index += 1
            pos = end + 1
        else:
            pos = end
            break
    return tokens


def lz77_text(tokens):
    return ", ".join(f"({off},{length},{ch})" for off, length, ch in tokens)


def lz78_text(tokens):
    return ", ".join(f"({idx},{ch})" for idx, ch in tokens)


class LZCompressionGenerator(ProblemGenerator):
    """
    LZ77 and LZ78 compression traces on short strings.

    LZ77 uses the longest non-overlapping match in the already-written prefix,
    breaking ties by the smaller offset. LZ78 starts with an empty dictionary
    and emits (dictionary index, next character).

    Op-codes used:
    - LZ_SETUP / LZ77_SEARCH / LZ77_MATCH / LZ77_EMIT
    - LZ78_MATCH / LZ78_EMIT / LZ78_DICT
    - Z: token stream
    """

    VARIANTS = ["lz77", "lz78"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        text = random.choice(SAMPLES)
        if variant == "lz77":
            steps, answer = self._generate_lz77(text)
            method = ("LZ77 using longest non-overlapping previous match, "
                      "smaller offset on ties, and $ as the end marker")
        else:
            steps, answer = self._generate_lz78(text)
            method = ("LZ78 with dictionary index 0 as the empty phrase and "
                      "$ as the end marker")
        problem = random.choice(PROBLEM_TEMPLATES).format(
            text=text,
            method=method,
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"lz_compression_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_lz77(self, text):
        steps = [
            step("LZ_SETUP", "LZ77", text),
        ]
        tokens = []
        pos = 0
        while pos < len(text):
            best_offset = 0
            best_length = 0
            best_start = None
            for start in range(pos):
                length = 0
                while (pos + length < len(text) and start + length < pos and
                       text[start + length] == text[pos + length]):
                    length += 1
                offset = pos - start
                steps.append(step("LZ77_SEARCH", f"pos {pos}",
                                  f"start {start}", f"len {length}"))
                if length > best_length or (
                    length == best_length and length > 0 and offset < best_offset
                ):
                    best_start = start
                    best_offset = offset
                    best_length = length
            next_char = text[pos + best_length] if pos + best_length < len(text) else "$"
            steps.append(step("LZ77_MATCH", f"pos {pos}",
                              "literal" if best_start is None else
                              f"start {best_start}",
                              f"offset {best_offset}, len {best_length}",
                              f"next {next_char}"))
            tokens.append((best_offset, best_length, next_char))
            steps.append(step("LZ77_EMIT", f"({best_offset},{best_length},{next_char})"))
            pos += best_length + (0 if next_char == "$" else 1)
            if next_char == "$":
                break
        return steps, f"LZ77 = {lz77_text(tokens)}"

    def _generate_lz78(self, text):
        steps = [
            step("LZ_SETUP", "LZ78", text),
            step("LZ78_DICT", "0", "empty"),
        ]
        dictionary = {}
        tokens = []
        pos = 0
        next_index = 1
        while pos < len(text):
            phrase = ""
            idx = 0
            end = pos
            while end < len(text) and phrase + text[end] in dictionary:
                phrase += text[end]
                idx = dictionary[phrase]
                end += 1
            next_char = text[end] if end < len(text) else "$"
            steps.append(step("LZ78_MATCH", f"pos {pos}",
                              f"phrase {phrase if phrase else 'empty'}",
                              f"index {idx}", f"next {next_char}"))
            tokens.append((idx, next_char))
            steps.append(step("LZ78_EMIT", f"({idx},{next_char})"))
            if next_char != "$":
                new_phrase = phrase + next_char
                dictionary[new_phrase] = next_index
                steps.append(step("LZ78_DICT", next_index, new_phrase))
                next_index += 1
                pos = end + 1
            else:
                break
        return steps, f"LZ78 = {lz78_text(tokens)}"
