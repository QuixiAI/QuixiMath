import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid


class CompoundProbabilityIndependentGenerator(ProblemGenerator):
    """
    Generates compound probability problems with independent events.

    P(A and B) = P(A) × P(B) for independent events

    Op-codes used:
    - PROB_DESCRIBE: Describe the probability scenario (event_description)
    - PROB_IDENTIFY: Identify individual probabilities (event, probability)
    - PROB_INDEPENDENT: Note that events are independent
    - PROB_MULTIPLY: Multiply probabilities (P(A), P(B), result)
    - PROB_SIMPLIFY: Simplify the fraction if needed (original, simplified)
    - Z: Final answer
    """

    CONTEXTS = [
        {
            "name": "coin_flip",
            "items": ["heads", "tails"],
            "total": 2,
            "object": "coin",
            "action": "flip"
        },
        {
            "name": "die_roll",
            "items": ["1", "2", "3", "4", "5", "6"],
            "total": 6,
            "object": "die",
            "action": "roll"
        },
        {
            "name": "card_suit",
            "items": ["hearts", "diamonds", "clubs", "spades"],
            "total": 4,
            "favorable": 1,
            "object": "card",
            "action": "draw"
        },
    ]

    COLORS = ["red", "blue", "green", "yellow", "purple", "orange",
              "white", "black", "silver", "gold"]
    CONTAINERS = [
        ("bag", "marbles"), ("jar", "beads"), ("box", "tokens"),
        ("basket", "balls"), ("tin", "buttons"), ("pouch", "chips"),
        ("crate", "cubes"), ("case", "tiles"),
    ]
    NAMES = [
        "Aisha", "Ben", "Cleo", "Diego", "Emi", "Farah", "Grace",
        "Hugo", "Imani", "Jonas", "Kavya", "Liam", "Maya", "Noah",
        "Omar", "Priya", "Quinn", "Rosa", "Samir", "Tara", "Uma",
        "Vera", "Wes", "Ximena", "Yara", "Zane", "Ana", "Bo",
        "Cam", "Devi", "Eli", "Fatima", "Gita", "Hana", "Ivan",
        "Jun", "Kofi", "Lena", "Mira", "Nadia",
    ]
    SETTINGS = [
        "math class", "science club", "study hall", "the library",
        "a probability workshop", "the school fair", "a game night",
        "the learning center", "a classroom warm-up", "an online lesson",
        "a practice quiz", "the community center", "a tutoring session",
        "the after-school program", "a statistics lab", "a review group",
    ]
    TEMPLATES = [
        "At {place}, {name} reads this setup: {setup} What is the "
        "probability of the stated target?",
        "At {place}, {name} considers this experiment: {setup} Find the "
        "probability of the target.",
        "{name} records the following setup during {place}: {setup} What is "
        "the probability of the target sequence?",
        "For a probability exercise at {place}, {setup} {name} must find the "
        "probability of the stated outcome.",
        "During {place}, {name} runs an independent-events experiment. "
        "{setup} Find the exact probability of the target.",
        "A worksheet for {name} at {place} says: {setup} Determine the "
        "probability of the target events.",
    ]

    def _problem(self, setup):
        return random.choice(self.TEMPLATES).format(
            setup=setup, name=random.choice(self.NAMES),
            place=random.choice(self.SETTINGS))

    def _finish(self, setup, description, labels, probabilities, reason):
        steps = [step("PROB_DESCRIBE", description)]
        for label, probability in zip(labels, probabilities):
            steps.append(step("PROB_IDENTIFY", f"P({label})",
                              str(probability)))
        steps.append(step("PROB_INDEPENDENT", reason))
        value = probabilities[0]
        for probability in probabilities[1:]:
            result = value * probability
            steps.append(step("PROB_MULTIPLY", str(value), str(probability),
                              str(result)))
            value = result
        answer = str(value)
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="compound_probability_independent",
            problem=self._problem(setup),
            steps=steps,
            final_answer=answer,
        )

    def generate(self) -> dict:
        """Generate a compound probability problem with independent events."""
        problem_type = random.choice(['two_coins', 'two_dice', 'coin_and_die', 'with_replacement'])

        if problem_type == 'two_coins':
            return self._generate_two_coins()
        elif problem_type == 'two_dice':
            return self._generate_two_dice()
        elif problem_type == 'coin_and_die':
            return self._generate_coin_and_die()
        else:
            return self._generate_with_replacement()

    def _generate_two_coins(self) -> dict:
        """Generate problem with two coin flips."""
        outcomes = [("heads", "heads"), ("heads", "tails"), ("tails", "heads"), ("tails", "tails")]
        target = random.choice(outcomes)

        setup = ("A fair coin is flipped twice. Target order: "
                 f"{target[0]}, then {target[1]}.")
        return self._finish(
            setup, f"Two fair coin flips: {target[0]} then {target[1]}",
            [f"first {target[0]}", f"second {target[1]}"],
            [Fraction(1, 2), Fraction(1, 2)],
            "Separate coin flips are independent events")

    def _generate_two_dice(self) -> dict:
        """Generate problem with two dice rolls."""
        sides1, sides2 = random.randint(4, 20), random.randint(4, 20)
        target1 = random.randint(1, sides1)
        target2 = random.randint(1, sides2)
        setup = (f"A fair {sides1}-sided die and a fair {sides2}-sided die "
                 f"are rolled. Target faces: {target1}, then {target2}.")
        return self._finish(
            setup, f"Two dice: d{sides1}={target1}, d{sides2}={target2}",
            [f"first die is {target1}", f"second die is {target2}"],
            [Fraction(1, sides1), Fraction(1, sides2)],
            "The two dice are independent events")

    def _generate_coin_and_die(self) -> dict:
        """Generate problem with coin flip and die roll."""
        coin_target = random.choice(["heads", "tails"])
        sides = random.randint(4, 20)
        die_target = random.randint(1, sides)
        setup = (f"A fair coin and a fair {sides}-sided die are used. Target "
                 f"outcomes: {coin_target}, then {die_target}.")
        return self._finish(
            setup, f"Coin and d{sides}: {coin_target}, then {die_target}",
            [coin_target, f"die is {die_target}"],
            [Fraction(1, 2), Fraction(1, sides)],
            "The coin flip and die roll are independent events")

    def _generate_with_replacement(self) -> dict:
        """Generate problem drawing with replacement (independent)."""
        colors = random.sample(self.COLORS, random.randint(3, 5))
        total = random.choice([8, 10, 12, 16, 20])
        while total < len(colors):
            total = random.choice([8, 10, 12, 16, 20])
        cuts = sorted(random.sample(range(1, total), len(colors) - 1))
        parts = [cuts[0]] + [right - left
                             for left, right in zip(cuts, cuts[1:])] \
            + [total - cuts[-1]]
        random.shuffle(parts)
        counts = dict(zip(colors, parts))
        draws = random.choice([2, 2, 3])
        targets = [random.choice(colors) for _ in range(draws)]
        container, objects = random.choice(self.CONTAINERS)
        roster = ", ".join(f"{color}={counts[color]}" for color in colors)
        sequence = ", then ".join(targets)
        setup = (f"A {container} contains {roster} {objects}. After every "
                 f"draw, the item is replaced and the {container} is mixed. "
                 f"Target order: {sequence}.")
        probabilities = [Fraction(counts[color], total) for color in targets]
        labels = [f"draw {index} is {color}"
                  for index, color in enumerate(targets, start=1)]
        return self._finish(
            setup, f"Draw with replacement: {sequence}", labels,
            probabilities,
            "Replacement restores the same distribution, so the draws are independent")


def _bare(text):
    """Drop a leading article so step labels read 'P(first heart)'."""
    for article in ("a ", "an ", "the "):
        if text.startswith(article):
            return text[len(article):]
    return text


class CompoundProbabilityDependentGenerator(ProblemGenerator):
    """
    Generates compound probability problems with dependent events.

    P(A and B) = P(A) × P(B|A) for dependent events, extended to three
    draws when the scenario asks for three.

    Scenarios:
    - without_replacement: a container of coloured objects, two or three
      drawn one at a time in a stated order
    - numbered: tickets/balls/tiles numbered 1..N, two or three drawn, all
      of them sharing a stated property (even, a multiple of m, above or
      below a cut-off)
    - cards: two or three cards from a standard 52-card deck, all of the
      same suit / colour / rank / kind

    Every count is drawn at random and the probability is built as an exact
    product of conditionals, so the numbers stay hand-friendly.

    Op-codes used:
    - PROB_DESCRIBE: Describe the probability scenario
    - PROB_IDENTIFY: Identify the first-draw probability (event, probability)
    - PROB_DEPENDENT: Note that events are dependent
    - PROB_CONDITIONAL: Conditional probability of a later draw (event,
      probability)
    - PROB_MULTIPLY: Multiply two probabilities (P(A), P(B), product)
    - PROB_SIMPLIFY: Reduce the product (original, simplified)
    - Z: Final answer
    """

    CONTAINERS = [
        ("bag", "marbles", "marble"),
        ("jar", "beads", "bead"),
        ("box", "tokens", "token"),
        ("basket", "balls", "ball"),
        ("drawer", "socks", "sock"),
        ("tin", "buttons", "button"),
        ("bucket", "blocks", "block"),
        ("pouch", "chips", "chip"),
        ("crate", "cubes", "cube"),
        ("case", "tiles", "tile"),
    ]

    COLORS = ["red", "blue", "green", "yellow", "purple", "orange",
              "white", "black", "silver", "gold"]

    NAMES = ["Maya", "Owen", "Priya", "Diego", "Aisha", "Noah", "Lena",
             "Kofi", "Yuki", "Sofia", "Ravi", "Emma"]

    NUMBERED_ITEMS = ["tickets", "balls", "tiles", "chips", "cards",
                      "tokens", "discs", "counters"]

    DECK_TEXT = ["a standard deck", "a well-shuffled standard 52-card deck",
                 "a shuffled 52-card deck", "a standard 52-card deck",
                 "an ordinary deck of playing cards"]

    # (plural description, singular description, cards in the deck)
    CARD_TARGETS = [
        ("hearts", "a heart", 13),
        ("diamonds", "a diamond", 13),
        ("clubs", "a club", 13),
        ("spades", "a spade", 13),
        ("red cards", "a red card", 26),
        ("black cards", "a black card", 26),
        ("face cards", "a face card", 12),
        ("number cards", "a number card", 36),
        ("aces", "an ace", 4),
        ("kings", "a king", 4),
        ("queens", "a queen", 4),
        ("jacks", "a jack", 4),
        ("tens", "a ten", 4),
        ("nines", "a nine", 4),
        ("eights", "an eight", 4),
        ("sevens", "a seven", 4),
        ("sixes", "a six", 4),
        ("fives", "a five", 4),
        ("fours", "a four", 4),
        ("threes", "a three", 4),
        ("twos", "a two", 4),
    ]

    BAG_TEMPLATES = [
        "A {container} contains {roster}. {d} {noun} are drawn without "
        "replacement. What is the probability of drawing {sequence}?",
        "{name} has a {container} containing {roster}. {name} draws {d} "
        "{noun} one at a time without replacement. Find the probability of "
        "drawing {sequence}.",
        "A {container} holds {roster}. Drawing {d} {noun} at random without "
        "replacement, what is the probability that the result is {sequence}?",
        "Without replacement, {d} {noun} are taken one after another from a "
        "{container} of {roster}. What is the probability of getting "
        "{sequence}?",
        "{name} removes {d} {noun} at random from a {container} that "
        "contains {roster}, drawing without replacement. What is the "
        "probability of drawing {sequence}?",
    ]

    NUMBERED_TEMPLATES = [
        "A hat holds {items} numbered 1 to {n}. {name} draws {d} {items} at "
        "random without replacement. What is the probability that the drawn "
        "{items} are all {prop}?",
        "{items} numbered 1 to {n} are placed in a bin, and {d} {items} are "
        "removed one at a time without replacement. Find the probability "
        "that the removed {items} are all {prop}.",
        "Without replacement, {d} {items} are drawn from a box of {items} "
        "numbered 1 to {n}. What is the probability that they are all "
        "{prop}?",
        "{name} picks {d} {items} at random, one after another and without "
        "replacement, from {items} numbered 1 to {n}. What is the "
        "probability that the picks are all {prop}?",
        "From a jar of {items} numbered 1 to {n}, {d} {items} are drawn "
        "without replacement. What is the probability that the drawn {items} "
        "are all {prop}?",
    ]

    CARD_TEMPLATES = [
        "{d} cards are drawn from {deck} without replacement. What is the "
        "probability that all of them are {plural}?",
        "{name} deals {d} cards from {deck} without replacement. What is the "
        "probability that the {d} cards are all {plural}?",
        "Without replacement, {d} cards are taken from {deck}. Find the "
        "probability that every one of them is {singular}.",
        "From {deck}, {d} cards are drawn one after another without "
        "replacement. What is the probability that all {d} are {plural}?",
        "{name} draws {d} cards in a row from {deck}, without replacement. "
        "What is the probability that all {d} are {plural}?",
        "{name} is dealt {d} cards from {deck} without replacement. Find "
        "the probability that they are all {plural}.",
    ]

    def generate(self) -> dict:
        """Generate a compound probability problem with dependent events."""
        roll = random.random()
        if roll < 0.60:
            return self._generate_without_replacement()
        if roll < 0.95:
            return self._generate_numbered()
        return self._generate_cards()

    # -- shared machinery ---------------------------------------------------

    def _finish(self, problem, describe, reason, labels, pairs):
        """Build the step list from (favorable, total) pairs, in order."""
        steps_list = [step("PROB_DESCRIBE", describe)]
        first_num, first_den = pairs[0]
        steps_list.append(step("PROB_IDENTIFY", f"P(first {labels[0]})",
                               f"{first_num}/{first_den}"))
        steps_list.append(step("PROB_DEPENDENT", reason))
        for idx in range(1, len(pairs)):
            num, den = pairs[idx]
            if idx == 1:
                given = f"first was {labels[0]}"
            else:
                given = " and ".join(labels[:idx]) + " drawn"
            steps_list.append(step(
                "PROB_CONDITIONAL",
                f"P({labels[idx]} given {given})",
                f"{num}/{den}"))
        acc_num, acc_den = pairs[0]
        for idx in range(1, len(pairs)):
            num, den = pairs[idx]
            raw_num, raw_den = acc_num * num, acc_den * den
            raw_text = f"{raw_num}/{raw_den}"
            steps_list.append(step("PROB_MULTIPLY", f"{acc_num}/{acc_den}",
                                   f"{num}/{den}", raw_text))
            reduced = Fraction(raw_num, raw_den)
            if raw_text != str(reduced):
                steps_list.append(step("PROB_SIMPLIFY", raw_text,
                                       str(reduced)))
                acc_num, acc_den = reduced.numerator, reduced.denominator
            else:
                acc_num, acc_den = raw_num, raw_den
        final_answer = str(Fraction(acc_num, acc_den))
        steps_list.append(step("Z", final_answer))
        return dict(
            problem_id=jid(),
            operation="compound_probability_dependent",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )

    # -- scenarios ----------------------------------------------------------

    def _generate_without_replacement(self) -> dict:
        """Coloured objects drawn from a container without replacement."""
        container, noun, singular = random.choice(self.CONTAINERS)
        k = random.choice([2, 2, 3])
        colors = random.sample(self.COLORS, k)
        counts = {c: random.randint(2, 12) for c in colors}
        total = sum(counts.values())
        draws = random.choice([2, 2, 3])
        sequence = []
        remaining = dict(counts)
        for _ in range(draws):
            choices = [c for c in colors if remaining[c] > 0]
            pick = random.choice(choices)
            remaining[pick] -= 1
            sequence.append(pick)

        pairs = []
        left = dict(counts)
        left_total = total
        for color in sequence:
            pairs.append((left[color], left_total))
            left[color] -= 1
            left_total -= 1

        if k == 2:
            roster = (f"{counts[colors[0]]} {colors[0]} and "
                      f"{counts[colors[1]]} {colors[1]} {noun}")
        else:
            roster = (f"{counts[colors[0]]} {colors[0]}, "
                      f"{counts[colors[1]]} {colors[1]}, and "
                      f"{counts[colors[2]]} {colors[2]} {noun}")
        seq_text = ", then ".join(sequence)
        problem = random.choice(self.BAG_TEMPLATES).format(
            container=container, roster=roster, d=draws, noun=noun,
            sequence=seq_text, name=random.choice(self.NAMES),
            singular=singular)
        return self._finish(
            problem,
            f"Draw without replacement: {seq_text}",
            "Drawing without replacement means dependent events",
            sequence, pairs)

    def _generate_numbered(self) -> dict:
        """Numbered items drawn without replacement, all sharing a property."""
        items = random.choice(self.NUMBERED_ITEMS)
        n = random.randint(10, 60)
        draws = random.choice([2, 2, 3])
        while True:
            kind = random.choice(["even", "odd"] + ["multiple"] * 2
                                 + ["greater"] * 3 + ["less"] * 3)
            if kind == "even":
                favorable = n // 2
                plural = singular = "even"
            elif kind == "odd":
                favorable = n - n // 2
                plural = singular = "odd"
            elif kind == "multiple":
                m = random.randint(3, 9)
                favorable = n // m
                plural = f"multiples of {m}"
                singular = f"a multiple of {m}"
            elif kind == "greater":
                cut = random.randint(2, n - 2)
                favorable = n - cut
                plural = singular = f"greater than {cut}"
            else:
                cut = random.randint(3, n - 1)
                favorable = cut - 1
                plural = singular = f"less than {cut}"
            if draws <= favorable < n:
                break

        pairs = [(favorable - i, n - i) for i in range(draws)]
        problem = random.choice(self.NUMBERED_TEMPLATES).format(
            items=items, n=n, d=draws, prop=plural,
            name=random.choice(self.NAMES))
        return self._finish(
            problem,
            f"Draw {draws} of 1 to {n} without replacement, all {plural}",
            "Drawing without replacement means dependent events",
            [_bare(singular)] * draws, pairs)

    def _generate_cards(self) -> dict:
        """Cards drawn from a standard deck without replacement."""
        plural, singular, favorable = random.choice(self.CARD_TARGETS)
        draws = random.choice([2, 2, 3, 3, 4])
        pairs = [(favorable - i, 52 - i) for i in range(draws)]
        problem = random.choice(self.CARD_TEMPLATES).format(
            d=draws, deck=random.choice(self.DECK_TEXT), plural=plural,
            singular=singular, name=random.choice(self.NAMES))
        return self._finish(
            problem,
            f"Draw {draws} {plural} without replacement",
            "Drawing without replacement means dependent events",
            [_bare(singular)] * draws, pairs)
