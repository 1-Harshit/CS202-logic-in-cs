from util.hash import rev_hash_fn
import random


def sat_to_sudoku(k, solved):
    res = []
    n = k * k
    if solved is not None:
        res = [[[0 for _ in range(n)] for _ in range(n)] for _ in range(2)]
        for x in solved:
            if x > 0:
                index, i, j, t = rev_hash_fn(k, x)
                res[index][i][j] = t
        # pprint(res[0])
        # pprint(res[1])
    else:
        print("No Solution")
    return res


def get_random_grid(n):
    # initialize a random sudoku
    grid = [[[0 for _ in range(n)] for _ in range(n)] for _ in range(2)]
    pairs = [(i, j) for i in range(n) for j in range(n)]
    t_list = [i for i in range(1, random.randint(1, n) + 1)]
    while len(t_list) > 0:
        i, j = random.choice(pairs)
        pairs.remove((i, j))

        index = random.randint(0, 1)

        t = random.choice(t_list)
        grid[index][i][j] = t
        t_list.remove(t)
    return grid
