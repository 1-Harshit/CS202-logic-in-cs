from pysat.solvers import Solver

from cnf import get_pair_cnf
from util import hash_fn

# solve sudoku pair
def pair_solver(k, sudoku1, sudoku2):
    cnf = get_pair_cnf(k, sudoku1, sudoku2)
    solve = Solver(use_timer=True)
    solve.append_formula(cnf.clauses)
    return sudoku_solver(k, sudoku1, sudoku2, solve)


# solve given sudoku using the solver
def sudoku_solver(k, sudoku1, sudoku2, solver):
    n = k * k

    # Assumptions, form the existing sudokus
    assumptions = []
    for i in range(n):
        for j in range(n):
            if sudoku1[i][j] != 0 and sudoku2[i][j] == 0:
                for t in range(1, n + 1):
                    if sudoku1[i][j] == t:
                        assumptions.append(hash_fn(k, 0, i, j, t))
            if sudoku1[i][j] == 0 and sudoku2[i][j] != 0:
                for t in range(1, n + 1):
                    if sudoku2[i][j] == t:
                        assumptions.append(hash_fn(k, 1, i, j, t))
            if sudoku1[i][j] != 0 and sudoku2[i][j] != 0:
                if sudoku1[i][j] == sudoku2[i][j]:
                    print("This set of sudokus cannot form a sudoku pair. Try again :)")
                    exit(1)
                else:
                    assumptions.append(hash_fn(k, 0, i, j, sudoku1[i][j]))
                    assumptions.append(hash_fn(k, 1, i, j, sudoku2[i][j]))

    # Solve the sudoku
    solver.solve(assumptions=assumptions)
    return solver.get_model(), solver.time_accum()
