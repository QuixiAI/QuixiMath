import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


H_VALUES = sorted({
    Fraction(n, d)
    for n in range(1, 61)
    for d in range(1, 13)
})

# Spins that keep the explicit matrices blackboard sized (dimension 2j+1).
VERIFY_SPINS = [Fraction(1, 2), Fraction(1), Fraction(3, 2), Fraction(2),
                Fraction(5, 2)]
SCALAR_SPINS = [Fraction(k, 2) for k in range(1, 13)]

SUBJECTS = ["particle", "nucleus", "atom", "ion", "quantum dot", "molecule",
            "lattice site", "state", "nuclear spin", "impurity site",
            "trapped ion", "defect centre"]

OPERATORS = ["JplusJminus", "JminusJplus", "Jz^2", "J^2"]

VERIFY_TEMPLATES = [
    ("Verify the spin-{j} Casimir of a {subject} for hbar={h} using "
     "Jplus={jp}, Jminus={jm}, and Jz={jz}."),
    ("A spin-{j} {subject} has Jz={jz}, Jplus={jp} and Jminus={jm} with "
     "hbar={h}. Verify that J^2=Jz^2+(JplusJminus+JminusJplus)/2 is a "
     "multiple of the identity."),
    ("For a spin-{j} {subject} in units where hbar={h}, the m-th diagonal "
     "entries are Jz -> m*hbar, JplusJminus -> (j+m)(j-m+1)hbar^2 and "
     "JminusJplus -> (j-m)(j+m+1)hbar^2 for m=j down to -j. Compute "
     "J^2=Jz^2+(JplusJminus+JminusJplus)/2."),
    ("Show that the Casimir J^2=Jz^2+(JplusJminus+JminusJplus)/2 of a "
     "spin-{j} {subject} is a multiple of the identity when hbar={h}. The "
     "diagonal entries are Jz^2 -> m^2 hbar^2, JplusJminus -> "
     "(j+m)(j-m+1)hbar^2 and JminusJplus -> (j-m)(j+m+1)hbar^2 for m=j down "
     "to -j."),
    ("Take a spin-{j} {subject} with hbar={h}, Jz={jz} and ladder operators "
     "Jplus={jp}, Jminus={jm}. Work out J^2=Jz^2+(JplusJminus+JminusJplus)/2 "
     "and give it as a multiple of the identity."),
    ("Using Jplus={jp}, Jminus={jm} and Jz={jz} for a spin-{j} {subject} "
     "with hbar={h}, evaluate the Casimir "
     "J^2=Jz^2+(JplusJminus+JminusJplus)/2."),
]

EIGENVALUE_TEMPLATES = [
    ("A spin-{j} {subject} has hbar={h}. Give the eigenvalue of the Casimir "
     "J^2=j(j+1)hbar^2 and the dimension of the multiplet."),
    ("For a spin-{j} {subject} in units where hbar={h}, state the J^2 "
     "eigenvalue and how many m states the multiplet holds."),
    ("Every state of a spin-{j} {subject} is an eigenstate of J^2 with the "
     "same eigenvalue. With hbar={h}, what is that eigenvalue and the "
     "multiplet dimension?"),
    ("The Casimir of angular momentum satisfies J^2=j(j+1)hbar^2. Evaluate "
     "it for a spin-{j} {subject} with hbar={h} and report the multiplet "
     "dimension too."),
    ("Report the Casimir eigenvalue and multiplet dimension of a spin-{j} "
     "{subject} when hbar={h}."),
    ("A spin-{j} {subject} sits in a field with hbar={h}. Compute the J^2 "
     "eigenvalue shared by every state of the multiplet and the number of "
     "those states."),
]

ELEMENT_TEMPLATES = [
    ("For a spin-{j} {subject} with hbar={h}, compute the {op} entry at "
     "m={m}. Use JplusJminus -> (j+m)(j-m+1)hbar^2, JminusJplus -> "
     "(j-m)(j+m+1)hbar^2, Jz^2 -> m^2 hbar^2 and J^2 -> j(j+1)hbar^2."),
    ("A spin-{j} {subject} has hbar={h}. What is the {op} entry at m={m}? "
     "The diagonal rules are JplusJminus -> (j+m)(j-m+1)hbar^2, JminusJplus "
     "-> (j-m)(j+m+1)hbar^2, Jz^2 -> m^2 hbar^2 and J^2 -> j(j+1)hbar^2."),
    ("In the spin-{j} basis of a {subject} with hbar={h}, each of "
     "JplusJminus -> (j+m)(j-m+1)hbar^2, JminusJplus -> (j-m)(j+m+1)hbar^2, "
     "Jz^2 -> m^2 hbar^2 and J^2 -> j(j+1)hbar^2 is diagonal. Give the {op} "
     "entry at m={m}."),
    ("Evaluate the {op} entry at m={m} for a spin-{j} {subject} with "
     "hbar={h}, using JplusJminus -> (j+m)(j-m+1)hbar^2, JminusJplus -> "
     "(j-m)(j+m+1)hbar^2, Jz^2 -> m^2 hbar^2 and J^2 -> j(j+1)hbar^2."),
    ("The operators JplusJminus -> (j+m)(j-m+1)hbar^2, JminusJplus -> "
     "(j-m)(j+m+1)hbar^2, Jz^2 -> m^2 hbar^2 and J^2 -> j(j+1)hbar^2 are "
     "diagonal for a spin-{j} {subject}. With hbar={h}, read off the {op} "
     "entry at m={m}."),
    ("A spin-{j} {subject} sits in a multiplet with hbar={h}. Using the "
     "diagonal rules JplusJminus -> (j+m)(j-m+1)hbar^2, JminusJplus -> "
     "(j-m)(j+m+1)hbar^2, Jz^2 -> m^2 hbar^2 and J^2 -> j(j+1)hbar^2, find "
     "the {op} entry at m={m}."),
]


def fraction_text(value):
    return str(Fraction(value))


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ", ".join(fraction_text(value) for value in row) + "]"
        for row in matrix
    ) + "]"


def radical_text(value):
    """Exact text for sqrt(value) with value a non-negative integer."""
    root = int(round(value ** 0.5))
    if root * root == value:
        return str(root)
    return f"sqrt{value}"


def symbol_matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ", ".join(row) + "]" for row in matrix
    ) + "]"


def diag(values):
    return [
        [values[i] if i == j else Fraction(0) for j in range(len(values))]
        for i in range(len(values))
    ]


def mat_add(A, B):
    return [
        [A[i][j] + B[i][j] for j in range(len(A[0]))]
        for i in range(len(A))
    ]


def mat_scale(A, scalar):
    return [[scalar * value for value in row] for row in A]


def m_values(j):
    """m = j, j-1, ..., -j."""
    return [j - k for k in range(int(2 * j) + 1)]


def spin_label(j):
    if j.denominator == 1:
        return str(j.numerator)
    return f"{j.numerator}_{j.denominator}"


def ladder_matrix_text(j, raising=True):
    """Jplus (or Jminus) as hbar times an exact radical matrix."""
    ms = m_values(j)
    size = len(ms)
    grid = [["0"] * size for _ in range(size)]
    for row, m in enumerate(ms):
        if raising:
            # Jplus connects m -> m+1, i.e. column row to row-1.
            if row == 0:
                continue
            lower = ms[row]
            coefficient = (j - lower) * (j + lower + 1)
            grid[row - 1][row] = radical_text(int(coefficient))
        else:
            if row == size - 1:
                continue
            upper = ms[row]
            coefficient = (j + upper) * (j - upper + 1)
            grid[row + 1][row] = radical_text(int(coefficient))
    return "hbar*" + symbol_matrix_text(grid)


def jz_matrix_text(j):
    ms = m_values(j)
    grid = [[fraction_text(ms[i]) if i == k else "0"
             for k in range(len(ms))] for i in range(len(ms))]
    return "hbar*" + symbol_matrix_text(grid)


class CasimirGenerator(ProblemGenerator):
    """
    Angular-momentum Casimir J^2 = Jz^2 + (J+J- + J-J+)/2 = j(j+1) hbar^2 I.

    Variants:
    - verify: build every diagonal matrix for a spin-j multiplet and confirm
      the Casimir is a multiple of the identity
    - eigenvalue: the shared J^2 eigenvalue and the multiplet dimension
    - element: one diagonal matrix element of J+J-, J-J+, Jz^2 or J^2

    All entries come from the exact ladder relations
    J+J- -> (j+m)(j-m+1) hbar^2 and J-J+ -> (j-m)(j+m+1) hbar^2, so the
    arithmetic stays rational for any half-integer spin.

    Op-codes used:
    - CASIMIR_SETUP / MATRIX_PRODUCT / MATRIX_ADD / MATRIX_SCALE / CHECK
    - DIM: multiplet dimension 2j+1
    - E / A / S / M (established/shared): scalar arithmetic
    - Z: exact Casimir value
    """

    VARIANTS = ["verify", "eigenvalue", "element"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _verify(self, hbar, subject):
        j = random.choice(VERIFY_SPINS)
        hbar_sq = hbar ** 2
        ms = m_values(j)
        j_plus_j_minus = diag([(j + m) * (j - m + 1) * hbar_sq for m in ms])
        j_minus_j_plus = diag([(j - m) * (j + m + 1) * hbar_sq for m in ms])
        ladder_sum = mat_add(j_plus_j_minus, j_minus_j_plus)
        ladder_half = mat_scale(ladder_sum, Fraction(1, 2))
        jz_sq = diag([m * m * hbar_sq for m in ms])
        casimir = mat_add(jz_sq, ladder_half)
        j_plus_one = j + 1
        jj1 = j * j_plus_one
        eigen = jj1 * hbar_sq
        identity_target = diag([eigen for _ in ms])

        steps = [
            step("CASIMIR_SETUP", f"spin={fraction_text(j)}",
                 f"hbar={fraction_text(hbar)}", "J^2=Jz^2+(J+J-+J-J+)/2"),
            step("E", fraction_text(hbar), 2, fraction_text(hbar_sq)),
            step("MATRIX_PRODUCT", "Jz^2", matrix_text(jz_sq)),
            step("MATRIX_PRODUCT", "J+J-", matrix_text(j_plus_j_minus)),
            step("MATRIX_PRODUCT", "J-J+", matrix_text(j_minus_j_plus)),
            step("MATRIX_ADD", "J+J- + J-J+", matrix_text(ladder_sum)),
            step("MATRIX_SCALE", "1/2 ladder sum", matrix_text(ladder_half)),
            step("MATRIX_ADD", "Jz^2 + ladder half", matrix_text(casimir)),
            step("A", fraction_text(j), 1, fraction_text(j_plus_one)),
            step("M", fraction_text(j), fraction_text(j_plus_one),
                 fraction_text(jj1)),
            step("M", fraction_text(jj1), fraction_text(hbar_sq),
                 fraction_text(eigen)),
            step("CHECK", "J^2", f"{fraction_text(eigen)}I", "verified"),
        ]
        answer = (
            f"J^2 = {fraction_text(eigen)}I = "
            f"{matrix_text(identity_target)}"
        )
        template = random.choice(VERIFY_TEMPLATES)
        problem = template.format(
            j=fraction_text(j),
            h=fraction_text(hbar),
            subject=subject,
            jp=ladder_matrix_text(j, True),
            jm=ladder_matrix_text(j, False),
            jz=jz_matrix_text(j),
        )
        return j, problem, steps, answer

    def _eigenvalue(self, hbar, subject):
        j = random.choice(SCALAR_SPINS)
        hbar_sq = hbar ** 2
        j_plus_one = j + 1
        jj1 = j * j_plus_one
        eigen = jj1 * hbar_sq
        dim = int(2 * j) + 1
        trace = dim * eigen
        steps = [
            step("CASIMIR_SETUP", f"spin={fraction_text(j)}",
                 f"hbar={fraction_text(hbar)}", "J^2=j(j+1)hbar^2"),
            step("A", fraction_text(j), 1, fraction_text(j_plus_one)),
            step("M", fraction_text(j), fraction_text(j_plus_one),
                 fraction_text(jj1)),
            step("E", fraction_text(hbar), 2, fraction_text(hbar_sq)),
            step("M", fraction_text(jj1), fraction_text(hbar_sq),
                 fraction_text(eigen)),
            step("DIM", f"2*{fraction_text(j)}+1", dim),
            step("CHECK", "trace",
                 f"{dim} * {fraction_text(eigen)} = {fraction_text(trace)}",
                 f"sum of {dim} equal diagonal entries = "
                 f"{fraction_text(trace)}"),
        ]
        answer = f"J^2 = {fraction_text(eigen)}; dim = {dim}"
        problem = random.choice(EIGENVALUE_TEMPLATES).format(
            j=fraction_text(j), h=fraction_text(hbar), subject=subject)
        return j, problem, steps, answer

    def _element(self, hbar, subject):
        j = random.choice(SCALAR_SPINS)
        m = random.choice(m_values(j))
        operator = random.choice(OPERATORS)
        hbar_sq = hbar ** 2
        steps = [
            step("CASIMIR_SETUP", f"spin={fraction_text(j)}",
                 f"hbar={fraction_text(hbar)}",
                 f"{operator} entry at m={fraction_text(m)}"),
            step("E", fraction_text(hbar), 2, fraction_text(hbar_sq)),
        ]
        if operator == "JplusJminus":
            left = j + m
            right = j - m + 1
            coefficient = left * right
            steps.append(step("A", fraction_text(j), fraction_text(m),
                              fraction_text(left)))
            steps.append(step("S", fraction_text(j), fraction_text(m),
                              fraction_text(j - m)))
            steps.append(step("A", fraction_text(j - m), 1,
                              fraction_text(right)))
            steps.append(step("M", fraction_text(left), fraction_text(right),
                              fraction_text(coefficient)))
        elif operator == "JminusJplus":
            left = j - m
            right = j + m + 1
            coefficient = left * right
            steps.append(step("S", fraction_text(j), fraction_text(m),
                              fraction_text(left)))
            steps.append(step("A", fraction_text(j), fraction_text(m),
                              fraction_text(j + m)))
            steps.append(step("A", fraction_text(j + m), 1,
                              fraction_text(right)))
            steps.append(step("M", fraction_text(left), fraction_text(right),
                              fraction_text(coefficient)))
        elif operator == "Jz^2":
            coefficient = m * m
            steps.append(step("E", fraction_text(m), 2,
                              fraction_text(coefficient)))
        else:
            j_plus_one = j + 1
            coefficient = j * j_plus_one
            steps.append(step("A", fraction_text(j), 1,
                              fraction_text(j_plus_one)))
            steps.append(step("M", fraction_text(j), fraction_text(j_plus_one),
                              fraction_text(coefficient)))
        value = coefficient * hbar_sq
        steps.append(step("M", fraction_text(coefficient),
                          fraction_text(hbar_sq), fraction_text(value)))
        if operator in ("JplusJminus", "JminusJplus"):
            partner = (j - m) * (j + m + 1) if operator == "JplusJminus" \
                else (j + m) * (j - m + 1)
            total = coefficient + partner
            expected = 2 * (j * (j + 1) - m * m)
            steps.append(step(
                "CHECK", "sum_rule",
                f"{fraction_text(coefficient)} + {fraction_text(partner)} = "
                f"{fraction_text(total)}",
                f"2(j(j+1) - m^2) = {fraction_text(expected)}",
            ))
        answer = (f"{operator} at m={fraction_text(m)} = "
                  f"{fraction_text(value)}")
        problem = random.choice(ELEMENT_TEMPLATES).format(
            j=fraction_text(j), h=fraction_text(hbar), subject=subject,
            m=fraction_text(m), op=operator)
        return j, problem, steps, answer

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        hbar = random.choice(H_VALUES)
        subject = random.choice(SUBJECTS)
        if variant == "verify":
            j, problem, steps, answer = self._verify(hbar, subject)
        elif variant == "eigenvalue":
            j, problem, steps, answer = self._eigenvalue(hbar, subject)
        else:
            j, problem, steps, answer = self._element(hbar, subject)

        if variant == "verify" and j == 1:
            operation = "casimir_spin1"
        else:
            operation = f"casimir_{variant}_spin{spin_label(j)}"

        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
