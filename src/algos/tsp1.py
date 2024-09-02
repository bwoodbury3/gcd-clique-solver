"""
Traveling salesman solver.
"""

from util import graphs, profile


@profile.timer("tsp1.solve")
def solve(graph: graphs.Graph, vertices: list[int]) -> list[int]:
    """
    Solve the travling salesman problem.

    Args:
        graph: The graph.
        vertices: The vertices to visit.
    """

    # Preprocess: reduce the graph to a clique with all of the relevant vertices
    # and the distances between them.
    vertices_reduced: graphs.GraphVertices = vertices.copy()
    edges_reduced: graphs.GraphEdges = []
    for i, v0 in enumerate(vertices_reduced):
        distances = graphs.dfs(graph, v0)
        for v1 in vertices_reduced[i + 1 :]:
            edges_reduced.append((v0, v1, distances[v1]))
    graph_reduced = graphs.Graph(vertices_reduced, edges_reduced)

    # Brute force all possible solutions
    solutions = [[]]
    for i in range(len(vertices)):
        new_solutions = []
        for solution in solutions:
            # Find all the vertices that this solution hasn't touched yet.
            for v in vertices_reduced:
                if v not in solution:
                    new_solution = solution.copy() + [v]
                    new_solutions.append(new_solution)
        solutions = new_solutions

    # Calculate the best solution
    best_solution = None
    best_score = 9999999
    for solution in solutions:
        score = 0
        for i in range(-1, len(solution) - 1):
            v0 = solution[i]
            v1 = solution[i + 1]
            score += graph_reduced.m_m_edges[v0][v1]
        if score < best_score:
            best_score = score
            best_solution = solution

    return best_solution, best_score
