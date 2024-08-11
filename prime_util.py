"""
Utilities for working with prime numbers.
"""

import math


class MathIsBroken(ValueError):
    """
    Exception raised when you have broken fundamental math.
    """

    pass


def prime_list(n: int) -> list[int]:
    """
    Return a list of the first n unique prime numbers.

    (ty: https://stackoverflow.com/questions/11619942/print-series-of-prime-numbers-in-python)

    Args:
        n: The number of prime numbers to return.
    """

    # The nth prime is <= `n * ln(n) + n * ln(ln(n))` for n >= 6.
    # Per: https://en.wikipedia.org/wiki/Prime_number_theorem
    max = int(n * math.log(n) + n * math.log(math.log(n)) + 7)

    out = list()
    sieve = [True] * (max + 1)
    for p in range(2, max + 1):
        if sieve[p]:
            out.append(p)

            # Exit if we found enough numbers.
            if len(out) == n:
                return out

            # Cross out the rest of the multiples in the seive.
            for i in range(p, max + 1, p):
                sieve[i] = False

    if len(out) < n:
        raise MathIsBroken(f"The Prime Number Theorem was violated for n={n}")

    return out


def divisors_from_prime_factors(factors: list[int]) -> list[int]:
    """
    Get a list of all divisors for a number given its prime factorization. The
    original number is implied from its prime factorization.

    Args:
        factors: The prime factorization.
    """

    def _generate_divisors(index: int, divisor: int, prime_counts: list[int, int]):
        """
        Recursive subroutine.

        (ty: https://www.geeksforgeeks.org/generating-all-divisors-of-a-number-using-its-prime-factorization/#)

        Args:
            index: The current index.
            divisor: The current divisor.
            prime_counts: A list of tuples representing the factorization as:
                          (prime, exponent)
        """
        divisors = []

        # Base case i.e. we do not have any more prime factors
        if index == len(prime_counts):
            return [divisor]

        for _ in range(prime_counts[index][1] + 1):
            divisors += _generate_divisors(index + 1, divisor, prime_counts)
            divisor *= prime_counts[index][0]

        return divisors

    m_prime_counts = {}
    for prime in factors:
        m_prime_counts[prime] = m_prime_counts.get(prime, 0) + 1
    l_prime_counts = [(prime, count) for prime, count in m_prime_counts.items()]

    return _generate_divisors(0, 1, l_prime_counts)


def prime_factorization(num: int) -> list[int]:
    """
    Return a prime factorization for a number.

    Args:
        num: The number to factor.
    """
    factors = []
    i = 2
    while num >= i:
        while num % i == 0:
            factors.append(i)
            num = num // i
        i += 1
    return factors
