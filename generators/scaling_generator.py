import random
from fractions import Fraction

from applied_common import apply_applied_modifier
from base_generator import ProblemGenerator
from helpers import step, jid


APPLIED = True


MAP_AREAS = [
    "coastal region", "mountain district", "river valley", "island chain",
    "national park", "county", "rail corridor", "walking trail",
    "historic district", "lake region", "desert route", "forest reserve",
    "campus", "transit network", "harbor", "farm region", "city center",
    "wildlife refuge", "survey zone", "cycling route",
]

BLUEPRINT_PROJECTS = [
    "library", "school", "workshop", "museum", "clinic", "community hall",
    "studio", "laboratory", "apartment", "office", "station", "theater",
    "warehouse", "classroom", "gymnasium", "visitor center", "cafe",
    "observatory", "gallery", "training center",
]

MODEL_OBJECTS = [
    "tower", "bridge", "building", "aircraft", "ship", "monument",
    "wind turbine", "rocket", "stadium", "lighthouse", "crane", "train",
    "water tank", "radio mast", "museum exhibit", "arch", "greenhouse",
    "factory", "observatory", "pavilion",
]


def pluralize(unit, value):
    if Fraction(value) == 1:
        return unit
    if unit.endswith("ch") or unit.endswith("s"):
        return unit + "es"
    return unit + "s"


def number_text(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    if value.denominator in (2, 4):
        whole, remainder = divmod(value.numerator, value.denominator)
        digits = {Fraction(1, 4): "25", Fraction(1, 2): "5",
                  Fraction(3, 4): "75"}
        tail = digits[Fraction(remainder, value.denominator)]
        return f"{whole}.{tail}"
    return str(value)


class ScalingGenerator(ProblemGenerator):
    """
    Generates scale factor problems.

    Problems involve using a scale factor to find actual or scaled dimensions.
    For example: "A map has a scale of 1 inch = 50 miles. If two cities
    are 3.5 inches apart on the map, what is the actual distance?"

    Op-codes used:
    - SCALE_SETUP: Set up the scale (scale_unit, actual_unit, scale_factor)
    - SCALE_IDENTIFY: Identify what we need to find (given_value, find_type)
    - SCALE_MULT: Multiply to find actual dimension (scaled_value, scale_factor, actual_value)
    - SCALE_DIV: Divide to find scaled dimension (actual_value, scale_factor, scaled_value)
    - Z: Final answer
    """

    # Scale contexts: (scale_unit, actual_unit, typical_scale_factors, context_type)
    MAP_CONTEXTS = [
        ("inch", "miles", [10, 20, 25, 50, 100, 150, 200], "map"),
        ("centimeter", "kilometers", [5, 10, 20, 25, 50, 100], "map"),
        ("inch", "feet", [10, 20, 50, 100, 200], "blueprint"),
        ("centimeter", "meters", [5, 10, 20, 50, 100], "blueprint"),
    ]

    MODEL_CONTEXTS = [
        ("inch", "feet", [2, 4, 5, 8, 10, 12, 16, 20], "model"),
        ("centimeter", "meters", [2, 5, 10, 20, 50, 100], "model"),
    ]

    def generate(self) -> dict:
        """Generate a scale factor problem."""
        problem_type = random.choice(["find_actual", "find_scaled"])

        # Choose context
        all_contexts = self.MAP_CONTEXTS + self.MODEL_CONTEXTS
        scale_unit, actual_unit, _scale_factors, context_type = random.choice(all_contexts)

        # Choose scale factor
        scale_factor = random.randint(2, 150)

        if problem_type == "find_actual":
            return self._generate_find_actual(scale_unit, actual_unit, scale_factor, context_type)
        else:
            return self._generate_find_scaled(scale_unit, actual_unit, scale_factor, context_type)

    def _generate_find_actual(self, scale_unit, actual_unit, scale_factor, context_type) -> dict:
        """Generate a problem where we find the actual dimension from scaled."""
        # Generate a scaled measurement
        scaled_value = Fraction(random.randint(1, 80), 4)

        # Calculate actual value
        actual_value = scaled_value * scale_factor

        if context_type == "map":
            subject = random.choice(MAP_AREAS)
            problem = (
                f"A map of a {subject} has a scale of 1 {scale_unit} = "
                f"{scale_factor} {actual_unit}. If two landmarks are "
                f"{number_text(scaled_value)} "
                f"{pluralize(scale_unit, scaled_value)} apart on the map, "
                f"what is the actual distance between them?"
            )
        elif context_type == "blueprint":
            subject = random.choice(BLUEPRINT_PROJECTS)
            problem = (
                f"A blueprint for a {subject} has a scale of 1 {scale_unit} = "
                f"{scale_factor} {actual_unit}. If a room measures "
                f"{number_text(scaled_value)} "
                f"{pluralize(scale_unit, scaled_value)} on the blueprint, "
                f"what is the actual length of the room?"
            )
        else:  # model
            subject = random.choice(MODEL_OBJECTS)
            problem = (
                f"A scale model of a {subject} uses a scale of 1 {scale_unit} "
                f"= {scale_factor} {actual_unit}. If the model is "
                f"{number_text(scaled_value)} "
                f"{pluralize(scale_unit, scaled_value)} tall, "
                f"what is the actual height?"
            )

        # Format answer
        actual_str = f"{number_text(actual_value)} {actual_unit}"

        # Build steps
        steps = []

        # Step 1: Set up the scale
        steps.append(step("SCALE_SETUP", f"1 {scale_unit}", f"{scale_factor} {actual_unit}", scale_factor))

        # Step 2: Identify given and what to find
        steps.append(step("SCALE_IDENTIFY",
                          f"{number_text(scaled_value)} "
                          f"{pluralize(scale_unit, scaled_value)}",
                          "actual_dimension"))

        # Step 3: Multiply (render whole results without the .0)
        steps.append(step("SCALE_MULT", number_text(scaled_value), scale_factor,
                          number_text(actual_value)))

        # Final answer
        steps.append(step("Z", actual_str))

        return dict(
            problem_id=jid(),
            operation="scale_find_actual",
            problem=problem,
            steps=steps,
            final_answer=actual_str,
        )

    def _generate_find_scaled(self, scale_unit, actual_unit, scale_factor, context_type) -> dict:
        """Generate a problem where we find the scaled dimension from actual."""
        # Generate an actual measurement (must be divisible by scale factor)
        multiplier = random.randint(1, 50)
        actual_value = scale_factor * multiplier

        # Calculate scaled value (exact integer — it is the multiplier)
        scaled_value = multiplier

        # Build problem text
        if context_type == "map":
            subject = random.choice(MAP_AREAS)
            problem = (
                f"A map of a {subject} has a scale of 1 {scale_unit} = "
                f"{scale_factor} {actual_unit}. If the actual distance between "
                f"two landmarks is {actual_value} {actual_unit}, "
                f"how far apart are they on the map?"
            )
        elif context_type == "blueprint":
            subject = random.choice(BLUEPRINT_PROJECTS)
            problem = (
                f"A blueprint for a {subject} has a scale of 1 {scale_unit} = "
                f"{scale_factor} {actual_unit}. "
                f"If a wall is actually {actual_value} {actual_unit} long, "
                f"how long is it on the blueprint?"
            )
        else:  # model
            subject = random.choice(MODEL_OBJECTS)
            problem = (
                f"A scale model of a {subject} uses a scale of 1 {scale_unit} "
                f"= {scale_factor} {actual_unit}. If the actual object is "
                f"{actual_value} {actual_unit} tall, "
                f"how tall should the model be?"
            )

        # Format answer
        scaled_str = f"{scaled_value} {pluralize(scale_unit, scaled_value)}"

        # Build steps
        steps = []

        # Step 1: Set up the scale
        steps.append(step("SCALE_SETUP", f"1 {scale_unit}", f"{scale_factor} {actual_unit}", scale_factor))

        # Step 2: Identify given and what to find
        steps.append(step("SCALE_IDENTIFY", f"{actual_value} {actual_unit}", "scaled_dimension"))

        # Step 3: Divide
        steps.append(step("SCALE_DIV", actual_value, scale_factor, scaled_value))

        # Final answer
        steps.append(step("Z", scaled_str))

        return dict(
            problem_id=jid(),
            operation="scale_find_scaled",
            problem=problem,
            steps=steps,
            final_answer=scaled_str,
        )


class SimilarFiguresScaleGenerator(ProblemGenerator):
    """
    Generates scale factor problems involving similar figures.

    Given two similar figures with some corresponding side lengths,
    find the scale factor or a missing side.

    Op-codes used:
    - SIMILAR_SETUP: Set up the similar figures (figure_type, sides_A, sides_B)
    - SIMILAR_SCALE: Calculate scale factor from known sides (side_A, side_B, scale_factor)
    - SIMILAR_APPLY: Apply scale factor to find missing side (known_side, scale_factor, missing_side)
    - SELECT_RELEVANT / ESTIMATE / ESTIMATE_CHECK / MODEL_EQ (established
      applied-strand modifiers; all four applied modifiers are supported —
      ``plans/applied_plan.md`` §7 close-out sweep)
    - Z: Final answer
    """

    FIGURE_TYPES = ["triangle", "rectangle", "square", "parallelogram"]
    MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")

    def __init__(self, modifier=None):
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.modifier = modifier

    def generate(self) -> dict:
        """Generate a similar figures scale factor problem."""
        figure = random.choice(self.FIGURE_TYPES)

        # Generate a scale factor (as a simple fraction or integer)
        scale_factors = [2, 3, 4, 5, 0.5, 1.5, 2.5]
        scale_factor = random.choice(scale_factors)

        # Generate sides for the smaller figure
        if figure == "triangle":
            sides_small = [random.randint(3, 10) for _ in range(3)]
        elif figure in ["rectangle", "parallelogram"]:
            sides_small = [random.randint(3, 10), random.randint(3, 10)]
        else:  # square
            sides_small = [random.randint(3, 10)]

        # Calculate larger figure sides (render whole values without .0)
        sides_large = [int(s * scale_factor)
                       if s * scale_factor == int(s * scale_factor)
                       else s * scale_factor
                       for s in sides_small]

        # Decide which side to "hide"
        hidden_idx = random.randint(0, len(sides_small) - 1)
        known_idx = (hidden_idx + 1) % len(sides_small) if len(sides_small) > 1 else 0

        # Build problem text
        if figure == "triangle":
            problem = (
                f"Triangles ABC and DEF are similar. In triangle ABC, the sides are "
                f"{sides_small[0]}, {sides_small[1]}, and {sides_small[2]} units. "
                f"In triangle DEF, one side corresponding to the {sides_small[known_idx]}-unit side "
                f"is {sides_large[known_idx]} units. "
                f"What is the length of the side corresponding to the {sides_small[hidden_idx]}-unit side?"
            )
        elif figure == "rectangle":
            problem = (
                f"Rectangles ABCD and EFGH are similar. Rectangle ABCD has dimensions "
                f"{sides_small[0]} by {sides_small[1]} units. "
                f"If the {sides_small[known_idx]}-unit side of ABCD corresponds to a "
                f"{sides_large[known_idx]}-unit side in EFGH, "
                f"what is the length corresponding to the {sides_small[hidden_idx]}-unit side?"
            )
        elif figure == "parallelogram":
            problem = (
                f"Parallelograms ABCD and EFGH are similar with sides "
                f"{sides_small[0]} and {sides_small[1]} units in ABCD. "
                f"If the {sides_small[known_idx]}-unit side corresponds to "
                f"{sides_large[known_idx]} units in EFGH, "
                f"what is the length of the side corresponding to {sides_small[hidden_idx]} units?"
            )
        else:  # square
            problem = (
                f"Squares ABCD and EFGH are similar. Square ABCD has sides of "
                f"{sides_small[0]} units. "
                f"If square EFGH has sides of {sides_large[0]} units, "
                f"what is the scale factor from ABCD to EFGH?"
            )

        # Build steps
        steps = []

        # For squares, we're finding the scale factor
        if figure == "square":
            steps.append(step("SIMILAR_SETUP", figure, str(sides_small[0]), str(sides_large[0])))
            steps.append(step("SIMILAR_SCALE", sides_large[0], sides_small[0], scale_factor))
            final_answer = str(scale_factor) if scale_factor == int(scale_factor) else str(scale_factor)
        else:
            # For other figures, find the missing side
            sides_small_str = ",".join(str(s) for s in sides_small)
            sides_large_known = f"{sides_large[known_idx]} (others unknown)"

            steps.append(step("SIMILAR_SETUP", figure, sides_small_str, sides_large_known))
            steps.append(step("SIMILAR_SCALE", sides_large[known_idx], sides_small[known_idx], scale_factor))

            missing_side = sides_large[hidden_idx]
            steps.append(step("SIMILAR_APPLY", sides_small[hidden_idx], scale_factor, missing_side))

            if missing_side == int(missing_side):
                final_answer = str(int(missing_side))
            else:
                final_answer = str(missing_side)

        steps.append(step("Z", final_answer))

        operation = "similar_scale_factor" if figure == "square" else "similar_missing_side"
        if figure == "square":
            used = [f"ABCD side {sides_small[0]}", f"EFGH side {sides_large[0]}"]
            value, model = Fraction(scale_factor), "scale factor = EFGH side/ABCD side"
        else:
            used = [f"small sides {sides_small}", f"large side {sides_large[known_idx]}"]
            value, model = Fraction(missing_side), "missing side = known side × scale factor"

        result = dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )
        modifier = self.modifier or random.choice(self.MODIFIERS)
        return apply_applied_modifier(result, modifier, used, value, model, renderer=str)
