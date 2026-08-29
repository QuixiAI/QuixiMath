"""Multi-part real-world scenarios threading shared state across sub-questions.

Variants (each an ``operation`` of ``scenario_<name>``): ``small_business``,
``road_trip``, ``event_planning``, ``home_project``, ``science_lab``,
``personal_finance``, ``sports_stats``, ``data_report``. Each scenario asks
3-6 numbered sub-questions over one shared set of facts, using the
:class:`applied_common.Scenario` / :class:`applied_common.Part` harness
(``plans/applied_plan.md`` §5 Strand X). All four applied modifiers apply to
the whole record. Every scenario is drawn backward with a redraw loop that
retries on any inexact intermediate value, so every part's arithmetic is
exact. Op-codes: ``SELECT_RELEVANT``, ``ESTIMATE``, ``ESTIMATE_CHECK``,
``MODEL_EQ``, ``PART``, ``BREAK_EVEN``, ``A``, ``S``, ``M``, ``D``, ``E``,
``DEC_TO_PERCENT``, ``CHECK``, ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import (NAMES, Part, Scenario, dec, estimate_first, exact,
                            frac_percent, money, select_relevant_step)
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("small_business", "road_trip", "event_planning", "home_project",
            "science_lab", "personal_finance", "sports_stats", "data_report")

BUSINESS_NAMES = ("Bright Bakery", "Maple Hardware", "Riverside Books",
                  "Sunny Coffee Cart", "Cedar Print Shop", "Harbor Bike Repair")
TRIP_NAMES = ("the coast road trip", "the mountain loop drive",
             "the cross-county trip", "the lake weekend drive")
EVENT_NAMES = ("a graduation party", "a community fundraiser",
              "a school science night", "a neighborhood picnic")
PROJECT_NAMES = ("a bedroom repaint", "a deck resurfacing",
                 "a garage floor project", "a fence rebuild")
LAB_NAMES = ("a chemistry class", "a biology lab section", "a physics lab section")
FINANCE_NAMES = ("a monthly budget", "a semester budget", "a household budget")
TEAM_NAMES = ("the Riverside Hawks", "the Maple Valley Sharks",
             "the Cedar Point Comets", "the Harbor City Lions")
REPORT_NAMES = ("a weekly sales report", "a daily attendance report",
                "a monthly rainfall report")


def _sum_steps(values):
    """Pairwise running-total ``A`` steps for a list of values (the
    established multi-term accumulation pattern), plus the total."""
    steps, total = [], values[0]
    for v in values[1:]:
        new_total = total + v
        steps.append(step("A", total, v, new_total))
        total = new_total
    return steps, total


class ScenarioGenerator(ProblemGenerator):
    """Generate eight exact multi-part scenarios without naming a method."""

    VARIANTS, MODIFIERS = VARIANTS, MODIFIERS

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant, self.modifier = variant, modifier

    # -- each builder returns (facts, parts, used, estimate_value) ---------

    @staticmethod
    def _small_business():
        for _ in range(500):
            try:
                jan_sales = random.choice((1000, 2000, 4000, 5000, 8000, 10000))
                margin_pct = random.choice((Fraction(20), Fraction(25), Fraction(30),
                                            Fraction(75, 2), Fraction(40), Fraction(50)))
                jan_costs = jan_sales * (1 - margin_pct / 100)
                if jan_costs.denominator != 1:
                    continue
                jan_costs = int(jan_costs)
                growth_pct = random.choice((Fraction(10), Fraction(20), Fraction(25),
                                            Fraction(30), Fraction(40), Fraction(50)))
                feb_sales = jan_sales * (1 + growth_pct / 100)
                if feb_sales.denominator != 1:
                    continue
                feb_sales = int(feb_sales)
                march_sales = feb_sales * (1 + growth_pct / 100)
                if march_sales.denominator != 1:
                    continue
                march_sales = int(march_sales)
                feb_costs = ((feb_sales * random.randint(50, 70)) // 100 // 50) * 50
                per_unit = random.choice((10, 15, 20, 25, 30))
                variable = random.choice((10, 15, 20, 25))
                price = variable + per_unit
                fixed = per_unit * random.randint(20, 150)
                breakeven = fixed // per_unit
                break
            except ZeroDivisionError:
                continue
        else:
            raise AssertionError("no small_business scenario found")

        def q1(_state):
            profit = jan_sales - jan_costs
            margin = Fraction(profit, jan_sales)
            steps = [step("S", jan_sales, jan_costs, profit),
                    step("D", profit, jan_sales, dec(margin)),
                    step("DEC_TO_PERCENT", dec(margin), frac_percent(margin))]
            return steps, frac_percent(margin)

        def q2(_state):
            diff = feb_sales - jan_sales
            rate = Fraction(diff, jan_sales)
            steps = [step("S", feb_sales, jan_sales, diff),
                    step("D", diff, jan_sales, dec(rate)),
                    step("DEC_TO_PERCENT", dec(rate), frac_percent(rate))]
            return steps, frac_percent(rate)

        def q3(_state):
            steps = [step("M", feb_sales, dec(1 + growth_pct / 100), march_sales)]
            return steps, money(march_sales)

        def q4(_state):
            steps = [step("BREAK_EVEN", f"{fixed} = ({price} − {variable})·u", breakeven)]
            return steps, f"{breakeven} units"

        parts = [
            Part("What was January's profit margin?", q1, skills=("percent_of_a_number",)),
            Part("By what percent did sales grow from January to February?", q2,
                skills=("percent_change",)),
            Part("If sales keep growing at that rate, what are March sales?", q3,
                skills=("percent_growth_projection",)),
            Part(f"Fixed costs are ${fixed} per month and each unit sells for "
                 f"${price} with ${variable} of variable cost; how many units "
                 "break even?", q4, skills=("break_even",)),
        ]
        facts = (f"{random.choice(BUSINESS_NAMES)} reports: Jan: sales "
                 f"${jan_sales}, costs ${jan_costs}. Feb: sales ${feb_sales}, "
                 f"costs ${feb_costs}.")
        used = [f"Jan ${jan_sales}/{jan_costs}", f"Feb ${feb_sales}/{feb_costs}"]
        return facts, parts, used, Fraction(margin_pct)

    @staticmethod
    def _road_trip():
        for _ in range(500):
            try:
                leg1, leg2 = 10 * random.randint(5, 30), 10 * random.randint(5, 30)
                total = leg1 + leg2
                mpg = random.choice((20, 25, 32, 40, 50))
                fuel = Fraction(total, mpg)
                dec(fuel)
                price_per_gallon = random.choice((Fraction(3), Fraction(7, 2),
                                                  Fraction(4), Fraction(9, 2)))
                cost = fuel * price_per_gallon
                money(cost)
                avg_speed = random.choice((40, 50, 55, 60, 65))
                travel_time = Fraction(total, avg_speed)
                dec(travel_time)
                people = random.randint(2, 5)
                per_person = cost / people
                money(per_person)
                break
            except ValueError:
                continue
        else:
            raise AssertionError("no road_trip scenario found")

        def q1(_state):
            return [step("A", leg1, leg2, total)], f"{total} miles"

        def q2(_state):
            return [step("D", total, mpg, dec(fuel))], f"{dec(fuel)} gallons"

        def q3(_state):
            steps = [step("M", dec(fuel), dec(price_per_gallon), money(cost))]
            return steps, money(cost)

        def q4(_state):
            return [step("D", total, avg_speed, dec(travel_time))], f"{dec(travel_time)} hours"

        def q5(_state):
            steps = [step("D", money(cost), people, money(per_person))]
            return steps, money(per_person)

        parts = [
            Part("What is the total distance for the trip?", q1, skills=("addition",)),
            Part("How many gallons of fuel are needed?", q2, skills=("unit_rate_division",)),
            Part("What will the fuel cost for the trip?", q3, skills=("unit_price_multiplication",)),
            Part("How many hours of driving at the average speed will it take?", q4,
                skills=("rate_time_distance",)),
            Part(f"If {people} people split the fuel cost evenly, what does each pay?", q5,
                skills=("equal_split",)),
        ]
        facts = (f"For {random.choice(TRIP_NAMES)}, the route has two legs: "
                 f"{leg1} miles and {leg2} miles. The car gets {mpg} miles per "
                 f"gallon, gas costs {money(price_per_gallon)} per gallon, and "
                 f"the average speed is {avg_speed} mph.")
        used = [f"legs {leg1}, {leg2} mi", f"{mpg} mpg", f"{money(price_per_gallon)}/gal",
                f"{avg_speed} mph"]
        return facts, parts, used, Fraction(total)

    @staticmethod
    def _event_planning():
        for _ in range(500):
            try:
                guests = 10 * random.randint(3, 20)
                per_table = random.choice((6, 8, 10, 12))
                tables = -(-guests // per_table)
                budget = 50 * random.randint(20, 200)
                fixed_cost = 50 * random.randint(2, budget // 100)
                remaining = budget - fixed_cost
                per_guest = Fraction(remaining, guests)
                money(per_guest)
                extra_pct = random.choice((Fraction(10), Fraction(20), Fraction(25)))
                extra_guests = guests * extra_pct / 100
                if extra_guests.denominator != 1:
                    continue
                extra_guests = int(extra_guests)
                new_guests = guests + extra_guests
                new_cost_for_food = per_guest * new_guests
                money(new_cost_for_food)
                break
            except ValueError:
                continue
        else:
            raise AssertionError("no event_planning scenario found")

        def q1(_state):
            steps = [step("D", guests, per_table, exact(Fraction(guests, per_table))),
                    step("CEIL", exact(Fraction(guests, per_table)), tables)]
            return steps, f"{tables} tables"

        def q2(_state):
            steps = [step("S", budget, fixed_cost, remaining),
                    step("D", remaining, guests, dec(per_guest))]
            return steps, money(per_guest)

        def q3(_state):
            steps = [step("M", guests, dec(extra_pct / 100), extra_guests),
                    step("A", guests, extra_guests, new_guests)]
            return steps, f"{new_guests} guests"

        def q4(_state):
            steps = [step("M", dec(per_guest), new_guests, dec(new_cost_for_food))]
            return steps, money(new_cost_for_food)

        parts = [
            Part(f"With {per_table} guests per table, how many tables are needed?", q1,
                skills=("ceiling_division",)),
            Part("How much can be spent per guest after fixed costs?", q2,
                skills=("budget_allocation",)),
            Part(f"If {extra_pct}% more guests RSVP than planned, how many guests "
                 "attend in total?", q3, skills=("percent_of_a_number",)),
            Part("At the same per-guest amount, what would food cost for that "
                 "many guests?", q4, skills=("unit_price_multiplication",)),
        ]
        facts = (f"For {random.choice(EVENT_NAMES)}, {guests} guests are "
                 f"expected. The total budget is {money(budget)}, and fixed "
                 f"costs (venue and decorations) are {money(fixed_cost)}.")
        used = [f"{guests} guests", f"budget {money(budget)}", f"fixed {money(fixed_cost)}"]
        return facts, parts, used, Fraction(guests)

    @staticmethod
    def _home_project():
        for _ in range(500):
            try:
                length, width = random.randint(3, 12), random.randint(3, 10)
                area = length * width
                coverage = random.choice((250, 300, 350, 400))
                gallons = Fraction(area, coverage)
                dec(gallons)
                price_per_gallon = random.choice((Fraction(25), Fraction(30),
                                                  Fraction(35), Fraction(40)))
                cost = gallons * price_per_gallon
                money(cost)
                rate = random.choice((20, 25, 30, 40))
                hours = Fraction(area, rate)
                dec(hours)
                waste_pct = random.choice((Fraction(10), Fraction(20), Fraction(25)))
                with_waste = cost * (1 + waste_pct / 100)
                money(with_waste)
                break
            except ValueError:
                continue
        else:
            raise AssertionError("no home_project scenario found")

        def q1(_state):
            steps = [step("M", length, width, area)]
            return steps, f"{area} sq ft"

        def q2(_state):
            steps = [step("D", area, coverage, dec(gallons))]
            return steps, f"{dec(gallons)} gallons"

        def q3(_state):
            steps = [step("M", dec(gallons), money(price_per_gallon), money(cost))]
            return steps, money(cost)

        def q4(_state):
            steps = [step("D", area, rate, dec(hours))]
            return steps, f"{dec(hours)} hours"

        def q5(_state):
            steps = [step("M", money(cost), dec(1 + waste_pct / 100), money(with_waste))]
            return steps, money(with_waste)

        parts = [
            Part("What is the area to be covered?", q1, skills=("area",)),
            Part(f"At {coverage} square feet per gallon, how many gallons are needed?", q2,
                skills=("unit_rate_division",)),
            Part(f"At {money(price_per_gallon)} per gallon, what does the material cost?", q3,
                skills=("unit_price_multiplication",)),
            Part(f"At a rate of {rate} square feet per hour, how many hours will the project take?", q4,
                skills=("rate_time_distance",)),
            Part(f"Adding {waste_pct}% extra for waste and mistakes, what is the total material cost?", q5,
                skills=("waste_allowance",)),
        ]
        facts = (f"{random.choice(PROJECT_NAMES).capitalize()} covers a "
                 f"{length} ft by {width} ft area.")
        used = [f"{length}x{width} ft", f"{coverage} sq ft/gal", f"rate {rate} sq ft/hr"]
        return facts, parts, used, Fraction(area)

    @staticmethod
    def _science_lab():
        for _ in range(500):
            try:
                stock_conc = random.choice((Fraction(20), Fraction(25), Fraction(40), Fraction(50)))
                target_conc = random.choice((Fraction(5), Fraction(8), Fraction(10)))
                if target_conc >= stock_conc:
                    continue
                final_volume = random.choice((100, 200, 250, 500))
                stock_volume = final_volume * target_conc / stock_conc
                if stock_volume.denominator != 1:
                    continue
                stock_volume = int(stock_volume)
                water_volume = final_volume - stock_volume
                theoretical_yield = random.choice((10, 20, 25, 40, 50))
                actual_yield = random.choice(range(theoretical_yield // 2, theoretical_yield))
                percent_yield = Fraction(actual_yield, theoretical_yield) * 100
                dec(percent_yield)
                celsius = random.choice((0, 10, 20, 25, 37, 100))
                fahrenheit = celsius * Fraction(9, 5) + 32
                dec(fahrenheit)
                break
            except ValueError:
                continue
        else:
            raise AssertionError("no science_lab scenario found")

        def q1(_state):
            steps = [step("M", final_volume, dec(target_conc / stock_conc), stock_volume)]
            return steps, f"{stock_volume} mL of stock"

        def q2(_state):
            steps = [step("S", final_volume, stock_volume, water_volume)]
            return steps, f"{water_volume} mL of water"

        def q3(_state):
            steps = [step("D", actual_yield, theoretical_yield, dec(Fraction(actual_yield, theoretical_yield))),
                    step("DEC_TO_PERCENT", dec(Fraction(actual_yield, theoretical_yield)), dec(percent_yield) + "%")]
            return steps, f"{dec(percent_yield)}%"

        def q4(_state):
            steps = [step("M", celsius, dec(Fraction(9, 5)), dec(celsius * Fraction(9, 5))),
                    step("A", dec(celsius * Fraction(9, 5)), 32, dec(fahrenheit))]
            return steps, f"{dec(fahrenheit)}°F"

        parts = [
            Part(f"To make {final_volume} mL of a {dec(target_conc)}% solution "
                 f"from {dec(stock_conc)}% stock, how much stock solution is needed?", q1,
                skills=("dilution",)),
            Part("How much water is added to reach the final volume?", q2, skills=("subtraction",)),
            Part(f"The theoretical yield is {theoretical_yield} g and the actual "
                 f"yield is {actual_yield} g; what is the percent yield?", q3,
                skills=("percent_yield",)),
            Part(f"The reaction runs at {celsius}°C; what is that in °F?", q4,
                skills=("unit_conversion",)),
        ]
        facts = f"In {random.choice(LAB_NAMES)}, a dilution and a reaction are recorded."
        used = [f"stock {dec(stock_conc)}%", f"target {dec(target_conc)}%",
                f"final volume {final_volume} mL"]
        return facts, parts, used, Fraction(theoretical_yield)

    @staticmethod
    def _personal_finance():
        for _ in range(500):
            try:
                income = 100 * random.randint(20, 60)
                housing_pct = random.choice((Fraction(25), Fraction(30), Fraction(35)))
                housing = income * housing_pct / 100
                if housing.denominator != 1:
                    continue
                housing = int(housing)
                savings_pct = random.choice((Fraction(5), Fraction(10), Fraction(15), Fraction(20)))
                monthly_savings = income * savings_pct / 100
                if monthly_savings.denominator != 1:
                    continue
                monthly_savings = int(monthly_savings)
                goal = monthly_savings * random.randint(6, 24)
                months = goal // monthly_savings
                rate_pct = random.choice((Fraction(2), Fraction(4), Fraction(5)))
                years = random.choice((1, 2))
                principal = 100 * random.randint(5, 40)
                factor = (1 + rate_pct / 100) ** years
                value = principal * factor
                money(value)
                debt = 50 * random.randint(6, 40)
                payment = 50 * random.randint(1, debt // 50 // 3)
                payments_made = random.randint(2, 5)
                if payment * payments_made >= debt:
                    continue
                remaining_debt = debt - payment * payments_made
                break
            except (ValueError, ZeroDivisionError):
                continue
        else:
            raise AssertionError("no personal_finance scenario found")

        def q1(_state):
            steps = [step("M", income, dec(housing_pct / 100), housing)]
            return steps, money(housing)

        def q2(_state):
            steps = [step("M", income, dec(savings_pct / 100), monthly_savings),
                    step("D", goal, monthly_savings, months)]
            return steps, f"{months} months"

        def q3(_state):
            steps = [step("E", dec(1 + rate_pct / 100), years, dec(factor)),
                    step("M", principal, dec(factor), money(value))]
            return steps, money(value)

        def q4(_state):
            paid = payment * payments_made
            steps = [step("M", payment, payments_made, paid),
                    step("S", debt, paid, remaining_debt)]
            return steps, money(remaining_debt)

        parts = [
            Part(f"With a monthly income of {money(income)} and {dec(housing_pct)}% "
                 "going to housing, how much is spent on housing?", q1,
                skills=("percent_of_a_number",)),
            Part(f"Saving {dec(savings_pct)}% of income each month toward a "
                 f"{money(goal)} goal, how many months will it take?", q2,
                skills=("percent_of_a_number", "division")),
            Part(f"{money(principal)} is invested at {dec(rate_pct)}% annual "
                 f"interest for {years} year(s); what is it worth then?", q3,
                skills=("compound_interest",)),
            Part(f"A {money(debt)} debt is paid down by {payments_made} monthly "
                 f"payments of {money(payment)} each; how much debt remains?", q4,
                skills=("multiplication", "subtraction")),
        ]
        facts = f"This month's {random.choice(FINANCE_NAMES)} is being reviewed."
        used = [f"income {money(income)}", f"goal {money(goal)}", f"debt {money(debt)}"]
        return facts, parts, used, Fraction(income)

    @staticmethod
    def _sports_stats():
        for _ in range(500):
            try:
                games_played = random.randint(10, 30)
                wins = random.randint(games_played // 3, games_played - 1)
                win_pct = Fraction(wins, games_played) * 100
                dec(win_pct)
                total_games = games_played + random.randint(4, 12)
                target_pct = random.choice((Fraction(50), Fraction(60), Fraction(70), Fraction(75)))
                needed_wins = target_pct * total_games / 100
                if needed_wins.denominator != 1:
                    continue
                needed_wins = int(needed_wins)
                more_wins_needed = max(0, needed_wins - wins)
                points = [random.randint(60, 100) for _ in range(random.choice((3, 4, 5)))]
                avg_points = Fraction(sum(points), len(points))
                dec(avg_points)
                games_left = total_games - games_played
                projected_total = wins + more_wins_needed if more_wins_needed <= games_left else None
                if projected_total is None:
                    continue
                break
            except ValueError:
                continue
        else:
            raise AssertionError("no sports_stats scenario found")

        def q1(_state):
            steps = [step("D", wins, games_played, dec(Fraction(wins, games_played))),
                    step("DEC_TO_PERCENT", dec(Fraction(wins, games_played)), dec(win_pct) + "%")]
            return steps, f"{dec(win_pct)}%"

        def q2(_state):
            steps = [step("M", total_games, dec(target_pct / 100), needed_wins),
                    step("S", needed_wins, wins, more_wins_needed)]
            return steps, f"{more_wins_needed} more wins"

        def q3(_state):
            sum_steps, total_points = _sum_steps(points)
            steps = sum_steps + [step("D", total_points, len(points), dec(avg_points))]
            return steps, f"{dec(avg_points)} points"

        parts = [
            Part(f"After {games_played} games with {wins} wins, what is the win percentage?", q1,
                skills=("percent_from_ratio",)),
            Part(f"To finish the {total_games}-game season at {dec(target_pct)}% "
                 "wins or better, how many more wins are needed?", q2,
                skills=("percent_of_a_number", "subtraction")),
            Part(f"Over the last {len(points)} games the team scored "
                 f"{', '.join(map(str, points))} points; what is the average?", q3,
                skills=("mean",)),
        ]
        facts = f"{random.choice(TEAM_NAMES)} track their season so far."
        used = [f"{wins}/{games_played} games", f"season length {total_games}"]
        return facts, parts, used, Fraction(games_played)

    @staticmethod
    def _data_report():
        for _ in range(500):
            try:
                n = random.choice((4, 5, 6))
                values = sorted(10 * random.randint(2, 40) for _ in range(n))
                total = sum(values)
                mean = Fraction(total, n)
                dec(mean)
                spread = values[-1] - values[0]
                target_value = values[-1]
                above_pct = Fraction(target_value - mean, mean) * 100
                dec(above_pct)
                next_value = 2 * values[-1] - values[-2]
                break
            except ValueError:
                continue
        else:
            raise AssertionError("no data_report scenario found")

        def q1(_state):
            sum_steps, total_check = _sum_steps(values)
            assert total_check == total
            steps = sum_steps + [step("D", total, n, dec(mean))]
            return steps, dec(mean)

        def q2(_state):
            steps = [step("S", values[-1], values[0], spread)]
            return steps, str(spread)

        def q3(_state):
            diff = target_value - mean
            steps = [step("S", target_value, dec(mean), dec(diff)),
                    step("D", dec(diff), dec(mean), dec(above_pct / 100)),
                    step("DEC_TO_PERCENT", dec(above_pct / 100), dec(above_pct) + "%")]
            return steps, f"{dec(above_pct)}%"

        def q4(_state):
            last_step_size = values[-1] - values[-2]
            steps = [step("S", values[-1], values[-2], last_step_size),
                    step("A", values[-1], last_step_size, next_value)]
            return steps, str(next_value)

        parts = [
            Part(f"The values recorded are {', '.join(map(str, values))}; what is the mean?", q1,
                skills=("mean",)),
            Part("What is the range (spread) of the values?", q2, skills=("range",)),
            Part(f"By what percent is the highest value ({values[-1]}) above the mean?", q3,
                skills=("percent_change",)),
            Part("Continuing the trend of the last two values, what would the next value be?", q4,
                skills=("linear_trend_projection",)),
        ]
        facts = f"{random.choice(REPORT_NAMES).capitalize()} lists {n} recorded values."
        used = [f"values {values}"]
        return facts, parts, used, mean

    @classmethod
    def _case(cls, variant):
        return getattr(cls, f"_{variant}")()

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        modifier = self.modifier or random.choice(self.MODIFIERS)
        facts, parts, used, value = self._case(variant)
        scenario = Scenario(parts)
        result = scenario.run()
        numbered = " ".join(f"({i}) {p.question}" for i, p in enumerate(parts, 1))
        problem = f"{facts} {numbered}"
        steps, answer = result.steps[:-1], result.answer  # drop the trailing Z; re-added below
        if modifier == "distractor":
            occupied = {int(token) for token in re.findall(r"\d+", problem)}
            extra = random.choice([n for n in range(801, 1101) if n not in occupied])
            problem = f"An unrelated memo mentions {extra} filed forms. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} filed forms"))
        elif modifier == "estimate_first":
            steps = estimate_first(steps + [step("Z", answer)], value,
                                   "predict the overall scale of the scenario",
                                   render=str)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", "each part reuses an established procedure",
                                 "scenario composition"))
            answer = f"composed of {len(parts)} parts; {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(), "operation": f"scenario_{variant}_{modifier}",
                "problem": problem, "steps": steps, "final_answer": answer,
                "skills": scenario.skills}
