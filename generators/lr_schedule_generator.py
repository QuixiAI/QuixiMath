import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class LRScheduleGenerator(ProblemGenerator):
    """
    Linear warmup plus cosine decay learning-rate schedule.

    Warmup uses lr = base_lr * t / warmup_steps. Decay uses
    min_lr + (base_lr-min_lr)(1+cos(pi*progress))/2 at progress values with
    exact cosine values.

    Op-codes used:
    - LR_SETUP / LR_PHASE / COSINE / LR_VALUE
    - S / D / M / A (established/shared): exact schedule arithmetic
    - Z: phase and learning rate
    """

    def generate(self) -> dict:
        base_lr = random.choice([Fraction(1, 10), Fraction(3, 100),
                                 Fraction(1, 100), Fraction(1, 1000)])
        min_lr = random.choice([Fraction(0), base_lr / 10])
        warmup = random.choice([10, 20, 40, 50, 100])
        span = random.choice([100, 200, 400, 800, 1000])
        total = warmup + span
        if random.choice([True, False]):
            phase = "warmup"
            t = random.randint(0, warmup)
        else:
            phase = "decay"
            progress = random.choice([Fraction(1, 2), Fraction(1)])
            t = warmup + int(span * progress)

        steps = [
            step("LR_SETUP", f"base={fraction_text(base_lr)}",
                 f"min={fraction_text(min_lr)}",
                 f"warmup={warmup},total={total},t={t}"),
        ]
        if t <= warmup:
            ratio = Fraction(t, warmup)
            lr = base_lr * ratio
            steps.extend([
                step("D", t, warmup, fraction_text(ratio)),
                step("M", fraction_text(base_lr), fraction_text(ratio),
                     fraction_text(lr)),
                step("LR_PHASE", "warmup"),
            ])
        else:
            elapsed = t - warmup
            decay_span = total - warmup
            progress = Fraction(elapsed, decay_span)
            cos_value = Fraction(0) if progress == Fraction(1, 2) else Fraction(-1)
            diff = base_lr - min_lr
            one_plus = 1 + cos_value
            product = diff * one_plus
            half = product / 2
            lr = min_lr + half
            steps.extend([
                step("S", t, warmup, elapsed),
                step("S", total, warmup, decay_span),
                step("D", elapsed, decay_span, fraction_text(progress)),
                step("COSINE", f"pi*{fraction_text(progress)}",
                     fraction_text(cos_value)),
                step("S", fraction_text(base_lr), fraction_text(min_lr),
                     fraction_text(diff)),
                step("A", 1, fraction_text(cos_value),
                     fraction_text(one_plus)),
                step("M", fraction_text(diff), fraction_text(one_plus),
                     fraction_text(product)),
                step("D", fraction_text(product), 2, fraction_text(half)),
                step("A", fraction_text(min_lr), fraction_text(half),
                     fraction_text(lr)),
                step("LR_PHASE", "decay"),
            ])
        steps.append(step("LR_VALUE", fraction_text(lr)))
        answer = f"phase={phase}; lr={fraction_text(lr)}"
        steps.append(step("Z", answer))
        problem = (
            "Evaluate a learning-rate schedule with "
            f"base_lr={fraction_text(base_lr)}, min_lr={fraction_text(min_lr)}, "
            f"warmup_steps={warmup}, total_steps={total}, at step t={t}. "
            "Use linear warmup, then cosine decay "
            "lr=min+1/2*(base-min)*(1+cos(pi*progress))."
        )
        return dict(
            problem_id=jid(),
            operation="lr_schedule_warmup_cosine",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
