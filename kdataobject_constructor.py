class KDoConstructor:
	def __init__(self, className):
		self.class_name = className

	def _init_type_value(self, tab_level, var):
		if 'SystemKey' in var.name:
			return '	' * tab_level + var.name + '("489DA7EA-46E8-467D-951D-092593943C01")' + ',\n'
		if var.type == 'string':
			return '	' * tab_level + var.name + '("' + self.class_name + '_' + var.name + '")' + ',\n'
		elif var.type == 'double' or var.type == 'float':
			return '	' * tab_level + var.name + '(' + '0.0' + ')' + ',\n'
		elif 'int' in var.type: #unsigned int or int
			return '	' * tab_level + var.name + '(' + '1' + ')' + ',\n'
		else:
			return ''

	def _init_var(self, tab_level, var_list):
		code = ':\n'
		#print(self.class_name)
		for var in var_list:

			code += self._init_type_value(tab_level, var)
		code = code[0:len(code)-2] + '\n' + '	' * tab_level
		return code

	def dotHCode(self, tab_level):
		code = '	' * tab_level + self.class_name
		code += '();'
		return code + '\n'

	def dotFullHCode(self, tab_level, var_list):
		code = self.dotHCode(tab_level)
		code = code[0:code.index(';')]

		if len(var_list) > 0:
			code += self._init_var(1, var_list) + '{}'
		else:
			code += ';'

		return code + '\n\n'

	def dotCppCode(self, tab_level, var_list, ref_list):
		#code = self.dotHCode()
		code = self.dotHCode(tab_level)

		code = self.class_name + '::' + code[0:code.index(';')]
		code += self._init_var(0, var_list)
		code += '{\n'
		code += '	' * (tab_level+1) + 'KDataPersistentObject::cv_SystemKey = "489DA7EA-46E8-467D-951D-092593943C01";\n'

		for ref_init in ref_list:
			code += '	' * (tab_level+1) + ref_init + '\n'

		code += '	' * (tab_level+1) + 'cv_ClassName = "' + self.class_name[len('KDo'):len(self.class_name)] + '";\n'
		code += '}'
		return code
