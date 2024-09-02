"""
3-SAT solver.
"""

import typing
from util import profile, sats


@profile.timer("three_sat2.expression_combos")
def expression_combos(
    expression: sats.BooleanExpression,
) -> typing.Iterable[sats.AnswerKey]:
    """
    Generator for all of the possible answer keys that satisfy this expression.

    Args:
        expression: The expression.
    """

    val_names = set(var.name for var in expression)
    digits = len(val_names)
    max_val = 2**digits
    for num in range(0, max_val):
        # Here's a possible key.
        key = {var: ((num >> i) & 1 == 1) for i, var in enumerate(val_names)}
        if sats.evaluate_expression(expression, key):
            yield key


@profile.timer("three_sat2.prune_independent_expressions")
def prune_independent_expressions(
    problem: sats.SatProblem,
) -> tuple[sats.SatProblem, sats.AnswerKey]:
    """
    Return a subproblem + answer key where all of the expressions are independent.
    """

    # First, track whether a variable appears in the problem. Create a map of vars
    # to whether they appear as normal or inverted.
    vars: map[list[bool]] = {}
    for expression in problem:
        for var in expression:
            seen = vars.get(var.name, [False, False])  # [normal, inverted]
            if var.inverted:
                seen[1] = True
            else:
                seen[0] = True
            vars[var.name] = seen

    # Next, build a problem where none of the variables in any expression are
    # independent.
    pruned_problem: sats.SatProblem = []
    pruned_key: sats.AnswerKey = {}
    for expression in problem:
        independent_var = None

        # Check if any of the variables are independent
        for var in expression:
            if vars[var.name].count(True) < 2:
                independent_var = var.name
                break

        # If it's independent, add it to the answer key.
        if independent_var is not None:
            if vars[var.name][0]:
                pruned_key[independent_var] = True
            else:
                pruned_key[independent_var] = False

        # Otherwise, the expression is not independent and cannot be discarded.
        else:
            pruned_problem.append(expression)

    print(
        f"Pruned {len(problem) - len(pruned_problem)} expressions and "
        f"{2**len(pruned_key)} possible answer keys."
    )

    return pruned_problem, pruned_key


@profile.timer("three_sat2.solve")
def solve(problem: sats.SatProblem) -> sats.AnswerKey:
    """
    Solve 3-sat.

    Args:
        problem: The SAT problem.
    """

    # Prune the problem of any indepdent expressions.
    problem, key = prune_independent_expressions(problem)

    # Maintain a list of all answer keys which solve the cumulative problem.
    answer_keys: list[sats.AnswerKey] = [key]

    for expression in problem:
        new_answer_keys = []

        # Get all of the keys that would satisfy this expression.
        for valid_key_for_expression in expression_combos(expression):

            # For each existing answer key, check whether it would satisfy
            # this particular expression solution, and add it if so.
            for key in answer_keys:

                # First, check whether the existing answer key could satisfy
                # this expression.
                valid = True
                for var, value in valid_key_for_expression.items():
                    # This answer key is not valid.
                    if var in key and key[var] != value:
                        valid = False
                        break

                # If this answer key works for the expression, merge it and add
                # to the list of new answer keys.
                if valid:
                    ak = key.copy()
                    for var, value in valid_key_for_expression.items():
                        ak[var] = value
                    new_answer_keys.append(ak)

        print(f"Num valid answer keys: {len(new_answer_keys)}")
        answer_keys = new_answer_keys

    if answer_keys:
        return answer_keys[0]
    else:
        return None
