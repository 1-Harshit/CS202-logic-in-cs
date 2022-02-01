from cnf.sudoku import get_pair_cnf
from util.parse import sat_to_sudoku
from solver.check_satisfiablity import check_satisfiablity
from solver.solver import sudoku_solver

from pysat.solvers import Solver
import random


def get_filled_sudoku(k, cnf, grid):
    solver = Solver()
    solver.append_formula(cnf.clauses)

    # solve the sudoku
    model, _ = sudoku_solver(k, grid, grid, solver)

    grid = sat_to_sudoku(k, model)[0]
    return grid


def generate_sudoku(k, n, cnf, grid):
    sudoku = grid
    pairs = [(i, j) for i in range(n) for j in range(n)]
    while len(pairs) > 0:
        i, j = random.choice(pairs)
        pairs.remove((i, j))

        x = sudoku[i][j]
        sudoku[i][j] = 0

        cnf_pair = get_pair_cnf(k, sudoku)
        satisfiable, _ = check_satisfiablity(k, sudoku, cnf_pair, cnf)
        if satisfiable:
            sudoku[i][j] = x
    return sudoku
