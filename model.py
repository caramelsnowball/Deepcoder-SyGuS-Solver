class Model:

	def __init__(self, constraint_list, int_var_name_list, function_name):
		self.constraint_list = constraint_list
		self.int_var_name_list = int_var_name_list
		self.function_name = function_name

	def get_var_names(self):
		return self.int_var_name_list

	def get_constraints(self):
		return self.constraint_list

	def get_function(self):
		return self.function_name