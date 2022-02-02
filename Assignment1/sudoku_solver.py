from util import get_solver_options, read_file, write_file, sat_to_sudoku, pretty_print
from solver import pair_solver

"""
	Driver Code
"""

# driver code for sudoku pair solver
def solver_main():
    k, file_path, output_file_path = get_solver_options()

    # Read the file
    sudoku1, sudoku2 = read_file(k, file_path)

    # Solve the sudoku
    solved, time = pair_solver(k, sudoku1, sudoku2)

    # parse the solved sudoku
    res = sat_to_sudoku(k, solved)

    # pretty print the solved sudoku
    pretty_print(k, res)

    # print to a file
    write_file(k, output_file_path, res)
    print("Ouput written to: ./" + output_file_path)

    # print the time taken
    print("Time: {} seconds".format(time))


if __name__ == "__main__":
    solver_main()
