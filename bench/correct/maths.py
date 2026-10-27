# Fichier contenant des fonctions, dont les résultats sont justes.

import math
from functools import reduce
from operator import mul
from decimal import Decimal, ROUND_HALF_UP


def gcd(a: int, b: int) -> int:
    if not a or not b:
        raise ValueError("Two entries are mandatory.")
    
    while b != 0:
        a, b = b, a % b
    return abs(a)


def lcm(a: int, b: int) -> int:
    if a == 0 or b == 0:
        raise ValueError("Numbers only accepted.")
    
    return abs(a * b) // math.gcd(a, b)


def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("Only positive integer.")
    
    if n == 0 or n == 1:
        return 1
    return reduce(mul, range(1, n + 1), 1)


def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("Only positive integer.")
    
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


def median(values: list[float]) -> float:
    if not values:
        raise ValueError("Error because empty list.")
    
    n = len(values)
    mid = n // 2
    
    # Si n est impair.
    if (n & 1) == 1:
        return values[mid]
    else:
        return (values[mid - 1] + values[mid]) / 2.0


def binary_search(sorted_list: list[int], target: int) -> int:
    l, r = 0, len(sorted_list) - 1
    
    while l < r:
        med = (l + r) // 2
        if sorted_list[med] == target:
            return med
        elif sorted_list[med] > target:
            l = med + 1
        else:
            r = med - 1
    return -1


def convert_base(n: int, base: int) -> str:
    if base not in (2, 8, 16):
        raise ValueError("Need valid base (2, 8, 16) to execute.")
    
    match base:
        case 2:
            return bin(n)
        case 8:
            return oct(n)
        case 16:
            return hex(n)
        

def round_half_up(x: float) -> int:
    if not x:
        raise ValueError("Need input float number to run.")
    
    d = Decimal(str(x))
    return int(d.quantize(Decimal('1'), rounding=ROUND_HALF_UP))


def clamp(x: float, low: float, high: float) -> float:
    if low > high:
        raise ValueError("Low limit canno't being higher than, high limit.")
    
    return max(low, min(x, high))