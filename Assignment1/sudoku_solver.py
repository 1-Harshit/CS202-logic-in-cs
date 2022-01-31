from pprint import pprint
import sys
from pysat.formula import CNFPlus
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType
import csv


"""
	maps (i,j,t) to a unique integer
	i,j are the indices of the grid
	t is the value of the cell
"""


def hash_fn(k, index, i, j, t):
    ksq = k**2 + 1
    return index*(ksq**3) + i*(ksq**2) + j*ksq + t


def rev_hash_fn(k, hash_value):
    ksq = k**2 + 1
    index = hash_value // (ksq**3)
    hash_value = hash_value % (ksq**3)
    i = hash_value // (ksq**2)
    hash_value = hash_value % (ksq**2)
    j = hash_value // ksq
    t = hash_value % ksq
    return index, i, j, t


def read_file(k, filepath):
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        grid = list(reader)
        grid = [list(map(int, row)) for row in grid]
        return grid[:k*k], grid[k*k:]


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
    k, file_path = get_options()
    n = k*k

    # Read the file
    sudoku1, sudoku2 = read_file(k, file_path)

    solved, time = pair_solver(k, sudoku1, sudoku2)

    sat_to_sudoku(k, solved)
    print("Time: ", time)


def sat_to_sudoku(k, solved):
    n= k*k
    if solved is not None:
        res = [[[0 for _ in range(n)] for _ in range(n)] for _ in range(2)]
        for x in solved:
            if x > 0:
                index, i, j, t = rev_hash_fn(k, x)
                res[index][i][j] = t
        pprint(res[0])
        pprint(res[1])
    else:
        print("No Solution")
    return res


def pair_solver(k, sudoku1, sudoku2):
    n =k*k
    cnf = sudoku_cnf(k)

    # add clauses for pair suduko
    for i in range(n):
        for j in range(n):
            if(sudoku1[i][j] == 0 or sudoku2[i][j] == 0):
                for t in range(1, n+1):
                    lst = []
                    lst.append(hash_fn(k, 0, i, j, t))
                    lst.append(hash_fn(k, 1, i, j, t))
                    cnf.extend(CardEnc.atmost(
                        lits=lst, bound=1, encoding=EncType.pairwise))


    solve = Solver(use_timer=True)
    solve.append_formula(cnf.clauses)
    
    
    return solve_sudoku(k, sudoku1, sudoku2, solve)

def solve_sudoku(k, sudoku1, sudoku2, solver):
    n = k*k

    # Assumptions, form the existing sudokus
    assumptions = []
    for i in range(n):
        for j in range(n):
            if sudoku1[i][j] != 0:
                for t in range(1, n+1):
                    if sudoku1[i][j] == t:
                        assumptions.append(hash_fn(k, 0, i, j, t))
                    else:
                        assumptions.append(-hash_fn(k, 0, i, j, t))
            if sudoku2[i][j] != 0:
                for t in range(1, n+1):
                    if sudoku2[i][j] == t:
                        assumptions.append(hash_fn(k, 1, i, j, t))
                    else:
                        assumptions.append(-hash_fn(k, 1, i, j, t))

    # Solve the sudoku
    solver.solve(assumptions=assumptions)
    return solver.get_model(), solver.time_accum()

def sudoku_cnf(k):
    n=k*k
    cnf = CNFPlus()

    # # add clauses for each cell has exactly one value
    for i in range(n):
        for j in range(n):
            lst1 = []
            lst2 = []
            for t in range(1, n+1):
                lst1.append(hash_fn(k, 0, i, j, t))
                lst2.append(hash_fn(k, 1, i, j, t))
            cnf.extend(CardEnc.equals(
                lits=lst1, bound=1, encoding=EncType.pairwise))
            cnf.extend(CardEnc.equals(
                lits=lst2, bound=1, encoding=EncType.pairwise))

    # add clauses for each row has all values
    for i in range(n):
        for t in range(1, n+1):
            lst1 = []
            lst2 = []
            for j in range(n):
                lst1.append(hash_fn(k, 0, i, j, t))
                lst2.append(hash_fn(k, 1, i, j, t))
            cnf.extend(CardEnc.equals(
                lits=lst1, bound=1, encoding=EncType.pairwise))
            cnf.extend(CardEnc.equals(
                lits=lst2, bound=1, encoding=EncType.pairwise))

    # add clauses for each column has all values
    for j in range(n):
        for t in range(1, n+1):
            lst1 = []
            lst2 = []
            for i in range(n):
                lst1.append(hash_fn(k, 0, i, j, t))
                lst2.append(hash_fn(k, 1, i, j, t))
            cnf.extend(CardEnc.equals(
                lits=lst1, bound=1, encoding=EncType.pairwise))
            cnf.extend(CardEnc.equals(
                lits=lst2, bound=1, encoding=EncType.pairwise))

    # add clauses for each subgrid has all values
    for i in range(0, n, k):
        for j in range(0, n, k):
            for t in range(1, n+1):
                lst1 = []
                lst2 = []
                for l in range(k):
                    for m in range(k):
                        lst1.append(hash_fn(k, 0, i+l, j+m, t))
                        lst2.append(hash_fn(k, 1, i+l, j+m, t))
                cnf.extend(CardEnc.equals(
                    lits=lst1, bound=1, encoding=EncType.pairwise))
                cnf.extend(CardEnc.equals(
                    lits=lst2, bound=1, encoding=EncType.pairwise))
                        
    return cnf


if __name__ == '__main__':
    main()
