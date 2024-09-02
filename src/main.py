import argparse

from algos import clique_solvers, sat_solvers, tsp_solvers
from util import graphs, profile, sats


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
            v, e = graphs.read_from_file(args.filename)
        elif args.vertices and args.edges:
            v, e = graphs.generate_random_graph(args.vertices, args.edges)
        else:
            raise ValueError(f"Must provide either --filename or --vertices & --edges")

        # Add the clique to the graph if requested
        if args.add_clique:
            graphs.add_clique(v, e, args.graphs.add_clique)

        func(v, e, args)

    return wrapper


def add_sat_args(parser: argparse.ArgumentParser) -> None:
    """
    Add argparse args that are relevant to Boolean Satisfiability problem.

    Args:
        parser: The parser or subparser.
    """
    parser.add_argument("--filename", type=str, help="File containing a graph")
    parser.add_argument(
        "--expressions", "-e", type=int, help="The number of expressions"
    )
    parser.add_argument("--variables", "-v", type=int, help="The number of variables")


def parse_sat_args(func: callable):
    """
    Run the sat solver.

    Args:
        args: The args.
    """

    def wrapper(args: argparse.Namespace):
        # Load the problem.
        if args.filename:
            problem, _ = sats.read_from_file(args.filename)
        elif args.expressions and args.variables:
            problem, _ = sats.generate_random_sat(args.expressions, args.variables, 3)
        else:
            raise ValueError(
                f"Must provide either --filename or --expressions and --variables"
            )

        func(problem, args)

    return wrapper


@parse_graph_args
def run_clique_solver(
    vertices: graphs.GraphVertices,
    edges: graphs.GraphEdges,
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


@parse_graph_args
def run_tsp_solver(
    vertices: graphs.GraphVertices,
    edges: graphs.GraphEdges,
    args: argparse.Namespace,
) -> None:
    """
    Run the traveling salesman solver.

    Args:
        vertices: The vertices of the graph.
        edges: The edges of the graph.
        args: The args.
    """
    graph = graphs.Graph(vertices, edges)
    solution, distance = args.solver(graph, args.cities)
    print(f"Solution: {solution}")
    print(f"Distance: {distance}")


@parse_sat_args
def run_3sat_solver(problem: sats.SatProblem, args: argparse.Namespace) -> None:
    """
    Run the 3-sat solver.

    Args:
        problem: The 3-sat problem.
        args: The args.
    """
    solution = args.solver(problem)
    print(f"Problem: {problem}")
    print(f"Solution: {solution}")


def parse_args() -> argparse.Namespace:
    """
    Parse args.
    """
    parser = argparse.ArgumentParser(prog="main.py")
    parser.add_argument(
        "--profile",
        action="store_true",
        help="Time all of the subroutines",
    )

    subparsers = parser.add_subparsers(required=True)

    #### CLIQUE ####
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

    #### Traveling Salesman ####
    tsp_parser = subparsers.add_parser(
        "tsp",
        help="Find the shortest cycle around N vertices (traveling salesman)",
    )
    add_solvers(tsp_parser, tsp_solvers)
    add_graph_args(tsp_parser)
    tsp_parser.add_argument(
        "--cities",
        "-c",
        nargs="+",
        type=int,
        help="The cities to traverse",
    )
    tsp_parser.set_defaults(func=run_tsp_solver)

    #### 3-SAT ####
    sat_parser = subparsers.add_parser(
        "3sat",
        help="Find a solution to the boolean expression",
    )
    add_solvers(sat_parser, sat_solvers)
    add_sat_args(sat_parser)
    sat_parser.set_defaults(func=run_3sat_solver)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.profile:
        profile.enable()

    args.func(args)

    if profile.is_enabled():
        profile.print_report()
