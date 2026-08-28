"""Model counts, waiting times, thinning, and superposition exactly.

Variants: ``count_in_interval``, ``no_event_interval``,
``interarrival_within``, ``time_to_second``, ``thinning_rate``,
``superposition_rate``, ``which_type_first``, and ``mean_variance``.
Transcendental values are always supplied to four decimals in the problem;
rate-only variants remain exact. Op-codes: ``PP_SETUP``,
``LOOKUP_SUPPLIED``, ``POW``, ``FACT``, ``RATE_FORMULA``, ``A``, ``S``,
``M``, ``D``, ``ROUND``, ``CHECK``, and ``Z``.
"""
import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import exact, p4, prob_txt


PROBABILITY = True
VENUES = ("amber study", "birch survey", "cedar trial", "delta project",
          "ember lab", "forest audit", "granite program", "harbor test",
          "indigo review", "jade pilot", "kestrel study", "lunar trial",
          "maple project", "nova lab", "onyx survey", "pearl audit",
          "quartz program", "river test", "solar review", "topaz pilot",
          "umber study", "violet trial", "willow project", "zephyr lab")
CITIES = ("Albany", "Boston", "Cedarville", "Dover", "Erie", "Fresno",
          "Galveston", "Hartford", "Ithaca", "Juneau", "Kingston", "Lowell",
          "Madison", "Norfolk", "Olympia", "Portland", "Quincy", "Raleigh",
          "Salem", "Trenton", "Utica", "Ventura", "Wichita", "Yonkers")
NAMES = ("Aiko", "Ben", "Chidi", "Daria", "Elena", "Farah", "Gita", "Hugo",
         "Imani", "Jae", "Kira", "Luca", "Mina", "Noah", "Omar", "Priya",
         "Quinn", "Ravi", "Sofia", "Tariq", "Uma", "Vera", "Wen", "Zola")
EVENTS = ("calls", "arrivals", "requests", "defects", "alerts", "visitors",
          "messages", "repairs", "orders", "registrations")
INTERVAL_BANK = (
    (1, 15), (1, 30), (1, 60), (2, 15), (2, 30), (2, 45),
    (3, 20), (3, 30), (3, 40), (4, 15), (4, 30), (4, 45),
    (5, 12), (5, 24), (6, 10), (6, 20), (6, 30), (6, 40),
)
TIME_BANK = (Fraction(1, 4), Fraction(1, 3), Fraction(1, 2),
             Fraction(2, 3), Fraction(3, 4), Fraction(1),
             Fraction(3, 2), Fraction(2))
P_BANK = (Fraction(1, 5), Fraction(1, 4), Fraction(1, 3), Fraction(2, 5),
          Fraction(1, 2), Fraction(3, 5), Fraction(2, 3), Fraction(3, 4),
          Fraction(4, 5))
RATE_BANK = (Fraction(1, 2), Fraction(2, 3), Fraction(3, 4), Fraction(1),
             Fraction(3, 2), Fraction(2), Fraction(5, 2), Fraction(3),
             Fraction(4), Fraction(5), Fraction(6), Fraction(8))
QUERIES = {
    "count_in_interval": (
        "Find the requested count probability to four decimal places.",
        "Use the Poisson point-mass formula with the supplied exponential value.",
        "Compute the probability of exactly the target number of events.",
        "Evaluate this interval-count probability to four decimals.",
        "Find P(N(t)=k) from the supplied constant.",
    ),
    "no_event_interval": (
        "Find the probability of no events to four decimal places.",
        "Use the supplied exponential value for P(N(t)=0).",
        "Compute the zero-count probability in this interval.",
        "What is the chance that the interval is event-free?",
        "Evaluate P(N(t)=0) from the supplied constant.",
    ),
    "interarrival_within": (
        "Find the probability that the first event occurs within the interval.",
        "Use the complement of the no-event probability.",
        "Compute P(T_1≤t) to four decimal places.",
        "What is the chance that the first arrival occurs by time t?",
        "Evaluate the first-interarrival cdf from the supplied constant.",
    ),
    "time_to_second": (
        "Find the probability that the second event occurs within the interval.",
        "Compute P(T_2≤t)=P(N(t)≥2) to four decimal places.",
        "Remove the zero- and one-event cases using the supplied value.",
        "What is the chance that at least two events occur by time t?",
        "Evaluate the second-arrival cdf from the supplied constant.",
    ),
    "thinning_rate": (
        "Find the type-A rate and expected type-A count in the interval.",
        "Apply independent thinning and report both requested quantities.",
        "Compute the retained process rate and its interval mean.",
        "What rate and expected count result after type-A filtering?",
        "Use the Poisson thinning rule exactly.",
    ),
    "superposition_rate": (
        "Find the combined rate and expected total count in the interval.",
        "Superpose the independent processes and report both quantities.",
        "Add the rates, then compute the interval mean.",
        "What rate and expected count does the merged stream have?",
        "Use the Poisson superposition rule exactly.",
    ),
    "which_type_first": (
        "Find the probability that the next combined event is type A.",
        "Use the competing Poisson rates to identify the next event type.",
        "Compute the exact type-A first-arrival probability.",
        "Which stream supplies the next event, with what type-A probability?",
        "Evaluate lambda_A/(lambda_A+lambda_B) exactly.",
    ),
    "mean_variance": (
        "Find the mean and variance of the interval count.",
        "Use the Poisson moment identity for N(t).",
        "Compute E[N(t)] and Var(N(t)) exactly.",
        "Report the center and variance of this count distribution.",
        "Find both Poisson count moments for the interval.",
    ),
}


def _setting():
    return (random.choice(VENUES), random.choice(CITIES),
            random.choice(NAMES), random.choice(EVENTS))


def _time_text(value):
    value = Fraction(value)
    return f"{prob_txt(value)} hour" + ("" if value == 1 else "s")


def _exp_label(mu):
    mu = Fraction(mu)
    if mu.denominator == 1 and mu != 1:
        return f"e^-{mu.numerator}"
    return f"e^(-{prob_txt(mu)})"


def _supplied(mu):
    return f"{math.exp(-float(mu)):.4f}"


def _interval_data():
    rate, minutes = random.choice(INTERVAL_BANK)
    duration = Fraction(minutes, 60)
    return rate, minutes, duration, rate * duration


def _approx_prefix(rate, minutes, duration, mu, target):
    venue, city, name, events = _setting()
    supplied = _supplied(mu)
    problem = (f"At the {venue} in {city}, {name} models {events} as a Poisson "
               f"process at rate lambda={rate} per hour. Interval length t={minutes} "
               f"minutes ({_time_text(duration)}). Supplied value: "
               f"{_exp_label(mu)} = {supplied}. Target: {target}.")
    return problem, supplied


def _base_steps(rate, minutes, duration, mu, target):
    return [
        step("PP_SETUP", f"rate {rate} per hour, t={minutes} minutes",
             target),
        step("M", rate, prob_txt(duration), prob_txt(mu)),
    ]


def _rounded_step(value):
    answer = p4(value)
    return step("ROUND", exact(value), "4 decimal places", answer), answer


class PoissonProcessGenerator(ProblemGenerator):
    """Generate Poisson-process count, waiting-time, and rate exercises."""

    VARIANTS = ("count_in_interval", "no_event_interval",
                "interarrival_within", "time_to_second", "thinning_rate",
                "superposition_rate", "which_type_first", "mean_variance")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _count():
        rate, minutes, duration, mu = _interval_data()
        k = random.randint(1, 5)
        target = f"P(N(t)={k})"
        problem, supplied = _approx_prefix(rate, minutes, duration, mu, target)
        supplied_value = Fraction(supplied)
        power = mu ** k
        factorial = math.factorial(k)
        numerator = supplied_value * power
        value = numerator / factorial
        rounded, answer = _rounded_step(value)
        steps = _base_steps(rate, minutes, duration, mu, target)
        steps.extend([
            step("LOOKUP_SUPPLIED", _exp_label(mu), supplied),
            step("POW", f"base {prob_txt(mu)}, exponent {k}", exact(power)),
            step("FACT", k, factorial),
            step("M", supplied, exact(power), exact(numerator)),
            step("D", exact(numerator), factorial, exact(value)),
            rounded,
            step("CHECK", "Poisson point mass lies in [0,1]", answer),
        ])
        return problem, steps, answer

    @staticmethod
    def _no_event():
        rate, minutes, duration, mu = _interval_data()
        target = "P(N(t)=0)"
        problem, supplied = _approx_prefix(rate, minutes, duration, mu, target)
        steps = _base_steps(rate, minutes, duration, mu, target)
        steps.extend([
            step("RATE_FORMULA", "P(N(t)=0)=e^(-lambda*t)"),
            step("LOOKUP_SUPPLIED", _exp_label(mu), supplied),
            step("CHECK", "zero-event probability", supplied),
        ])
        return problem, steps, supplied

    @staticmethod
    def _interarrival():
        rate, minutes, duration, mu = _interval_data()
        target = "P(T_1≤t)"
        problem, supplied = _approx_prefix(rate, minutes, duration, mu, target)
        value = 1 - Fraction(supplied)
        answer = f"{float(value):.4f}"
        steps = _base_steps(rate, minutes, duration, mu, target)
        steps.extend([
            step("RATE_FORMULA", "P(T_1≤t)=1-e^(-lambda*t)"),
            step("LOOKUP_SUPPLIED", _exp_label(mu), supplied),
            step("S", 1, supplied, exact(value)),
            step("CHECK", "complement of no event", answer),
        ])
        return problem, steps, answer

    @staticmethod
    def _second_arrival():
        rate, minutes, duration, mu = _interval_data()
        target = "P(T_2≤t)=P(N(t)≥2)"
        problem, supplied = _approx_prefix(rate, minutes, duration, mu, target)
        supplied_value = Fraction(supplied)
        one_plus_mu = 1 + mu
        excluded = supplied_value * one_plus_mu
        value = 1 - excluded
        rounded, answer = _rounded_step(value)
        steps = _base_steps(rate, minutes, duration, mu, target)
        steps.extend([
            step("RATE_FORMULA", "P(T_2≤t)=1-e^(-lambda*t)(1+lambda*t)"),
            step("LOOKUP_SUPPLIED", _exp_label(mu), supplied),
            step("A", 1, prob_txt(mu), prob_txt(one_plus_mu)),
            step("M", supplied, prob_txt(one_plus_mu), exact(excluded)),
            step("S", 1, exact(excluded), exact(value)),
            rounded,
            step("CHECK", "at least two events", answer),
        ])
        return problem, steps, answer

    @staticmethod
    def _thinning():
        venue, city, name, events = _setting()
        rate = random.randint(2, 12)
        probability = random.choice(P_BANK)
        duration = random.choice(TIME_BANK)
        thinned_rate = rate * probability
        mean = thinned_rate * duration
        problem = (f"At the {venue} in {city}, {name} observes a Poisson stream "
                   f"of {events} at base rate lambda={rate} per hour. Each event "
                   f"is independently type A with probability p={prob_txt(probability)}. "
                   f"The interval length is t={_time_text(duration)}. Target: the "
                   f"type-A rate and expected type-A count.")
        steps = [
            step("PP_SETUP", f"lambda={rate}, p={prob_txt(probability)}",
                 f"t={prob_txt(duration)} hour"),
            step("RATE_FORMULA", "thinned rate=p*lambda; mean=p*lambda*t"),
            step("M", rate, prob_txt(probability), prob_txt(thinned_rate)),
            step("M", prob_txt(thinned_rate), prob_txt(duration), prob_txt(mean)),
            step("CHECK", "independent thinning", "type A is Poisson"),
        ]
        answer = (f"type-A rate = {prob_txt(thinned_rate)} per hour; "
                  f"expected type-A count = {prob_txt(mean)}")
        return problem, steps, answer

    @staticmethod
    def _superposition():
        venue, city, name, events = _setting()
        first, second = random.sample(RATE_BANK, 2)
        duration = random.choice(TIME_BANK)
        total_rate = first + second
        mean = total_rate * duration
        problem = (f"At the {venue} in {city}, {name} merges two independent "
                   f"Poisson streams of {events}. Their rates are lambda_1="
                   f"{prob_txt(first)} per hour and lambda_2={prob_txt(second)} per "
                   f"hour. The interval length is t={_time_text(duration)}. Target: "
                   f"the combined rate and expected total count.")
        steps = [
            step("PP_SETUP", f"lambda_1={prob_txt(first)}, lambda_2={prob_txt(second)}",
                 f"t={prob_txt(duration)} hour"),
            step("RATE_FORMULA", "superposed rate=lambda_1+lambda_2; mean=rate*t"),
            step("A", prob_txt(first), prob_txt(second), prob_txt(total_rate)),
            step("M", prob_txt(total_rate), prob_txt(duration), prob_txt(mean)),
            step("CHECK", "independent superposition", "combined stream is Poisson"),
        ]
        answer = (f"combined rate = {prob_txt(total_rate)} per hour; "
                  f"expected total count = {prob_txt(mean)}")
        return problem, steps, answer

    @staticmethod
    def _which_first():
        venue, city, name, events = _setting()
        first, second = random.sample(RATE_BANK, 2)
        total = first + second
        probability = first / total
        other_probability = second / total
        problem = (f"At the {venue} in {city}, {name} monitors independent type-A "
                   f"and type-B Poisson streams of {events}. Their rates are "
                   f"lambda_A={prob_txt(first)} per hour and lambda_B="
                   f"{prob_txt(second)} per hour. Target: the probability that the "
                   f"next combined event is type A.")
        steps = [
            step("PP_SETUP", f"lambda_A={prob_txt(first)}, lambda_B={prob_txt(second)}",
                 "next event type"),
            step("RATE_FORMULA", "P(type A first)=lambda_A/(lambda_A+lambda_B)"),
            step("A", prob_txt(first), prob_txt(second), prob_txt(total)),
            step("D", prob_txt(first), prob_txt(total), prob_txt(probability)),
            step("D", prob_txt(second), prob_txt(total), prob_txt(other_probability)),
            step("A", prob_txt(probability), prob_txt(other_probability), 1),
            step("CHECK", "type-A plus type-B first probabilities", 1),
        ]
        return problem, steps, prob_txt(probability)

    @staticmethod
    def _moments():
        venue, city, name, events = _setting()
        rate = random.choice(RATE_BANK)
        duration = random.choice(TIME_BANK)
        mu = rate * duration
        problem = (f"At the {venue} in {city}, {name} models {events} as a Poisson "
                   f"process at rate lambda={prob_txt(rate)} per hour over an interval "
                   f"of length t={_time_text(duration)}. Target: E[N(t)] and Var(N(t)).")
        steps = [
            step("PP_SETUP", f"lambda={prob_txt(rate)}", f"t={prob_txt(duration)} hour"),
            step("RATE_FORMULA", "N(t)~Poisson(lambda*t); mean=variance=lambda*t"),
            step("M", prob_txt(rate), prob_txt(duration), prob_txt(mu)),
            step("CHECK", "Poisson mean equals variance", prob_txt(mu)),
        ]
        answer = f"E[N(t)] = {prob_txt(mu)}; Var(N(t)) = {prob_txt(mu)}"
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "count_in_interval":
            problem, steps, answer = self._count()
        elif variant == "no_event_interval":
            problem, steps, answer = self._no_event()
        elif variant == "interarrival_within":
            problem, steps, answer = self._interarrival()
        elif variant == "time_to_second":
            problem, steps, answer = self._second_arrival()
        elif variant == "thinning_rate":
            problem, steps, answer = self._thinning()
        elif variant == "superposition_rate":
            problem, steps, answer = self._superposition()
        elif variant == "which_type_first":
            problem, steps, answer = self._which_first()
        else:
            problem, steps, answer = self._moments()
        problem = f"{problem} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_poisson_process_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
