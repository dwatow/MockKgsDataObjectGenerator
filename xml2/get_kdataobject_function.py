class Parameter:
	def CovertType(self, type):
		if type == 'u4':
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
		self.parameter_list = parameter_list

	def dotHCode(self, tab_level):
		code = 'static ' + self.returnType + ' ' + self.functionName + '('
		for parameter in self.parameter_list:
			if ' =' in parameter.GetName():
				code += parameter.GetType() + ' ' + parameter.GetName()[0:parameter.GetName().index(' =')] + ', '
			else:
				code += parameter.GetType() + ' ' + parameter.GetName() + ', '
		if ', ' in code:
			code = code[0:len(code)-2] #remove ', '
		code += ');'
		return code

	def CppFunctionFilterHitListMap(self, field_var):
#		if 'SystemKey' in field_var.GetName():
#			return '((*it)[' + self.className + '::Field_' + field_var.GetName() + '].empty() || (*it)[' + self.className + '::Field_' + field_var.GetName() + '] == "489DA7EA-46E8-467D-951D-092593943C01")'
#		el
		if field_var.GetType() == 'unsigned int' or field_var.GetType() == 'int':
			return '((*it)[' + self.className + '::Field_' + field_var.GetName() + '].empty() || (*it)[' + self.className + '::Field_' + field_var.GetName() + '] == IntToStr((*tobj_it)->' + field_var.GetName() + '))'
		elif field_var.GetType() == 'unsigned __int64' or field_var.GetType() == 'int':
			return '((*it)[' + self.className + '::Field_' + field_var.GetName() + '].empty() || (*it)[' + self.className + '::Field_' + field_var.GetName() + '] == UintToStr((*tobj_it)->' + field_var.GetName() + '))'
		elif field_var.GetType() == 'float' or field_var.GetType() == 'double':
			return '((*it)[' + self.className + '::Field_' + field_var.GetName() + '].empty() || (*it)[' + self.className + '::Field_' + field_var.GetName() + '] == FloatToStr((*tobj_it)->' + field_var.GetName() + '))'
		elif field_var.GetType() == 'KDateTime':
			return '((*it)[' + self.className + '::Field_' + field_var.GetName() + '].empty() || (*it)[' + self.className + '::Field_' + field_var.GetName() + '] == (*tobj_it)->' + field_var.GetName() + '.LongDateTimeString())'
		else:
			return '((*it)[' + self.className + '::Field_' + field_var.GetName() + '].empty() || (*it)[' + self.className + '::Field_' + field_var.GetName() + '] == (*tobj_it)->' + field_var.GetName() + ')'

	def CppFunctionFilterHitMapList(self, field_var):
#		if 'SystemKey' in field_var.GetName():
#			return '(m_Filter[' + self.className + '::Field_' + field_var.GetName() + '].empty() || find(m_Filter[' + self.className + '::Field_' + field_var.GetName() + '].begin(), m_Filter[' + self.className + '::Field_' + field_var.GetName() + '].end(), "489DA7EA-46E8-467D-951D-092593943C01") != m_Filter[' + self.className + '::Field_' + field_var.GetName() + '].end())'
#		el
		if field_var.GetType() == 'unsigned int' or field_var.GetType() == 'int':
			return '(m_Filter[' + self.className + '::Field_' + field_var.GetName() + '].empty() || find(m_Filter[' + self.className + '::Field_' + field_var.GetName() + '].begin(), m_Filter[' + self.className + '::Field_' + field_var.GetName() + '].end(), IntToStr((*tobj_it)->' + field_var.GetName() + ')) != m_Filter[' + self.className + '::Field_' + field_var.GetName() + '].end())'
		elif field_var.GetType() == 'unsigned __int64':
			return '(m_Filter[' + self.className + '::Field_' + field_var.GetName() + '].empty() || find(m_Filter[' + self.className + '::Field_' + field_var.GetName() + '].begin(), m_Filter[' + self.className + '::Field_' + field_var.GetName() + '].end(), UintToStr((*tobj_it)->' + field_var.GetName() + ')) != m_Filter[' + self.className + '::Field_' + field_var.GetName() + '].end())'
		elif field_var.GetType() == 'float' or field_var.GetType() == 'double':
			return '(m_Filter[' + self.className + '::Field_' + field_var.GetName() + '].empty() || find(m_Filter[' + self.className + '::Field_' + field_var.GetName() + '].begin(), m_Filter[' + self.className + '::Field_' + field_var.GetName() + '].end(), FloatToStr((*tobj_it)->' + field_var.GetName() + ')) != m_Filter[' + self.className + '::Field_' + field_var.GetName() + '].end())'
		elif field_var.GetType() == 'KDateTime':
			return '(m_Filter[' + self.className + '::Field_' + field_var.GetName() + '].empty() || find(m_Filter[' + self.className + '::Field_' + field_var.GetName() + '].begin(), m_Filter[' + self.className + '::Field_' + field_var.GetName() + '].end(), (*tobj_it)->' + field_var.GetName() + '.LongDateTimeString()) != m_Filter[' + self.className + '::Field_' + field_var.GetName() + '].end())'
		else:
			return '(m_Filter[' + self.className + '::Field_' + field_var.GetName() + '].empty() || find(m_Filter[' + self.className + '::Field_' + field_var.GetName() + '].begin(), m_Filter[' + self.className + '::Field_' + field_var.GetName() + '].end(), (*tobj_it)->' + field_var.GetName() + ') != m_Filter[' + self.className + '::Field_' + field_var.GetName() + '].end())'

	def CppFunctionFilterHitMap(self, field_var):
#		if 'SystemKey' in field_var.GetName():
#			return '(' + field_var.GetName().lower() + '_it == m_Filter.end() || ' + field_var.GetName().lower() + '_it->second == "489DA7EA-46E8-467D-951D-092593943C01")'
#		el
		if field_var.GetType() == 'unsigned int' or field_var.GetType() == 'int':
			return '(' + field_var.GetName().lower() + '_it == m_Filter.end() || ' + field_var.GetName().lower() + '_it->second == IntToStr((*tobj_it)->' + field_var.GetName() + '))'
		elif field_var.GetType() == 'unsigned __int64':
			return '(' + field_var.GetName().lower() + '_it == m_Filter.end() || ' + field_var.GetName().lower() + '_it->second == UintToStr((*tobj_it)->' + field_var.GetName() + '))'
		elif field_var.GetType() == 'float' or field_var.GetType() == 'double':
			return '(' + field_var.GetName().lower() + '_it == m_Filter.end() || ' + field_var.GetName().lower() + '_it->second == FloatToStr((*tobj_it)->' + field_var.GetName() + '))'
		elif field_var.GetType() == 'KDateTime':
			return '(' + field_var.GetName().lower() + '_it == m_Filter.end() || ' + field_var.GetName().lower() + '_it->second == (*tobj_it)->' + field_var.GetName() + '.LongDateTimeString())'
		else:
			return '(' + field_var.GetName().lower() + '_it == m_Filter.end() || ' + field_var.GetName().lower() + '_it->second == (*tobj_it)->' + field_var.GetName() + ')'

	def HitMapList(self, tab_level, member_list, is_true_run_code):
		code =''
		code += '	' * tab_level + 'for (list<' + self.className + '*>::iterator tobj_it = curr_list.begin(); tobj_it != curr_list.end(); ++tobj_it)\n'
		code += '	' * tab_level + '{\n'
		tab_level += 1
		code += '	' * tab_level + 'if ('
		for member in member_list:
			code += self.CppFunctionFilterHitMapList(member)
			if member is not member_list[-1]:
				code += ' &&\n' + '	' * (tab_level+1)

		code += ')\n'
		code += '	' * tab_level + '{\n'
		code += '	' * (tab_level+1) + is_true_run_code
		code += '	' * tab_level + '}\n'
		tab_level -= 1
		code += '	' * tab_level + '}\n'
		return code

	def HitListMap(self, tab_level, member_list, is_true_run_code):
		code =''
		code += '	' * tab_level + 'for (list< map<string, string> >::iterator it = m_Filter.begin(); it != m_Filter.end(); ++it)\n'
		code += '	' * tab_level + '{\n'
		tab_level += 1
		code += '	' * tab_level + 'for (list<' + self.className + '*>::iterator tobj_it = curr_list.begin(); tobj_it != curr_list.end(); ++tobj_it)\n'
		code += '	' * tab_level + '{\n'
		tab_level += 1
		code += '	' * tab_level + 'if ('
		for member in member_list:
			code += self.CppFunctionFilterHitListMap(member)
			if member is not member_list[-1]:
				code += ' &&\n' + '	' * (tab_level+1)

		code += ')\n'
		code += '	' * tab_level + '{\n'
		tab_level += 1
		code += '	' * tab_level + is_true_run_code
		tab_level -= 1
		code += '	' * tab_level + '}\n'
		tab_level -= 1
		code += '	' * tab_level + '}\n'
		tab_level -= 1
		code += '	' * tab_level + '}\n'
		return code

	def HitMap(self, tab_level, member_list, is_true_run_code):
		code =''
		for member in member_list:
			code +=  '	' * tab_level + 'map<string, string>::iterator ' + member.GetName().lower() + '_it = m_Filter.find(' + self.className + '::Field_' + member.GetName() + ');\n'

		code += '	' * tab_level + 'int index_table(0);\n'
		code += '	' * tab_level + 'for (list<' + self.className + '*>::iterator tobj_it = curr_list.begin(); tobj_it != curr_list.end(); ++tobj_it)\n'
		code += '	' * tab_level + '{\n'
		tab_level += 1
		code += '	' * tab_level + 'if ('
		for member in member_list:
			code += self.CppFunctionFilterHitMap(member)
			if member is not member_list[-1]:
				code += ' &&\n' + '	' * (tab_level+1)
		code += ')\n'
		code += '	' * tab_level + '{\n'
		tab_level += 1
		code += '	' * tab_level + is_true_run_code
		tab_level -= 1
		code += '	' * tab_level + '}\n'
		code += '	' * tab_level + '++index_table;\n'
		tab_level -= 1
		code += '	' * tab_level + '}\n'
		return code

	def CppFunctionFilter(self, tab_level, member_list, is_true_run_code):
		code = ''
		if len(self.parameter_list) is not 0 and len(member_list) is not 0 and 'map<string, list<string> >' in self.parameter_list[0].GetType():
			code += self.HitMapList(tab_level, member_list, is_true_run_code)
		elif len(self.parameter_list) is not 0 and len(member_list) is not 0 and 'list< map<string, string> >' in self.parameter_list[0].GetType():
			code += self.HitListMap(tab_level, member_list, is_true_run_code)
		elif len(self.parameter_list) is not 0 and len(member_list) is not 0 and 'map<string, string>' in self.parameter_list[0].GetType():
			code += self.HitMap(tab_level, member_list, is_true_run_code)
		#else:
		#	code += '	' * tab_level + is_true_run_code
		return code


	def CppFunction(self, tab_level, member_list):
		code = ''
		code += '	' * tab_level + 'DbObjectPool database;\n'
		if self.functionName == 'GetDoObject':  #直接用假Systemkey來取值的
			code += '	' * tab_level + 'if ("489DA7EA-46E8-467D-951D-092593943C01" == m_SystemKey)\n'
			code += '	' * tab_level + '{\n'
			code += '	' * tab_level + '	return database.GetObj<' + self.className + '*>("' + self.className + '");\n'
			code += '	' * tab_level + '}\n'
			code += '	' * tab_level + 'else\n'
			code += '	' * tab_level + '{\n'
			code += '	' * tab_level + '	return 0;\n'
			code += '	' * tab_level + '}\n'
		elif self.functionName == 'CreateDoObject':
			code += '	' * tab_level + self.className + '* new_obj = new ' + self.className + '();\n'
			code += '	' * tab_level + 'database.SetData(new_obj);\n'
			code += '	' * tab_level + 'return new_obj;\n'
		elif self.returnType == 'int' and 'BySql' in self.functionName:
			code += '	' * tab_level + 'return ' + '(int)(database.GetList<' + self.className + '*>("' + self.className + '").size());\n'
		elif 'list' in self.returnType and 'BySql' in self.functionName:
			code += '	' * tab_level + 'return ' + 'database.GetList<' + self.className + '*>("' + self.className + '");\n'
		elif '*' in self.returnType and 'BySql' in self.functionName:
			code += '	' * tab_level + 'list<' + self.className + '*> curr_list;\n'
			code += '	' * tab_level + 'curr_list = ' + 'database.GetList<' + self.className + '*>("' + self.className + '");\n'
			code += '	' * tab_level + 'if (curr_list.empty())\n'
			code += '	' * tab_level + '{\n'
			code += '	' * tab_level + '	return 0;\n'
			code += '	' * tab_level + '}\n'
			code += '	' * tab_level + 'else\n'
			code += '	' * tab_level + '{\n'
			code += '	' * tab_level + '	return curr_list.front();\n'
			code += '	' * tab_level + '}\n'
		elif 'list' in self.returnType:  #回傳list<KDataObject*>
			code += '	' * tab_level + 'list<' + self.className + '*>' + ' curr_list = database.GetList<' + self.className + '*>("' + self.className + '");\n'
			code += '	' * tab_level + 'list<' + self.className + '*>' + ' target_objs_list;\n'
			code += self.CppFunctionFilter(tab_level, member_list, 'target_objs_list.push_back(*tobj_it);\n')
			code += '	' * tab_level + 'return target_objs_list;\n'
		elif 'int' in self.returnType and '*' not in self.returnType: #回傳總數
			code += '	' * tab_level + 'int i(0);\n'
			code += '	' * tab_level + 'list<' + self.className + '*>' + ' curr_list = database.GetList<' + self.className + '*>("' + self.className + '");\n'
			code += self.CppFunctionFilter(tab_level, member_list, 'i += 1;\n')
			code += '	' * tab_level + 'return i;\n'
		elif self.className + '*' == self.returnType:  #回傳KDataObject*
			code += '	' * tab_level + 'list<' + self.className + '*>' + ' curr_list = database.GetList<' + self.className + '*>("' + self.className + '");\n'
			code += self.CppFunctionFilter(tab_level, member_list, 'return database.GetObj<' + self.className + '*>("' + self.className + '", index_table);\n')
			code += '	' * tab_level + 'return 0;\n'

		return code;

	def dotCppCode(self, tab_level, member_list):
		code = '\n'
		code += self.returnType + ' '  + self.className + '::' + self.functionName + '('
		for parameter in self.parameter_list:
			code += parameter.GetType() + ' ' + parameter.GetName() + ', '
		if ', ' in code :
			code = code[0:len(code)-2] #remove ', '
		code += ')\n'
		code += '{\n'
		code += '	' * tab_level + self.CppFunction(tab_level+1, member_list)
		code += '}'
		return code
