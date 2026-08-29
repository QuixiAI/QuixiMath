"""Problem-text-only brute-force oracles for ScenarioGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.scenario_generator import APPLIED, MODIFIERS, VARIANTS, ScenarioGenerator
from helpers import DELIM

#: Number of Part()s per scenario, for the with_model "composed of N parts" prefix.
PART_COUNTS = {
    "small_business": 4, "road_trip": 5, "event_planning": 4,
    "home_project": 5, "science_lab": 4, "personal_finance": 4,
    "sports_stats": 3, "data_report": 4,
}


def dec(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    scaled, places = value, 0
    while scaled.denominator != 1 and places < 12:
        scaled *= 10
        places += 1
    if scaled.denominator != 1:
        raise AssertionError(f"does not terminate: {value}")
    digits = str(abs(scaled.numerator)).rjust(places + 1, "0")
    text = (digits[:-places] + "." + digits[-places:]).rstrip("0").rstrip(".")
    return ("-" if value < 0 else "") + text


def money(value):
    cents = Fraction(value) * 100
    if cents.denominator != 1:
        raise AssertionError(f"not exact cents: {value}")
    cents = int(cents)
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}${cents // 100}.{cents % 100:02d}"


def frac_percent(fr):
    pct_value = Fraction(fr) * 100
    whole, remainder = divmod(pct_value.numerator, pct_value.denominator)
    remainder = Fraction(remainder, pct_value.denominator)
    if remainder == 0:
        return f"{whole}%"
    try:
        return dec(pct_value) + "%"
    except AssertionError:
        return f"{whole} {remainder.numerator}/{remainder.denominator}%"


def clean(problem):
    return re.sub(r"^An unrelated memo mentions \d+ filed forms\. ", "", problem)


def _solve_small_business(text):
    jan_sales, jan_costs, feb_sales, feb_costs = map(int, re.search(
        r"Jan: sales \$(\d+), costs \$(\d+)\. Feb: sales \$(\d+), costs \$(\d+)", text).groups())
    fixed, price, variable = map(int, re.search(
        r"Fixed costs are \$(\d+) per month and each unit sells for \$(\d+) "
        r"with \$(\d+) of variable cost", text).groups())
    margin = Fraction(jan_sales - jan_costs, jan_sales)
    growth = Fraction(feb_sales - jan_sales, jan_sales)
    march = feb_sales * (1 + growth)
    breakeven = fixed // (price - variable)
    return (f"Q1 {frac_percent(margin)}; Q2 {frac_percent(growth)}; "
            f"Q3 {money(march)}; Q4 {breakeven} units")


def _solve_road_trip(text):
    leg1, leg2, mpg, price, speed = re.search(
        r"the route has two legs: (\d+) miles and (\d+) miles\. The car gets "
        r"(\d+) miles per gallon, gas costs \$(\d+(?:\.\d+)?) per gallon, and the "
        r"average speed is (\d+) mph", text).groups()
    leg1, leg2, mpg, speed = int(leg1), int(leg2), int(mpg), int(speed)
    price = Fraction(price)
    people = int(re.search(r"If (\d+) people split the fuel cost evenly", text).group(1))
    total = leg1 + leg2
    fuel = Fraction(total, mpg)
    cost = fuel * price
    travel_time = Fraction(total, speed)
    per_person = cost / people
    return (f"Q1 {total} miles; Q2 {dec(fuel)} gallons; Q3 {money(cost)}; "
            f"Q4 {dec(travel_time)} hours; Q5 {money(per_person)}")


def _solve_event_planning(text):
    guests, budget, fixed_cost = re.search(
        r"(\d+) guests are expected\. The total budget is \$(\d+(?:\.\d+)?), and "
        r"fixed costs \(venue and decorations\) are \$(\d+(?:\.\d+)?)", text).groups()
    guests, budget, fixed_cost = int(guests), Fraction(budget), Fraction(fixed_cost)
    per_table = int(re.search(r"With (\d+) guests per table", text).group(1))
    extra_pct = Fraction(re.search(r"If (\d+)% more guests RSVP", text).group(1))
    tables = -(-guests // per_table)
    remaining = budget - fixed_cost
    per_guest = Fraction(remaining, guests)
    extra_guests = guests * extra_pct / 100
    assert extra_guests.denominator == 1, text
    extra_guests = int(extra_guests)
    new_guests = guests + extra_guests
    food_cost = per_guest * new_guests
    return (f"Q1 {tables} tables; Q2 {money(per_guest)}; Q3 {new_guests} guests; "
            f"Q4 {money(food_cost)}")


def _solve_home_project(text):
    length, width = map(int, re.search(r"covers a (\d+) ft by (\d+) ft area", text).groups())
    coverage = int(re.search(r"At (\d+) square feet per gallon", text).group(1))
    price_per_gallon = Fraction(re.search(r"At \$(\d+(?:\.\d+)?) per gallon", text).group(1))
    rate = int(re.search(r"At a rate of (\d+) square feet per hour", text).group(1))
    waste_pct = Fraction(re.search(r"Adding (\d+)% extra for waste", text).group(1))
    area = length * width
    gallons = Fraction(area, coverage)
    cost = gallons * price_per_gallon
    hours = Fraction(area, rate)
    with_waste = cost * (1 + waste_pct / 100)
    return (f"Q1 {area} sq ft; Q2 {dec(gallons)} gallons; Q3 {money(cost)}; "
            f"Q4 {dec(hours)} hours; Q5 {money(with_waste)}")


def _solve_science_lab(text):
    final_volume, target_pct, stock_pct = re.search(
        r"To make (\d+) mL of a (\d+)% solution from (\d+)% stock", text).groups()
    final_volume, target_pct, stock_pct = int(final_volume), Fraction(target_pct), Fraction(stock_pct)
    theo_yield, actual_yield = map(int, re.search(
        r"theoretical yield is (\d+) g and the actual yield is (\d+) g", text).groups())
    celsius = int(re.search(r"reaction runs at (-?\d+)°C", text).group(1))
    stock_volume = final_volume * target_pct / stock_pct
    assert stock_volume.denominator == 1, text
    stock_volume = int(stock_volume)
    water = final_volume - stock_volume
    pct_yield = Fraction(actual_yield, theo_yield) * 100
    fahrenheit = celsius * Fraction(9, 5) + 32
    return (f"Q1 {stock_volume} mL of stock; Q2 {water} mL of water; "
            f"Q3 {dec(pct_yield)}%; Q4 {dec(fahrenheit)}°F")


def _solve_personal_finance(text):
    income, housing_pct = re.search(
        r"monthly income of \$(\d+(?:\.\d+)?) and (\d+)% going to housing", text).groups()
    income, housing_pct = Fraction(income), Fraction(housing_pct)
    savings_pct, goal = re.search(
        r"Saving (\d+)% of income each month toward a \$(\d+(?:\.\d+)?) goal", text).groups()
    savings_pct, goal = Fraction(savings_pct), Fraction(goal)
    principal, rate_pct, years = re.search(
        r"\$(\d+(?:\.\d+)?) is invested at (\d+)% annual interest for (\d+) year", text).groups()
    principal, rate_pct, years = Fraction(principal), Fraction(rate_pct), int(years)
    debt, payments_made, payment = re.search(
        r"A \$(\d+(?:\.\d+)?) debt is paid down by (\d+) monthly payments of "
        r"\$(\d+(?:\.\d+)?) each", text).groups()
    debt, payments_made, payment = Fraction(debt), int(payments_made), Fraction(payment)

    housing = income * housing_pct / 100
    monthly_savings = income * savings_pct / 100
    months = goal / monthly_savings
    assert months.denominator == 1, text
    months = int(months)
    factor = (1 + rate_pct / 100) ** years
    value = principal * factor
    remaining = debt - payment * payments_made
    return (f"Q1 {money(housing)}; Q2 {months} months; Q3 {money(value)}; "
            f"Q4 {money(remaining)}")


def _solve_sports_stats(text):
    games_played, wins = map(int, re.search(
        r"After (\d+) games with (\d+) wins", text).groups())
    total_games, target_pct = re.search(
        r"finish the (\d+)-game season at (\d+)% wins or better", text).groups()
    total_games, target_pct = int(total_games), Fraction(target_pct)
    points = [int(v) for v in re.search(
        r"scored ([\d, ]+) points", text).group(1).split(", ")]

    win_pct = Fraction(wins, games_played) * 100
    needed_wins = target_pct * total_games / 100
    assert needed_wins.denominator == 1, text
    needed_wins = int(needed_wins)
    more_needed = max(0, needed_wins - wins)
    avg_points = Fraction(sum(points), len(points))
    return (f"Q1 {dec(win_pct)}%; Q2 {more_needed} more wins; "
            f"Q3 {dec(avg_points)} points")


def _solve_data_report(text):
    values = [int(v) for v in re.search(
        r"values recorded are ([\d, ]+); what is the mean", text).group(1).split(", ")]
    mean = Fraction(sum(values), len(values))
    spread = values[-1] - values[0]
    above_pct = Fraction(values[-1] - mean, mean) * 100
    next_value = 2 * values[-1] - values[-2]
    return (f"Q1 {dec(mean)}; Q2 {spread}; Q3 {dec(above_pct)}%; Q4 {next_value}")


_SOLVERS = {
    "small_business": (r"reports: Jan: sales", _solve_small_business),
    "road_trip": (r"the route has two legs", _solve_road_trip),
    "event_planning": (r"guests are expected", _solve_event_planning),
    "home_project": (r"covers a \d+ ft by \d+ ft area", _solve_home_project),
    "science_lab": (r"a dilution and a reaction are recorded", _solve_science_lab),
    "personal_finance": (r"budget is being reviewed", _solve_personal_finance),
    "sports_stats": (r"track their season so far", _solve_sports_stats),
    "data_report": (r"lists \d+ recorded values", _solve_data_report),
}


def solve(problem):
    text = clean(problem)
    for variant, (marker, solver) in _SOLVERS.items():
        if re.search(marker, text):
            return variant, solver(text)
    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, operation):
    variant, answer = solve(problem)
    if "with_model" in operation:
        answer = f"composed of {PART_COUNTS[variant]} parts; {answer}"
    return variant, answer


class TestScenarioGenerator(unittest.TestCase):
    def test_marker_contract_and_full_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(440)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(20):
                    result = ScenarioGenerator(variant, modifier).generate()
                    self.assertEqual(result["steps"][-1], f"Z{DELIM}{result['final_answer']}")
                    parsed, answer = expected(result["problem"], result["operation"])
                    self.assertEqual(parsed, variant, result["problem"])
                    self.assertEqual(result["final_answer"], answer, result["problem"])
                    self.assertTrue(result.get("skills"), result)
                    seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})

    def test_plans_worked_example(self):
        self.assertEqual(
            _solve_small_business(
                "Jan: sales $4000, costs $2500. Feb: sales $5000, costs "
                "$3000. (1) What was January's profit margin? (2) By what "
                "percent did sales grow from January to February? (3) If "
                "sales keep growing at that rate, what are March sales? "
                "(4) Fixed costs are $1500 per month and each unit sells "
                "for $50 with $20 of variable cost; how many units break "
                "even?"),
            "Q1 37.5%; Q2 25%; Q3 $6250.00; Q4 50 units")

    def test_operation_naming(self):
        random.seed(441)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = ScenarioGenerator(variant, modifier).generate()
                self.assertEqual(result["operation"], f"scenario_{variant}_{modifier}")

    def test_part_markers_are_numbered_in_order(self):
        random.seed(442)
        for variant in VARIANTS:
            result = ScenarioGenerator(variant, "plain").generate()
            part_indices = [int(raw.split(DELIM)[1]) for raw in result["steps"]
                            if raw.split(DELIM)[0] == "PART"]
            self.assertEqual(part_indices, list(range(1, PART_COUNTS[variant] + 1)))

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(443)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = ScenarioGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
                    self.assertTrue(result["final_answer"].startswith(
                        f"composed of {PART_COUNTS[variant]} parts; "))
        with self.assertRaises(ValueError):
            ScenarioGenerator("bogus")
        with self.assertRaises(ValueError):
            ScenarioGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(444)
        for _ in range(1000):
            result = ScenarioGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)

    def test_determinism_under_seed(self):
        random.seed(23)
        gen = ScenarioGenerator()
        first = [gen.generate()["problem"] for _ in range(30)]
        random.seed(23)
        second = [gen.generate()["problem"] for _ in range(30)]
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
