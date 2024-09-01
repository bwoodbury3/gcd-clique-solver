"""
Functional test of clique.
"""

from algos import clique1, clique2
from util import graphs


def test_clique1_noclique():
    v, e = graphs.read_from_file("datasets/100x400.txt")
    solution = clique1.solve(v, e, 5)
    assert solution is None


def test_clique1_yesclique():
    v, e = graphs.read_from_file("datasets/100x400_5clique.txt")
    solution = clique1.solve(v, e, 5)
    assert set(solution) == set([5, 7, 36, 62, 97])


def test_clique2_noclique():
    v, e = graphs.read_from_file("datasets/100x400.txt")
    solution = clique2.solve(v, e, 5)
    assert solution is None


def test_clique2_yesclique():
    v, e = graphs.read_from_file("datasets/100x400_5clique.txt")
    solution = clique2.solve(v, e, 5)
    assert set(solution) == set([5, 7, 36, 62, 97])
