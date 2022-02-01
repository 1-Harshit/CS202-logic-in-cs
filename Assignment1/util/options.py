import sys

"""
	Get k and file path from options
"""

# Get k from options


def get_generator_options():
    options = sys.argv
    if len(options) != 2:
        print("Usage: python3 soduku_generator.py <k>")
        exit(1)
    try:
        k = int(options[1])
    except:
        print("Usage: python3 soduku_generator.py <k>")
        exit(1)
    return k


# Get k and file path from options


def get_solver_options():
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
