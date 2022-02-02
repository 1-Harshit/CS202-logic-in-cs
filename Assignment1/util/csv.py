import csv

# Read grid from csv file
def read_file(k, filepath):
    with open(filepath, "r") as f:
        reader = csv.reader(f)
        grid = list(reader)
        grid = [list(map(int, row)) for row in grid]
        return grid[: k * k], grid[k * k :]

# Write grid to csv file
def write_file(k, filepath, grid):
    with open(filepath, "w") as f:
        writer = csv.writer(f)
        writer.writerows(grid[0])
        writer.writerows(grid[1])
