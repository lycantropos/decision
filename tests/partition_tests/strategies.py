from itertools import repeat

from hypothesis import strategies

MAX_AMOUNT = 10 ** 4
amounts = strategies.integers(0, MAX_AMOUNT)
denominations = strategies.integers(1, MAX_AMOUNT)
denominations_lists = strategies.lists(denominations,
                                       min_size=1,
                                       unique=True)
invalid_amounts = strategies.integers(max_value=-1)
invalid_denominations_lists = (
        strategies.builds(list)
        | strategies.lists(strategies.integers(max_value=0),
                           min_size=1,
                           unique=True)
        | strategies.builds(repeat,
                            denominations,
                            strategies.integers(2, 100)))
