from typing import List

import pytest
from hypothesis import given

from decision.partition import coin_change
from . import strategies


@given(strategies.amounts, strategies.denominations_lists)
def test_basic(amount: int, denominations: List[int]) -> None:
    result = coin_change(amount, denominations)

    assert isinstance(result, tuple)
    assert all(isinstance(element, int) for element in result)


@given(strategies.amounts, strategies.denominations_lists)
def test_elements(amount: int, denominations: List[int]) -> None:
    result = coin_change(amount, denominations)

    assert all(element in denominations for element in result)


@given(strategies.amounts, strategies.denominations_lists)
def test_sum(amount: int, denominations: List[int]) -> None:
    result = coin_change(amount, denominations)

    assert sum(result) >= amount


@given(strategies.invalid_amounts, strategies.denominations_lists)
def test_invalid_amount(amount: int, denominations: List[int]) -> None:
    with pytest.raises(ValueError):
        coin_change(amount, denominations)


@given(strategies.amounts, strategies.invalid_denominations_lists)
def test_invalid_denominations(amount: int, denominations: List[int]) -> None:
    with pytest.raises(ValueError):
        coin_change(amount, denominations)
