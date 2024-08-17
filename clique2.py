"""
Trivial clique solver.
"""

import json
import math
import time

from graph_util import add_clique, generate_random_graph, GraphVertices, GraphEdges


class Clique:
    def __init__(self, vertices: tuple[int], reachable: list[int]):
        self.vertices = vertices
        self.reachable = reachable
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


def clique(vertices: GraphVertices, edges: GraphEdges, k: int) -> list[Clique]:
    """
    Return all cliques of size k found in the graph.

    Args:
        vertices:
        edges:
        k: The clique size
    """
    m_neighbors = {v: [] for v in vertices}
    for v0, v1 in edges:
        m_neighbors[v0].append(v1)
        m_neighbors[v1].append(v0)

    # A running list of all cliques. Using a set prevents duplicate permutations
    # (i.e. [1, 2, 3] == [1, 3, 2])
    cliques = set(Clique(vertices=(v,), reachable=m_neighbors[v]) for v in vertices)

    # In each iteration N, take all cliques of size N-1 and add a new vertex if
    # that vertex would create another valid clique.
    for i in range(1, k):
        print(f"Iteration: {i}")
        new_cliques = set()
        for c in cliques:
            for vertex in c.reachable:
                # Ignore the vertex if it's already part of this clique. That's
                # not very helpful.
                if vertex in c.vertices:
                    continue

                # Add this vertex to the clique and trim down the list of clique
                # suspects as needed.
                neighbors = m_neighbors[vertex]
                new_cliques.add(
                    Clique(
                        vertices=c.vertices + (vertex,),
                        reachable=[r for r in c.reachable if r in neighbors],
                    )
                )
        cliques = new_cliques

    return cliques


if __name__ == "__main__":
    print("Loading graph")

    # Uncomment this to read in data from a file
    # filename = sys.argv[1]
    # v, e = read_from_file(filename)

    v, e = generate_random_graph(10_000, 100_000)
    add_clique(v, e, 8)

    print("Finding clique")

    t0 = time.monotonic()
    ans = clique(v, e, 8)
    print(ans if ans else "No clique found")
    t1 = time.monotonic()

    print(f"RUNTIME: {t1 - t0:.2f}s")
