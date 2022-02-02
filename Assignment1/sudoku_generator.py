from util import get_generator_options, get_random_grid, pretty_print
from solver import get_filled_sudoku, generate_sudoku

# Driver code for sudoku pair generator
def generator_main():
    k = get_generator_options()
    grid = get_random_grid(k * k)
    grid = get_filled_sudoku(k, grid)
    # pretty_print(k, grid)
    x = generate_sudoku(k, grid)

    pretty_print(k, x)


if __name__ == "__main__":
    generator_main()
