from pprint import pprint
from util import get_solver_options, read_file, sat_to_sudoku
from solver import pair_solver

"""
	Driver Code
"""


def solver_main():
    k, file_path = get_solver_options()

    # Read the file
    sudoku1, sudoku2 = read_file(k, file_path)

    solved, time = pair_solver(k, sudoku1, sudoku2)

    res = sat_to_sudoku(k, solved)

    pprint(res)

    print("Time: ", time)


if __name__ == "__main__":
    solver_main()
