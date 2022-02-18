#include "dimacs.hpp"

class dpll
{
private:
	// local variables
	set<int> model;
	dimacs cnf;

	// to check if a literal guess is true
	bool test_literal(int literal)
	{
		dimacs d = dimacs(cnf);
		d.singleton_propagation(literal);
		dpll dpll_test = dpll(d);
		bool sat = dpll_test.solve();
		if (sat == true)
		{
			model.insert(literal);
			for (auto lit : dpll_test.get_model())
				model.insert(lit);
		}
		return sat;
	}

public:
	// constructor
	dpll(dimacs d)
	{
		cnf = dimacs(d);
	}

	// solver function
	bool solve()
	{
		if (cnf.is_satisfiable())
			return true;
		if (cnf.is_unsatisfiable())
			return false;
		int literal = cnf.get_singleton();
		if (literal != 0)
		{
			model.insert(literal);
			cnf.singleton_propagation(literal);
			return solve();
		}
		literal = cnf.get_literal();
		if (literal != 0)
		{
			return test_literal(literal) or test_literal(-literal);
		}
		return false;
	}

	// get the model
	set<int> get_model()
	{
		return set<int>(model.begin(), model.end());
	}

	/*
	// print function for debugging
	void print()
	{
		cout << "Model ";
		for (auto literal : model)
			cout << literal << " ";
		cout << endl
			 << "CNF" << endl;
		cnf.print();
		cout << "-----------\n";
	}
	*/
};
