from collections.abc import (
    Iterable as _Iterable,
    Iterator as _Iterator,
    Sequence as _Sequence,
)
from itertools import chain as _chain, groupby as _groupby, repeat as _repeat
from typing import Any as _Any

from ._core.partition import coins_counter as _coins_counter


def coin_change(
    amount: int, denominations: _Iterable[int], /
) -> tuple[int, ...]:
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
    return _to_change(
        _coins_counter(amount, denominations, len(denominations)),
        denominations,
    )


def _has_single_value(iterator: _Iterator[_Any], /) -> bool:
    return next(iterator, None) is not None and next(iterator, None) is None


def _to_change(
    counts: _Sequence[int], denominations: _Sequence[int], /
) -> tuple[int, ...]:
    return tuple(_chain.from_iterable(map(_repeat, denominations, counts)))


def _validate_amount(amount: int, /) -> None:
    if amount < 0:
        raise ValueError('Amount should be non-negative.')


def _validate_denominations(denominations: _Sequence[int], /) -> None:
    if not denominations:
        raise ValueError('Denominations should be non-empty.')
    if not all(denomination > 0 for denomination in denominations):
        raise ValueError('Denominations should be positive.')
    if not all(
        _has_single_value(group) for _, group in _groupby(denominations)
    ):
        raise ValueError('All denominations should be unique.')
