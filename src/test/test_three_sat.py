"""
Functional test of 3sat.
"""

from algos import three_sat1, three_sat2
from util import sats


def test_three_sat1():
    problem, _ = sats.read_from_file("datasets/sat_10x3.txt")
    solution = three_sat1.solve(problem)
    assert solution is not None
    assert sats.evaluate(problem, solution) == True


def test_three_sat2():
    problem, _ = sats.read_from_file("datasets/sat_10x3.txt")
    solution = three_sat2.solve(problem)
    assert solution is not None
    assert sats.evaluate(problem, solution) == True
