from pprint import pprint

from util import get_generator_options, get_random_grid
from cnf import sudoku_cnf, get_pair_cnf
from solver import get_filled_sudoku, check_satisfiablity, generate_sudoku
import random


def generator_main():
    k = get_generator_options()
    n = k * k
    cnf = sudoku_cnf(k)
    grid = get_random_grid(n)
    grid = get_filled_sudoku(k, cnf, grid)
    pprint(grid)
    x = generate_sudoku(k, n, cnf, grid)

    pprint(x)


if __name__ == "__main__":
    generator_main()
