import math
from bisect import bisect_left
from functools import lru_cache
from itertools import (accumulate,
                       chain,
                       repeat)
from operator import sub
from typing import (Callable,
                    Iterator,
                    Sequence,
                    Tuple)

from .utils import (ceil_division,
                    diophantine_initial_solution)

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
    elif denominations_count == 2:
        return (_two_coin_counter(amount, denominations[0], denominations[1])
                + _zeros(len(denominations) - 2))
    else:
        def key(counts: Tuple[int, ...]) -> Tuple[int, int]:
            return (sum(count * denomination
                        for count, denomination in zip(counts, denominations)
                        if count),
                    sum(counts))

        if amount <= denominations[-1]:
            ceil_index = bisect_left(denominations, amount)
            ceil_denomination = denominations[ceil_index]
            zeros_tail = _zeros(len(denominations) - ceil_index - 1)
            return (_zeros(ceil_index) + (1,) + zeros_tail
                    if amount == ceil_denomination
                    else min(_zeros(ceil_index)
                             + (ceil_division(amount, ceil_denomination),),
                             coins_counter(amount, denominations[:ceil_index],
                                           ceil_index) + (0,),
                             key=key) + zeros_tail)
        last_denomination_index = denominations_count - 1
        last_denomination = denominations[last_denomination_index]
        max_last_denomination_count = amount // last_denomination
        return min([_add_at_index(coins_counter(start_amount, denominations,
                                                last_denomination_index),
                                  last_denomination_index,
                                  last_denomination_count)
                    for last_denomination_count, start_amount
                    in zip(range(max_last_denomination_count + 1),
                           accumulate(chain((amount,),
                                            repeat(last_denomination)),
                                      sub))],
                   key=key)


def coins_counters(amount: int,
                   denominations: Sequence[int],
                   denominations_count: int) -> Iterator[CoinsCounter]:
    if not amount:
        yield _zeros(len(denominations))
    elif denominations_count == 1:
        yield (_one_coin_counter(amount, denominations[0])
               + _zeros(len(denominations) - 1))
    else:
        last_denomination_index = denominations_count - 1
        last_denomination = denominations[last_denomination_index]
        max_last_denomination_count = amount // last_denomination
        start_amount = amount - max_last_denomination_count * last_denomination
        for last_denomination_count in range(max_last_denomination_count, -1,
                                             -1):
            for candidate in coins_counters(start_amount, denominations,
                                            last_denomination_index):
                yield _add_at_index(candidate, last_denomination_index,
                                    last_denomination_count)
            start_amount += last_denomination


def _one_coin_counter(amount: int, denomination: int) -> Tuple[int]:
    return ceil_division(amount, denomination),


def _two_coin_counter(amount: int,
                      first_denomination: int,
                      second_denomination: int) -> Tuple[int, int]:
    gcd = math.gcd(first_denomination, second_denomination)
    prime_first_denomination = first_denomination // gcd
    prime_second_denomination = second_denomination // gcd
    for amount in range(amount,
                        min(ceil_division(amount, first_denomination)
                            * first_denomination,
                            ceil_division(amount, second_denomination)
                            * second_denomination) + 1):
        first_count, second_count = diophantine_initial_solution(
                first_denomination, second_denomination, amount)
        offset = ceil_division(-first_count, prime_second_denomination)
        has_non_negative_solution = offset <= (second_count
                                               // prime_first_denomination)
        if has_non_negative_solution:
            return (first_count + offset * prime_second_denomination,
                    second_count - offset * prime_first_denomination)


def _add_at_index(counter: CoinsCounter,
                  index: int,
                  count: int) -> CoinsCounter:
    return counter[:index] + (counter[index] + count,) + counter[index + 1:]
