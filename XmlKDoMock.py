from kdataobject_constructor import KDoConstructor as kdo_initfun
from xml2.get_kdataobject_function import Parameter as para
from xml2.get_kdataobject_function import GetDoObjectFunction as xml2sfun
from xml2.references import References as xml2ref
from xml2.references import ExtendReferences as xml2exref

class xml2Class:
	def _init_static_function(self):
		self.static_function_list.append(xml2sfun(self.className, '' + self.className + '*', 'CreateDoObject', []))
		self.static_function_list.append(xml2sfun(self.className, '' + self.className + '*', 'GetDoObject', [para('string', 'm_SystemKey')]))
		self.static_function_list.append(xml2sfun(self.className, 'list<' + self.className + '*>', 'GetDoObjectsByFilter', [para('map<string, string>&', 'm_Filter')]))
		self.static_function_list.append(xml2sfun(self.className, 'list<' + self.className + '*>', 'GetDoObjectsByFilter', [para('map<string, list<string> >&', 'm_Filter')]))
		self.static_function_list.append(xml2sfun(self.className, 'list<' + self.className + '*>', 'GetDoObjectsByFilter', [para('list< map<string, string> >&', 'm_Filter')]))
		self.static_function_list.append(xml2sfun(self.className, 'list<' + self.className + '*>', 'GetDoObjectsByFilter', [para('map<string, string>&', 'm_Filter'), para('int', 'm_StartIndex'), para('int', 'm_Number'), para('list<string>&', 'm_OrderList'), para('bool', 'm_AscendingFlag = true')]))
		self.static_function_list.append(xml2sfun(self.className, 'list<' + self.className + '*>', 'GetDoObjectsByFilter', [para('map<string, list<string> >&', 'm_Filter'), para('int', 'm_StartIndex'), para('int', 'm_Number'), para('list<string>&', 'm_OrderList'), para('bool', 'm_AscendingFlag = true')]))
		self.static_function_list.append(xml2sfun(self.className, 'list<' + self.className + '*>', 'GetDoObjectsByFilter', [para('list< map<string, string> >&', 'm_Filter'), para('int', 'm_StartIndex'), para('int', 'm_Number'), para('list<string>&', 'm_OrderList'), para('bool', 'm_AscendingFlag = true')]))
		self.static_function_list.append(xml2sfun(self.className, 'list<' + self.className + '*>', 'GetDoObjectsBySql', [para('string', 'm_SqlFilter')]))
		self.static_function_list.append(xml2sfun(self.className, 'int', 'GetDoObjectsCountBySql', [para('string', 'm_SqlFilter')]))
		self.static_function_list.append(xml2sfun(self.className, 'int', 'GetDoObjectsCountByFilter', [para('map<string, string>&', 'm_Filter')]))
		self.static_function_list.append(xml2sfun(self.className, 'int', 'GetDoObjectsCountByFilter', [para('map<string, list<string> >&', 'm_Filter')]))
		self.static_function_list.append(xml2sfun(self.className, 'int', 'GetDoObjectsCountByFilter', [para('list< map<string, string> >&', 'm_Filter')]))
		self.static_function_list.append(xml2sfun(self.className, 'int', 'GetDoObjectsCountByFilter', [para('map<string, string>&', 'm_Filter'), para('set<string>&', 'm_LikeColumns')]))
		self.static_function_list.append(xml2sfun(self.className, 'int', 'GetDoObjectsCountByFilter', [para('map<string, list<string> >&', 'm_Filter'), para('set<string>&', 'm_LikeColumns')]))
		self.static_function_list.append(xml2sfun(self.className, 'int', 'GetDoObjectsCountByFilter', [para('list< map<string, string> >&', 'm_Filter'), para('set<string>&', 'm_LikeColumns')]))
		self.static_function_list.append(xml2sfun(self.className, 'list<' + self.className + '*>', 'GetDoObjectsBySql', [para('string', 'm_SqlFilter'), para('int', 'm_StartIndex'), para('int', 'm_Number'), para('list<string>&', 'm_OrderList'), para('bool', 'm_AscendingFlag = true')]))
		self.static_function_list.append(xml2sfun(self.className, 'list<' + self.className + '*>', 'GetDoObjectsByFilter', [para('map<string, string>&', 'm_Filter'), para('set<string>&', 'm_LikeColumns')]))
		self.static_function_list.append(xml2sfun(self.className, 'list<' + self.className + '*>', 'GetDoObjectsByFilter', [para('map<string, list<string> >&', 'm_Filter'), para('set<string>&', 'm_LikeColumns')]))
		self.static_function_list.append(xml2sfun(self.className, 'list<' + self.className + '*>', 'GetDoObjectsByFilter', [para('list< map<string, string> >&', 'm_Filter'), para('set<string>&', 'm_LikeColumns')]))
		self.static_function_list.append(xml2sfun(self.className, 'list<' + self.className + '*>', 'GetDoObjectsByFilter', [para('map<string, string>&', 'm_Filter'), para('set<string>&', 'm_LikeColumns'), para('int', 'm_StartIndex'), para('int', 'm_Number'), para('list<string>&', 'm_OrderList'), para('bool', 'm_AscendingFlag = true')]))
		self.static_function_list.append(xml2sfun(self.className, 'list<' + self.className + '*>', 'GetDoObjectsByFilter', [para('map<string, list<string> >&', 'm_Filter'), para('set<string>&', 'm_LikeColumns'), para('int', 'm_StartIndex'), para('int', 'm_Number'), para('list<string>&', 'm_OrderList'), para('bool', 'm_AscendingFlag = true')]))
		self.static_function_list.append(xml2sfun(self.className, 'list<' + self.className + '*>', 'GetDoObjectsByFilter', [para('list< map<string, string> >&', 'm_Filter'), para('set<string>&', 'm_LikeColumns'), para('int', 'm_StartIndex'), para('int', 'm_Number'), para('list<string>&', 'm_OrderList'), para('bool', 'm_AscendingFlag = true')]))
		self.static_function_list.append(xml2sfun(self.className, '' + self.className + '*', 'GetDoObjectByFilter', [para('map<string, string>&', 'm_Filter')]))
		self.static_function_list.append(xml2sfun(self.className, '' + self.className + '*', 'GetDoObjectBySql', [para('string', 'm_SqlFilter')]))

	def __init__(self, name):
		self.member_list = []
		self.before_class_name_list = []
		self.reference_list = []
		self.static_function_list = []
		self.include_list = []
		self.include_stdlib_list = []
		self.using_namespace = []
		self.className = 'KDo' + name
		self.collection_function_list = []
		self.init_ref_var_list = []
		self.init_ref_list_function = []
		self.ref_static_systemkey_list = []
		self.ref_init_static_systemkey_list = []
		self.construct = kdo_initfun(self.className)
		self._init_static_function()

	def AddCollectionFunction(self, code):
		self.collection_function_list.append(code)

	def AddMemberVariable(self, type, name):
		self.member_list.append(para(type, name))
		if type == 'string':
			self.include_stdlib_list.append(type)
			self.using_namespace.append('std::' + type)

		if type == 'datetime':
			self.include_list.append('KDateTime')
			self.using_namespace.append(str('KGS::DateTime'))

	def AddReference(self, dot_h_code):
		self.reference_list.append(dot_h_code)

	def AddInitRef(self, dot_cpp_code):
		self.init_ref_var_list.append(dot_cpp_code)

	def AddRelListFunction(self, dot_cpp_code):
		self.init_ref_list_function.append(dot_cpp_code)

	def AddRefField(self, dot_h_code):
		self.ref_static_systemkey_list.append(dot_h_code)

	def AddInitRefField(self, dot_cpp_code):
		self.ref_init_static_systemkey_list.append(dot_cpp_code)

	def AddBeforeClass(self, class_name):
		self.before_class_name_list.append(class_name)

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

	def CppInclude(self):
		code = '#include "stdafx.h"\n'
		code += '#include "' + self.className + '.h"\n'
		code += '#include "MockKDataObjectPool.h"\n'
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
		return code


	def PrintDotCppFile(self):
		code = ''
		code += self.CppInclude()
		code += self.CppFieldStaticString()

		for static_str in self.ref_init_static_systemkey_list:
			code += static_str + '\n'
		code += '\n'
		code += self.construct.dotCppCode(0, self.member_list, self.init_ref_var_list)

		for function in self.static_function_list:
			code += '\n' + function.dotCppCode(0, self.member_list)

		for function in self.init_ref_list_function:
			code += '\n' + function + '\n'

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
		dot_h_include += '\n'
		dot_h_include += '#ifndef KDOObjectsH\n'
		dot_h_include += '#include "KDoObjects.h"\n'
		dot_h_include += '#endif\n'
		dot_h_include += '\n'
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

	def HClassCode(self, tab_level, var_list):
		out = ''
		for class_kdo_name in set(self.before_class_name_list):
			out += class_kdo_name + '\n'
		out += 'class ' + self.className + ' : public KDataPersistentObject' + '\n'
		out += '{\n'
		out += 'public:\n'
		tab_level += 1
		out += self.HFieldStaticString(tab_level) + '\n'
		for ref_field in set(self.ref_static_systemkey_list):
			out += '	' * tab_level + ref_field + '\n';
		out += 'public:\n'
		for ref in self.reference_list:
			out += '	' * tab_level + ref + '\n';
		out += '\n'
		out += 'public:\n'
		for member_var in self.member_list:
			out += '	' + str(member_var) + '\n'
		out += '\n'
		out += 'public:\n'
		out += '	' * tab_level + 'friend class KDoFactory;\n'
		for static_function in self.static_function_list:
			out += '	' * tab_level + static_function.dotHCode(tab_level) + '\n'
		for collection_function in self.collection_function_list:
			out += collection_function
		out += '\n'
		out += 'public:\n'
		out += self.construct.dotHCode(tab_level) + '\n'
		out += '};\n'
		return out

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
	ref_obj1 = xml2ref("Employee", 'RawMaterial', 'Link' , 'Has')
	classX.AddReference(ref_obj1.MyDotHCode())
	ref_obj2 = xml2ref("Employee", 'RawMaterialSize', 'Unique' , 'Has')
	classX.AddReference(ref_obj2.MyDotHCode())
	classX.Write2DotHFile('')
	classX.Write2DotCppFile('')
