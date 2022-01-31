from pprint import pprint
from unicodedata import name

from sudoku_solver import *
from sudoku_solver import solve_sudoku as ss
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver
from pysat.formula import CNFPlus


import random
import sys


def get_generator_options():
	options = sys.argv
	if len(options) != 2:
		print("Usage: python3 soduku_generator.py <k>")
		exit(1)
	try:
		k = int(options[1])
	except:
		print("Usage: python3 soduku_generator.py <k>")
		exit(1)
	return k


def main():
	k = get_generator_options()
	n = k*k
	cnf = sudoku_cnf(k)
	solver = Solver()
	solver.append_formula(cnf.clauses)

	grid = get_random_grid(n)

	# solve the sudoku
	model, _ = solve_sudoku(k, grid, grid, solver)

	grid = sat_to_sudoku(k, model)[0]
	pprint(grid)
	pairs = [(i, j) for i in range(n) for j in range(n)]
	while len(pairs)>0:
		i,j = random.choice(pairs)
		pairs.remove((i,j))
		print("i,j:", i, j)
		x = grid[i][j]
		print("x:", x)
		grid[i][j] = 0

		cnf_pair = get_pair_cnf(k, grid)
		satisfiable, _ = check_satisfiablity(k, grid, cnf_pair, cnf)
		if satisfiable:
			grid[i][j] = x
			pprint(grid)

	pprint(grid)


def check_satisfiablity(k, sudoku1, cnf1, cnf2):
    n = k*k
    solver = Solver(use_timer=True)
    solver.append_formula(cnf1.clauses)
    solver.append_formula(cnf2.clauses)

    # Assumptions, form the existing sudokus
    assumptions = []
    for i in range(n):
        for j in range(n):
            if sudoku1[i][j] != 0:
                for t in range(1, n+1):
                    if sudoku1[i][j] == t:
                        assumptions.append(hash_fn(k, 0, i, j, t))
                        assumptions.append(hash_fn(k, 1, i, j, t))
                    else:
                        assumptions.append(-hash_fn(k, 0, i, j, t))
                        assumptions.append(-hash_fn(k, 1, i, j, t))

    return solver.solve(assumptions=assumptions), solver.time_accum()
    


def get_random_grid(n):
    # initialize a random sudoku
    grid = [[0 for _ in range(n)] for _ in range(n)]
    t_list = [i for i in range(1, random.randint(1,n)+1)]
    while len(t_list)>0:
     i = random.randint(0, n-1)
     j = random.randint(0, n-1)
     if grid[i][j] == 0:
      t = random.choice(t_list)
      grid[i][j] = t
      t_list.remove(t)
    return grid
	


def get_pair_cnf(k, sudoku):
	n = k*k
	cnf = CNFPlus()

	# add clauses for pair suduko
	for i in range(n):
		for j in range(n):
			if sudoku[i][j] == 0:
				for t in range(1, n+1):
					lst = []
					lst.append(hash_fn(k, 0, i, j, t))
					lst.append(hash_fn(k, 1, i, j, t))
					cnf.extend(CardEnc.atmost(
						lits=lst, bound=1, encoding=EncType.pairwise))

	return cnf

if __name__ == "__main__":
	main()
