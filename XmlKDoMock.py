class xml2Variable:
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

class Constructor:
	def __init__(self, className):
		self.className = className

	def init_type_value(self, tab_level, var):
		if var.type == 'string':
			return '	' * tab_level + var.name + '("' + self.className + '_' + var.name + '")' + ',\n'
		elif var.type == 'double' or var.type == 'float':
			return '	' * tab_level + var.name + '(' + '0.0' + ')' + ',\n'
		elif 'int' in var.type: #unsigned int or int
			return '	' * tab_level + var.name + '(' + '1' + ')' + ',\n'
		else:
			return ''

	def init_var(self, tab_level, var_list):
		code = ':\n'
		#print(self.className)
		for var in var_list:
			#print('	', var.name)
			code += self.init_type_value(tab_level, var)
		code = code[0:len(code)-2] + '\n' + '	' * tab_level
		return code

	def dotHCode(self, tab_level):
		code = '	' * tab_level + self.className
		code += '();'
		return code + '\n'

	def dotFullHCode(self, tab_level, var_list):
		code = self.dotHCode(tab_level)
		code = code[0:code.index(';')]

		if len(var_list) > 0:
			code += self.init_var(1, var_list) + '{}'
		else:
			code += ';'

		return code + '\n\n'

	def dotCppCode(self, tab_level, var_list, ref_list):
		#code = self.dotHCode()
		code = self.dotHCode(tab_level)

		code = self.className + '::' + code[0:code.index(';')]
		code += self.init_var(0, var_list)
		code += '{\n'
		code += '	' * (tab_level+1) + 'KDataPersistentObject::cv_SystemKey = "489DA7EA-46E8-467D-951D-092593943C01";'
		for ref in ref_list:
			#print (ref.dotCppInit())
			code += '	' * (tab_level+1) + ref.dotCppInit() + '\n'
		code += '	' * (tab_level+1) + 'cv_ClassName = "' + self.className[len('KDo'):len(self.className)] + '";\n'
		code += '}'
		return code

class xmlFunction:
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
			return '(*it)[' + self.className + '::Field_' + field_name + '] == ' + '"1"'
		else:
			return '(*it)[' + self.className + '::Field_' + field_name + '] == "' + self.className + '_' + field_name + '"'

	def CppFunctionFilterHitMapList(self, field_name):
		if field_name is 'ActiveFlag':
			return 'find(m_Filter[' + self.className + '::Field_' + field_name + '].begin(), m_Filter[' + self.className + '::Field_' + field_name + '].end(), "1") != m_Filter[' + self.className + '::Field_' + field_name + '].end()'
		else:
			return 'find(m_Filter[' + self.className + '::Field_' + field_name + '].begin(), m_Filter[' + self.className + '::Field_' + field_name + '].end(), "' + self.className + '_' + field_name + '") != m_Filter[' + self.className + '::Field_' + field_name + '].end()'

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
			code += 'id_it != m_Filter.end() && id_it->second == "KDo' + self.className + '_Id"'
			if 'ActiveFlag' in var_list:
				code += ' &&\n' + '	' * (tab_level+1)
		if 'ActiveFlag' in var_list:
			code += 'activeflag_it != m_Filter.end() && activeflag_it->second == "1"'
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
		elif 'int' in self.returnType: #回傳總數
			code = self.CppFunctionFilter(tab_level, member_list, 'return 1;\n')
			if '{' in code:
				code += '	' * tab_level + 'return 0;\n'
		elif self.functionName == 'GetDoObject':  #直接用Systemkey來取值的
			code  = '	' * tab_level + 'if ("SystemKey" == m_SystemKey)\n'
			code += '	' * tab_level + '{\n'
			code += '	' * tab_level + '	return new ' + self.className + '();\n'
			code += '	' * tab_level + '}\n'
			code += '	' * tab_level + 'else\n'
			code += '	' * tab_level + '{\n'
			code += '	' * tab_level + '	return 0;\n'
			code += '	' * tab_level + '}\n'
		elif '' + self.className + '*' in self.returnType:  #回傳KDataObject*
			code = self.CppFunctionFilter(tab_level, member_list, 'return new ' + self.className + '();\n')
			if '{' in code:
				code += '	' * tab_level + 'return 0;\n'

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

class xmlRef:
	def _init_ref(self, ref_type):
		if ref_type == 'Link':
			self.type = '*'
		else:
			print('unknow type: ', ref_type)

	def _init_relation(self, relation):
		if relation == 'Has':
			self.has = True
		else:
			self.has = False

	def __init__(self, name, ref_type, relation):
		self.name = name
		self._init_ref(ref_type)
		self._init_relation(relation)

	def dotHCode(self):
		return 'KDo' + self.name + '* ' + self.name + ';'

	def dotCppInit(self):
		return self.name + ' = new KDo' + self.name + '();'
	def BeforeClass(self):
		return 'class KDo' + self.name + ';'

class xml2Class:
	def _InitStaticFunction(self):
		self.static_function_list.append(xmlFunction(self.className, '' + self.className + '*', 'CreateDoObject', []))
		self.static_function_list.append(xmlFunction(self.className, '' + self.className + '*', 'GetDoObject', [xml2Variable('string', 'm_SystemKey')]))
		self.static_function_list.append(xmlFunction(self.className, 'list<' + self.className + '*>', 'GetDoObjectsByFilter', [xml2Variable('map<string, string>&', 'm_Filter')]))
		self.static_function_list.append(xmlFunction(self.className, 'list<' + self.className + '*>', 'GetDoObjectsByFilter', [xml2Variable('map<string, list<string> >&', 'm_Filter')]))
		self.static_function_list.append(xmlFunction(self.className, 'list<' + self.className + '*>', 'GetDoObjectsByFilter', [xml2Variable('list< map<string, string> >&', 'm_Filter')]))
		self.static_function_list.append(xmlFunction(self.className, 'list<' + self.className + '*>', 'GetDoObjectsByFilter', [xml2Variable('map<string, string>&', 'm_Filter'), xml2Variable('int', 'm_StartIndex'), xml2Variable('int', 'm_Number'), xml2Variable('list<string>&', 'm_OrderList'), xml2Variable('bool', 'm_AscendingFlag = true')]))
		self.static_function_list.append(xmlFunction(self.className, 'list<' + self.className + '*>', 'GetDoObjectsByFilter', [xml2Variable('map<string, list<string> >&', 'm_Filter'), xml2Variable('int', 'm_StartIndex'), xml2Variable('int', 'm_Number'), xml2Variable('list<string>&', 'm_OrderList'), xml2Variable('bool', 'm_AscendingFlag = true')]))
		self.static_function_list.append(xmlFunction(self.className, 'list<' + self.className + '*>', 'GetDoObjectsByFilter', [xml2Variable('list< map<string, string> >&', 'm_Filter'), xml2Variable('int', 'm_StartIndex'), xml2Variable('int', 'm_Number'), xml2Variable('list<string>&', 'm_OrderList'), xml2Variable('bool', 'm_AscendingFlag = true')]))
		self.static_function_list.append(xmlFunction(self.className, 'int', 'GetDoObjectsCountBySql', [xml2Variable('string', 'm_SqlFilter')]))
		self.static_function_list.append(xmlFunction(self.className, 'int', 'GetDoObjectsCountByFilter', [xml2Variable('map<string, string>&', 'm_Filter')]))
		self.static_function_list.append(xmlFunction(self.className, 'int', 'GetDoObjectsCountByFilter', [xml2Variable('map<string, list<string> >&', 'm_Filter')]))
		self.static_function_list.append(xmlFunction(self.className, 'int', 'GetDoObjectsCountByFilter', [xml2Variable('list< map<string, string> >&', 'm_Filter')]))
		self.static_function_list.append(xmlFunction(self.className, 'int', 'GetDoObjectsCountByFilter', [xml2Variable('map<string, string>&', 'm_Filter'), xml2Variable('set<string>&', 'm_LikeColumns')]))
		self.static_function_list.append(xmlFunction(self.className, 'int', 'GetDoObjectsCountByFilter', [xml2Variable('map<string, list<string> >&', 'm_Filter'), xml2Variable('set<string>&', 'm_LikeColumns')]))
		self.static_function_list.append(xmlFunction(self.className, 'int', 'GetDoObjectsCountByFilter', [xml2Variable('list< map<string, string> >&', 'm_Filter'), xml2Variable('set<string>&', 'm_LikeColumns')]))
		self.static_function_list.append(xmlFunction(self.className, 'list<' + self.className + '*>', 'GetDoObjectsBySql', [xml2Variable('string', 'm_SqlFilter'), xml2Variable('int', 'm_StartIndex'), xml2Variable('int', 'm_Number'), xml2Variable('list<string>&', 'm_OrderList'), xml2Variable('bool', 'm_AscendingFlag = true')]))
		self.static_function_list.append(xmlFunction(self.className, 'list<' + self.className + '*>', 'GetDoObjectsByFilter', [xml2Variable('map<string, string>&', 'm_Filter'), xml2Variable('set<string>&', 'm_LikeColumns')]))
		self.static_function_list.append(xmlFunction(self.className, 'list<' + self.className + '*>', 'GetDoObjectsByFilter', [xml2Variable('map<string, list<string> >&', 'm_Filter'), xml2Variable('set<string>&', 'm_LikeColumns')]))
		self.static_function_list.append(xmlFunction(self.className, 'list<' + self.className + '*>', 'GetDoObjectsByFilter', [xml2Variable('list< map<string, string> >&', 'm_Filter'), xml2Variable('set<string>&', 'm_LikeColumns')]))
		self.static_function_list.append(xmlFunction(self.className, 'list<' + self.className + '*>', 'GetDoObjectsByFilter', [xml2Variable('map<string, string>&', 'm_Filter'), xml2Variable('set<string>&', 'm_LikeColumns'), xml2Variable('int', 'm_StartIndex'), xml2Variable('int', 'm_Number'), xml2Variable('list<string>&', 'm_OrderList'), xml2Variable('bool', 'm_AscendingFlag = true')]))
		self.static_function_list.append(xmlFunction(self.className, 'list<' + self.className + '*>', 'GetDoObjectsByFilter', [xml2Variable('map<string, list<string> >&', 'm_Filter'), xml2Variable('set<string>&', 'm_LikeColumns'), xml2Variable('int', 'm_StartIndex'), xml2Variable('int', 'm_Number'), xml2Variable('list<string>&', 'm_OrderList'), xml2Variable('bool', 'm_AscendingFlag = true')]))
		self.static_function_list.append(xmlFunction(self.className, 'list<' + self.className + '*>', 'GetDoObjectsByFilter', [xml2Variable('list< map<string, string> >&', 'm_Filter'), xml2Variable('set<string>&', 'm_LikeColumns'), xml2Variable('int', 'm_StartIndex'), xml2Variable('int', 'm_Number'), xml2Variable('list<string>&', 'm_OrderList'), xml2Variable('bool', 'm_AscendingFlag = true')]))
		self.static_function_list.append(xmlFunction(self.className, '' + self.className + '*', 'GetDoObjectByFilter', [xml2Variable('map<string, string>&', 'm_Filter')]))
		self.static_function_list.append(xmlFunction(self.className, '' + self.className + '*', 'GetDoObjectBySql', [xml2Variable('string', 'm_SqlFilter')]))

	def __init__(self, name):
		self.member_list = []
		self.reference_list = []
		self.static_function_list = []
		self.include_list = []
		self.include_stdlib_list = []
		self.using_namespace = []
		self.className = 'KDo' + name
		self.construct = Constructor(self.className)
		self._InitStaticFunction()

	def AddMemberVariable(self, type, name):
		self.member_list.append(xml2Variable(type, name))
		if type == 'string':
			self.include_stdlib_list.append(type)
			self.using_namespace.append('std::' + type)

		if type == 'datetime':
			self.include_list.append('KDateTime')
			self.using_namespace.append(str('KGS::DateTime'))

	def AddReference(self, name, type, relation):
		self.reference_list.append(xmlRef(name, type, relation))
	#.cpp file

	def CppFieldStaticString(self):
		code = '\n'
		#code += 'const string ' + self.className + '::ClassDbTableName = "' + '";
		code += 'const string ' + self.className + '::Field_SystemKey = "SystemKey";\n'
		code += 'const string ' + self.className + '::Field_SystemKeyType = "SystemKeyType";\n\n'

		for member in self.member_list:
			if member.name == 'SystemKey':
				continue
			code += member.dotCppFieldStr(self.className) + '\n'

		return code

	def PrintDotCppFile(self):
		code = '#include "stdafx.h"\n'
		code += '#include "' + self.className + '.h"\n'
		code += '#include <algorithm>\n'
		code += '#include <map>\n'
		code += '#include <list>\n'
		code += '#include <iterator>\n'
		code += '#include <string>\n'
		code += '\n'
		code += 'using std::find;\n'
		code += 'using std::map;\n'
		code += 'using std::list;\n'
		code += 'using std::iterator;\n'
		code += 'using std::string;\n'
		code += self.CppFieldStaticString()
		code += '\n' + self.construct.dotCppCode(0, self.member_list, self.reference_list)

		for function in self.static_function_list:
			code += '\n' + function.dotCppCode(0, self.member_list)

		return code

	def Write2DotCppFile(self, filePath):
		fil_path_ename = ""
		if len(filePath) != 0:
			fil_path_ename = filePath + '\\' + self.className + '.cpp'
		else:
			fil_path_ename = self.className + '.cpp'
		file = open( fil_path_ename, 'w')
		file.write(self.PrintDotCppFile())
		file.close()
	#.h file
	def HInclude(self):
		dot_h_include = '#include "KDo.h"\n'
		dot_h_include += '#include "KDoObjects.h"\n'
		for filename in set(self.include_list):
			dot_h_include += '#include "' + filename + '"\n'
		dot_h_include += '#include <string>\n'
		dot_h_include += '#include <list>\n'
		dot_h_include += '#include <map>\n\n'
		for std_namespace in set(self.include_stdlib_list):
			dot_h_include += '#include <' + std_namespace + '>\n'
		dot_h_include += 'using std::string;\n'
		dot_h_include += 'using std::list;\n'
		dot_h_include += 'using std::map;\n'
		return dot_h_include

	def HUsingNameSpace(self):
		dot_h_using_namespace = ''
		for namespace in set(self.using_namespace):
			dot_h_using_namespace += 'using ' + namespace + '\n'
		return dot_h_using_namespace

	def HFieldStaticString(self, tab_level):
		code = ''
		#code += '	' * tab_level + 'static const string ClassDbTableName;\n\n'
		code += '	' * tab_level + 'static const string Field_SystemKey;\n'
		code += '	' * tab_level + 'static const string Field_SystemKeyType;\n'

		code += '\n'
		for var in self.member_list:
			if var.name == 'SystemKey':
				continue
			code += '	' * tab_level + var.dotHFieldStr() + '\n'
		return code

	def HStaticFunction(self, tab_level):
		code =''
		for static_function in self.static_function_list:
			code += '	' * tab_level + static_function.dotHCode(tab_level) + '\n'
		return code

	def HRef(self, tab_level):
		code =''
		for ref in self.reference_list:
			code += '	' * tab_level + ref.dotHCode() + '\n';
		return code

	def HClassCode(self, tab_level, var_list):
		out = ''
		for ref in self.reference_list:
			out += ref.BeforeClass() + '\n'
		out += 'class ' + self.className + ' : public KDataPersistentObject' + '\n'
		out += '{\n'
		out += 'public:\n'
		tab_level += 1
		out += self.HFieldStaticString(tab_level) + '\n'
		out += 'public:\n'
		out += self.HRef(tab_level)
		out += 'public:\n'
		out += '	' * tab_level + 'friend class KDoFactory;\n\n'
		out += self.HStaticFunction(tab_level) + '\n'
		out += self.construct.dotHCode(tab_level) + '\n'
		#out += self.construct.dotFullHCode(tab_level, var_list)

		for member_var in self.member_list:
			out += '	' + str(member_var) + '\n'
		return out + '};\n'

	def PrintDotHFile(self):
		dot_h_code = '#ifndef ' + self.className + '_H\n'
		dot_h_code += '#define ' + self.className + '_H\n\n'
		dot_h_code += self.HInclude() + '\n'
		dot_h_code += self.HUsingNameSpace() + '\n'
		dot_h_code += self.HClassCode(0, self.member_list)
		dot_h_code += '\n#endif'
		return dot_h_code

	def Write2DotHFile(self, filePath):
		fil_path_ename = ""
		if len(filePath) != 0:
			fil_path_ename = filePath + '\\' + self.className + '.h'
		else:
			fil_path_ename = self.className + '.h'
		file = open( fil_path_ename, 'w')
		file.write(self.PrintDotHFile())
		file.close()


if __name__ == "__main__":
	classX = xml2Class("Employee")
	classX.AddMemberVariable("string", "Id")
	#classX.AddMemberVariable("string", "SystemKey")
	classX.AddMemberVariable("unsigned int", "ActiveFlag")
	classX.AddMemberVariable("float", "SomeValue")
	classX.AddReference('RawMaterial', 'Link' , 'Has')
	classX.AddReference('RawMaterialSize', 'Link' , 'Has')
	classX.Write2DotHFile('')
	classX.Write2DotCppFile('')
