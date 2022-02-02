from util import get_generator_options, get_random_grid, pretty_print, write_file
from solver import get_filled_sudoku, generate_sudoku

# Driver code for sudoku pair generator
def generator_main():
    # Get the options
    k, output_file_path = get_generator_options()

    # Generate a random grid
    grid = get_random_grid(k * k)

    # Generate a filled sudoku
    grid = get_filled_sudoku(k, grid)

    # # Uncomment to print the key
    # # save the solved grid
    # write_file(k, output_file_path+".key", grid)

    # generate a sudoku pair
    x = generate_sudoku(k, grid)

    # pretty print the sudoku pair
    pretty_print(k, x)

    # print to a file
    write_file(k, output_file_path, x)
    print("\nOuput written to: ./" + output_file_path)


if __name__ == "__main__":
    generator_main()
