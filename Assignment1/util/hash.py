"""
	maps (i,j,t) to a unique integer
	i,j are the indices of the grid
	t is the value of the cell
"""
# A hash function to map 3D coordinates to 1D index


def hash_fn(k, index, i, j, t):
    ksq = k ** 2 + 1
    return index * (ksq ** 3) + i * (ksq ** 2) + j * ksq + t


# Reverse hash function to map 1D index to 3D coordinates


def rev_hash_fn(k, hash_value):
    ksq = k ** 2 + 1
    index = hash_value // (ksq ** 3)
    hash_value = hash_value % (ksq ** 3)
    i = hash_value // (ksq ** 2)
    hash_value = hash_value % (ksq ** 2)
    j = hash_value // ksq
    t = hash_value % ksq
    return index, i, j, t
