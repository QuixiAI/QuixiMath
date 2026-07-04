import random
from base_generator import ProblemGenerator
from helpers import step, jid


class NumberComparisonGenerator(ProblemGenerator):
    """Compares whole numbers or decimals by place value.

    The scratchpad walks aligned digits left to right (CMP_DIGIT per
    position) until the first difference decides the comparison — the
    actual place-value skill, not an opaque one-step compare.
    """

    def generate(self) -> dict:
        mode = random.choice(["whole", "decimal"])
        if mode == "whole":
            a = random.randint(10, 99999)
            b = random.randint(10, 99999)
            a_str, b_str = str(a), str(b)
            int_width = max(len(a_str), len(b_str))
            a_pad, b_pad = a_str.zfill(int_width), b_str.zfill(int_width)
        else:
            a = round(random.uniform(0.1, 999.9), 2)
            b = round(random.uniform(0.1, 999.9), 2)
            a_str, b_str = str(a), str(b)
            a_int, _, a_frac = a_str.partition(".")
            b_int, _, b_frac = b_str.partition(".")
            int_width = max(len(a_int), len(b_int))
            frac_width = max(len(a_frac), len(b_frac))
            a_pad = a_int.zfill(int_width) + "." + a_frac.ljust(frac_width, "0")
            b_pad = b_int.zfill(int_width) + "." + b_frac.ljust(frac_width, "0")

        # Equal draws are redrawn; equal strings compare trivially
        if a == b:
            return self.generate()

        steps = []
        steps.append(step("ALIGN_NUM", a_pad, b_pad))

        # Walk aligned digits left to right until the first difference
        for idx, (da, db) in enumerate(zip(a_pad, b_pad)):
            if da == ".":
                continue
            if da == db:
                steps.append(step("CMP_DIGIT", f"pos_{idx}", da, db, "="))
            else:
                verdict = ">" if da > db else "<"
                steps.append(step("CMP_DIGIT", f"pos_{idx}", da, db, verdict))
                break

        relation = ">" if a > b else "<"
        steps.append(step("CMP_NUM", a, b, relation))
        steps.append(step("Z", f"{a} {relation} {b}"))

        return dict(
            problem_id=jid(),
            operation="number_compare",
            problem=f"Compare: {a} ? {b}",
            steps=steps,
            final_answer=f"{a} {relation} {b}",
        )
