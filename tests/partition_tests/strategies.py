from hypothesis import strategies

MAX_AMOUNT = 10 ** 7
amounts = strategies.integers(0, MAX_AMOUNT)
denominations_lists = strategies.lists(strategies.integers(1, MAX_AMOUNT),
                                       min_size=1,
                                       unique=True)
