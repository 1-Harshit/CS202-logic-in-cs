from util.hash import hash_fn
from cnf.sudoku import get_pair_cnf
from util.parse import sat_to_sudoku
from solver.check_satisfiablity import check_satisfiablity
from pysat.card import CardEnc, EncType
from solver.solver import pair_solver, sudoku_solver

from pysat.solvers import Solver
import random


def get_filled_sudoku(k, grid):
    model, _ = pair_solver(k, grid[0], grid[1])
    grid = sat_to_sudoku(k, model)
    return grid


def generate_sudoku(k, grid):
    cnf = get_pair_cnf(k, grid[0], grid[1])
    n = k * k
    lst = []
    for index in range(2):
        for i in range(n):
            for j in range(n):
                lst.append(-hash_fn(k, index, i, j, grid[index][i][j]))
    cnf.extend(CardEnc.atleast(lits=lst, bound=1, encoding=EncType.pairwise))

    solver = Solver(use_timer=True)
    solver.append_formula(cnf.clauses)

    triplets = [(index, i, j) for i in range(n) for j in range(n) for index in range(2)]
    while len(triplets) > 0:
        index, i, j = random.choice(triplets)
        triplets.remove((index, i, j))

        x = grid[index][i][j]
        grid[index][i][j] = 0

        if check_satisfiablity(k, grid, solver):
            grid[index][i][j] = x
    return grid
