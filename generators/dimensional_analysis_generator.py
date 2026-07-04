import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec


class DimensionalAnalysisGenerator(ProblemGenerator):
    """
    Performs multi-factor dimensional analysis across dosing (mg/kg), flow rates,
    pressure, and rate conversions with explicit factor-label multiplications/divisions.

    All arithmetic is exact: factor values are Fractions rendered as
    terminating decimals, and kPa->atm inputs are constructed backward as
    multiples of 101.325 so the division is exact.
    """

    def generate(self) -> dict:
        scenarios = [
            {
                "type": "dosing",
                "desc": "Medication dosing",
                "value_unit": "kg",
                "target_unit": "mg",
                "factors": [("dosage", "10 mg", "1 kg")],  # 10 mg/kg
                "note": " at a dosage of 10 mg per kg",
            },
            {
                "type": "flow",
                "desc": "IV flow rate",
                "value_unit": "L/min",
                "target_unit": "mL/hr",
                "factors": [
                    ("volume", "1000 mL", "1 L"),
                    ("time", "60 min", "1 hr"),
                ],
            },
            {
                "type": "pressure",
                "desc": "Pressure conversion",
                "value_unit": "psi",
                "target_unit": "kPa",
                # 1 psi ≈ 6.9 kPa (rounded)
                "factors": [("pressure", "6.9 kPa", "1 psi")],
                "note": " using 1 psi = 6.9 kPa",
            },
            {
                "type": "pressure_atm",
                "desc": "Pressure conversion",
                "value_unit": "kPa",
                "target_unit": "atm",
                # 1 atm = 101.325 kPa => multiply by 1/101.325
                "factors": [("pressure", "1 atm", "101.325 kPa")],
                "note": " using 1 atm = 101.325 kPa",
            },
            {
                "type": "pressure_atm_to_kpa",
                "desc": "Pressure conversion",
                "value_unit": "atm",
                "target_unit": "kPa",
                "factors": [("pressure", "101.325 kPa", "1 atm")],
                "note": " using 1 atm = 101.325 kPa",
            },
            {
                "type": "dose_rate",
                "desc": "Dose rate conversion",
                "value_unit": "mcg/min",
                "target_unit": "mg/hr",
                # mcg -> mg (1 mg / 1000 mcg), min -> hr (60 min / 1 hr)
                "factors": [
                    ("time", "60 min", "1 hr"),
                    ("mass", "1 mg", "1000 mcg"),
                ],
            },
        ]

        scenario = random.choice(scenarios)

        base_value = random.randint(1, 20)
        if scenario["type"] == "dosing":
            value = Fraction(base_value * 5)  # 5,10,... keeps numbers tidy
        elif scenario["type"] in ("flow",):
            value = Fraction(base_value * 2)  # 2,4,... L/min
        elif scenario["type"] == "dose_rate":
            value = Fraction(base_value * 10)  # 10,20,... mcg/min
        elif scenario["type"] == "pressure_atm":
            # Constructed backward: a multiple of 101.325 divides exactly
            value = Fraction("101.325") * base_value
        else:
            value = Fraction(base_value * 3)  # pressure multiples

        steps = []
        running = value
        value_str = dec(value)

        problem = (f"{scenario['desc']}: Convert {value_str} "
                   f"{scenario['value_unit']} to {scenario['target_unit']}"
                   f"{scenario.get('note', '')}")

        for name, num, den in scenario["factors"]:
            steps.append(step("CONV_FACTOR", den, num))
            num_val = Fraction(num.split()[0])
            den_val = Fraction(den.split()[0])
            after_mul = running * num_val
            steps.append(step("M", dec(running), dec(num_val), dec(after_mul)))
            running = after_mul
            if den_val != 1:
                after_div = running / den_val
                steps.append(step("D", dec(running), dec(den_val), dec(after_div)))
                running = after_div

        final_answer = f"{dec(running)} {scenario['target_unit']}"
        steps.append(step("CONV_RESULT", f"{value_str} {scenario['value_unit']}", final_answer))
        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="dimensional_analysis",
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )
