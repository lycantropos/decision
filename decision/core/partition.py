import math
from functools import lru_cache
from typing import (Sequence,
                    Tuple)

from .utils import (ceil_division,
                    diophantine_initial_solution)


@lru_cache(256)
def coin_change(amount: int,
                denominations: Sequence[int],
                denominations_count: int) -> Tuple[int, ...]:
    if not amount:
        return _zeros(len(denominations))
    elif denominations_count == 1:
        return (_one_coin_change(amount, denominations[0])
                + _zeros(len(denominations) - 1))
    elif denominations_count == 2:
        return (_two_coin_change(amount, denominations[0],
                                 denominations[1])
                + _zeros(len(denominations) - 2))
    else:
        last_denomination_index = denominations_count - 1
        last_denomination = denominations[last_denomination_index]
        candidates = []
        max_last_denomination_count = amount // last_denomination
        start_amount = amount - max_last_denomination_count * last_denomination
        min_sum = None
        for last_denomination_count in range(max_last_denomination_count, -1,
                                             -1):
            candidate = _add_at_index(coin_change(start_amount, denominations,
                                                  last_denomination_index),
                                      last_denomination_index,
                                      last_denomination_count)
            candidate_sum = sum(count * denomination
                                for count, denomination in zip(candidate,
                                                               denominations)
                                if count)
            if candidates:
                if (sum(candidate) > sum(candidates[-1])
                        and candidate_sum > min_sum):
                    break
                min_sum = min(min_sum, candidate_sum)
            else:
                min_sum = candidate_sum
            candidates.append(candidate)
            start_amount += last_denomination
        return min(candidates,
                   key=len)


def _one_coin_change(amount: int, denomination: int) -> Tuple[int]:
    return ceil_division(amount, denomination),


def _two_coin_change(amount: int,
                     first_denomination: int,
                     second_denomination: int) -> Tuple[int, int]:
    first_count, second_count = diophantine_initial_solution(
            first_denomination, second_denomination, amount)
    if first_count < 0:
        gcd = math.gcd(first_denomination, second_denomination)
        step = -(first_count * gcd // second_denomination)
        first_count += step * second_denomination // gcd
        second_count -= step * first_denomination // gcd
    elif second_count < 0:
        gcd = math.gcd(first_denomination, second_denomination)
        step = -(second_count * gcd // first_denomination)
        first_count -= step * second_denomination // gcd
        second_count += step * first_denomination // gcd
    if first_count < 0 or second_count < 0:
        first_count = ceil_division(amount, first_denomination)
        second_count = 0
    return first_count, second_count


def _add_at_index(counts: Tuple[int, ...],
                  index: int,
                  count: int) -> Tuple[int, ...]:
    return counts[:index] + (counts[index] + count,) + counts[index + 1:]


_zeros = (0,).__mul__
