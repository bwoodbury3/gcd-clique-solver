"""
Utils for boolean satisfiability.
"""

import random

from util import fileio


class BooleanVariable:
    def __init__(self, name: str, inverted: bool):
        self.name = name
        self.inverted = inverted

    def eval(self, value: bool) -> bool:
        return value == (not self.inverted)

    def __str__(self) -> str:
        invert = "!" if self.inverted else ""
        return invert + self.name

    def __repr__(self) -> str:
        return str(self)


BooleanExpression = tuple[BooleanVariable]
SatProblem = list[BooleanExpression]
AnswerKey = dict[str, bool]

_VALID_VAR_CHARS = "abcdefghijklmnopqrstuvwxyz"


def _variable_name(n: int) -> str:
    """
    Procedurally generate a variable name from a number.

    Args:
        n: The number.
    """
    assert n >= 0, "Variable names for values < 0 are not unique"

    name = ""
    while True:
        name += _VALID_VAR_CHARS[n % len(_VALID_VAR_CHARS)]
        if n < len(_VALID_VAR_CHARS):
            break
        n = n // len(_VALID_VAR_CHARS)
    return name


def evaluate_expression(expression: BooleanExpression, answer_key: AnswerKey) -> bool:
    """
    Evaluate a single expression.

    Args:
        expression: The expression to evaluate
        answer_key: The answer key
    """
    exp_result = False
    for var in expression:
        # If the variable is not in the answer key, do not include it. This
        # implicitly assumes it will evaluate to false for this expression and
        # therefore doesn't matter for the solution.
        if var.name in answer_key:
            exp_result = exp_result or var.eval(answer_key[var.name])
    return exp_result


def evaluate(problem: SatProblem, answer_key: AnswerKey) -> bool:
    """
    Evaluate a problem with an answer key. Return True if the boolean
    result is True, else false.

    Args:
        problem: The SAT problem.
        answer_key: The answer key.
    """
    result = True
    for expression in problem:
        exp_result = evaluate_expression(expression, answer_key)
        if not exp_result:
            print(f"Expression failed: {expression}")
        result = result and exp_result
    return result


def generate_random_sat(
    num_expressions: int,
    num_variables: int,
    expression_len: int,
) -> tuple[SatProblem, AnswerKey]:
    """
    Generate a random sat problem. Ensures that there is a valid solution.

    Args:
        num_expressions: The total number of expressions
        num_variables: The total number of variables
        expression_len: The length of each expression
    """
    problem: SatProblem = []
    true_or_false = (True, False)

    # Build a list of variables
    variables = [_variable_name(n) for n in range(num_variables)]

    # Build the answer key
    answer_key = {v: random.choice(true_or_false) for v in variables}

    for _ in range(num_expressions):
        # Find k random variables to build into an expression.
        expression_vars = random.choices(variables, k=expression_len)

        expression: BooleanExpression = tuple(
            BooleanVariable(var, random.choice(true_or_false))
            for var in expression_vars
        )

        # Pick one of them which must evaluate to true.
        var = random.choice(expression)
        var.inverted = not answer_key[var.name]

        problem.append(expression)
    return problem, answer_key


def read_from_file(filename: str) -> tuple[SatProblem, AnswerKey]:
    """
    Load a SAT problem from a file.

    Expected format:
        n_expressions
        n_variables

        v0 v1 !v2
        v1 v2 !v0
        ...

        v0 [true|false]
        v1 [true|false]
        ...

    Args:
        filename: The filename.
    """
    lines = fileio.read_data_lines(filename)

    n_expressions = int(lines[0])
    n_variables = int(lines[1])

    problem: SatProblem = []
    answer_key: AnswerKey = {}

    index = 2
    for _ in range(n_expressions):
        toks = lines[index].split()
        expression = ()
        for tok in toks:
            name = tok.lstrip("!")
            inverted = tok.startswith("!")
            expression += (BooleanVariable(name, inverted),)
        problem.append(expression)
        index += 1
    for _ in range(n_variables):
        toks = lines[index].split()
        answer_key[toks[0]] = bool(toks[1])
        index += 1

    return problem, answer_key


def write_to_file(filename: str, problem: SatProblem, answer_key: AnswerKey):
    """
    Write a SAT problem to a file.

    Args:
        filename: The filename.
        problem: The SAT problem.
        answer_key: The answer key.
    """

    with open(filename, "w") as f:
        f.write(f"{len(problem)}\n")
        f.write(f"{len(answer_key)}\n")
        for expression in problem:
            f.write(" ".join(str(var) for var in expression) + "\n")
        for var, answer in answer_key.items():
            f.write(f"{var} {answer}\n")


if __name__ == "__main__":
    problem, answer_key = generate_random_sat(10, 10, 3)
    write_to_file("datasets/sat_10x3.txt", problem, answer_key)
    print(problem)
    print(answer_key)
    print(f"Result: {evaluate(problem, answer_key)}")
