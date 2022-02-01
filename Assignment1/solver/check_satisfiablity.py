from util import hash_fn
from pysat.solvers import Solver


def check_satisfiablity(k, sudoku1, cnf1, cnf2):
    n = k * k
    solver = Solver()
    solver.append_formula(cnf1.clauses)
    solver.append_formula(cnf2.clauses)

    # Assumptions, form the existing sudokus
    assumptions = []
    for i in range(n):
        for j in range(n):
            if sudoku1[i][j] != 0:
                for t in range(1, n + 1):
                    if sudoku1[i][j] == t:
                        assumptions.append(hash_fn(k, 0, i, j, t))
                        assumptions.append(hash_fn(k, 1, i, j, t))
                    else:
                        assumptions.append(-hash_fn(k, 0, i, j, t))
                        assumptions.append(-hash_fn(k, 1, i, j, t))

    return bool(solver.solve(assumptions=assumptions))
