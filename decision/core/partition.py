import math
from functools import lru_cache
from typing import (Optional,
                    Sequence,
                    Tuple)

from .utils import (ceil_division,
                    diophantine_initial_solution)


@lru_cache(256)
def coin_change(amount: int,
                denominations: Sequence[int],
                denominations_count: int) -> Optional[Tuple[int, ...]]:
    if not amount:
        return ()
    elif denominations_count == 1:
        return _one_coin_change(amount, denominations[0])
    elif denominations_count == 2:
        return _two_coin_change(amount, denominations[0], denominations[1])
    else:
        last_denomination_index = denominations_count - 1
        less_denominations = coin_change(amount, denominations,
                                         last_denomination_index)
        last_denomination = denominations[last_denomination_index]
        less_amount = amount - last_denomination
        return (min(less_denominations,
                    coin_change(less_amount, denominations,
                                denominations_count)
                    + (last_denomination,),
                    key=len)
                if less_amount >= 0
                else less_denominations)


def _one_coin_change(amount: int, denomination: int) -> Tuple[int, ...]:
    return (denomination,) * ceil_division(amount, denomination)


def _two_coin_change(amount: int,
                     first_denomination: int,
                     second_denomination: int) -> Tuple[int, ...]:
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
    return ((first_denomination,) * first_count
            + (second_denomination,) * second_count)
