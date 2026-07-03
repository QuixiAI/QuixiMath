"""Package marker for the generator modules.

Import generators from their modules directly, e.g.::

    from generators.long_division_generator import LongDivisionGenerator

The registry / source of truth for which generators are active is
``ALL_GENERATORS`` in ``dolphin_math_datagen.py``; grade/difficulty metadata
lives in ``curriculum.py``.
"""
