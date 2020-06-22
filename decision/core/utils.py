from typing import Tuple


def diophantine_initial_solution(left_coefficient: int,
                                 right_coefficient: int,
                                 right_part: int) -> Tuple[int, int]:
    quotient, remainder = divmod(left_coefficient, right_coefficient)
    if remainder:
        left_mid, right_mid = diophantine_initial_solution(
                right_coefficient, remainder, right_part)
        return right_mid, left_mid - quotient * right_mid
    return 0, ceil_division(right_part, right_coefficient)


def ceil_division(dividend: int, divisor: int) -> int:
    return -(-dividend // divisor)
