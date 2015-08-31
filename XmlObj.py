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
			return '	' * tab_level + var.name + '(' + '0' + ')' + ',\n'
		else:
			return ''

	def GetClassNameNum(self, num):
		return self.className + str(num)

	def init_var(self, tab_level, var_list):
		code = ':\n'
		#print(self.className)
		for var in var_list:
			#print('	', var.name)
			code += self.init_type_value(tab_level, var)
		code = code[0:len(code)-2] + '\n' + '	' * tab_level
		return code

	def dotHCode(self, tab_level):
		code = '	' * tab_level + self.GetClassNameNum(1) + '();\n'
		code += '	' * tab_level + self.GetClassNameNum(1) + '(KDo' + self.className + '* KDataObject);\n'
		return code

	def dotCppCode(self, tab_level, var_list, ref_list):
		#code = self.dotHCode()
		code = self.dotHCode(tab_level)
		code = self.className + '::' + code[0:code.index(';')]
		code += self.init_var(0, var_list) + '{\n'
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

	def CppFunction(self, tab_level):
		code = ''
		if 'list' in self.returnType:
			code  = '	' * tab_level + self.returnType + ' list;\n'
			code += '	' * tab_level + 'list.push_back(new ' + self.className + '());\n'
			code += '	' * tab_level + 'return list;\n'
		elif 'Count' in self.functionName:
			code = '	' * tab_level + 'return 1;\n'
		elif self.functionName == 'GetDoObject':
			code  = '	' * tab_level + 'if ("SystemKey" == m_SystemKey)\n'
			code += '	' * tab_level + '{\n'
			code += '	' * tab_level + '	return new ' + self.className + '();\n'
			code += '	' * tab_level + '}\n'
			code += '	' * tab_level + 'else\n'
			code += '	' * tab_level + '{\n'
			code += '	' * tab_level + '	return 0;\n'
			code += '	' * tab_level + '}\n'
		elif '' + self.className + '*' in self.returnType:
			code = '	' * tab_level + 'return new ' + self.className + '();\n'

		return code;

	def dotCppCode(self, tab_level):
		code = '\n'
		code += self.returnType + ' '  + self.className + '::' + self.functionName + '('
		for parameter in self.parameterList:
			code += parameter.GetType() + ' ' + parameter.GetName() + ', '
		if ', ' in code :
			code = code[0:len(code)-2] #remove ', '
		code += ')\n'
		code += '{\n'
		code += '	' * tab_level + self.CppFunction(tab_level+1)
		code += '}'
		return code

class xml2Class:
	def _InitCollection(self):
		self.member_list = []
		self.include_list = []
		self.include_stdlib_list = []
		self.using_namespace = []

	def __init__(self, name):
		self._InitCollection()
		self.className = name
		self.construct = Constructor(self.className)

	def AddMemberVariable(self, type, name):
		print(type, name)
		self.member_list.append(xml2Variable(type, name))
		if type == 'string':
			self.include_stdlib_list.append(type)
			self.using_namespace.append('std::' + type)
		elif 'map' in type:
			self.include_stdlib_list.append('map')
			self.using_namespace.append('std::map')
		elif 'list' in type:
			self.include_stdlib_list.append('list')
			self.using_namespace.append('std::list')

		if type == 'datetime':
			self.include_list.append('KDateTime')
			self.using_namespace.append(str('KGS::DateTime'))

	def GetClassNameNum(self, num):
		return self.className + str(num)

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
		code += self.CppFieldStaticString()
		code += '\n' + self.construct.dotCppCode(0, self.member_list, self.reference_list)

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
		dot_h_include = '#include "KDoProxy1.h"\n'
		dot_h_include += '#include "KDoTransaction.h"\n'
		dot_h_include += '#include "KXmlItem.h"\n'
		dot_h_include += '#include "KDo' + self.className + '.h"\n'

		for filename in set(self.include_list):
			dot_h_include += '#include "' + filename + '"\n'
		for std_namespace in set(self.include_stdlib_list):
			dot_h_include += '#include <' + std_namespace + '>\n'
		return dot_h_include

	def HUsingNameSpace(self):
		dot_h_using_namespace = ''
		for namespace in set(self.using_namespace):
			dot_h_using_namespace += 'using ' + namespace + ';\n'
		return dot_h_using_namespace

	def ditHTableBaseEvent(self, tab_level):
		code = ''
		code += '	' * tab_level + 'void CreateToTable(KXmlItem m_XmlInfo);\n'
		code += '	' * tab_level + 'void ModifyToTable(KXmlItem m_XmlInfo);\n'
		code += '	' * tab_level + 'void Delete();\n'
		return code

	def HClassCode(self, tab_level, var_list):
		out = ''
		out += 'class ' + self.GetClassNameNum(1) + ' : public KDoProxy1' + '\n'
		out += '{\n'
		tab_level += 1
		out += '	' * tab_level + 'KDoTransaction* cv_Transaction;\n'
		out += 'public:\n'
		out += self.construct.dotHCode(tab_level)
		out += 'public:\n'
		out += '	' * tab_level + 'KDo' + self.className + '* GetDataObject() const;\n'
		out += '	' * tab_level + 'KDo' + self.className + '* operator->() const;\n'
		out += 'public:\n'
		out += self.ditHTableBaseEvent(tab_level)
		out += 'public:\n'
		out += '	' * tab_level + 'KXmlItem GetXml_' + self.className + 'Info();\n'
		return out + '};\n'

	def PrintDotHFile(self):
		dot_h_code  = '#ifndef ' + self.className + '_H\n'
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
	classX.AddMemberVariable("string", "SystemKey")
	classX.AddMemberVariable("unsigned int", "Active_Flag")
	classX.AddMemberVariable("float", "SomeValue")
	classX.AddReference('RawMaterial', 'Link' , 'Has')
	classX.AddReference('RawMaterialSize', 'Link' , 'Has')
	classX.Write2DotHFile('')
	classX.Write2DotCppFile('')
