#include <iostream>
#include "dpll.hpp"
using namespace std;

int main(int argc, char *argv[])
{
	string filename;

	if(argc != 2){
		cout << "usage: ./a.out <filename>" << endl;
		return 1;
	}

	filename = argv[1];

	dimacs d(filename);
	d.scan();

	dpll solver(d);
	bool sat = solver.solve();

	cout << (sat ? "SAT" : "UNSAT") << endl;
	if (sat)
	{
		for (auto x : solver.get_model())
			cout << x << " ";
		cout << endl;
	}

	return 0;
}
