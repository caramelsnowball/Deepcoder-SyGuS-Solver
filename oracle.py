import random
from intexp import Const

def query(constraint_list, candidate_expression, var_name_list, candidate_name):
	# just a stand-in for an actual SMT solver – this "oracle" simply tests
	# 900 randomly generated points against the proposed solution and constraints
	varmap = {}
	varmap[candidate_name] = candidate_expression
	for i in range(30): 
		for j in range(30):
			for var_name in var_name_list:
				# create a random assignment of variables
				varmap[var_name] = Const(random.randint(-i, i))
			if not check(constraint_list, varmap):
				# return the point that broke it
				return varmap
	return None


def check(constraint_list, varmap):
	for constraint in constraint_list:
		if not constraint.execute(varmap):
			return False
	return True
