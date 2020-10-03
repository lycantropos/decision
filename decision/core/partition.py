from functools import lru_cache
from typing import (Callable,
                    Iterator,
                    Sequence,
                    Tuple)

from .utils import ceil_division

CoinsCounter = Tuple[int, ...]
_zeros = (0,).__mul__  # type: Callable[[int], CoinsCounter]


@lru_cache(1024)
def coins_counter(amount: int, denominations: Sequence[int]) -> CoinsCounter:
    denominations_count = len(denominations)
    if not amount:
        return _zeros(denominations_count)
    elif denominations_count == 1:
        return (_one_coin_counter(amount, denominations[0])
                + _zeros(denominations_count - 1))
    elif amount <= denominations[0]:
        return (1,) + _zeros(denominations_count - 1)
    else:
        def key(counter: CoinsCounter) -> Tuple[int, int]:
            return (sum(count * denomination
                        for count, denomination in zip(counter, denominations)
                        if count),
                    sum(counter))

        return min(_coins_counters(amount, denominations, denominations_count),
                   key=key)


def coins_counters(amount: int,
                   denominations: Sequence[int],
                   denominations_count: int) -> Iterator[CoinsCounter]:
    if not amount:
        yield _zeros(len(denominations))
    elif amount <= denominations[0]:
        yield (1,) + _zeros(len(denominations) - 1)
    elif denominations_count == 1:
        yield (_one_coin_counter(amount, denominations[0])
               + _zeros(len(denominations) - 1))
    else:
        yield from _coins_counters(amount, denominations, denominations_count)


def _coins_counters(amount: int,
                    denominations: Sequence[int],
                    denominations_count: int) -> Iterator[CoinsCounter]:
    last_denomination_index = denominations_count - 1
    last_denomination = denominations[last_denomination_index]
    max_last_denomination_count, amount_remainder = divmod(
            amount, last_denomination)
    step = amount_remainder
    for last_denomination_count in range(max_last_denomination_count, 0, -1):
        for counter in coins_counters(step, denominations,
                                      last_denomination_index):
            yield (counter[:last_denomination_index]
                   + (counter[last_denomination_index]
                      + last_denomination_count,)
                   + counter[last_denomination_index + 1:])
        step += last_denomination
    yield from coins_counters(step, denominations, last_denomination_index)
    if amount_remainder:
        yield (_zeros(last_denomination_index)
               + (max_last_denomination_count + 1,)
               + _zeros(len(denominations) - 1 - last_denomination_index))


def _one_coin_counter(amount: int, denomination: int) -> Tuple[int]:
    return ceil_division(amount, denomination),
