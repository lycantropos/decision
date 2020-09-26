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


@lru_cache(256)
def coin_change(amount: int,
                denominations: Sequence[int],
                denominations_count: int,
                *,
                zeros: Callable[[int], Tuple[int, ...]] = (0,).__mul__
                ) -> Tuple[int, ...]:
    if not amount:
        return zeros(len(denominations))
    elif denominations_count == 1:
        return (_one_coin_change(amount, denominations[0])
                + zeros(len(denominations) - 1))
    elif amount <= denominations[0]:
        return (1,) + zeros(len(denominations) - 1)
    elif denominations_count == 2:
        return (_two_coin_change(amount, denominations[0], denominations[1])
                + zeros(len(denominations) - 2))
    else:
        def key(counts: Tuple[int, ...]) -> Tuple[int, int]:
            return (sum(count * denomination
                        for count, denomination in zip(counts, denominations)
                        if count),
                    sum(counts))

        if amount <= denominations[-1]:
            ceil_index = bisect_left(denominations, amount)
            ceil_denomination = denominations[ceil_index]
            zeros_tail = zeros(len(denominations) - ceil_index - 1)
            return (zeros(ceil_index) + (1,) + zeros_tail
                    if amount == ceil_denomination
                    else min(zeros(ceil_index)
                             + (ceil_division(amount, ceil_denomination),),
                             coin_change(amount, denominations[:ceil_index],
                                         ceil_index) + (0,),
                             key=key) + zeros_tail)
        last_denomination_index = denominations_count - 1
        last_denomination = denominations[last_denomination_index]
        max_last_denomination_count = amount // last_denomination
        return min([_add_at_index(coin_change(start_amount, denominations,
                                              last_denomination_index),
                                  last_denomination_index,
                                  last_denomination_count)
                    for last_denomination_count, start_amount
                    in zip(range(max_last_denomination_count + 1),
                           accumulate(chain((amount,),
                                            repeat(last_denomination)),
                                      sub))],
                   key=key)


def coin_changes(amount: int,
                 denominations: Sequence[int],
                 denominations_count: int,
                 *,
                 zeros: Callable[[int], Tuple[int, ...]] = (0,).__mul__
                 ) -> Iterator[Tuple[int, ...]]:
    if not amount:
        yield zeros(len(denominations))
    elif denominations_count == 1:
        yield (_one_coin_change(amount, denominations[0])
               + zeros(len(denominations) - 1))
    else:
        last_denomination_index = denominations_count - 1
        last_denomination = denominations[last_denomination_index]
        max_last_denomination_count = amount // last_denomination
        start_amount = amount - max_last_denomination_count * last_denomination
        for last_denomination_count in range(max_last_denomination_count, -1,
                                             -1):
            for candidate in coin_changes(start_amount, denominations,
                                          last_denomination_index):
                yield _add_at_index(candidate, last_denomination_index,
                                    last_denomination_count)
            start_amount += last_denomination


def _one_coin_change(amount: int, denomination: int) -> Tuple[int]:
    return ceil_division(amount, denomination),


def _two_coin_change(amount: int,
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


def _add_at_index(counts: Tuple[int, ...],
                  index: int,
                  count: int) -> Tuple[int, ...]:
    return counts[:index] + (counts[index] + count,) + counts[index + 1:]
