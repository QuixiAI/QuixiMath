import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def imag_text(value):
    return f"{fraction_text(value)}j"


def complex_text(real, imag):
    real = Fraction(real)
    imag = Fraction(imag)
    if imag == 0:
        return fraction_text(real)
    if real == 0:
        return imag_text(imag)
    sign = "+" if imag > 0 else "-"
    return f"{fraction_text(real)}{sign}{fraction_text(abs(imag))}j"


class ACCircuitGenerator(ProblemGenerator):
    """
    AC circuit impedance, phasor current, and resonance.

    Variants:
    - series_rlc: compute Z and I = V/Z in rectangular phasor form
    - resonance: compute omega0 = 1/sqrt(LC) and resonant impedance

    Op-codes used:
    - AC_SETUP: component values and phasor source
    - AC_FORMULA: impedance, phasor, or resonance relation
    - AC_COMPLEX: rectangular complex value
    - A / S / M / D / E / ROOT (established/shared): exact arithmetic
    - Z: requested AC circuit result
    """

    VARIANTS = ["series_rlc", "resonance"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "series_rlc":
            problem, steps, answer = self._generate_series_rlc()
        else:
            problem, steps, answer = self._generate_resonance()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"ac_circuit_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_series_rlc(self):
        resistance = random.randint(1, 30)
        x_l = random.randint(1, 40)
        x_c = random.randint(1, 40)
        voltage = random.randint(1, 120)
        reactance = x_l - x_c
        z_text = complex_text(resistance, reactance)
        r_sq = resistance ** 2
        x_sq = reactance ** 2
        denominator = r_sq + x_sq
        real_num = voltage * resistance
        neg_voltage = -voltage
        imag_num = neg_voltage * reactance
        current_real = Fraction(real_num, denominator)
        current_imag = Fraction(imag_num, denominator)
        current = complex_text(current_real, current_imag)
        steps = [
            step("AC_SETUP", "series_rlc", f"R={resistance}, XL={x_l}",
                 f"XC={x_c}, V={voltage}"),
            step("AC_FORMULA", "Z=R+j(XL-XC)"),
            step("S", x_l, x_c, reactance),
            step("AC_COMPLEX", "Z", resistance, imag_text(reactance)),
            step("AC_FORMULA", "I=V/Z=V*(R-jX)/(R^2+X^2)"),
            step("E", resistance, 2, r_sq),
            step("E", reactance, 2, x_sq),
            step("A", r_sq, x_sq, denominator),
            step("M", voltage, resistance, real_num),
            step("M", -1, voltage, neg_voltage),
            step("M", neg_voltage, reactance, imag_num),
            step("D", real_num, denominator, fraction_text(current_real)),
            step("D", imag_num, denominator, fraction_text(current_imag)),
            step("AC_COMPLEX", "I", fraction_text(current_real),
                 imag_text(current_imag)),
        ]
        answer = f"Z={z_text} ohm; I={current} A"
        problem = (
            f"A series RLC circuit has R={resistance} ohm, inductive "
            f"reactance XL={x_l} ohm, capacitive reactance XC={x_c} ohm, "
            f"and source phasor V={voltage}+0j V. Find total impedance "
            "and current phasor."
        )
        return problem, steps, answer

    def _generate_resonance(self):
        resistance = random.randint(1, 40)
        omega = random.randint(1, 12)
        inductance = random.randint(1, 12)
        capacitance = Fraction(1, omega ** 2 * inductance)
        lc_product = inductance * capacitance
        omega_sq = omega ** 2
        steps = [
            step("AC_SETUP", "resonance", f"R={resistance}, L={inductance}",
                 f"C={fraction_text(capacitance)}"),
            step("AC_FORMULA", "omega0^2=1/(L*C)"),
            step("M", inductance, fraction_text(capacitance),
                 fraction_text(lc_product)),
            step("D", 1, fraction_text(lc_product), omega_sq),
            step("ROOT", omega_sq, omega),
            step("AC_FORMULA", "at resonance XL=XC so Z=R"),
            step("AC_COMPLEX", "Z", resistance, "0j"),
        ]
        answer = f"omega0={omega} rad/s; Z={resistance} ohm"
        problem = (
            f"A series RLC circuit has R={resistance} ohm, L={inductance} H, "
            f"and C={fraction_text(capacitance)} F. Find the resonant "
            "angular frequency and impedance at resonance."
        )
        return problem, steps, answer
