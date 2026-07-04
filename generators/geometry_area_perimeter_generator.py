import random
from base_generator import ProblemGenerator
from helpers import step, jid

# Pythagorean (leg, hypotenuse) pairs keyed by the other leg (the height),
# used to compose triangles/trapezoids whose stated sides, height, and base
# are geometrically consistent with integer values.
HEIGHT_PAIRS = {
    3: [(4, 5)],
    4: [(3, 5)],
    5: [(12, 13)],
    6: [(8, 10)],
    8: [(6, 10), (15, 17)],
    9: [(12, 15)],
    12: [(5, 13), (9, 15), (16, 20)],
    15: [(8, 17), (20, 25)],
    16: [(12, 20)],
    20: [(15, 25), (21, 29)],
    24: [(7, 25), (10, 26), (18, 30)],
}


class GeometryAreaPerimeterGenerator(ProblemGenerator):
    """Computes perimeter and area for basic shapes with human-style steps.

    Figures are constructed to actually exist: triangle sides/height come
    from Pythagorean pairs sharing the height leg, parallelogram height is
    less than the slant side, and trapezoid legs satisfy
    leg^2 = height^2 + offset^2.
    """

    def generate(self) -> dict:
        shape = random.choice(["rectangle", "triangle", "parallelogram", "trapezoid"])
        steps = []

        if shape == "rectangle":
            w = random.randint(2, 20)
            h = random.randint(2, 20)
            problem = f"Rectangle width {w}, height {h}: find perimeter and area"
            # Perimeter: 2*(w+h)
            s = w + h
            steps.append(step("A", w, h, s))
            perim = 2 * s
            steps.append(step("M", 2, s, perim))
            steps.append(step("PERIM", perim))
            # Area: w*h
            area = w * h
            steps.append(step("M", w, h, area))
            steps.append(step("AREA", area))

        elif shape == "triangle":
            # Compose two right triangles sharing the height leg: the
            # stated sides, base, and height are consistent by construction
            height = random.choice(list(HEIGHT_PAIRS))
            m, side2 = random.choice(HEIGHT_PAIRS[height])
            k, side3 = random.choice(HEIGHT_PAIRS[height])
            base = m + k
            problem = f"Triangle sides {base}, {side2}, {side3} with height {height} to base {base}: find perimeter and area"
            perim = base + side2 + side3
            steps.append(step("A", base, side2, base + side2))
            steps.append(step("A", base + side2, side3, perim))
            steps.append(step("PERIM", perim))
            # Area = (base * height)/2
            mult = base * height
            steps.append(step("M", base, height, mult))
            area = mult // 2
            steps.append(step("D", mult, 2, area))
            steps.append(step("AREA", area))

        elif shape == "parallelogram":
            height = random.randint(3, 12)
            side = random.randint(height + 1, 16)  # slant side exceeds height
            base = random.randint(3, 15)
            problem = f"Parallelogram base {base}, side {side}, height {height}: find perimeter and area"
            perim = 2 * (base + side)
            steps.append(step("A", base, side, base + side))
            steps.append(step("M", 2, base + side, perim))
            steps.append(step("PERIM", perim))
            area = base * height
            steps.append(step("M", base, height, area))
            steps.append(step("AREA", area))

        else:  # trapezoid (isosceles)
            # leg^2 = height^2 + offset^2 with a Pythagorean triple
            height = random.choice(list(HEIGHT_PAIRS))
            offset, leg = random.choice(HEIGHT_PAIRS[height])
            base2 = random.randint(3, 15)
            base1 = base2 + 2 * offset
            problem = f"Trapezoid bases {base1}, {base2}, legs {leg}, height {height}: find perimeter and area"
            sum_bases = base1 + base2
            perim = sum_bases + 2 * leg
            steps.append(step("A", base1, base2, sum_bases))
            steps.append(step("M", 2, leg, 2 * leg))
            steps.append(step("A", sum_bases, 2 * leg, perim))
            steps.append(step("PERIM", perim))
            # Area = ((b1 + b2) / 2) * h — sum of bases is even by construction
            half_sum = sum_bases // 2
            steps.append(step("D", sum_bases, 2, half_sum))
            area = half_sum * height
            steps.append(step("M", half_sum, height, area))
            steps.append(step("AREA", area))

        perim_val = next(s.split("|")[1] for s in steps if s.startswith("PERIM"))
        area_val = next(s.split("|")[1] for s in steps if s.startswith("AREA"))
        final_answer = f"Perimeter={perim_val}, Area={area_val}"
        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation=f"geometry_{shape}",
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )
