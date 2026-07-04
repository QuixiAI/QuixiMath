import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


VARIANTS = ["matmul_forward", "kv_cache"]


def fraction_text(value):
    return str(Fraction(value))


class FLOPsMemoryGenerator(ProblemGenerator):
    """
    FLOPs and memory arithmetic for transformer-adjacent computations.

    Variants:
    - matmul_forward: two chained matmuls using the 2mnk FLOPs rule.
    - kv_cache: KV-cache bytes = 2*L*h*d_k*seq*precision_bytes.

    Op-codes used:
    - FLOPS_SETUP / MATMUL_FLOPS / MEMORY_SETUP / KV_CACHE / MEMORY_UNIT
    - M / A / D (established/shared): exact FLOPs and byte arithmetic
    - Z: final FLOPs or memory values
    """

    VARIANTS = VARIANTS

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "matmul_forward":
            problem, steps, answer = self._generate_matmul()
        else:
            problem, steps, answer = self._generate_kv_cache()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"flops_memory_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_matmul(self):
        m = random.choice([8, 16, 32, 64, 128])
        d = random.choice([64, 128, 256, 512])
        hidden = random.choice([128, 256, 512, 1024, 2048])
        out = random.choice([32, 64, 128, 256, 512])
        md = m * d
        first_half = md * hidden
        flops1 = 2 * first_half
        mh = m * hidden
        second_half = mh * out
        flops2 = 2 * second_half
        total = flops1 + flops2
        steps = [
            step("FLOPS_SETUP", "rule=2mnk",
                 f"m={m},d={d},h={hidden},o={out}"),
            step("M", m, d, md),
            step("M", md, hidden, first_half),
            step("M", 2, first_half, flops1),
            step("MATMUL_FLOPS", "XW1", flops1),
            step("M", m, hidden, mh),
            step("M", mh, out, second_half),
            step("M", 2, second_half, flops2),
            step("MATMUL_FLOPS", "HW2", flops2),
            step("A", flops1, flops2, total),
        ]
        answer = f"flops1={flops1}; flops2={flops2}; total_flops={total}"
        problem = (
            "Compute FLOPs for an MLP forward pass X(mxd) @ W1(dxh) then "
            "H(mxh) @ W2(hxo), using 2mnk per matmul, with "
            f"m={m}, d={d}, h={hidden}, o={out}."
        )
        return problem, steps, answer

    def _generate_kv_cache(self):
        layers = random.choice([4, 8, 12, 16, 24, 32])
        heads = random.choice([4, 8, 12, 16, 32])
        d_k = random.choice([32, 64, 80, 96, 128])
        seq = random.choice([128, 256, 512, 1024, 2048, 4096])
        precision = random.choice([1, 2, 4])
        lh = layers * heads
        lhd = lh * d_k
        lhd_seq = lhd * seq
        kv_values = 2 * lhd_seq
        bytes_total = kv_values * precision
        mib = Fraction(bytes_total, 1024 * 1024)
        steps = [
            step("MEMORY_SETUP", "kv_cache",
                 f"L={layers},h={heads},d_k={d_k}",
                 f"seq={seq},precision_bytes={precision}"),
            step("M", layers, heads, lh),
            step("M", lh, d_k, lhd),
            step("M", lhd, seq, lhd_seq),
            step("M", 2, lhd_seq, kv_values),
            step("KV_CACHE", "values", kv_values),
            step("M", kv_values, precision, bytes_total),
            step("KV_CACHE", "bytes", bytes_total),
            step("D", bytes_total, 1024 * 1024, fraction_text(mib)),
            step("MEMORY_UNIT", "MiB", fraction_text(mib)),
        ]
        answer = f"bytes={bytes_total}; MiB={fraction_text(mib)}"
        problem = (
            f"Compute KV-cache memory bytes for L={layers}, h={heads}, "
            f"d_k={d_k}, seq={seq}, precision_bytes={precision} using "
            "2*L*h*d_k*seq*precision_bytes."
        )
        return problem, steps, answer
