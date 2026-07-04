import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class ScalingLawGenerator(ProblemGenerator):
    """
    Scaling-law arithmetic for model size, tokens, compute, and throughput.

    Computes training compute C = 6ND, Chinchilla-optimal tokens 20N, and
    tokens/s from a FLOPs/s budget as F/(6N).

    Op-codes used:
    - SCALING_SETUP / SCALING_COMPUTE / CHINCHILLA / THROUGHPUT
    - M / D (established/shared): exact compute and tokens/s arithmetic
    - Z: compute, optimal tokens, tokens/s
    """

    def generate(self) -> dict:
        params = random.choice([
            50_000_000, 125_000_000, 350_000_000, 760_000_000,
            1_300_000_000, 2_700_000_000, 6_700_000_000,
        ])
        tokens = random.choice([
            1_000_000_000, 2_000_000_000, 5_000_000_000,
            10_000_000_000, 20_000_000_000, 50_000_000_000,
        ])
        flops_per_second = random.choice([
            10**15, 2 * 10**15, 5 * 10**15, 10**16, 2 * 10**16,
        ])
        nd = params * tokens
        compute = 6 * nd
        optimal_tokens = 20 * params
        denom = 6 * params
        tokens_per_second = Fraction(flops_per_second, denom)
        steps = [
            step("SCALING_SETUP", f"N={params}", f"D={tokens}",
                 f"F={flops_per_second}"),
            step("M", params, tokens, nd),
            step("M", 6, nd, compute),
            step("SCALING_COMPUTE", "6ND", compute),
            step("M", 20, params, optimal_tokens),
            step("CHINCHILLA", "20N", optimal_tokens),
            step("M", 6, params, denom),
            step("D", flops_per_second, denom,
                 fraction_text(tokens_per_second)),
            step("THROUGHPUT", "tokens_per_second",
                 fraction_text(tokens_per_second)),
        ]
        answer = (
            f"C={compute}; optimal_tokens={optimal_tokens}; "
            f"tokens_per_second={fraction_text(tokens_per_second)}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"For scaling-law arithmetic with N={params} parameters, "
            f"D={tokens} tokens, and training budget F={flops_per_second} "
            "FLOPs/s, compute C=6ND, Chinchilla-optimal tokens 20N, and "
            "tokens/s=F/(6N)."
        )
        return dict(
            problem_id=jid(),
            operation="scaling_law_compute",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
