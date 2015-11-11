class Parameter:
	def CovertType(self, type):
		if type == 'u4' or type == 'u8':
			return 'unsigned int'
		elif type == 'i4':
			return 'int'
		elif type == 'f4':
			return 'float'
		elif type == 'u8':
			return 'unsigned __int64'
		elif type == 'datetime':
			return 'KDateTime'
		else:
			return str(type)

	def __init__(self, type, name):
		self.name = name
		self.type = self.CovertType(type.lower())
	def __str__(self):
		return str(self.type) + ' ' + str(self.name) + ';'
	def dotHFieldStr(self):
		return 'static const string Field_' + str(self.name) + ';'
	def dotCppFieldStr(self, class_name):
		return 'const string ' + class_name + '::Field_' + str(self.name) + ' = "' + str(self.name) + '";'

	def GetType(self):
		return self.type
	def GetName(self):
		return self.name

class GetDoObjectFunction:
	def __init__(self, class_name, return_type, function_name, parameter_list):
		self.className = class_name
		self.returnType = return_type
		self.functionName = function_name
		self.parameterList = parameter_list

	def dotHCode(self, tab_level):
		code = 'static ' + self.returnType + ' ' + self.functionName + '('
		for parameter in self.parameterList:
			if ' =' in parameter.GetName():
				code += parameter.GetType() + ' ' + parameter.GetName()[0:parameter.GetName().index(' =')] + ', '
			else:
				code += parameter.GetType() + ' ' + parameter.GetName() + ', '
		if ', ' in code:
			code = code[0:len(code)-2] #remove ', '
		code += ');'
		return code

	def CppFunctionFilterHitMap(self, field_name):
		if field_name is 'ActiveFlag':
			return '((*it)[' + self.className + '::Field_' + field_name + '].empty() || (*it)[' + self.className + '::Field_' + field_name + '] == ' + '"1")'
		else:
			return '((*it)[' + self.className + '::Field_' + field_name + '].empty() || (*it)[' + self.className + '::Field_' + field_name + '] == "' + self.className + '_' + field_name + '")'

	def CppFunctionFilterHitMapList(self, field_name):
		if field_name is 'ActiveFlag':
			return '(m_Filter[' + self.className + '::Field_' + field_name + '].empty() || find(m_Filter[' + self.className + '::Field_' + field_name + '].begin(), m_Filter[' + self.className + '::Field_' + field_name + '].end(), "1") != m_Filter[' + self.className + '::Field_' + field_name + '].end())'
		else:
			return '(m_Filter[' + self.className + '::Field_' + field_name + '].empty() || find(m_Filter[' + self.className + '::Field_' + field_name + '].begin(), m_Filter[' + self.className + '::Field_' + field_name + '].end(), "' + self.className + '_' + field_name + '") != m_Filter[' + self.className + '::Field_' + field_name + '].end())'

	def HitMapList(self, tab_level, var_list, is_true_run_code):
		code =''
		code += '	' * tab_level + 'if ('
		if 'Id' in var_list:
			code += self.CppFunctionFilterHitMapList('Id')
			if 'ActiveFlag' in var_list:
				code += ' &&\n' + '	' * (tab_level+1)
		if 'ActiveFlag' in var_list:
			code += self.CppFunctionFilterHitMapList('ActiveFlag')
		code += ')\n'
		code += '	' * tab_level + '{\n'
		code += '	' * (tab_level+1) + is_true_run_code
		code += '	' * tab_level + '}\n'
		return code

	def HitListMap(self, tab_level, var_list, is_true_run_code):
		code =''
		code += '	' * tab_level + 'for (list< map<string, string> >::iterator it = m_Filter.begin(); it != m_Filter.end(); ++it)\n'
		code += '	' * tab_level + '{\n'
		tab_level += 1
		code += '	' * tab_level + 'if ('
		if 'Id' in var_list:
			code += self.CppFunctionFilterHitMap('Id')
			if 'ActiveFlag' in var_list:
				code += ' &&\n' + '	' * (tab_level+1)
		if 'ActiveFlag' in var_list:
			code += self.CppFunctionFilterHitMap('ActiveFlag')
		code += ')\n'
		code += '	' * tab_level + '{\n'
		tab_level += 1
		code += '	' * tab_level + is_true_run_code
		tab_level -= 1
		code += '	' * tab_level + '}\n'
		tab_level -= 1
		code += '	' * tab_level + '}\n'
		return code

	def HitMap(self, tab_level, var_list, is_true_run_code):
		code =''
		if 'Id' in var_list:
			code +=  '	' * tab_level + 'map<string, string>::iterator id_it = m_Filter.find(' + self.className + '::Field_Id);\n'
		if 'ActiveFlag' in var_list:
			code +=  '	' * tab_level + 'map<string, string>::iterator activeflag_it = m_Filter.find(' + self.className + '::Field_ActiveFlag);\n'

		code += '	' * tab_level + 'if ('
		if 'Id' in var_list:
			code += '(id_it != m_Filter.end() || id_it->second == "KDo' + self.className + '_Id")'
			if 'ActiveFlag' in var_list:
				code += ' &&\n' + '	' * (tab_level+1)
		if 'ActiveFlag' in var_list:
			code += '(activeflag_it != m_Filter.end() || activeflag_it->second == "1")'
		code += ')\n'
		code += '	' * tab_level + '{\n'
		code += '	' * (tab_level+1) + is_true_run_code
		code += '	' * tab_level + '}\n'
		return code

	def CppFunctionFilter(self, tab_level, member_list, is_true_run_code):
		code = ''
		var_list = []
		for var in member_list:
			var_list.append(var.GetName())
		if len(self.parameterList) != 0 and 'map<string, list<string> >' in self.parameterList[0].GetType():
			if 'Id' in var_list or 'ActiveFlag' in var_list:
				code += self.HitMapList(tab_level, var_list, is_true_run_code)
		elif len(self.parameterList) != 0 and 'list< map<string, string> >' in self.parameterList[0].GetType():
			if 'Id' in var_list or 'ActiveFlag' in var_list:
				code += self.HitListMap(tab_level, var_list, is_true_run_code)
		elif len(self.parameterList) != 0 and 'map<string, string>' in self.parameterList[0].GetType():
			if 'Id' in var_list or 'ActiveFlag' in var_list:
				code += self.HitMap(tab_level, var_list, is_true_run_code)
		else:
			code = '	' * tab_level + is_true_run_code
		return code


	def CppFunction(self, tab_level, member_list):
		code = ''
		if 'list' in self.returnType:  #回傳list<KDataObject*>
			code  = '	' * tab_level + self.returnType + ' curr_list;\n'
			code += self.CppFunctionFilter(tab_level, member_list, 'curr_list.push_back(new ' + self.className + '());\n')
			code += '	' * tab_level + 'return curr_list;\n'
		elif 'int' in self.returnType and '*' not in self.returnType: #回傳總數
			code = self.CppFunctionFilter(tab_level, member_list, 'return 1;\n')
			if '{' in code:
				code += '	' * tab_level + 'return 0;\n'
			elif len(code) == 0:
				code += '	' * tab_level + 'return 1;\n'
		elif self.functionName == 'GetDoObject':  #直接用假Systemkey來取值的
			code  = '	' * tab_level + 'if ("489DA7EA-46E8-467D-951D-092593943C01" == m_SystemKey)\n'
			code += '	' * tab_level + '{\n'
			code += '	' * tab_level + '	return new ' + self.className + '();\n'
			code += '	' * tab_level + '}\n'
			code += '	' * tab_level + 'else\n'
			code += '	' * tab_level + '{\n'
			code += '	' * tab_level + '	return 0;\n'
			code += '	' * tab_level + '}\n'
		elif self.className + '*' == self.returnType:  #回傳KDataObject*
			code = self.CppFunctionFilter(tab_level, member_list, 'return new ' + self.className + '();\n')
			if '{' in code:
				code += '	' * tab_level + 'return 0;\n'
			elif len(code) == 0:
				code += '	' * tab_level + 'return new ' + self.className + '();\n'

		return code;

	def dotCppCode(self, tab_level, member_list):
		code = '\n'
		code += self.returnType + ' '  + self.className + '::' + self.functionName + '('
		for parameter in self.parameterList:
			code += parameter.GetType() + ' ' + parameter.GetName() + ', '
		if ', ' in code :
			code = code[0:len(code)-2] #remove ', '
		code += ')\n'
		code += '{\n'
		code += '	' * tab_level + self.CppFunction(tab_level+1, member_list)
		code += '}'
		return code
