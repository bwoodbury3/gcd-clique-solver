from algos import clique1, clique2, three_sat1, three_sat2

clique_solvers = {
    "clique1": clique1.solve,
    "clique2": clique2.solve,
}
"""
Clique solver algorithms.
"""

sat_solvers = {
    "3-sat1": three_sat1.solve,
    "3-sat2": three_sat2.solve,
}
"""
3-SAT solver algorithms.
"""
