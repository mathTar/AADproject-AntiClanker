"""
Trial Division Primality Test

This module implements the trial division algorithm for primality testing.
It is a deterministic algorithm that tests divisibility by all integers up to √n.

Time Complexity: O(√n)
Space Complexity: O(1)
Deterministic: Yes (100% accurate)
"""

import sys
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.helpers import extended_gcd, sqrt_int


def is_prime(num: int) -> tuple[bool, float]:
    """
    Check if a number is prime using trial division.
    
    This is the most straightforward primality test. It checks if the number
    is divisible by any integer from 2 to √num. While deterministic and always
    correct, it becomes slow for large numbers.
    
    Algorithm:
    1. Handle edge cases (n ≤ 1, n ≤ 3, even numbers)
    2. Check divisibility by all numbers from 2 to √n
    3. If any divisor found, number is composite
    4. Otherwise, number is prime
    
    Args:
        num (int): The integer to check for primality (should be positive)
    
    Returns:
        tuple[bool, float]: A tuple containing:
            - bool: True if num is prime, False if composite
            - float: Execution time in seconds
    
    Examples:
        >>> is_prime(17)
        (True, 0.0001...)
        >>> is_prime(20)
        (False, 0.0001...)
        >>> is_prime(2)
        (True, 0.0)
    """
    # Edge cases: numbers ≤ 1 are not prime
    if num <= 1:
        return False, 0.0
    
    # 2 and 3 are prime
    if num <= 3:
        return True, 0.0
    
    # Even numbers (except 2) are not prime
    if num % 2 == 0:
        return False, 0.0
    
    # Start timing for the actual computation
    start_time = time.time()
    
    # Check divisibility by all odd numbers from 3 to √num
    # We use GCD to check divisibility: if gcd(num, i) ≠ 1, then i divides num
    for i in range(3, sqrt_int(num) + 1, 2):
        if extended_gcd(num, i) != 1:
            # Found a divisor, number is composite
            return False, time.time() - start_time
    
    # No divisors found, number is prime
    return True, time.time() - start_time


if __name__ == "__main__":
    # Test cases
    test_numbers = [2, 3, 17, 19, 100, 7919, 561]  # 561 is a Carmichael number
    
    print("Trial Division Primality Test")
    print("-" * 50)
    
    for num in test_numbers:
        result, exec_time = is_prime(num)
        print(f"n={num:5d} | Prime: {result:5} | Time: {exec_time:.6f}s")
