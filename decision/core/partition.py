from bisect import bisect_left
from functools import lru_cache
from typing import (Callable,
                    Iterator,
                    Sequence,
                    Tuple)

from .utils import ceil_division

CoinsCounter = Tuple[int, ...]
_zeros = (0,).__mul__  # type: Callable[[int], CoinsCounter]


@lru_cache(1024)
def coins_counter(amount: int,
                  denominations: Sequence[int],
                  denominations_count: int) -> CoinsCounter:
    if not amount:
        return _zeros(len(denominations))
    elif denominations_count == 1:
        return (_one_coin_counter(amount, denominations[0])
                + _zeros(len(denominations) - 1))
    elif amount <= denominations[0]:
        return (1,) + _zeros(len(denominations) - 1)
    else:
        if amount <= denominations[-1]:
            denomination_index = bisect_left(denominations, amount)
            if amount == denominations[denomination_index]:
                return (_zeros(denomination_index) + (1,)
                        + _zeros(len(denominations) - denomination_index - 1))
        for denomination_index, denomination in enumerate(
                denominations[:ceil_division(len(denominations), 2)]):
            difference = amount - denomination
            nearest_denomination_index = bisect_left(denominations, difference)
            if (nearest_denomination_index < len(denominations)
                    and (denominations[nearest_denomination_index]
                         == difference)):
                return (_zeros(denomination_index) + (2,)
                        + _zeros(len(denominations) - denomination_index - 1)
                        if nearest_denomination_index == denomination_index
                        else
                        _zeros(denomination_index) + (1,)
                        + _zeros(nearest_denomination_index
                                 - denomination_index - 1)
                        + (1,)
                        + _zeros(len(denominations)
                                 - nearest_denomination_index - 1))

        def key(counter: CoinsCounter) -> Tuple[int, int]:
            return (sum(count * denomination
                        for count, denomination in zip(counter, denominations)
                        if count),
                    sum(counter))

        return min(_coins_counters(amount, denominations, denominations_count),
                   key=key)


def _coins_counters(amount: int,
                    denominations: Sequence[int],
                    denominations_count: int) -> Iterator[CoinsCounter]:
    if denominations_count == 1:
        yield (_one_coin_counter(amount, denominations[0])
               + _zeros(len(denominations) - 1))
    else:
        last_denomination_index = denominations_count - 1
        last_denomination = denominations[last_denomination_index]
        max_last_denomination_count, remainder = divmod(amount,
                                                        last_denomination)
        has_remainder = bool(remainder)
        if has_remainder:
            for last_denomination_count in range(max_last_denomination_count,
                                                 0, -1):
                counter = coins_counter(remainder, denominations,
                                        last_denomination_index)
                yield (counter[:last_denomination_index]
                       + (counter[last_denomination_index]
                          + last_denomination_count,)
                       + counter[last_denomination_index + 1:])
                remainder += last_denomination
        yield (_zeros(last_denomination_index)
               + (max_last_denomination_count + has_remainder,)
               + _zeros(len(denominations) - 1 - last_denomination_index))
        yield from _coins_counters(amount, denominations,
                                   last_denomination_index)


def _one_coin_counter(amount: int, denomination: int) -> Tuple[int]:
    return ceil_division(amount, denomination),
