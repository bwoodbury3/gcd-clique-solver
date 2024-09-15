"""
Basic graph util
"""

from queue import PriorityQueue
import random

from util import fileio, profile

GraphVertices = list[int]
GraphEdges = list[tuple[int, int, int]]


class Graph:
    """
    Convenience object for storing vertices, edges, and a lookup table of
    neighbors for each vertex.
    """

    @profile.timer("graphs.Graph.__init__")
    def __init__(self, vertices: GraphVertices, edges: GraphEdges):
        self.vertices = vertices
        self.edges = edges

        # Construct a lookup table to map vertices to their neighbor vertices.
        self.m_neighbors: dict[int, list[int]] = {v: [] for v in self.vertices}
        for v0, v1, weight in self.edges:
            self.m_neighbors[v0].append(v1)
            self.m_neighbors[v1].append(v0)

        # Another lookup table for finding weights
        self.m_m_edges: dict[int, dict[int, int]] = {}
        for v0, v1, weight in self.edges:
            self.m_m_edges.setdefault(v0, {})[v1] = weight
            self.m_m_edges.setdefault(v1, {})[v0] = weight

    def __repr__(self) -> str:
        s = ""
        for v, neighbors in self.m_neighbors.items():
            s += f"{v}: {neighbors}\n"
        return s

    @profile.timer("graphs.Graph.subgraph")
    def subgraph(
        self,
        vertices: GraphVertices = None,
        edges: GraphEdges = None,
    ) -> "Graph":
        """
        Construct a new subgraph with only the provided vertices/edges. If either
        argument is None then no filter will be applied.

        Args:
            vertices: If provided, will filter the graph down to only these vertices.
            edges: If provided, will filter the graph down to only these edges.

        Return: the subgraph.
        """
        new_vertices = self.vertices
        new_edges = self.edges

        # Filter out the vertices that we were asked to.
        # Filter out edges for vertices that are no longer present.
        if vertices is not None:
            new_vertices = [vertex for vertex in self.vertices if vertex in vertices]
            new_edges = [
                edge
                for edge in self.edges
                if edge[0] in new_vertices and edge[1] in new_vertices
            ]

        # Filter out edges that we were asked to.
        if edges is not None:
            new_edges = [edge for edge in self.edges if edge in edges]

        return Graph(new_vertices, new_edges)

    def dim(self) -> tuple[int, int]:
        """
        Return: the number of vertices and edges.
        """
        return len(self.vertices), len(self.edges)


@profile.timer("graphs.generate_random_graph")
def generate_random_graph(
    v: int,
    e: int,
    min_weight: int = 1,
    max_weight: int = 1,
) -> tuple[GraphVertices, GraphEdges]:
    """
    Generate a random graph with v vertices and e edges.

    Args:
        v: The number of vertices
        e: The number of edges
        min_weight: The minimum weight
        max_weight: The maximum weight
    """
    vertices = [i for i in range(v)]
    all_possible_edges = [
        (i, j, random.randint(min_weight, max_weight))
        for i in vertices
        for j in vertices[i + 1 :]
    ]
    edges = random.sample(all_possible_edges, e)
    return vertices, edges


@profile.timer("graphs.add_clique")
def add_clique(vertices: GraphVertices, edges: GraphEdges, k: int):
    """
    Add a clique to the provided graph of the provided size.

    Args:
        vertices: The vertices
        edges: The edges
        k: The clique size.

    Returns: The clique that was added.
    """
    clique_vertices = random.sample(vertices, k)
    clique_vertices.sort()
    for i in range(len(clique_vertices)):
        for j in range(i + 1, len(clique_vertices)):
            edge = (clique_vertices[i], clique_vertices[j], 1)
            if edge not in edges:
                edges.append(edge)
    return clique_vertices


@profile.timer("graphs.read_from_file")
def read_from_file(filename: str) -> tuple[GraphVertices, GraphEdges]:
    """
    Read a graph from a file.

    Expected format:
        n_vertices
        n_edges

        v02
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
        edge = lines[index].split()
        if len(edge) == 2:
            edges.append((int(edge[0]), int(edge[1]), 1))
        elif len(edge) == 3:
            edges.append((int(edge[0]), int(edge[1]), int(edge[2])))
        else:
            raise ValueError("Edge must have 2 or 3 tokens")

        index += 1

    return vertices, edges


@profile.timer("graphs.write_to_file")
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
        for v0, v1, weight in edges:
            f.write(f"{v0} {v1} {weight}\n")


@profile.timer("graphs.dfs")
def dfs(graph: Graph, start_node: int, target_node: int = None) -> dict[int, int]:
    """
    Depth-first search from a start node. If target_node is specified, this
    function will return when it is reached. Otherwise, it will return a map
    representing all nodes and the distance to those nodes.

    Args:
        graph: The graph to search.
        start_node: The start node.
        target_node: The node to search for. If omitted, the algorithm will just
                     search the entire graph for everything.
    """

    distances = {}
    q = PriorityQueue()
    q.put((0, start_node))

    while not q.empty():
        cur_distance, node = q.get()

        # We've already seen this node; skip.
        if node in distances:
            continue

        # Add this node to the map of distances. If it matches the node we're
        # looking for, break.
        distances[node] = cur_distance
        if node == target_node:
            break

        # Otherwise, explore all of the neighbors of this node and add them to
        # the search queue.
        neighbors = graph.m_m_edges[node]
        for node, weight in neighbors.items():
            if node not in distances:
                q.put((weight + cur_distance, node))

    return distances


if __name__ == "__main__":
    v, e = generate_random_graph(1_000, 100_000)
    add_clique(v, e, 10)
    write_to_file("datasets/1000x100000_10clique.txt", v, e)
