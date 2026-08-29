import random
from fractions import Fraction

from applied_common import apply_applied_modifier, method_word_hits
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.pythagorean_common import (
    random_scaled_triple,
    triangle_labels,
)


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")


class PythagoreanLegGenerator(ProblemGenerator):
    """
    Generates Pythagorean theorem problems to find a leg.

    Given hypotenuse (c) and one leg (a), find the other leg (b).
    Formula: a² + b² = c², so b = √(c² - a²)

    Uses Pythagorean triples to ensure clean answers.

    Op-codes used:
    - PYTHAG_SETUP: Set up the right triangle (hypotenuse, known_leg, unknown)
    - PYTHAG_FORMULA: State the theorem (a² + b² = c²)
    - PYTHAG_SUBSTITUTE: Substitute known values (equation)
    - PYTHAG_SQUARE: Calculate squares (value, squared)
    - PYTHAG_SOLVE: Solve for unknown (calculation, result)
    - PYTHAG_ROOT: Take square root (value, root)
    - Z: Final answer
    """

    def generate(self) -> dict:
        """Generate a Pythagorean theorem find-leg problem."""
        a, b, c = random_scaled_triple()
        vertex_a, vertex_b, vertex_c = triangle_labels()
        first_leg = f"{vertex_a}{vertex_b}"
        second_leg = f"{vertex_b}{vertex_c}"
        hypotenuse = f"{vertex_a}{vertex_c}"

        # Randomly choose which leg is given and which to find
        if random.choice([True, False]):
            given_leg = a
            unknown_leg = b
            given_side = first_leg
            unknown_side = second_leg
        else:
            given_leg = b
            unknown_leg = a
            given_side = second_leg
            unknown_side = first_leg

        problem = (
            f"In right triangle {vertex_a}{vertex_b}{vertex_c}, "
            f"hypotenuse {hypotenuse} is {c} units and leg {given_side} "
            f"is {given_leg} units. Find leg {unknown_side}."
        )

        steps_list = []
        steps_list.append(step("PYTHAG_SETUP", f"{hypotenuse}={c}",
                               f"{given_side}={given_leg}",
                               f"{unknown_side}=?"))
        steps_list.append(step("PYTHAG_FORMULA", "a² + b² = c²"))
        steps_list.append(step("PYTHAG_SUBSTITUTE", f"{given_leg}² + b² = {c}²"))

        given_squared = given_leg ** 2
        hyp_squared = c ** 2

        steps_list.append(step("PYTHAG_SQUARE", given_leg, given_squared))
        steps_list.append(step("PYTHAG_SQUARE", c, hyp_squared))
        steps_list.append(step("PYTHAG_SOLVE", f"b² = {hyp_squared} - {given_squared}", hyp_squared - given_squared))

        b_squared = hyp_squared - given_squared
        steps_list.append(step("PYTHAG_ROOT", b_squared, unknown_leg))

        final_answer = f"{unknown_leg} units"
        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="pythagorean_find_leg",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )


class PythagoreanWordProblemGenerator(ProblemGenerator):
    """
    Generates word problems involving the Pythagorean theorem.

    Contexts include ladders against walls, diagonal of rectangles, etc.

    Op-codes used:
    - PYTHAG_CONTEXT: Describe the real-world setup (context, values)
    - PYTHAG_MODEL: Model as a right triangle (a, b, c identification)
    - PYTHAG_FORMULA: State the theorem
    - PYTHAG_SUBSTITUTE: Substitute values
    - PYTHAG_CALCULATE: Perform calculations
    - SELECT_RELEVANT / ESTIMATE / ESTIMATE_CHECK / MODEL_EQ (established
      applied-strand modifiers; all four applied modifiers are supported —
      ``plans/applied_plan.md`` §7 close-out sweep)
    - Z: Final answer
    """

    MODIFIERS = MODIFIERS

    def __init__(self, modifier=None):
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.modifier = modifier

    def generate(self) -> dict:
        """Generate a Pythagorean theorem word problem."""
        context = random.choice(['ladder', 'diagonal', 'distance'])
        a, b, c = random_scaled_triple()
        # Vertex letters are drawn independently of any wordlist; redraw the
        # rare triple that happens to spell a banned method abbreviation
        # (e.g. GCF, LCM) so the diagram note never names a method.
        while True:
            vertices = triangle_labels()
            diagram = "".join(vertices)
            if not method_word_hits(diagram):
                break
        diagram_note = (f"Use right-triangle diagram {diagram}, with the "
                        f"right angle at {vertices[1]}.")

        if context == 'ladder':
            result, used, value, model = self._generate_ladder(a, b, c, diagram, diagram_note)
        elif context == 'diagonal':
            result, used, value, model = self._generate_diagonal(a, b, c, diagram, diagram_note)
        else:
            result, used, value, model = self._generate_distance(a, b, c, diagram, diagram_note)

        modifier = self.modifier or random.choice(self.MODIFIERS)
        return apply_applied_modifier(result, modifier, used, value, model, renderer=str)

    def _generate_ladder(self, a, b, c, diagram, diagram_note):
        """Generate ladder against wall problem."""
        # Ladder (c) against wall, find either height (b) or distance from wall (a)
        find_height = random.choice([True, False])

        if find_height:
            problem = (f"A {c}-foot ladder is placed against a wall. The "
                       f"base of the ladder is {a} feet from the wall. How "
                       f"high up the wall does the ladder reach? "
                       f"{diagram_note}")
            answer = b
            given = a
        else:
            problem = (f"A {c}-foot ladder reaches {b} feet up a wall. "
                       f"How far is the base of the ladder from the wall? "
                       f"{diagram_note}")
            answer = a
            given = b

        steps_list = []
        steps_list.append(step("PYTHAG_CONTEXT", "ladder",
                               f"ladder={c}ft, given={given}ft",
                               f"diagram={diagram}"))
        # model the unknown as ? — never leak the answer in the setup
        if find_height:
            steps_list.append(step("PYTHAG_MODEL", f"ground={a}", "wall=?", f"ladder={c}"))
        else:
            steps_list.append(step("PYTHAG_MODEL", "ground=?", f"wall={b}", f"ladder={c}"))
        steps_list.append(step("PYTHAG_FORMULA", "a² + b² = c²"))

        if find_height:
            steps_list.append(step("PYTHAG_SUBSTITUTE", f"{a}² + h² = {c}²"))
            steps_list.append(step("PYTHAG_CALCULATE", f"h² = {c**2} - {a**2} = {c**2 - a**2}", c**2 - a**2))
            steps_list.append(step("PYTHAG_CALCULATE", f"h = √{c**2 - a**2}", answer))
        else:
            steps_list.append(step("PYTHAG_SUBSTITUTE", f"d² + {b}² = {c}²"))
            steps_list.append(step("PYTHAG_CALCULATE", f"d² = {c**2} - {b**2} = {c**2 - b**2}", c**2 - b**2))
            steps_list.append(step("PYTHAG_CALCULATE", f"d = √{c**2 - b**2}", answer))

        final_answer = f"{answer} feet"
        steps_list.append(step("Z", final_answer))

        result = dict(
            problem_id=jid(),
            operation="pythagorean_word_problem",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )
        used = [f"ladder {c} ft", f"given {given} ft"]
        return result, used, Fraction(answer), "a² + b² = c²"

    def _generate_diagonal(self, a, b, c, diagram, diagram_note):
        """Generate rectangle diagonal problem."""
        problem = (f"A rectangle has a length of {a} units and a width of "
                   f"{b} units. What is the length of its diagonal? "
                   f"{diagram_note}")

        steps_list = []
        steps_list.append(step("PYTHAG_CONTEXT", "rectangle_diagonal",
                               f"length={a}, width={b}",
                               f"diagram={diagram}"))
        steps_list.append(step("PYTHAG_MODEL", f"length={a}", f"width={b}", "diagonal=?"))
        steps_list.append(step("PYTHAG_FORMULA", "d² = l² + w²"))
        steps_list.append(step("PYTHAG_SUBSTITUTE", f"d² = {a}² + {b}²"))
        steps_list.append(step("PYTHAG_CALCULATE", f"d² = {a**2} + {b**2} = {a**2 + b**2}", a**2 + b**2))
        steps_list.append(step("PYTHAG_CALCULATE", f"d = √{c**2}", c))

        final_answer = f"{c} units"
        steps_list.append(step("Z", final_answer))

        result = dict(
            problem_id=jid(),
            operation="pythagorean_word_problem",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )
        used = [f"length {a}", f"width {b}"]
        return result, used, Fraction(c), "d² = l² + w²"

    def _generate_distance(self, a, b, c, diagram, diagram_note):
        """Generate distance/displacement problem."""
        problem = (f"A person walks {a} meters east and then {b} meters "
                   f"north. What is the straight-line distance from the "
                   f"starting point? {diagram_note}")

        steps_list = []
        steps_list.append(step("PYTHAG_CONTEXT", "displacement",
                               f"east={a}m, north={b}m",
                               f"diagram={diagram}"))
        steps_list.append(step("PYTHAG_MODEL", f"east={a}", f"north={b}", "distance=?"))
        steps_list.append(step("PYTHAG_FORMULA", "d² = east² + north²"))
        steps_list.append(step("PYTHAG_SUBSTITUTE", f"d² = {a}² + {b}²"))
        steps_list.append(step("PYTHAG_CALCULATE", f"d² = {a**2} + {b**2} = {a**2 + b**2}", a**2 + b**2))
        steps_list.append(step("PYTHAG_CALCULATE", f"d = √{c**2}", c))

        final_answer = f"{c} meters"
        steps_list.append(step("Z", final_answer))

        result = dict(
            problem_id=jid(),
            operation="pythagorean_word_problem",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )
        used = [f"east {a} m", f"north {b} m"]
        return result, used, Fraction(c), "d² = east² + north²"
