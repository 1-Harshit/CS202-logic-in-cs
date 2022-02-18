# cs202-logic-in-computer-science Assignment 2
Assignment 2 submission of CS202 offered in the semester 2021-22-II IIT Kanpur

## CNF-SAT Solver
Given a CNF formula, this program will find a satisfying assignment for the formula. If not satisfying assignment is found, it will print "UNSAT"

## how to run the program
You can simply use the shell script file as follows:
```bash
./run.sh <path-to-test-case-file>
```
or you can run the program directly:
```bash
# compile the cpp file
g++ -std=c++11 *.hpp CNFsolver.cpp -o solver

# run the solver
./solver <path-to-test-case-file>
```

## Test cases
- There are test cases in the `testcases` folder
- to use test cases run the following, example usage:
```bash
./run.sh testcases/uf20-01.cnf
```

## Report
Detailed report is available in the `report.pdf` file

## Collaborator
- Harshit Raj 200433
- Shubhan R 200971
