import random

from base_generator import ProblemGenerator
from helpers import step, jid


LETTER_POOL = "abcdefghmnoprstuvwxy"
MIN_LEN = 6
MAX_LEN = 11

NAMES = [
    "Ana", "Bo", "Cleo", "Devi", "Emil", "Farid", "Greta", "Hana",
    "Ivan", "Jun", "Kira", "Liam", "Mira", "Noor", "Omar", "Pia",
    "Quinn", "Rosa", "Sami", "Tao", "Uma", "Vero", "Wes", "Yara",
]

ENCODE_TEMPLATES = [
    ("Compress the string \"{text}\" with {name}. {rule} List the emitted "
     "tokens."),
    ("Run {name} on input \"{text}\". {rule} Show each dictionary or match "
     "step and give the token stream."),
    ("For text \"{text}\", perform {name} compression and report the "
     "emitted tokens. {rule}"),
    ("{who} is compressing the string \"{text}\" by hand with {name}. "
     "{rule} What token stream does {who} write down?"),
    ("Encode \"{text}\" with {name}, listing the emitted tokens in order. "
     "{rule}"),
]

DECODE_TEMPLATES = [
    ("Decode the {name} token stream {tokens} back to the original string. "
     "{legend}"),
    ("{who} received the {name} token stream {tokens}. Reconstruct the "
     "string it encodes. {legend}"),
    ("The tokens {tokens} were produced by {name}. Rebuild the original "
     "text. {legend}"),
    ("Expand the {name} tokens {tokens} into the string they represent. "
     "{legend}"),
    ("Given the {name} output {tokens}, recover the input string. {legend}"),
]

LZ77_RULE = ("Use the longest non-overlapping previous match, breaking ties "
             "by the smaller offset, and $ as the end marker.")
LZ78_RULE = ("Start from an empty dictionary with index 0 as the empty "
             "phrase and use $ as the end marker.")
LZ77_LEGEND = ("Each token is (offset,length,next character) and $ is the "
               "end marker.")
LZ78_LEGEND = ("Each token is (dictionary index,next character), index 0 is "
               "the empty phrase, and $ is the end marker.")


def random_text():
    """A short, genuinely compressible string over a small random alphabet."""
    size = random.randint(2, 5)
    alphabet = sorted(random.sample(LETTER_POOL, size))
    length = random.randint(MIN_LEN, MAX_LEN)
    out = [random.choice(alphabet)]
    while len(out) < length:
        if len(out) >= 2 and random.random() < 0.55:
            start = random.randrange(len(out))
            span = random.randint(1, min(4, len(out) - start))
            out.extend(out[start:start + span])
        else:
            out.append(random.choice(alphabet))
    return "".join(out[:length])


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


def lz77_decode(tokens):
    out = ""
    for offset, length, ch in tokens:
        if length:
            start = len(out) - offset
            out += out[start:start + length]
        if ch != "$":
            out += ch
    return out


def lz78_decode(tokens):
    phrases = {0: ""}
    out = ""
    for idx, ch in tokens:
        phrase = phrases[idx] + ("" if ch == "$" else ch)
        out += phrase
        if ch != "$":
            phrases[len(phrases)] = phrase
    return out


class LZCompressionGenerator(ProblemGenerator):
    """
    LZ77 and LZ78 compression and decompression traces on short random
    strings over small random alphabets.

    LZ77 uses the longest non-overlapping match in the already-written prefix,
    breaking ties by the smaller offset. LZ78 starts with an empty dictionary
    and emits (dictionary index, next character). The decode variants run the
    same token grammars backward.

    Op-codes used:
    - LZ_SETUP / LZ77_SEARCH / LZ77_MATCH / LZ77_EMIT
    - LZ78_MATCH / LZ78_EMIT / LZ78_DICT
    - LZ77_EXPAND / LZ78_LOOKUP / LZ78_APPEND
    - CHECK (decode / encode round trips)
    - Z: token stream, or the recovered text
    """

    VARIANTS = ["lz77", "lz78", "lz77_decode", "lz78_decode"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        text = random_text()
        who = random.choice(NAMES)
        if variant == "lz77":
            steps, answer = self._generate_lz77(text)
            problem = random.choice(ENCODE_TEMPLATES).format(
                text=text, name="LZ77", rule=LZ77_RULE, who=who)
        elif variant == "lz78":
            steps, answer = self._generate_lz78(text)
            problem = random.choice(ENCODE_TEMPLATES).format(
                text=text, name="LZ78", rule=LZ78_RULE, who=who)
        elif variant == "lz77_decode":
            tokens = lz77_tokens(text)
            steps, answer = self._generate_lz77_decode(tokens)
            problem = random.choice(DECODE_TEMPLATES).format(
                tokens=lz77_text(tokens), name="LZ77", legend=LZ77_LEGEND,
                who=who)
        else:
            tokens = lz78_tokens(text)
            steps, answer = self._generate_lz78_decode(tokens)
            problem = random.choice(DECODE_TEMPLATES).format(
                tokens=lz78_text(tokens), name="LZ78", legend=LZ78_LEGEND,
                who=who)
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
        if random.random() < 0.5:
            steps.append(step("CHECK", "decode",
                              f"rebuild = {lz77_decode(tokens)}",
                              f"input = {text}"))
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
        if random.random() < 0.5:
            steps.append(step("CHECK", "decode",
                              f"rebuild = {lz78_decode(tokens)}",
                              f"input = {text}"))
        return steps, f"LZ78 = {lz78_text(tokens)}"

    def _generate_lz77_decode(self, tokens):
        steps = [step("LZ_SETUP", "LZ77 decode", lz77_text(tokens))]
        out = ""
        for offset, length, ch in tokens:
            if length:
                start = len(out) - offset
                piece = out[start:start + length]
                detail = f"copy {piece} from pos {start}"
            else:
                piece = ""
                detail = "no copy"
            out += piece
            if ch != "$":
                out += ch
                tail = f"then add {ch}"
            else:
                tail = "end marker"
            steps.append(step("LZ77_EXPAND", f"({offset},{length},{ch})",
                              detail, tail, f"out = {out}"))
        if random.random() < 0.5:
            steps.append(step("CHECK", "encode",
                              f"re-encode = {lz77_text(lz77_tokens(out))}",
                              f"given = {lz77_text(tokens)}"))
        return steps, f"text = {out}"

    def _generate_lz78_decode(self, tokens):
        steps = [
            step("LZ_SETUP", "LZ78 decode", lz78_text(tokens)),
            step("LZ78_DICT", "0", "empty"),
        ]
        phrases = {0: ""}
        out = ""
        for idx, ch in tokens:
            prefix = phrases[idx]
            steps.append(step("LZ78_LOOKUP", f"index {idx}",
                              f"phrase {prefix if prefix else 'empty'}"))
            phrase = prefix + ("" if ch == "$" else ch)
            out += phrase
            steps.append(step("LZ78_APPEND", f"{prefix if prefix else 'empty'} + {ch}",
                              f"out = {out}"))
            if ch != "$":
                phrases[len(phrases)] = phrase
                steps.append(step("LZ78_DICT", len(phrases) - 1, phrase))
        if random.random() < 0.5:
            steps.append(step("CHECK", "encode",
                              f"re-encode = {lz78_text(lz78_tokens(out))}",
                              f"given = {lz78_text(tokens)}"))
        return steps, f"text = {out}"
