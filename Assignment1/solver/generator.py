from pysat.card import CardEnc, EncType
from pysat.solvers import Solver
import random

from cnf import get_pair_cnf
from util import sat_to_sudoku, hash_fn
from solver import pair_solver, sudoku_solver

# Get a filled sudoku pair based on grid
def get_filled_sudoku(k, grid):
    model, _ = pair_solver(k, grid[0], grid[1])
    grid = sat_to_sudoku(k, model)
    return grid


#  check satisfiablity of grid
def check_satisfiablity(k, grid, solver):
    x, _ = sudoku_solver(k, grid[0], grid[1], solver)
    return bool(x)


# generate sudoku from filled grid
def generate_sudoku(k, grid):
    n = k * k
    solver = get_generator_solver(k, grid)

    triplets = [(index, i, j) for i in range(n) for j in range(n) for index in range(2)]

    while len(triplets) > 0:
        index, i, j = random.choice(triplets)
        triplets.remove((index, i, j))

        x = grid[index][i][j]
        grid[index][i][j] = 0

        if check_satisfiablity(k, grid, solver):
            grid[index][i][j] = x
    return grid


# A extention of the solver pair such that it doesn't give original grid
def get_generator_solver(k, grid):
    # Get the cnf of normal sudoku pair
    cnf = get_pair_cnf(k, grid[0], grid[1])
    n = k * k
    lst = []

    # atleast one of the new grid should be diffrent from the original grid
    for index in range(2):
        for i in range(n):
            for j in range(n):
                lst.append(-hash_fn(k, index, i, j, grid[index][i][j]))
    cnf.extend(CardEnc.atleast(lits=lst, bound=1, encoding=EncType.pairwise))

    # generate a solver on given cnf
    solver = Solver(use_timer=True)
    solver.append_formula(cnf.clauses)
    return solver
