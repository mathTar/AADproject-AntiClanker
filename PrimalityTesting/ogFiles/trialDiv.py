"""
Trial division primality test (Legacy file - use trial_division.py instead)
"""
from imports import math, time
from helpers import eGcd


def isPrime(num):
    """
    Check if a number is prime using trial division.
    
    Args:
        num: Integer to check for primality
    
    Returns:
        Tuple of (is_prime: bool, execution_time: float)
    """
    if num <= 1:
        return False, 0
    if num <= 3:
        return True, 0
    if num % 2 == 0:
        return False, 0
    
    startTime = time.time()
    for i in range(2, math.isqrt(num) + 1):
        if eGcd(num, i) != 1:
            return False, time.time() - startTime
    return True, time.time() - startTime
