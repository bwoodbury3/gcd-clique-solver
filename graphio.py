"""
IO for reading/writing graphs to files.
"""

from graph_util import add_clique, generate_random_graph, GraphVertices, GraphEdges


def read_from_file(filename: str) -> tuple[GraphVertices, GraphEdges]:
    """
    Read a graph from a file.

    Args:
        filename: The filename.
    """
    lines = []
    with open(filename) as f:
        for line in f.readlines():
            # Strip comments
            if "#" in line:
                line = line[: line.find("#")]

            # Strip spaces
            line = line.strip()

            if len(line) != 0:
                lines.append(line)

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
