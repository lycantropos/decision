from itertools import (chain,
                       repeat)
from typing import (Iterable,
                    Iterator)

from .core.partition import coin_change as _coin_change


def coin_change(amount: int, denominations: Iterable[int]) -> Iterator[int]:
    """
    Solves coin change problem:
    what is the minimal number of coins of given unique denominations
    such that their sum will be no less than the given amount?

    Reference:
        https://en.wikipedia.org/wiki/Change-making_problem

    >>> coin_change(0, [2, 3])
    ()
    >>> coin_change(5, [2, 3])
    (2, 3)
    >>> coin_change(5, [2, 3, 5])
    (5,)
    >>> coin_change(15, [2, 3])
    (3, 3, 3, 3, 3)
    >>> coin_change(15, [2, 3, 5])
    (5, 5, 5)
    """
    if amount < 0:
        raise ValueError('Amount should be non-negative.')
    denominations = tuple(sorted(denominations))
    if not denominations:
        raise ValueError('Denominations should be non-empty.')
    elif not all(denomination > 0
                 for denomination in denominations):
        raise ValueError('Denominations should be positive.')
    return chain.from_iterable(
            repeat(denomination, count)
            for count, denomination in zip(_coin_change(amount, denominations,
                                                        len(denominations)),
                                           denominations)
            if count)
