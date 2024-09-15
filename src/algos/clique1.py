"""
clique1 solver.
"""

import json
import math

from util import profile
from util.graphs import GraphVertices, GraphEdges
from util.primes import divisors_from_prime_factors, prime_list


class PrimeGraph:
    """
    A graph backed by prime numbers. Every vertex is represented by a prime
    number, and each vertex points to a composite number whos factors represent
    the edges to other vertices. For example:

    2 --- 3
         /
        /
       5

    {
        2: 2 * 3       # 2 is connected to itself and 3.
        3: 3 * 2 * 5   # 3 is connected to itself, 3, and 5.
        5: 5 * 3       # 5 is connected to itself and 3.
    }
    """

    def __init__(self, vertices: GraphVertices, edges: GraphEdges):
        """
        Constructor.
        """
        # Save off the vertices/edges just in case that's somehow useful later.
        self.vertices = vertices
        self.edges = edges

        # Build a list of the first N primes so that we can map every vertex to
        # a prime number.
        self.primes = prime_list(len(vertices))
        assert len(self.primes) == len(vertices)

        # Map vertices to primes and vice versa.
        self.v2p = {vertices[i]: self.primes[i] for i in range(len(vertices))}
        self.p2v = {self.primes[i]: vertices[i] for i in range(len(vertices))}

        # Save off the same vertex/edge list using the new prime mapping.
        self.pvertices = [self.v2p[v] for v in vertices]
        self.pedges = [(self.v2p[v0], self.v2p[v1]) for v0, v1, _ in edges]

        # Construct a graph where each vertex is mapped to a composite number
        # whose prime factors are the product of reachable edges.
        self.m = {vert: vert for vert in self.pvertices}
        for v0, v1 in self.pedges:
            self.m[v0] *= v1
            self.m[v1] *= v0

        # Construct a lookup table to map vertices to their neighbors.
        self.m_neighbors = {vert: [] for vert in self.pvertices}
        for v0, v1 in self.pedges:
            self.m_neighbors[v0].append(v1)
            self.m_neighbors[v1].append(v0)

    def __str__(self) -> str:
        """
        Get a string representation of this prime graph.
        """
        o = {"v2p": self.v2p, "edges": self.pedges, "graph": self.m}
        return json.dumps(o, indent=4)

    @profile.timer("PrimeGraph.is_clique")
    def is_clique(self, pvertices: GraphVertices) -> bool:
        """
        Returns whether the list of vertices forms a clique.

        Args:
            pvertices: list of prime vertices.
        """
        # Multiply all of the vertices together
        product = math.prod(pvertices)

        # If the product divides all vertices evenly, we have a clique.
        for v in pvertices:
            if self.m[v] % product != 0:
                return False
        return True


@profile.timer("clique1.solve")
def solve(vertices: GraphVertices, edges: GraphEdges, k: int) -> list[int]:
    """
    Return a clique of size k if one exists, else None.

    Args:
        vertices:
        edges:
        k: The clique size
    """
    graph = PrimeGraph(vertices, edges)

    # Store all of the divisors for all vertex.
    m_divisor_count = {}
    for v in graph.pvertices:
        # Grab the value and its prime factors
        value = graph.m[v]
        l_prime_factors = graph.m_neighbors[v]
        l_prime_factors.append(v)
        assert (
            math.prod(l_prime_factors) == value
        ), f"Factors {l_prime_factors} do not match product {value}"

        # Grab all of the divisors.
        l_divisors = divisors_from_prime_factors(l_prime_factors)

        # Add the divisors to the m_divisor_count list.
        for divisor in l_divisors:
            m_divisor_count[divisor] = m_divisor_count.get(divisor, 0) + 1

    print(f"Total number of divisors: {len(m_divisor_count)}")

    # This is the meat of the algorithm.
    #
    # Now that we have a list of all divisors for every node, our goal is to
    # now find a divisor for which satisfies the two criteria:
    #   * the count is >= k (k vertices have this divisor)
    #   * k vertices with this divisor are also present in the divisor
    best_divisor = -1
    for divisor, count in m_divisor_count.items():
        if count >= k:
            num_clique_members = 0
            for v in graph.pvertices:
                # graph.m[v] % divisor == 0
                #    This check rules out whether this vertex can view the same
                #    nodes represented by the divisor
                # divisor % v == 0
                #    This check tells us whether this node is also present in the
                #    clique
                if graph.m[v] % divisor == 0 and divisor % v == 0:
                    num_clique_members += 1
            if num_clique_members >= k:
                best_divisor = divisor
                break

    # Best divisor is none, meaning no divisors of high enough value were found.
    if best_divisor == -1:
        return None

    # Next, gather all of the vertices in cur_vertices for which their value
    # can be evenly divided by the candidate divisor. There should be at
    # least k vertices or we messed something up.
    clique = [v for v in graph.pvertices if graph.m[v] % best_divisor == 0]
    assert len(clique) >= k

    # The clique found is >=k, so return a subclique as needed.
    clique = clique[:k]
    assert graph.is_clique(clique)

    return [graph.p2v[v] for v in clique]
