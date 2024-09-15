"""
Trivial clique solver.
"""

import json
import math

from util.graphs import GraphVertices, GraphEdges
from util import profile


class Clique:
    def __init__(self, vertices: tuple[int], reachable: list[int]):
        self.vertices = vertices
        self.reachable = reachable

        # We safe off a multiplication of all the vertices. This is not a unique
        # identification of the clique because the vertex IDs are not prime,
        # but it's a quick way to rule out whether two cliques might be equal.
        # See __eq__().
        self.mult = math.prod(self.vertices)

    def __eq__(self, other: "Clique") -> bool:
        return self.mult == other.mult and set(self.vertices) == set(other.vertices)

    def __hash__(self) -> int:
        return self.mult

    def __str__(self) -> str:
        o = {"vertices": self.vertices}
        return json.dumps(o, indent=4)

    def __repr__(self) -> str:
        return str(self)


@profile.timer("clique2.solve")
def solve(vertices: GraphVertices, edges: GraphEdges, k: int) -> list[Clique]:
    """
    Return all cliques of size k found in the graph.

    Args:
        vertices:
        edges:
        k: The clique size
    """
    m_neighbors = {v: set() for v in vertices}
    for v in vertices:
        m_neighbors[v].add(v)
    for v0, v1, _ in edges:
        m_neighbors[v0].add(v1)
        m_neighbors[v1].add(v0)

    # A running list of all cliques. Using a set prevents duplicate permutations
    # (i.e. [1, 2, 3] == [1, 3, 2])
    cliques = set(
        Clique(vertices=(v,), reachable=m_neighbors[v])
        for v in vertices
        if len(m_neighbors[v]) >= k
    )

    # In each iteration N, take all cliques of size N-1 and add a new vertex if
    # that vertex would create another valid clique.
    for i in range(1, k):
        print(f"Iteration: {i}, num cliques: {len(cliques)}")
        new_cliques = set()
        for c in cliques:
            for vertex in c.reachable:
                # Ignore the vertex if it's already part of this clique. That's
                # not very helpful.
                if vertex in c.vertices:
                    continue

                # Check if this new clique has enough visible nodes remaining
                # to form a clique of size k.
                new_reachable = [r for r in c.reachable if r in m_neighbors[vertex]]

                if len(new_reachable) >= k:
                    # Add this vertex to the clique.
                    new_cliques.add(
                        Clique(vertices=c.vertices + (vertex,), reachable=new_reachable)
                    )
        cliques = new_cliques

    if cliques:
        clique = cliques.pop()
        return clique.vertices
    return None
