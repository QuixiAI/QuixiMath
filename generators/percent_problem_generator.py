import random
from decimal import Decimal, ROUND_HALF_UP
from base_generator import ProblemGenerator
from helpers import step, jid, DELIM # Import DELIM

# Op-Codes:
# PERCENT_TO_DEC: Convert percent to decimal (percent_str, decimal_val)
# SETUP_PERCENT_EQ: Show the equation setup (e.g., "part = percent_dec * whole", "percent_dec = part / whole")
# REARRANGE_EQ: Show rearranged equation to solve for unknown (e.g., "whole = part / percent_dec")
# PERCENT_CALC_PART: Calculate the part (percent_dec, whole, part_result) - Only for find_part
# DEC_TO_PERCENT: Convert decimal result back to percent (decimal_val, percent_str) - Only for find_percent
# --- Plus division steps (DEC_SHIFT, DIV_SETUP, B, D, M, S, PLACE_DP_Q) used internally ---

def plain(value):
    """Decimal -> minimal plain string (no exponent, no trailing zeros)."""
    value = value.normalize()
    if value.as_tuple().exponent > 0:
        value = value.quantize(Decimal(1))
    return str(value)


class PercentProblemGenerator(ProblemGenerator):
    """Generates various types of percentage problems with detailed division steps."""

    def _generate_division_steps(self, dividend_str, divisor_str):
        """
        Generates detailed long division steps for dividend_str / divisor_str.
        Returns a list of steps and the exact quotient string.
        """
        division_steps = []
        a_dec, b_dec = Decimal(dividend_str), Decimal(divisor_str)

        # 1. Shift decimals: multiply BOTH by 10^(divisor decimals) so the
        # divisor becomes an integer and the ratio is unchanged; skip the
        # no-op step when the divisor is already an integer
        b_dp = len(divisor_str.split(".")[1]) if '.' in divisor_str else 0
        shift_places = b_dp
        scale = Decimal(10) ** shift_places
        new_a_str = plain(a_dec * scale)
        divisor_ld = int(b_dec * scale)
        if divisor_ld == 0: return [], "DivByZero" # Avoid division by zero
        if shift_places:
            division_steps.append(step("DEC_SHIFT", f"{dividend_str}/{divisor_str}", f"{new_a_str}/{divisor_ld}", shift_places))

        # Prepare for long division
        dividend_str_ld = new_a_str.replace('.', '')

        dividend_dp_pos = new_a_str.find('.')
        if dividend_dp_pos == -1: dividend_dp_pos = len(new_a_str)

        division_steps.append(step("DIV_SETUP", dividend_str_ld, divisor_ld))

        # 2. Perform Long Division (Copied from DecimalDivGenerator)
        rem = 0
        q_str = ""
        dividend_digits = list(dividend_str_ld)
        processed_digits = 0
        current_num_str = ""

        while processed_digits < len(dividend_digits) or rem > 0:
             rem_before_bringdown = rem

             if processed_digits < len(dividend_digits):
                 digit = dividend_digits[processed_digits]
                 current_num_str += digit
                 cur = int(current_num_str) if current_num_str else 0
                 if q_str: # Show B only after first quotient digit
                     division_steps.append(step("B", rem_before_bringdown, digit, cur))
             elif rem > 0:
                 digit = '0'
                 current_num_str += digit
                 cur = int(current_num_str) if current_num_str else 0
                 if q_str: # Show B only after first quotient digit
                     division_steps.append(step("B", rem_before_bringdown, digit, cur))
             else:
                 break

             processed_digits += 1

             if cur < divisor_ld:
                 # If we add a '0' to the quotient, we should show the division step
                 if q_str or processed_digits > dividend_dp_pos:
                      q_str += "0"
                      # Add the D step showing division by zero resulted in 0
                      division_steps.append(step("D", cur, divisor_ld, 0))
                 rem = cur
                 current_num_str = str(rem) if rem > 0 else ""
                 # Limit precision for safety
                 if processed_digits >= len(dividend_digits) + 6: break
                 continue

             q_dig = cur // divisor_ld
             prod = q_dig * divisor_ld
             new_rem = cur - prod

             division_steps.append(step("D", cur, divisor_ld, q_dig))
             division_steps.append(step("M", q_dig, divisor_ld, prod))
             division_steps.append(step("S", cur, prod, new_rem))

             q_str += str(q_dig)
             rem = new_rem
             current_num_str = str(rem) if rem > 0 else ""

             if rem == 0 and processed_digits >= len(dividend_digits):
                 break
             if len(q_str.replace('.','')) > len(dividend_str_ld) + 6: # Precision limit
                 break

        # 3. Place Decimal Point Step: the raw quotient digits are exactly
        # the answer's digits; the point goes after its integer digits
        if not q_str: q_str = "0" # Ensure quotient isn't empty
        quotient_str = plain(a_dec / b_dec)
        answer_digits = quotient_str.replace('.', '')
        int_digit_count = (quotient_str.index('.')
                           if '.' in quotient_str else len(quotient_str))
        assert int(q_str) == int(answer_digits), \
            f"quotient digits {q_str} disagree with {quotient_str}"
        division_steps.append(step("PLACE_DP_Q", answer_digits,
                                   int_digit_count, quotient_str))

        return division_steps, quotient_str

    def generate(self) -> dict:
        problem_type = random.choice(['find_part', 'find_percent', 'find_whole'])
        steps = []

        # Generate numbers ensuring relatively clean results
        percent_val = random.choice([10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90])
        percent_dec = Decimal(percent_val) / 100

        if problem_type == 'find_part':
            # "What is P% of W?" - Calculation is multiplication, no division needed
            whole = random.choice([10, 20, 40, 50, 60, 80, 100, 120, 150, 200])
            part = (percent_dec * Decimal(whole)).normalize()
            operation = "percent_find_part"
            problem = f"What is {percent_val}% of {whole}?"

            steps.append(step("PERCENT_TO_DEC", f"{percent_val}%", str(percent_dec)))
            steps.append(step("SETUP_PERCENT_EQ", f"part = {percent_dec} * {whole}"))
            # This step is high-level, but the core operation is multiplication,
            # which has its own detailed generator (DecimalMultGenerator).
            # For simplicity here, we keep this high-level step.
            part_str = plain(part)
            steps.append(step("PERCENT_CALC_PART", str(percent_dec), whole, part_str))
            final_answer_str = part_str

        elif problem_type == 'find_percent':
            # "P is what percent of W?" - Requires division: part / whole
            whole = random.choice([10, 20, 40, 50, 80, 100, 150, 200])
            part_options = [p for p in range(1, whole * 2) if (Decimal(p) / Decimal(whole)).normalize().as_tuple().exponent >= -2] # Allow > 100%
            if not part_options:
                 part = int(Decimal('0.2') * Decimal(whole))
            else:
                 part = random.choice(part_options)

            # Use Decimal for precise final answer calculation
            calculated_percent_dec = (Decimal(part) / Decimal(whole)).normalize()
            calculated_percent_val = calculated_percent_dec * 100

            operation = "percent_find_percent"
            problem = f"{part} is what percent of {whole}?"

            steps.append(step("SETUP_PERCENT_EQ", f"percent_dec = {part} / {whole}"))
            # Generate division steps
            division_steps, quotient_str = self._generate_division_steps(str(part), str(whole))
            steps.extend(division_steps)
            # Convert the final decimal result to percent, minimal digits
            percent_str = f"{plain(calculated_percent_val)}%"
            steps.append(step("DEC_TO_PERCENT", quotient_str, percent_str))
            final_answer_str = percent_str


        else: # find_whole
            # "P is P% of what number?" - Requires division: part / percent_dec
            part = random.choice([5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 90, 100, 120])
            # Use Decimal for precise final answer calculation
            whole_dec = (Decimal(part) / percent_dec).normalize()
            # Ensure the generated 'whole' is an integer for cleaner problems
            if whole_dec != whole_dec.to_integral_value():
                 return self.generate() # Retry if not integer

            whole = int(whole_dec)
            operation = "percent_find_whole"
            problem = f"{part} is {percent_val}% of what number?"

            steps.append(step("PERCENT_TO_DEC", f"{percent_val}%", str(percent_dec)))
            steps.append(step("SETUP_PERCENT_EQ", f"{part} = {percent_dec} * whole"))
            steps.append(step("REARRANGE_EQ", f"whole = {part} / {percent_dec}"))
            # Generate division steps
            division_steps, _ = self._generate_division_steps(str(part), str(percent_dec))
            steps.extend(division_steps)
            final_answer_str = str(whole)


        steps.append(step("Z", final_answer_str))

        return dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=final_answer_str
        )
