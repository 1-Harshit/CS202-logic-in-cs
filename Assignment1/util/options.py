import sys

"""
	Get k and file path from options
"""

# Get k from options
def get_generator_options():
    output_file_path = "generator_output.csv"
    options = sys.argv
    if len(options) < 2:
        print("Usage: python3 soduku_generator.py <k> [<output_file_path>]")
        exit(1)
    try:
        k = int(options[1])
    except:
        print("Usage: python3 soduku_generator.py <k> [<output_file_path>]")
        exit(1)
    try:
        output_file_path = options[2]
    except:
        pass
    return k, output_file_path


# Get k and file path from options
def get_solver_options():
    output_file_path = "solver_output.csv"
    options = sys.argv
    if len(options) < 3:
        print("Usage: python3 soduku_sat.py <k> <input_file_path> [<output_file_path>]")
        exit(1)
    try:
        k = int(options[1])
    except:
        print("Usage: python3 soduku_sat.py <k> <input_file_path> [<output_file_path>]")
        exit(1)
    input_file_path = options[2]
    try:
        output_file_path = options[3]
    except:
        pass
    return k, input_file_path, output_file_path
