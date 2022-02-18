#!/usr/bin/bash

# read a filename
filename=$1

# check if file exists
if [ -f $filename ]
then
	echo "Compiling..."
else
	echo "File does not exist"
fi

# compile the cpp file
g++ -std=c++11 *.hpp CNFsolver.cpp -o solver

# run the solver
echo "Running..."
./solver $filename

# remove the executable
rm ./solver
