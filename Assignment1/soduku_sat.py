from pprint import pprint
import sys
from pysat.formula import CNF
from pysat.solvers import Solver
import csv

k = 3

"""
	maps (i,j,t) to a unique integer
	i,j are the indices of the grid
	t is the value of the cell
"""


def hash_fn(index: int, i: int, j: int, t: int) -> int:
    ksq = k**2 + 1
    return index*(ksq**3) + i*(ksq**2) + j*ksq + t


def rev_hash_fn(hash_value: int) -> tuple[int, int, int, int]:
    ksq = k**2 + 1
    index = hash_value // (ksq**3)
    hash_value = hash_value % (ksq**3)
    i = hash_value // (ksq**2)
    hash_value = hash_value % (ksq**2)
    j = hash_value // ksq
    t = hash_value % ksq
    return index, i, j, t


def read_file(filepath: str) -> tuple[list, list]:
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        grid = list(reader)
        grid = [list(map(int, row)) for row in grid]
        return grid[:9], grid[9:]


"""
	Get k and file path from options
"""


def get_options() -> tuple[int, str]:
    options = sys.argv
    if len(options) != 3:
        print("Usage: python3 soduku_sat.py <k> <file_path>")
        exit(1)
    try:
        k = int(options[1])
    except:
        print("Usage: python3 soduku_sat.py <k> <file_path>")
        exit(1)
    file_path = options[2]
    return k, file_path


"""
	Driver Code
"""


def main():
    global k
    k, file_path = get_options()
    n = k*k

    # Read the file
    sudoku1, sudoku2 = read_file(file_path)

    cnf = CNF()

    # add clauses for each cell has atleast one value
    for i in range(n):
        for j in range(n):
            cnf.append([hash_fn(0, i, j, t) for t in range(1, n+1)])
            cnf.append([hash_fn(1, i, j, t) for t in range(1, n+1)])

    # add clauses for each cell has atmost one value
    for i in range(n):
        for j in range(n):
            for t1 in range(1, n+1):
                for t2 in range(t1+1, n+1):
                    cnf.append([-hash_fn(0, i, j, t1), -hash_fn(0, i, j, t2)])
                    cnf.append([-hash_fn(1, i, j, t1), -hash_fn(1, i, j, t2)])

    # add clauses for each row has all values
    for i in range(n):
        for t in range(1, n+1):
            cnf.append([hash_fn(0, i, j, t) for j in range(n)])
            cnf.append([hash_fn(1, i, j, t) for j in range(n)])

    # add clauses for each column has all values
    for j in range(n):
        for t in range(1, n+1):
            cnf.append([hash_fn(0, i, j, t) for i in range(n)])
            cnf.append([hash_fn(1, i, j, t) for i in range(n)])

    # add clauses for each subgrid has all values
    for i in range(0, n, k):
        for j in range(0, n, k):
            for t in range(1, n+1):
                cnf.append([hash_fn(0, i+x, j+y, t)
                            for x in range(k) for y in range(k)])
                cnf.append([hash_fn(1, i+x, j+y, t)
                            for x in range(k) for y in range(k)])

    # add clauses for pair suduko
    for i in range(n):
        for j in range(n):
            if sudoku1[i][j] == 0:
                for t in range(1, n+1):
                    cnf.append([-hash_fn(0, i, j, t), -hash_fn(1, i, j, t)])
            elif sudoku2[i][j] == 0:
                for t in range(1, n+1):
                    cnf.append([-hash_fn(0, i, j, t), -hash_fn(1, i, j, t)])

    # Assumptions, form the existing sudokus
    assumptions = []
    for i in range(n):
        for j in range(n):
            if sudoku1[i][j] != 0:
                for t in range(1, n+1):
                    if sudoku1[i][j] == t:
                        assumptions.append(hash_fn(0, i, j, t))
                    else:
                        assumptions.append(-hash_fn(0, i, j, t))
            if sudoku2[i][j] != 0:
                for t in range(1, n+1):
                    if sudoku2[i][j] == t:
                        assumptions.append(hash_fn(1, i, j, t))
                    else:
                        assumptions.append(-hash_fn(1, i, j, t))

    # Solve the sudoku
    solve = Solver()
    solve.append_formula(cnf.clauses)
    solved = solve.solve(assumptions=assumptions)

    if solved:
        model = solve.get_model()
        res = [[[0 for _ in range(n)] for _ in range(n)] for _ in range(2)]
        for x in model:
            if x > 0:
                index, i, j, t = rev_hash_fn(x)
                res[index][i][j] = t
        pprint(res[0])
        pprint(res[1])
    else:
        print("No Solution")


if __name__ == '__main__':
    main()
