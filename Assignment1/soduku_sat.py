from pprint import pprint
from pysat.formula import CNF
from pysat.solvers import Solver

k = 3

""" 
	maps (i,j,t) to a unique integer
	i,j are the indices of the grid
	t is the value of the cell
"""
def hash_fn(index: int, i: int, j: int, t: int)-> int:
	ksq = k**2 + 1
	return index*(ksq**3) + i*(ksq**2) + j*ksq + t

def rev_hash_fn(hash_value: int)-> tuple[int, int, int, int]:
	ksq = k**2 + 1
	index = hash_value // (ksq**3)
	hash_value = hash_value % (ksq**3)
	i = hash_value // (ksq**2)
	hash_value = hash_value % (ksq**2)
	j = hash_value // ksq
	t = hash_value % ksq
	return index, i, j, t

""" 
	Driver Code
"""
def main():
	global k
	k = 3
	n = k*k
	sudoku1 = [
            [0, 0, 7, 0, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 8, 0, 0, 6],
            [0, 4, 1, 0, 0, 0, 9, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 7, 0],
            [0, 0, 0, 0, 0, 6, 0, 0, 0],
            [0, 0, 8, 7, 0, 0, 2, 0, 0],
            [3, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 2, 0, 0, 0, 0],
            [8, 6, 0, 0, 7, 0, 0, 0, 5]
        ]
	# sudoku2 = [
    #         [0, 0, 7, 0, 4, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 8, 0, 0, 6],
    #         [0, 4, 1, 0, 0, 0, 9, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 1, 7, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 8, 7, 0, 0, 2, 0, 0],
    #         [3, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 1, 2, 0, 0, 0, 0],
    #         [8, 6, 0, 0, 7, 0, 0, 0, 5]
    #     ]
	sudoku2 = list(sudoku1)
	
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
				cnf.append([hash_fn(0, i+x, j+y, t) for x in range(k) for y in range(k)])
				cnf.append([hash_fn(1, i+x, j+y, t) for x in range(k) for y in range(k)])
	
	# add clauses for pair suduko
	for i in range(n):
		for j in range(n):
			if sudoku1[i][j] == 0:
				for t in range(1, n+1):
					cnf.append([-hash_fn(0, i, j, t), -hash_fn(1, i, j, t)])
			if sudoku2[i][j] == 0:
				for t in range(1, n+1):
					cnf.append([-hash_fn(0, i, j, t), -hash_fn(1, i, j, t)])

	# Assumptions
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
	solve = Solver()
	solve.append_formula(cnf.clauses)
	solved = solve.solve(assumptions=assumptions)
	print(solved)

	if solved:
		model = solve.get_model()
		for x in model:
			if x > 0:
				index, i, j, t = rev_hash_fn(x)
				if index == 0:
					sudoku1[i][j] = t
				else:
					sudoku2[i][j] = t
		pprint(sudoku1)
		pprint(sudoku2)
	else:
		print("No Solution")

	
	s =[]

if __name__ == '__main__':
	main()