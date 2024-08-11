"""
Basic graph util
"""

import random

GraphVertices = list[int]
GraphEdges = list[tuple[int, int]]


def generate_random_graph(v: int, e: int) -> tuple[GraphVertices, GraphEdges]:
    """
    Generate a random graph with v vertices and e edges.

    Args:
        v: The number of vertices
        e: The number of edges
    """
    vertices = [i for i in range(v)]
    all_possible_edges = [(i, j) for i in vertices for j in vertices[i + 1 :]]
    edges = random.choices(all_possible_edges, k=e)
    return vertices, edges


def add_clique(vertices: GraphVertices, edges: GraphEdges, k: int):
    """
    Add a clique to the provided graph of the provided size.

    Args:
        vertices: The vertices
        edges: The edges
        k: The clique size.
    """
    clique_vertices = random.choices(vertices, k=k)
    for i in range(len(clique_vertices)):
        for j in range(i + 1, len(clique_vertices)):
            edge = (clique_vertices[i], clique_vertices[j])
            if edge not in edges:
                edges.append(edge)
