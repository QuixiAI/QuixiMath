import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid

# display symbols per A0: < > ≤ ≥
SYM = {'<': '<', '<=': '≤', '>': '>', '>=': '≥'}


def frac_str(num, den):
    """num/den reduced to lowest terms (6/4 -> 3/2, 6/3 -> 2)."""
    value = Fraction(num, den)
    return (str(value.numerator) if value.denominator == 1
            else f"{value.numerator}/{value.denominator}")

class AbsoluteValueInequalityGenerator(ProblemGenerator):
    """
    Generates absolute value inequalities: |ax + b| < c, |ax + b| > c, etc.
    
    Problem types:
    - Less than (AND): |ax + b| < c  ->  -c < ax + b < c
    - Greater than (OR): |ax + b| > c ->  ax + b > c OR ax + b < -c
    
    Steps:
    1. Setup
    2. Split into compound inequality
    3. Solve
    4. Graph/Interval notation (text representation)
    """
    
    def __init__(self):
        pass
        
    def generate(self) -> dict:
        outcome = random.choices(['standard', 'special'], weights=[90, 10])[0]
        
        # Operators
        ops = ['<', '<=', '>', '>=']
        op = random.choice(ops)
        
        a = random.choice([1, 1, 2, 3, 4, 5])
        b = random.randint(-10, 10)
        
        if outcome == 'standard':
            c = random.randint(1, 20)
        else:
            # Special cases: c <= 0
            c = random.randint(-5, 0)
            
        # Format inner expression
        if a == 1:
            if b == 0:
                inner = "x"
            elif b > 0:
                inner = f"x + {b}"
            else:
                inner = f"x - {abs(b)}"
        else:
            if b == 0:
                inner = f"{a}x"
            elif b > 0:
                inner = f"{a}x + {b}"
            else:
                inner = f"{a}x - {abs(b)}"
                
        sym = SYM[op]
        problem_str = f"|{inner}| {sym} {c}"
        steps = []
        # pipe-safety: step fields must not contain raw '|' — use abs()
        steps.append(step("ABS_INEQ_SETUP", f"abs({inner}) {sym} {c}"))
        
        # Handle special cases with c <= 0
        if c < 0:
            if op in ['<', '<=']:
                ans = "No solution"
                steps.append(step("ABS_INEQ_CHECK", f"{c} < 0", "Absolute value cannot be negative"))
                steps.append(step("Z", ans))
                return self._pack(problem_str, steps, ans)
            else: # >, >=
                ans = "All real numbers"
                steps.append(step("ABS_INEQ_CHECK", f"{c} < 0", "Absolute value is always non-negative"))
                steps.append(step("Z", ans))
                return self._pack(problem_str, steps, ans)
        elif c == 0:
            if op == '<':
                ans = "No solution" # |u| < 0 impossible
            elif op == '<=':
                ans = self._solve_linear_eq(a, b, 0) # |u| <= 0 -> u = 0
            elif op == '>':
                ans = f"x != {self._solve_linear_eq(a, b, 0).split('=')[-1].strip()}" # |u| > 0 -> u != 0
            else: # >=
                ans = "All real numbers"
            
            steps.append(step("ABS_INEQ_SPECIAL", f"c = 0", f"Check logic for {op}"))
            steps.append(step("Z", ans))
            return self._pack(problem_str, steps, ans)

        # Standard cases c > 0
        is_and = op in ['<', '<=']
        
        if is_and:
            # -c < ax + b < c
            steps.append(step("ABS_INEQ_SPLIT", "AND case", f"-{c} {sym} {inner} {sym} {c}"))
            
            # Solve compound: -c < ax + b < c
            # Step 1: subtract b
            left = -c
            right = c
            
            if b != 0:
                op_b = "subtract" if b > 0 else "add"
                val_b = abs(b)
                if op_b == "subtract":
                    left -= val_b
                    right -= val_b
                else:
                    left += val_b
                    right += val_b
                steps.append(step("INEQ_OP_ALL", op_b, val_b, f"{left} {sym} {a}x {sym} {right}"))
                
            # Step 2: divide by a (a is positive here)
            if a != 1:
                l_str = frac_str(left, a)
                r_str = frac_str(right, a)
                steps.append(step("INEQ_OP_ALL", "divide", a, f"{l_str} {sym} x {sym} {r_str}"))
                ans = f"{l_str} {sym} x {sym} {r_str}"
            else:
                ans = f"{left} {sym} x {sym} {right}"
                
            steps.append(step("Z", ans))
            return self._pack(problem_str, steps, ans)
            
        else:
            # OR Case: ax + b > c OR ax + b < -c
            # Be careful with direction flips if we multiply/divide by neg (a is pos here so safe)
            
            # Relation 1: inner > c (keep op)
            rel1 = f"{inner} {sym} {c}"
            # Relation 2: inner < -c (flip op)
            op_flip = '<' if op == '>' else '<='
            rel2 = f"{inner} {SYM[op_flip]} -{c}"

            steps.append(step("ABS_INEQ_SPLIT", "OR case", f"{rel1} or {rel2}"))

            # Solve Part 1
            sol1 = self._solve_simple_ineq(a, b, c, op)
            steps.append(step("ABS_INEQ_PART", "Part 1", f"{rel1} -> {sol1}"))

            # Solve Part 2
            sol2 = self._solve_simple_ineq(a, b, -c, op_flip)
            steps.append(step("ABS_INEQ_PART", "Part 2", f"{rel2} -> {sol2}"))

            ans = f"{sol1} or {sol2}"
            steps.append(step("Z", ans))
            return self._pack(problem_str, steps, ans)

    def _solve_simple_ineq(self, a, b, rhs, op):
        # ax + b op rhs
        curr = rhs
        if b != 0:
            if b > 0: curr -= b
            else: curr += abs(b)

        sym = SYM[op]
        if a != 1:
            return f"x {sym} {frac_str(curr, a)}"
        return f"x {sym} {curr}"

    def _solve_linear_eq(self, a, b, rhs):
        # ax + b = rhs -> x = ...
        curr = rhs - b
        if a != 1:
            return f"x = {frac_str(curr, a)}"
        return f"x = {curr}"

    def _pack(self, prob, steps, ans):
        return dict(
            problem_id=jid(),
            operation="absolute_value_ineq",
            problem=f"Solve: {prob}",
            steps=steps,
            final_answer=ans
        )
