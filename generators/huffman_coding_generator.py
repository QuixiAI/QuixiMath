import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


SYMBOLS = "ABCDEFGH"


def fraction_text(value):
    return str(Fraction(value))


def bit_unit(value):
    return "bit" if Fraction(value) == 1 else "bits"


def distribution_text(symbols, probabilities):
    return ", ".join(
        f"{symbol}={fraction_text(probability)}"
        for symbol, probability in zip(symbols, probabilities)
    )


def power_counts():
    depth = random.randint(3, 8)
    total = 2 ** depth
    counts = [total]
    target = random.randint(2, min(8, total))
    while len(counts) < target:
        choices = [idx for idx, count in enumerate(counts) if count > 1]
        if not choices:
            break
        idx = random.choice(choices)
        count = counts.pop(idx)
        counts.extend([count // 2, count // 2])
    random.shuffle(counts)
    return counts, total


def label(symbols):
    return "".join(sorted(symbols))


def node_text(node_label, weight):
    return f"{node_label}:{fraction_text(weight)}"


def huffman_trace(symbols, probabilities):
    nodes = [
        (probability, symbol, (symbol,))
        for symbol, probability in zip(symbols, probabilities)
    ]
    lengths = {symbol: 0 for symbol in symbols}
    merge_steps = []
    while len(nodes) > 1:
        nodes.sort(key=lambda item: (item[0], item[1]))
        left_weight, left_label, left_symbols = nodes.pop(0)
        right_weight, right_label, right_symbols = nodes.pop(0)
        merged_symbols = tuple(sorted(left_symbols + right_symbols))
        merged_label = label(merged_symbols)
        merged_weight = left_weight + right_weight
        for symbol in merged_symbols:
            lengths[symbol] += 1
        merge_steps.append(
            step("HUFFMAN_MERGE",
                 f"{node_text(left_label, left_weight)} + "
                 f"{node_text(right_label, right_weight)}",
                 node_text(merged_label, merged_weight))
        )
        nodes.append((merged_weight, merged_label, merged_symbols))
    return merge_steps, lengths


class HuffmanCodingGenerator(ProblemGenerator):
    """
    Huffman tree construction with expected length, entropy, and Kraft check.

    Probabilities are dyadic, so each entropy log2 term is exact.

    Op-codes used:
    - HUFFMAN_SETUP / HUFFMAN_MERGE / CODE_LENGTH / KRAFT_CHECK
    - LOG2 / E / D / M / A (established/shared): exact entropy and lengths
    - Z: code lengths, expected length, entropy, and Kraft sum
    """

    def generate(self) -> dict:
        counts, total = power_counts()
        symbols = list(SYMBOLS[:len(counts)])
        probabilities = [Fraction(count, total) for count in counts]
        steps = [
            step("HUFFMAN_SETUP", distribution_text(symbols, probabilities)),
        ]
        merge_steps, lengths = huffman_trace(symbols, probabilities)
        steps.extend(merge_steps)
        for symbol in symbols:
            steps.append(step("CODE_LENGTH", symbol, f"l={lengths[symbol]}"))

        expected_length = self._append_expected_length(
            steps, symbols, probabilities, lengths
        )
        entropy = self._append_entropy(steps, probabilities)
        kraft = self._append_kraft(steps, symbols, lengths)
        steps.append(step("KRAFT_CHECK", f"sum={fraction_text(kraft)}",
                          "complete" if kraft == 1 else "incomplete"))
        length_text = ",".join(
            f"{symbol}:{lengths[symbol]}" for symbol in symbols
        )
        answer = (
            f"lengths={length_text}; "
            f"L={fraction_text(expected_length)} {bit_unit(expected_length)}; "
            f"H={fraction_text(entropy)} {bit_unit(entropy)}; "
            f"Kraft={fraction_text(kraft)}"
        )
        steps.append(step("Z", answer))
        problem = (
            "Build a Huffman code for symbols with probabilities "
            f"{distribution_text(symbols, probabilities)}. Report code "
            "lengths, expected length L, entropy H, and Kraft sum."
        )
        return dict(
            problem_id=jid(),
            operation="huffman_coding",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _append_expected_length(self, steps, symbols, probabilities, lengths):
        steps.append(step("HUFFMAN_FORMULA", "L=sum p_i*l_i"))
        running = Fraction(0)
        for symbol, probability in zip(symbols, probabilities):
            term = probability * lengths[symbol]
            steps.append(step("M", fraction_text(probability), lengths[symbol],
                              fraction_text(term)))
            new_running = running + term
            steps.append(step("A", fraction_text(running),
                              fraction_text(term), fraction_text(new_running)))
            running = new_running
        return running

    def _append_entropy(self, steps, probabilities):
        steps.append(step("ENTROPY_SETUP", "H", "-sum p log2(p)"))
        running = Fraction(0)
        for probability in probabilities:
            exponent = probability.denominator.bit_length() - 1
            term = probability * exponent
            steps.append(step("LOG2", fraction_text(probability), -exponent))
            steps.append(step("M", fraction_text(probability), exponent,
                              fraction_text(term)))
            new_running = running + term
            steps.append(step("A", fraction_text(running),
                              fraction_text(term), fraction_text(new_running)))
            running = new_running
        return running

    def _append_kraft(self, steps, symbols, lengths):
        steps.append(step("KRAFT_FORMULA", "sum 2^-l_i"))
        running = Fraction(0)
        for symbol in symbols:
            denominator = 2 ** lengths[symbol]
            term = Fraction(1, denominator)
            steps.append(step("E", 2, lengths[symbol], denominator))
            steps.append(step("D", 1, denominator, fraction_text(term)))
            new_running = running + term
            steps.append(step("A", fraction_text(running),
                              fraction_text(term), fraction_text(new_running)))
            running = new_running
        return running
