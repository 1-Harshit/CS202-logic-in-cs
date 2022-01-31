from soduku_sat import *
import random


def get_k():
    options = sys.argv
    if len(options) != 2:
        print("Usage: python3 soduku_sat.py <k>")
        exit(1)
    try:
        k = int(options[1])
    except:
        print("Usage: python3 soduku_sat.py <k>")
        exit(1)
    return k


n = k*k
i = random.randint(0, n)
j = random.randint(0, n)
sodu
