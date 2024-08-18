"""
Basic graph util
"""

import random

from util import fileio

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


def read_from_file(filename: str) -> tuple[GraphVertices, GraphEdges]:
    """
    Read a graph from a file.

    Expected format:
        n_vertices
        n_edges

        v0
        v1
        ...
        vN

        vN vM   # Edge0
        vN vM   # Edge1
        ...

    Args:
        filename: The filename.
    """
    lines = fileio.read_data_lines(filename)

    num_vertices = int(lines[0])
    num_edges = int(lines[1])
    vertices = []
    edges = []

    index = 2
    for _ in range(num_vertices):
        vertex = int(lines[index])
        vertices.append(vertex)
        index += 1
    for _ in range(num_edges):
        s_v0, s_v1 = lines[index].split()
        edges.append((int(s_v0), int(s_v1)))
        index += 1

    return vertices, edges


def write_to_file(filename: str, vertices: GraphVertices, edges: GraphEdges):
    """
    Store the graph in a file.

    Args:
        filename: The filename.
        vertices: The vertices.
        edges: The edges.
    """
    with open(filename, "w") as f:
        f.write(f"{len(vertices)}\n")
        f.write(f"{len(edges)}\n")
        for v in vertices:
            f.write(f"{v}\n")
        for v0, v1 in edges:
            f.write(f"{v0} {v1}\n")


if __name__ == "__main__":
    v, e = generate_random_graph(20_000, 200_000)
    add_clique(v, e, 8)
    write_to_file("datasets/20000x200000_8clique.txt", v, e)
