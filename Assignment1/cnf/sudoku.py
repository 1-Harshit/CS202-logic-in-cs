# Normal Sudoku cnf
from util.hash import hash_fn
from pysat.formula import CNFPlus
from pysat.card import CardEnc, EncType


def sudoku_cnf(k):
    n = k * k
    cnf = CNFPlus()

    # # add clauses for each cell has exactly one value
    for i in range(n):
        for j in range(n):
            lst1 = []
            lst2 = []
            for t in range(1, n + 1):
                lst1.append(hash_fn(k, 0, i, j, t))
                lst2.append(hash_fn(k, 1, i, j, t))
            cnf.extend(CardEnc.equals(lits=lst1, bound=1, encoding=EncType.pairwise))
            cnf.extend(CardEnc.equals(lits=lst2, bound=1, encoding=EncType.pairwise))

    # add clauses for each row has all values
    for i in range(n):
        for t in range(1, n + 1):
            lst1 = []
            lst2 = []
            for j in range(n):
                lst1.append(hash_fn(k, 0, i, j, t))
                lst2.append(hash_fn(k, 1, i, j, t))
            cnf.extend(CardEnc.equals(lits=lst1, bound=1, encoding=EncType.pairwise))
            cnf.extend(CardEnc.equals(lits=lst2, bound=1, encoding=EncType.pairwise))

    # add clauses for each column has all values
    for j in range(n):
        for t in range(1, n + 1):
            lst1 = []
            lst2 = []
            for i in range(n):
                lst1.append(hash_fn(k, 0, i, j, t))
                lst2.append(hash_fn(k, 1, i, j, t))
            cnf.extend(CardEnc.equals(lits=lst1, bound=1, encoding=EncType.pairwise))
            cnf.extend(CardEnc.equals(lits=lst2, bound=1, encoding=EncType.pairwise))

    # add clauses for each subgrid has all values
    for i in range(0, n, k):
        for j in range(0, n, k):
            for t in range(1, n + 1):
                lst1 = []
                lst2 = []
                for l in range(k):
                    for m in range(k):
                        lst1.append(hash_fn(k, 0, i + l, j + m, t))
                        lst2.append(hash_fn(k, 1, i + l, j + m, t))
                cnf.extend(
                    CardEnc.equals(lits=lst1, bound=1, encoding=EncType.pairwise)
                )
                cnf.extend(
                    CardEnc.equals(lits=lst2, bound=1, encoding=EncType.pairwise)
                )

    return cnf


def get_pair_cnf(k, sudoku):
    n = k * k
    cnf = CNFPlus()

    # add clauses for pair suduko
    for i in range(n):
        for j in range(n):
            if sudoku[i][j] == 0:
                for t in range(1, n + 1):
                    lst = [hash_fn(k, 0, i, j, t), hash_fn(k, 1, i, j, t)]
                    cnf.extend(
                        CardEnc.atmost(lits=lst, bound=1, encoding=EncType.pairwise)
                    )

    return cnf
