"""
Miller-Rabin Primality Test

This module implements the Miller-Rabin probabilistic primality test.
It's more robust than Fermat's test and can detect Carmichael numbers.

Time Complexity: O(k log³n) where k is the number of rounds
Space Complexity: O(1)
Deterministic: No (probabilistic, but no known pseudoprimes for random bases)
Error Probability: At most 4^(-k) for k rounds
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
    Check if a number is probably prime using the Miller-Rabin primality test.
    
    The Miller-Rabin test is based on writing n-1 = 2^s × t where t is odd.
    For a prime n and random base a:
    - Either a^t ≡ 1 (mod n), or
    - a^(2^r × t) ≡ -1 (mod n) for some 0 ≤ r < s
    
    This test can detect Carmichael numbers that fool Fermat's test.
    
    Algorithm:
    1. Handle edge cases (small numbers, even numbers)
    2. Write n-1 = 2^s × t where t is odd
    3. Repeat k times:
       a. Choose random base a in [2, n-2]
       b. If gcd(a, n) ≠ 1, n is composite
       c. Compute x = a^t mod n
       d. If x = 1 or x = -1, continue to next round
       e. Square x (s-1) times, checking if we get -1
       f. If we never get -1, n is composite
    4. If all k tests pass, n is probably prime
    
    Args:
        num (int): The integer to check for primality (should be positive)
        k (int): Number of testing rounds (higher k = higher confidence)
                 Default is 10. Error probability ≤ 4^(-k)
    
    Returns:
        tuple[bool, float]: A tuple containing:
            - bool: True if probably prime, False if definitely composite
            - float: Execution time in seconds
    
    Examples:
        >>> is_prime(17, k=5)
        (True, 0.0001...)
        >>> is_prime(561, k=10)  # Carmichael number - correctly identified as composite
        (False, 0.0001...)
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
    
    # Write num-1 as 2^s × t where t is odd
    # We do this by repeatedly dividing by 2
    s = 0
    t = num - 1
    while t % 2 == 0:
        s += 1
        t //= 2
    
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
        
        # Compute x = a^t mod num
        x = pow(a, t, num)
        
        # If x = 1 or x = -1 (mod num), this round passes
        # -1 mod num is equivalent to num-1
        if x == 1 or x == num - 1:
            continue
        
        # Square x repeatedly (s-1 times) and check for -1
        # The sequence is: a^t, a^(2t), a^(4t), ..., a^(2^(s-1) × t)
        composite = True
        for _ in range(s - 1):
            x = (x * x) % num
            
            # If we find -1 (mod num), this round passes
            if x == num - 1:
                composite = False
                break
        
        # If we never found -1, num is composite
        if composite:
            return False, time.time() - start_time
    
    # All k tests passed, num is probably prime
    # With k=10, error probability ≤ 4^(-10) ≈ 0.00000095
    return True, time.time() - start_time


if __name__ == "__main__":
    # Test cases including Carmichael numbers
    test_numbers = [
        2, 3, 17, 19, 100, 7919,
        561,    # Carmichael number (should be detected as composite)
        1105,   # Carmichael number
        1729    # Carmichael number
    ]
    
    print("Miller-Rabin Primality Test (k=20 rounds)")
    print("-" * 60)
    
    for num in test_numbers:
        result, exec_time = is_prime(num, k=20)
        # Verify correctness
        actual_prime = num in [2, 3, 17, 19, 7919]
        status = "✓" if result == actual_prime else "✗"
        print(f"n={num:5d} | Result: {result:5} | Actual: {actual_prime:5} | {status} | Time: {exec_time:.6f}s")
