import prime_util

import math


def test_prime_factorization():
    assert prime_util.prime_factorization(20) == [2, 2, 5]
    assert prime_util.prime_factorization(412) == [2, 2, 103]
    assert prime_util.prime_factorization(8018367) == [3, 7, 31, 109, 113]


def _test_divisor_helper(num: int, factors: list[int]):
    """
    Helper function to test divisors using some math laws.

    Args:
        num: The num to find divisors for.
        factors: The prime factorization.
    """
    assert math.prod(factors) == num
    divisors = prime_util.divisors_from_prime_factors(factors)

    # They should all be legit divisors
    for divisor in divisors:
        assert num % divisor == 0

    # All the divisors should all be unique.
    assert len(set(divisors)) == len(divisors)

    expected_n_divisors = 1
    m_factor_count = {f: factors.count(f) for f in factors}
    for count in m_factor_count.values():
        expected_n_divisors *= count + 1
    assert expected_n_divisors == len(divisors)


def test_divisors_from_prime_factors():
    """
    Test divisors_from_prime_factors()
    """
    factors = [3, 7, 31, 109, 113]
    product = math.prod(factors)
    assert prime_util.prime_factorization(product) == factors

    _test_divisor_helper(product, factors)


def test_large_number_divisors():
    """
    Test big numbers for divisors.
    """
    num = 9626106318124170308144127606972801521
    factors = prime_util.prime_factorization(num)
    _test_divisor_helper(num, factors)
