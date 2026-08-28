"""Standard errors and CLT probabilities with supplied normal-table rows.

The ten variants cover sample means and sample proportions. Every standard
error is exact by construction, every probability cutoff is built backward
from a table z-score, and every Φ value used by the scratchpad is printed in
the problem with two decoy rows.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import p4, phi, phi_table, prob_txt
from stats_common import PROP_SE_BANK, num_txt


STATISTICS = True
VENUES = (
    "amber study", "birch survey", "cedar trial", "delta project",
    "ember lab", "forest audit", "granite program", "harbor test",
    "indigo review", "jade pilot", "kestrel study", "lunar trial",
)
LOCATIONS = (
    "north campus", "south campus", "east annex", "west annex",
    "river center", "lake center", "hill school", "valley school",
    "maple office", "oak office", "pine clinic", "cedar clinic",
)
MEAN_CONTEXTS = (
    "commute-time measurements", "package-weight measurements",
    "battery-life measurements", "reaction-time measurements",
    "daily-output measurements", "service-time measurements",
    "water-use measurements", "delivery-time measurements",
)
PROP_CONTEXTS = (
    "residents who approve", "components that pass inspection",
    "customers who renew", "seeds that germinate",
    "packages that arrive on time", "devices that connect",
    "applicants who qualify", "samples that test positive",
)
SHAPES = ("right-skewed", "left-skewed", "uniform", "unknown")
QUERIES = {
    "se_mean": (
        "Find the standard error of x̄.",
        "Compute SD(x̄) from σ and n.",
        "What is SE(x̄)?",
        "Give the exact spread of the sampling distribution of x̄.",
    ),
    "se_prop": (
        "Find the standard error of p̂.",
        "Compute SD(p̂) from p and n.",
        "What is SE(p̂)?",
        "Give the exact spread of the sampling distribution of p̂.",
    ),
    "mean_sd_xbar": (
        "Find the mean and standard deviation of x̄.",
        "Give the center and spread of the sampling distribution of x̄.",
        "Compute E[x̄] and SD(x̄).",
        "Report both sampling-distribution parameters for x̄.",
    ),
    "shape_and_center": (
        "Describe the approximate shape, mean, and standard error of x̄.",
        "Apply the CLT and report the center and spread of x̄.",
        "Give the sampling distribution's approximate shape, mean, and SE.",
        "Use n ≥ 30 to summarize the distribution of x̄.",
    ),
    "n_for_target_se": (
        "Find the required integer sample size.",
        "Solve the standard-error equation for n.",
        "What sample size gives the stated target SE(x̄)?",
        "Determine n from σ and the requested standard error.",
    ),
    "mean_above": (
        "Find the upper-tail probability to four decimal places.",
        "Use the CLT and supplied table to evaluate the x̄ event.",
        "Standardize the sample-mean cutoff and find its upper tail.",
        "Compute the displayed probability for x̄.",
    ),
    "mean_between": (
        "Find the between probability to four decimal places.",
        "Use the CLT and supplied table to evaluate the x̄ interval.",
        "Standardize both sample-mean bounds and subtract the CDF values.",
        "Compute the displayed interval probability for x̄.",
    ),
    "prop_below": (
        "Find the lower-tail probability to four decimal places.",
        "Use the supplied table to evaluate the p̂ event.",
        "Standardize the sample-proportion cutoff and find its lower tail.",
        "Compute the displayed probability for p̂.",
    ),
    "prob_proportion": (
        "Find the interval probability to four decimal places.",
        "Use the supplied table to evaluate the p̂ interval.",
        "Standardize both sample-proportion bounds and subtract the CDF values.",
        "Compute the displayed between probability for p̂.",
    ),
    "unusual_sample_mean": (
        "Classify the observed sample mean as usual or unusual.",
        "Compute z and apply the supplied abs(z) > 2 rule.",
        "Is this x̄ unusual? Include its z-score.",
        "Standardize the observed x̄ and give a composite verdict.",
    ),
}


def _site():
    code = f"cohort {random.choice('ABCDEFGH')}{random.randint(10, 99)}"
    return (f"{random.choice(LOCATIONS)} during the "
            f"{random.choice(VENUES)} ({code})")


def _z_text(value):
    return f"{float(value):.2f}"


def _mean_case():
    root_n = random.randint(6, 15)
    se = random.randint(1, 6)
    sigma = root_n * se
    mean = random.randint(4 * sigma, 4 * sigma + 180)
    return mean, sigma, root_n * root_n, se


def _mean_prefix(mean, sigma, n, target, include_n=True):
    context = random.choice(MEAN_CONTEXTS)
    start = (f"At the {_site()}, {context} have population mean μ = {mean} "
             f"units and population standard deviation σ = {sigma} units. "
             f"The population shape is {random.choice(SHAPES)}. ")
    sampling = (f"Independent random samples of size n = {n} are taken. "
                if include_n else "A future independent random sample will be taken. ")
    return f"{start}{sampling}Target: {target}."


def _prop_prefix(p, n, target):
    return (f"At the {_site()}, the population proportion for "
            f"{random.choice(PROP_CONTEXTS)} is p = {prob_txt(p)}. "
            f"Independent random samples of size n = {n} are taken. "
            f"Target: {target}.")


def _mean_se_steps(sigma, n, se):
    root_n = int(n ** 0.5)
    assert root_n * root_n == n and Fraction(sigma, root_n) == se
    return [step("SE_FORMULA", "SE(x̄) = σ/√n"),
            step("ROOT", n, 2, root_n),
            step("D", sigma, root_n, num_txt(se))]


def _prop_se_steps(p, n, se):
    q = 1 - p
    product = p * q
    variance = product / n
    assert se * se == variance
    return [step("SE_FORMULA", "SE(p̂) = √(p(1 − p)/n)"),
            step("S", 1, prob_txt(p), prob_txt(q)),
            step("M", prob_txt(p), prob_txt(q), prob_txt(product)),
            step("D", prob_txt(product), n, prob_txt(variance)),
            step("ROOT", prob_txt(variance), 2, num_txt(se))]


def _mean_clt_step(n):
    assert n >= 30
    return step("CLT_CHECK", f"n = {n} ≥ 30", "approximately normal")


def _prop_clt_step(p, n):
    successes, failures = n * p, n * (1 - p)
    assert successes >= 10 and failures >= 10
    return step("CLT_CHECK",
                f"np = {prob_txt(successes)} ≥ 10, "
                f"n(1 − p) = {prob_txt(failures)} ≥ 10",
                "approximately normal")


def _table_value(z):
    return Fraction(p4(phi(float(abs(z)))))


def _cdf_steps(z):
    magnitude = abs(z)
    lookup = _table_value(z)
    steps = [step("TABLE_LOOKUP", f"Φ({_z_text(magnitude)})", p4(lookup))]
    if z < 0:
        cdf = 1 - lookup
        steps.extend([
            step("REWRITE", f"Φ({_z_text(z)}) = 1 − Φ({_z_text(magnitude)})"),
            step("S", "1.0000", p4(lookup), p4(cdf)),
        ])
        return steps, cdf
    return steps, lookup


def _two_magnitudes():
    candidates = [Fraction(k, 10) for k in range(4, 26)]
    while True:
        first, second = sorted(random.sample(candidates, 2))
        if second - first != Fraction(1, 5):
            return first, second


class CLTProbabilityGenerator(ProblemGenerator):
    """Generate exact standard errors and supplied-table CLT procedures."""

    VARIANTS = ("se_mean", "se_prop", "mean_sd_xbar", "shape_and_center",
                "n_for_target_se", "mean_above", "mean_between",
                "prop_below", "prob_proportion", "unusual_sample_mean")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _mean_variant(variant):
        mean, sigma, n, se = _mean_case()
        steps = [step("SAMP_DIST_SETUP", f"μ = {mean}, σ = {sigma}, n = {n}",
                      "sampling distribution of x̄")]
        steps.extend(_mean_se_steps(sigma, n, se))
        table = None
        if variant == "se_mean":
            target = "find SE(x̄)"
            answer = num_txt(se)
        elif variant == "mean_sd_xbar":
            target = "find E[x̄] and SD(x̄)"
            steps.append(step("CLT_CENTER", "E[x̄] = μ", mean))
            answer = f"mean {mean}; SD {num_txt(se)}"
        elif variant == "shape_and_center":
            target = "describe the shape, center, and standard error of x̄"
            steps.extend([_mean_clt_step(n),
                          step("CLT_CENTER", "E[x̄] = μ", mean)])
            answer = (f"approximately normal (n = {n} ≥ 30); mean {mean}; "
                      f"SE {num_txt(se)}")
        elif variant == "n_for_target_se":
            target = f"choose n so SE(x̄) = {num_txt(se)}"
            root_n = sigma // se
            steps = [step("SAMP_DIST_SETUP", f"σ = {sigma}, target SE = {num_txt(se)}",
                          "solve for sample size"),
                     step("SE_FORMULA", "SE(x̄) = σ/√n"),
                     step("REWRITE", "√n = σ/SE(x̄)"),
                     step("D", sigma, num_txt(se), root_n),
                     step("E", root_n, 2, n),
                     step("CHECK", "σ/√n", f"{sigma}/{root_n}", num_txt(se))]
            answer = str(n)
            prefix = _mean_prefix(mean, sigma, n, target, include_n=False)
            return prefix, steps, answer, table
        elif variant == "mean_above":
            z = Fraction(random.randint(4, 25), 10)
            cutoff = Fraction(mean) + z * se
            target = f"find P(x̄ > {num_txt(cutoff)})"
            steps.extend([_mean_clt_step(n),
                          step("ZSCORE",
                               f"({num_txt(cutoff)} − {mean})/{num_txt(se)}",
                               _z_text(z))])
            cdf_steps, cdf = _cdf_steps(z)
            answer_value = 1 - cdf
            steps.extend(cdf_steps + [
                step("REWRITE", f"P(x̄ > {num_txt(cutoff)}) = 1 − Φ({_z_text(z)})"),
                step("S", "1.0000", p4(cdf), p4(answer_value)),
            ])
            answer = p4(answer_value)
            table = phi_table([float(z)])
        elif variant == "mean_between":
            lower_z, upper_z = _two_magnitudes()
            lower = Fraction(mean) - lower_z * se
            upper = Fraction(mean) + upper_z * se
            target = f"find P({num_txt(lower)} < x̄ < {num_txt(upper)})"
            steps.extend([_mean_clt_step(n),
                          step("ZSCORE",
                               f"({num_txt(lower)} − {mean})/{num_txt(se)}",
                               _z_text(-lower_z)),
                          step("ZSCORE",
                               f"({num_txt(upper)} − {mean})/{num_txt(se)}",
                               _z_text(upper_z))])
            low_steps, low_cdf = _cdf_steps(-lower_z)
            high_steps, high_cdf = _cdf_steps(upper_z)
            answer_value = high_cdf - low_cdf
            steps.extend(low_steps + high_steps + [
                step("REWRITE", f"P({num_txt(lower)} < x̄ < {num_txt(upper)}) = "
                     f"Φ({_z_text(upper_z)}) − Φ({_z_text(-lower_z)})"),
                step("S", p4(high_cdf), p4(low_cdf), p4(answer_value)),
            ])
            answer = p4(answer_value)
            table = phi_table([float(lower_z), float(upper_z)])
        else:
            z = random.choice((Fraction(3, 2), Fraction(9, 5), Fraction(2),
                               Fraction(21, 10), Fraction(5, 2), Fraction(3)))
            if random.choice((True, False)):
                z = -z
            observed = Fraction(mean) + z * se
            target = (f"classify x̄ = {num_txt(observed)} using the rule "
                      "unusual when abs(z) > 2")
            label = "unusual" if abs(z) > 2 else "usual"
            relation = ">" if abs(z) > 2 else "≤"
            steps.extend([
                _mean_clt_step(n),
                step("ZSCORE", f"({num_txt(observed)} − {mean})/{num_txt(se)}",
                     _z_text(z)),
                step("CHECK", "abs(z) > 2",
                     f"abs({_z_text(z)}) = {num_txt(abs(z))} {relation} 2", label),
            ])
            answer = f"{label}; z = {num_txt(z)}"
        prefix = _mean_prefix(mean, sigma, n, target)
        return prefix, steps, answer, table

    @staticmethod
    def _prop_variant(variant):
        p, n, se = random.choice(PROP_SE_BANK)
        steps = [step("SAMP_DIST_SETUP", f"p = {prob_txt(p)}, n = {n}",
                      "sampling distribution of p̂")]
        steps.extend(_prop_se_steps(p, n, se))
        table = None
        if variant == "se_prop":
            target = "find SE(p̂)"
            answer = num_txt(se)
        elif variant == "prop_below":
            valid = [Fraction(k, 10) for k in range(-25, 26) if k and
                     0 < p + Fraction(k, 10) * se < 1]
            z = random.choice(valid)
            cutoff = p + z * se
            target = f"find P(p̂ < {num_txt(cutoff)})"
            steps.extend([_prop_clt_step(p, n),
                          step("ZSCORE",
                               f"({num_txt(cutoff)} − {prob_txt(p)})/{num_txt(se)}",
                               _z_text(z))])
            cdf_steps, answer_value = _cdf_steps(z)
            steps.extend(cdf_steps)
            answer = p4(answer_value)
            table = phi_table([float(abs(z))])
        else:
            lower_z, upper_z = _two_magnitudes()
            lower, upper = p - lower_z * se, p + upper_z * se
            assert 0 < lower < upper < 1
            target = f"find P({num_txt(lower)} < p̂ < {num_txt(upper)})"
            steps.extend([_prop_clt_step(p, n),
                          step("ZSCORE",
                               f"({num_txt(lower)} − {prob_txt(p)})/{num_txt(se)}",
                               _z_text(-lower_z)),
                          step("ZSCORE",
                               f"({num_txt(upper)} − {prob_txt(p)})/{num_txt(se)}",
                               _z_text(upper_z))])
            low_steps, low_cdf = _cdf_steps(-lower_z)
            high_steps, high_cdf = _cdf_steps(upper_z)
            answer_value = high_cdf - low_cdf
            steps.extend(low_steps + high_steps + [
                step("REWRITE", f"P({num_txt(lower)} < p̂ < {num_txt(upper)}) = "
                     f"Φ({_z_text(upper_z)}) − Φ({_z_text(-lower_z)})"),
                step("S", p4(high_cdf), p4(low_cdf), p4(answer_value)),
            ])
            answer = p4(answer_value)
            table = phi_table([float(lower_z), float(upper_z)])
        prefix = _prop_prefix(p, n, target)
        return prefix, steps, answer, table

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant in ("se_prop", "prop_below", "prob_proportion"):
            prefix, steps, answer, table = self._prop_variant(variant)
        else:
            prefix, steps, answer, table = self._mean_variant(variant)
        pieces = [prefix]
        if table:
            pieces.append(table)
        pieces.append(random.choice(QUERIES[variant]))
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_clt_probability_{variant}",
                "problem": "\n".join(pieces), "steps": steps,
                "final_answer": answer}
