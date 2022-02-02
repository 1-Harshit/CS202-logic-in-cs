from solver.solver import sudoku_solver
from util import hash_fn
from pysat.solvers import Solver


def check_satisfiablity(k, grid, solver):

    x, _ = sudoku_solver(k, grid[0], grid[1], solver)

    return bool(x)
