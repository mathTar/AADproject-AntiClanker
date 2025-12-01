"""
Fermat Primality Test

This module implements Fermat's probabilistic primality test based on Fermat's Little Theorem.

Fermat's Little Theorem: If p is prime and a is not divisible by p, then a^(p-1) ≡ 1 (mod p)

Time Complexity: O(k log³n) where k is the number of rounds
Space Complexity: O(1)
Deterministic: No (probabilistic, can have false positives for Carmichael numbers)
"""

import sys
import random
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.helpers import extended_gcd


def is_prime(num: int, k: int = 10) -> tuple[bool, float]:
    """
    Check if a number is probably prime using Fermat's primality test.
    
    This test is based on Fermat's Little Theorem. For a prime p and any a
    coprime to p, we have a^(p-1) ≡ 1 (mod p). We test this with k random
    bases. If any base fails the test, the number is definitely composite.
    If all bases pass, the number is probably prime.
    
    Limitations:
    - Can give false positives for Carmichael numbers (e.g., 561, 1105, 1729)
    - These are composite numbers that satisfy a^(n-1) ≡ 1 (mod n) for all a coprime to n
    
    Algorithm:
    1. Handle edge cases (small numbers, even numbers)
    2. Repeat k times:
       a. Choose random base a in [2, n-2]
       b. If gcd(a, n) ≠ 1, n is composite
       c. If a^(n-1) ≢ 1 (mod n), n is composite (Fermat witness found)
    3. If all k tests pass, n is probably prime
    
    Args:
        num (int): The integer to check for primality (should be positive)
        k (int): Number of testing rounds (higher k = higher confidence)
                 Default is 10. Each round reduces error probability.
    
    Returns:
        tuple[bool, float]: A tuple containing:
            - bool: True if probably prime, False if definitely composite
            - float: Execution time in seconds
    
    Examples:
        >>> is_prime(17, k=5)
        (True, 0.0001...)
        >>> is_prime(561, k=10)  # Carmichael number - may give false positive!
        (True, 0.0001...)
        >>> is_prime(100, k=5)
        (False, 0.0001...)
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
    
    # Start timing
    start_time = time.time()
    
    # Perform k rounds of testing with random bases
    for _ in range(k):
        # Choose a random base a in the range [2, num-2]
        # Using SystemRandom for cryptographically secure randomness
        a = random.SystemRandom().randint(2, num - 2)
        
        # Check if a and num are coprime
        # If gcd(a, num) ≠ 1, then num is composite
        if extended_gcd(num, a) != 1:
            return False, time.time() - start_time
        
        # Fermat's test: check if a^(num-1) ≡ 1 (mod num)
        # Using Python's built-in modular exponentiation pow(base, exp, mod)
        if pow(a, num - 1, num) != 1:
            # Found a Fermat witness: a proves num is composite
            return False, time.time() - start_time
    
    # All k tests passed, num is probably prime
    # Note: Still could be a Carmichael number (false positive)
    return True, time.time() - start_time


if __name__ == "__main__":
    # Test cases including Carmichael numbers
    test_numbers = [
        2, 3, 17, 19, 100, 7919,
        561,    # Carmichael number (false positive)
        1105,   # Carmichael number
        1729    # Carmichael number (Hardy-Ramanujan number)
    ]
    
    print("Fermat Primality Test (k=20 rounds)")
    print("-" * 60)
    
    for num in test_numbers:
        result, exec_time = is_prime(num, k=20)
        # Verify with trial division for comparison
        actual_prime = num in [2, 3, 17, 19, 7919]
        status = "✓" if result == actual_prime else "✗ (Carmichael)"
        print(f"n={num:5d} | Result: {result:5} | Actual: {actual_prime:5} | {status} | Time: {exec_time:.6f}s")
