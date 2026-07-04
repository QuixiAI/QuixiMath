import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.systems_elimination_generator import (
    coeff_term, signed_term, subst_term,
)


def linear_expr(coeff, var, const):
    """Render coeff*var + const with 1-coefficients dropped and signed
    constants: '3y + 2', '-y - 4', 'y', '5'."""
    if coeff == 0:
        return str(const)
    text = coeff_term(coeff, var)
    if const > 0:
        text += f" + {const}"
    elif const < 0:
        text += f" - {abs(const)}"
    return text


class SystemsSubstitutionGenerator(ProblemGenerator):
    """
    Generates systems of linear equations to be solved by substitution.

    Structure:
    Eq1: ax + by = c
    Eq2: dx + ey = f

    At least one variable will have coeff 1 or -1 to make substitution natural.
    Or one equation will be given as y = ... or x = ...
    Coefficients are drawn so the system has a unique solution.
    """

    def __init__(self):
        pass

    def generate(self) -> dict:
        # Construct integer solution
        x_sol = random.randint(-10, 10)
        y_sol = random.randint(-10, 10)

        # Decide format:
        # Type 1: y = mx + b (already isolated)
        # Type 2: x + by = c (easy to isolate)

        type_choice = random.choice(['isolated', 'easy_isolate'])

        steps = []

        if type_choice == 'isolated':
            # Eq1: y = ax + b (or x = ay + b)
            # Eq2: cx + dy = e

            # Decide isolating x or y
            target_var = random.choice(['x', 'y'])
            other_var = 'y' if target_var == 'x' else 'x'

            # Coeffs for Eq1
            a1 = random.randint(-5, 5)
            if a1 == 0: a1 = 1

            val_target = x_sol if target_var == 'x' else y_sol
            val_other = y_sol if target_var == 'x' else x_sol

            b1_const = val_target - a1 * val_other

            # Eq2: cx + dy = e — target_var must actually appear in Eq 2,
            # and substituting Eq1 must leave a nonzero coefficient on
            # other_var (unique solution)
            while True:
                c2 = random.randint(-5, 5)
                d2 = random.randint(-5, 5)
                target_c = c2 if target_var == 'x' else d2
                new_coeff = c2 * a1 + d2 if target_var == 'x' else c2 + d2 * a1
                if target_c != 0 and new_coeff != 0:
                    break

            e2 = c2 * x_sol + d2 * y_sol

            # Format Eq1
            rhs1 = linear_expr(a1, other_var, b1_const)
            eq1_str = f"{target_var} = {rhs1}"

            # Format Eq2
            if c2 == 0:
                eq2_str = f"{coeff_term(d2, 'y')} = {e2}"
            elif d2 == 0:
                eq2_str = f"{coeff_term(c2, 'x')} = {e2}"
            else:
                eq2_str = f"{coeff_term(c2, 'x')} {signed_term(d2, 'y')} = {e2}"

            steps.append(step("SYS_SETUP", eq1_str, eq2_str))

            # Step 1: Subst
            steps.append(step("SYS_SUBST", f"Substitute ({rhs1}) for {target_var} in Eq 2"))

            # Expand and solve: after substitution the equation in
            # other_var alone is new_coeff*other_var + new_const = e2
            if target_var == 'x':
                new_const = c2 * b1_const
            else:
                new_const = d2 * b1_const

            steps.append(step("SYS_EQ_NEW", f"New equation with {other_var} only"))
            steps.append(step("DIST_COMBINE",
                              f"{linear_expr(new_coeff, other_var, new_const)} = {e2}"))

            # Solve linear
            rhs_final = e2 - new_const
            if new_const != 0:
                steps.append(step("EQ_OP_BOTH", "subtract", new_const,
                                  coeff_term(new_coeff, other_var), rhs_final))

            res_other = rhs_final // new_coeff
            steps.append(step("EQ_OP_BOTH", "divide", new_coeff, other_var, res_other))

            # Step Back-Subst
            steps.append(step("SYS_SUBST_BACK", f"Substitute {other_var}={val_other} into Eq 1"))
            steps.append(step("CALC", f"{target_var} = {val_target}"))

            ans = f"x={x_sol}, y={y_sol}"
            steps.append(step("Z", ans))

            return dict(
                problem_id=jid(),
                operation="systems_substitution",
                problem=f"Solve the system:\n1) {eq1_str}\n2) {eq2_str}",
                steps=steps,
                final_answer=ans
            )

        else:
            # Type 2: easy isolate
            # Eq1: x + by = c (coeff 1)
            # Eq2: cx + dy = e

            # Keep both variables present and the system nonsingular:
            # b1, c2, d2 nonzero and -c2*b1 + d2 != 0
            while True:
                b1 = random.randint(-5, 5)
                c2 = random.randint(-5, 5)
                d2 = random.randint(-5, 5)
                new_coeff = -c2 * b1 + d2
                if b1 != 0 and c2 != 0 and d2 != 0 and new_coeff != 0:
                    break

            c1 = x_sol + b1 * y_sol
            e2 = c2 * x_sol + d2 * y_sol

            eq1_str = f"x {signed_term(b1, 'y')} = {c1}"
            eq2_str = f"{coeff_term(c2, 'x')} {signed_term(d2, 'y')} = {e2}"

            steps.append(step("SYS_SETUP", eq1_str, eq2_str))

            # Step Isolate: x = -b1*y + c1
            rhs_iso = linear_expr(-b1, 'y', c1)
            steps.append(step("SYS_ISOLATE", "Isolate x in Eq 1", f"x = {rhs_iso}"))

            # Substitute into Eq 2
            steps.append(step("SYS_SUBST", f"Substitute x in Eq 2"))

            # Solve
            # c2(-b1y + c1) + d2y = e2
            # (-c2*b1 + d2)y + c2*c1 = e2
            new_const = c2 * c1

            steps.append(step("DIST_COMBINE",
                              f"{linear_expr(new_coeff, 'y', new_const)} = {e2}"))

            # Solve linear
            rhs_final = e2 - new_const
            if new_const != 0:
                steps.append(step("EQ_OP_BOTH", "subtract", new_const,
                                  coeff_term(new_coeff, 'y'), rhs_final))

            y_res = rhs_final // new_coeff
            steps.append(step("EQ_OP_BOTH", "divide", new_coeff, "y", y_res))

            # Back subst
            steps.append(step("SYS_SUBST_BACK", f"Substitute y={y_sol} into x = {rhs_iso}"))
            steps.append(step("CALC", f"x = {x_sol}"))

            ans = f"x={x_sol}, y={y_sol}"
            steps.append(step("Z", ans))

            return dict(
                problem_id=jid(),
                operation="systems_substitution",
                problem=f"Solve the system:\n1) {eq1_str}\n2) {eq2_str}",
                steps=steps,
                final_answer=ans
            )
