"""
Fermat primality test

Implementation caveat: test is defined only for co-prime a (bases).
If a is not co-prime to num, num is composite - we can use this for practical purposes!
"""
from imports import random, time
from helpers import eGcd


def isPrime(num: int, k: int) -> tuple[bool, float]:
    """
    Check if a number is probably prime using Fermat's primality test.
    
    Args:
        num (int): Integer to check for primality
        k (int): Number of rounds/bases to test (higher k = more accurate)
    
    Returns:
        tuple[bool, float]: A tuple containing:
            - bool: True if probably prime, False if definitely composite
            - float: Execution time in seconds
    """
    startTime = time.time()
    if num <= 1:
        return False, 0
    if num <= 3:
        return True, 0
    if num % 2 == 0:
        return False, 0
    
    for _ in range(k):
        a = random.SystemRandom().randint(2, num - 2)
        if eGcd(num, a) != 1:
            return False, time.time() - startTime  # composite number so not co-prime with a
        if pow(a, num - 1, num) != 1:
            return False, time.time() - startTime  # fermat witness
    return True, time.time() - startTime


if __name__ == "__main__":
    # Test cases
    print(isPrime(7919, 2))