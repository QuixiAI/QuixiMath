import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


VARIANTS = ["transformer_stack", "lora_matrix"]


def fraction_text(value):
    return str(Fraction(value))


class ParamCountGenerator(ProblemGenerator):
    """
    Transformer and LoRA parameter counting.

    Variants:
    - transformer_stack: embeddings plus attention and MLP parameters per layer,
      compared with the 12*d^2*L back-of-envelope.
    - lora_matrix: LoRA rank-r parameters r(d_in+d_out) versus a full dense
      d_in*d_out matrix.

    Op-codes used:
    - PARAM_SETUP / PARAM_PART / APPROX / LORA_COUNT
    - M / A / D (established/shared): exact counts and ratios
    - Z: final parameter counts
    """

    VARIANTS = VARIANTS

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "transformer_stack":
            problem, steps, answer = self._generate_transformer()
        else:
            problem, steps, answer = self._generate_lora()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"param_count_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_transformer(self):
        vocab = random.choice([8000, 12000, 16000, 24000, 32000])
        d_model = random.choice([128, 192, 256, 384, 512, 768])
        layers = random.randint(2, 24)
        mlp_mult = 4
        d2 = d_model * d_model
        attention = 4 * d2
        mlp = 2 * mlp_mult * d2
        per_layer = attention + mlp
        stack = per_layer * layers
        embeddings = vocab * d_model
        total = stack + embeddings
        approx_per_layer = 12 * d2
        approx_stack = approx_per_layer * layers
        steps = [
            step("PARAM_SETUP", "type=transformer",
                 f"vocab={vocab},d={d_model},layers={layers}",
                 f"mlp_mult={mlp_mult}"),
            step("M", d_model, d_model, d2),
            step("M", 4, d2, attention),
            step("PARAM_PART", "attention_per_layer", attention),
            step("M", 2 * mlp_mult, d2, mlp),
            step("PARAM_PART", "mlp_per_layer", mlp),
            step("A", attention, mlp, per_layer),
            step("PARAM_PART", "per_layer", per_layer),
            step("M", per_layer, layers, stack),
            step("PARAM_PART", "layer_stack", stack),
            step("M", vocab, d_model, embeddings),
            step("PARAM_PART", "embeddings", embeddings),
            step("A", stack, embeddings, total),
            step("M", 12, d2, approx_per_layer),
            step("M", approx_per_layer, layers, approx_stack),
            step("APPROX", "12*d^2*L", approx_stack),
        ]
        answer = (
            f"embeddings={embeddings}; per_layer={per_layer}; "
            f"stack={stack}; total={total}; approx_stack={approx_stack}"
        )
        problem = (
            f"Count parameters for a transformer with vocab={vocab}, "
            f"d_model={d_model}, layers={layers}, and MLP multiplier "
            f"{mlp_mult}. Include embeddings, attention matrices, MLP "
            "matrices, and the 12*d^2*L estimate."
        )
        return problem, steps, answer

    def _generate_lora(self):
        d_in = random.choice([128, 192, 256, 384, 512, 768, 1024])
        d_out = random.choice([128, 192, 256, 384, 512, 768, 1024])
        rank = random.choice([2, 4, 8, 16, 32])
        full = d_in * d_out
        dim_sum = d_in + d_out
        lora = rank * dim_sum
        ratio = Fraction(lora, full)
        steps = [
            step("PARAM_SETUP", "type=lora",
                 f"d_in={d_in},d_out={d_out},rank={rank}"),
            step("M", d_in, d_out, full),
            step("PARAM_PART", "full_matrix", full),
            step("A", d_in, d_out, dim_sum),
            step("M", rank, dim_sum, lora),
            step("LORA_COUNT", "r*(d_in+d_out)", lora),
            step("D", lora, full, fraction_text(ratio)),
            step("APPROX", "lora/full", fraction_text(ratio)),
        ]
        answer = f"full={full}; lora={lora}; ratio={fraction_text(ratio)}"
        problem = (
            f"Count LoRA parameters for a dense layer with d_in={d_in}, "
            f"d_out={d_out}, and rank r={rank}. Compare r(d_in+d_out) "
            "with full fine-tuning d_in*d_out."
        )
        return problem, steps, answer
