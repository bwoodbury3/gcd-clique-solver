"""
3-SAT solver.
"""

from dataclasses import dataclass
import itertools

import typing
from util import sats


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


def three_sat(problem: sats.SatProblem) -> sats.AnswerKey:
    """
    Solve 3-sat.

    Args:
        problem: The SAT problem.
    """

    # Maintain a list of all answer keys which solve the cumulative problem.
    answer_keys: list[sats.AnswerKey] = [{}]

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
    return answer_keys


if __name__ == "__main__":
    problem, answer_key = sats.generate_random_sat(1000, 25, 3)

    print("Solving...")
    keys = three_sat(problem)
    print(problem)
    print("---")
    print(keys[0])

    # Sanity check
    for key in keys:
        assert sats.evaluate(problem, key)
