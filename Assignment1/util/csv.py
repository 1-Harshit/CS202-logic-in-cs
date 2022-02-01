import csv


def read_file(k, filepath):
    with open(filepath, "r") as f:
        reader = csv.reader(f)
        grid = list(reader)
        grid = [list(map(int, row)) for row in grid]
        return grid[: k * k], grid[k * k :]


def write_file(k, filepath, sudoku1, sudoku2):
    with open(filepath, "w") as f:
        writer = csv.writer(f)
        writer.writerows(sudoku1)
        writer.writerows(sudoku2)
