"""
Helper functions for primality testing algorithms.

This module contains utility functions used across different primality testing implementations.
"""

import math


def extended_gcd(a: int, b: int) -> int:
    """
    Compute the Greatest Common Divisor (GCD) of two integers using Euclidean algorithm.
    
    This is used to check if two numbers are coprime (GCD = 1).
    
    Args:
        a (int): First integer
        b (int): Second integer
    
    Returns:
        int: The GCD of a and b
    
    Example:
        >>> extended_gcd(48, 18)
        6
        >>> extended_gcd(17, 19)
        1
    """
    while b:
        a, b = b, a % b
    return abs(a)


def is_even(n: int) -> bool:
    """
    Check if a number is even.
    
    Args:
        n (int): The number to check
    
    Returns:
        bool: True if n is even, False otherwise
    """
    return n % 2 == 0


def sqrt_int(n: int) -> int:
    """
    Calculate the integer square root of n.
    
    Args:
        n (int): A non-negative integer
    
    Returns:
        int: The largest integer k such that k² ≤ n
    """
    return math.isqrt(n)
