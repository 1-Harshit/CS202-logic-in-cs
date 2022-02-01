from cnf import sudoku_cnf
from util import hash_fn, sat_to_sudoku
from pysat.solvers import Solver
from pysat.card import EncType, CardEnc


def pair_solver(k, sudoku1, sudoku2):
    n = k * k
    cnf = sudoku_cnf(k)

    # add clauses for pair suduko
    for i in range(n):
        for j in range(n):
            if sudoku1[i][j] == 0 or sudoku2[i][j] == 0:
                for t in range(1, n + 1):
                    lst = [hash_fn(k, 0, i, j, t), hash_fn(k, 1, i, j, t)]
                    cnf.extend(
                        CardEnc.atmost(lits=lst, bound=1, encoding=EncType.pairwise)
                    )

    solve = Solver(use_timer=True)
    solve.append_formula(cnf.clauses)

    return sudoku_solver(k, sudoku1, sudoku2, solve)


def sudoku_solver(k, sudoku1, sudoku2, solver):
    n = k * k

    # Assumptions, form the existing sudokus
    assumptions = []
    for i in range(n):
        for j in range(n):
            if sudoku1[i][j] != 0:
                for t in range(1, n + 1):
                    if sudoku1[i][j] == t:
                        assumptions.append(hash_fn(k, 0, i, j, t))
                    else:
                        assumptions.append(-hash_fn(k, 0, i, j, t))
            if sudoku2[i][j] != 0:
                for t in range(1, n + 1):
                    if sudoku2[i][j] == t:
                        assumptions.append(hash_fn(k, 1, i, j, t))
                    else:
                        assumptions.append(-hash_fn(k, 1, i, j, t))

    # Solve the sudoku
    solver.solve(assumptions=assumptions)
    return solver.get_model(), solver.time_accum()
