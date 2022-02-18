#include <iostream>
#include "dpll.hpp"
using namespace std;

int main()
{
	dimacs d("test.cnf");
	d.scan();

	dpll solver(d);
	bool sat = solver.solve();

	cout << sat << endl;
	if (sat)
	{
		for (auto x : solver.get_model())
			cout << x << " ";
		cout << endl;
	}

	return 0;
}
