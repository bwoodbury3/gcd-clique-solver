import argparse

from algos import clique_solvers
from util.graphs import (
    add_clique,
    generate_random_graph,
    GraphVertices,
    GraphEdges,
    read_from_file,
)


def add_solvers(
    parser: argparse.ArgumentParser, m_solvers: dict[str, callable]
) -> None:
    """
    Add a list of solvers to the argument parser.

    Args:
        parser: The parser or subparser.
        m_solvers: The map of strings to solvers.
    """
    parser.add_argument(
        "solver",
        type=m_solvers.get,
        choices=m_solvers.values(),
        metavar=", ".join(m_solvers.keys()),
    )


def add_graph_args(parser: argparse.ArgumentParser) -> None:
    """
    Add argparse args that are relevant to a graph.

    Args:
        parser: The parser or subparser.
    """
    parser.add_argument("--filename", type=str, help="File containing a graph")
    parser.add_argument("--vertices", "-v", type=int, help="The number of vertices")
    parser.add_argument("--edges", "-e", type=int, help="The number of edges")
    parser.add_argument(
        "--add-clique", type=int, help="Add a clique of this size to the input graph"
    )


def parse_graph_args(func: callable):
    """
    Run the clique solver.

    Args:
        args: The args.
    """

    def wrapper(args: argparse.Namespace):
        # Load the graph.
        if args.filename:
            v, e = read_from_file(args.filename)
        elif args.vertices and args.edges:
            v, e = generate_random_graph(args.vertices, args.edges)
        else:
            raise ValueError(f"Must provide either --filename or --vertices & --edges")

        # Add the clique to the graph if requested
        if args.add_clique:
            add_clique(v, e, args.add_clique)

        func(v, e, args)

    return wrapper


@parse_graph_args
def run_clique_solver(
    vertices: GraphVertices,
    edges: GraphEdges,
    args: argparse.Namespace,
) -> None:
    """
    Run the clique solver.

    Args:
        vertices: The vertices of the graph.
        edges: The edges of the graph.
        args: The args.
    """
    solution = args.solver(vertices, edges, args.clique_size)
    print(solution)


def parse_args() -> argparse.Namespace:
    """
    Parse args.
    """
    parser = argparse.ArgumentParser(prog="main.py")
    subparsers = parser.add_subparsers(required=True)

    clique_parser = subparsers.add_parser(
        "clique",
        help="Find a clique of size k in a graph",
    )
    add_solvers(clique_parser, clique_solvers)
    add_graph_args(clique_parser)
    clique_parser.add_argument(
        "--clique-size",
        "-k",
        required=True,
        type=int,
        help="Clique size to search for",
    )
    clique_parser.set_defaults(func=run_clique_solver)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    args.func(args)
