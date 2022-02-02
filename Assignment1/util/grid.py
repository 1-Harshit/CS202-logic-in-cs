# Preety print the grid
def pretty_print(k, grid):
    # print sudoku
    print_sudoku(k, grid[0])
    print("-" * (k * k * 3 + 3))
    print_sudoku(k, grid[1])


# print sudoku
def print_sudoku(k, grid):
    n = k * k
    for i in range(n):
        for j in range(n):
            seperator = "  " if ((j + 1) % k == 0 and j != n - 1) else " "
            print("{:2}".format(grid[i][j]), end=seperator)
        print()
        if (i + 1) % k == 0 and i != n - 1:
            print()
