import random
from math import gcd


VERTEX_LABELS = "ABCDEFGHJKLMNPQRSTUVWXYZ"


def random_scaled_triple():
    """Return a moderately sized integer triple built by Euclid's formula."""
    while True:
        m = random.randint(2, 15)
        n = random.randint(1, m - 1)
        if gcd(m, n) == 1 and (m - n) % 2 == 1:
            break
    scale = random.randint(1, 12)
    leg_a = scale * (m * m - n * n)
    leg_b = scale * (2 * m * n)
    hypotenuse = scale * (m * m + n * n)
    if random.random() < 0.5:
        leg_a, leg_b = leg_b, leg_a
    return leg_a, leg_b, hypotenuse


def triangle_labels():
    """Three distinct vertices; the middle vertex is the right angle."""
    return tuple(random.sample(VERTEX_LABELS, 3))
