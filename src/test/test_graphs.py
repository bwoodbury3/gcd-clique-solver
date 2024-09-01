"""
Functional test of graphs.
"""

from util import graphs


def test_read():
    vertices, edges = graphs.read_from_file("datasets/100x400.txt")
    assert vertices == [i for i in range(100)]

    for v0, v1, weight in edges:
        assert v0 in vertices
        assert v1 in vertices
        assert v0 != v1
        assert weight == 1


def test_random_graph():
    vertices, edges = graphs.generate_random_graph(10, 40, 1, 10)
    assert vertices == [i for i in range(10)]

    for v0, v1, weight in edges:
        assert v0 in vertices
        assert v1 in vertices
        assert v0 != v1
        assert weight >= 1 and weight <= 10


def test_dfs():
    vertices, edges = graphs.read_from_file("datasets/100x400.txt")
    graph = graphs.Graph(vertices, edges)

    # Every node is reachable from every other node in this graph, so the
    # distances should always be 100.
    distances0 = graphs.dfs(graph, 0)
    assert len(distances0) == 100
    distances10 = graphs.dfs(graph, 10)
    assert len(distances10) == 100
    distances42 = graphs.dfs(graph, 42)
    assert len(distances42) == 100

    # Double check that we get the same result searching from another node.
    assert distances0[42] == distances42[0]
    assert distances0[10] == distances10[0]
    assert distances42[10] == distances10[42]
