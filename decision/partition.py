from itertools import (chain,
                       groupby,
                       repeat)
from typing import (Any,
                    Iterable,
                    Iterator,
                    Sequence,
                    Tuple)

from .core.partition import coins_counter as _coins_counter


def coin_change(amount: int, denominations: Iterable[int]) -> Tuple[int, ...]:
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
    _validate_amount(amount)
    denominations = tuple(sorted(denominations))
    _validate_denominations(denominations)
    return _to_change(_coins_counter(amount, denominations,
                                     len(denominations)),
                      denominations)


def _to_change(counts: Sequence[int],
               denominations: Sequence[int]) -> Tuple[int, ...]:
    return tuple(chain.from_iterable(map(repeat, denominations, counts)))


def _validate_amount(amount: int) -> None:
    if amount < 0:
        raise ValueError('Amount should be non-negative.')


def _validate_denominations(denominations: Sequence[int]) -> None:
    if not denominations:
        raise ValueError('Denominations should be non-empty.')
    elif not all(denomination > 0
                 for denomination in denominations):
        raise ValueError('Denominations should be positive.')
    elif not all(_has_single_value(group)
                 for _, group in groupby(denominations)):
        raise ValueError('All denominations should be unique.')


def _has_single_value(iterator: Iterator, _sentinel: Any = object()) -> bool:
    return (next(iterator, _sentinel) is not _sentinel
            and next(iterator, _sentinel) is _sentinel)
