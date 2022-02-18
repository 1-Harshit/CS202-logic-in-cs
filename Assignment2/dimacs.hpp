#include <fstream>
#include <set>
#include <sstream>
#include <unordered_map>
using namespace std;

class dimacs
{
private:
	// A type for itterators
	typedef std::set<std::set<int>>::iterator set_it;

	// local variables
	int clauses_count, literal_count;
	string file_name;
	set<set<int>> clauses;

	// occurence of each literal
	unordered_map<int, int> literal_map;
	set<pair<int, int>, greater<pair<int, int>>> literal_count_map;

	// to remove a litteral from the set
	set_it prune_literal(set_it itr, int literal)
	{
		set<int> new_clause;
		for (auto itr2 = itr->begin(); itr2 != itr->end(); itr2++)
		{
			if (*itr2 != -literal)
			{
				new_clause.insert(*itr2);
			}
		}
		clauses.insert(new_clause);
		return clauses.erase(itr);
	}

	// set count
	void set_count(string line)
	{
		stringstream ss(line);
		string str;
		ss >> str;
		ss >> str;
		ss >> str;
		literal_count = stoi(str);
		ss >> str;
		clauses_count = stoi(str);
	}

public:
	// constructor
	dimacs()
	{
	}

	dimacs(string file_name)
	{
		this->file_name = file_name;
	}

	dimacs(const dimacs &other)
	{
		this->clauses_count = other.clauses_count;
		this->literal_count = other.literal_count;
		this->clauses = other.clauses;
		this->literal_map = other.literal_map;
		this->literal_count_map = other.literal_count_map;
	}

	// to scan the file
	void scan()
	{
		// read the file
		ifstream file(file_name);
		string line;
		while (getline(file, line))
		{
			if (line[0] == 'c')
				continue;
			else if (line[0] == 'p')
			{
				set_count(line);
				continue;
			}
			set<int> clause;
			stringstream ss(line);
			int literal;
			while (ss >> literal)
				if (literal != 0)
				{
					literal_map[literal]++;
					clause.insert(literal);
				}
			clauses.insert(clause);
		}
		file.close();

		// update the literal count map
		for (auto itr = literal_map.begin(); itr != literal_map.end(); itr++)
		{
			literal_count_map.insert(make_pair(itr->second, itr->first));
		}
	}

	// get a litteral to guess
	int get_literal()
	{
		int literal = literal_count_map.begin()->second;
		literal_count_map.erase(make_pair(literal_map[literal], literal));
		literal_count_map.erase(make_pair(literal_map[-literal], -literal));
		return literal;
	}

	// get a literal that can be deduced
	int get_singleton()
	{
		for (auto clause : clauses)
		{
			if (clause.size() == 1)
			{
				int literal = *clause.begin();
				literal_count_map.erase(make_pair(literal_map[literal], literal));
				literal_count_map.erase(make_pair(literal_map[-literal], -literal));
				return literal;
			}
		}
		return 0;
	}

	// update cnf after a judgement
	void singleton_propagation(int literal)
	{
		for (auto itr = clauses.begin(); itr != clauses.end();)
		{
			if (itr->find(literal) != itr->end())
				itr = clauses.erase(itr);
			else if (itr->find(-literal) != itr->end())
				itr = prune_literal(itr, literal);
			else
				itr++;
		}
	}

	// whether the cnf is satisfiable
	bool is_satisfiable()
	{
		return clauses.empty();
	}

	// whether the cnf is unsatisfiable
	bool is_unsatisfiable()
	{
		for (auto clause : clauses)
		{
			if (clause.size() == 0)
			{
				return true;
			}
		}
		return false;
	}

	/* 
	// print for debugging
	void print()
	{
		cout << "Clauses: " << clauses.size() << "/" << clauses_count << endl;
		cout << "Literals: " << literal_count << endl;
		for (auto clause : clauses)
		{
			for (auto literal : clause)
			{
				cout << literal << " ";
			}
			cout << endl;
		}
	} 
	*/
};
