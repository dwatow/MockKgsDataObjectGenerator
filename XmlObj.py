class xml2Variable:
	def CovertType_Xml2Cpp(self, cpp_type):
		if cpp_type == 'u4' or cpp_type == 'u8':
			return 'unsigned int'
		elif cpp_type == 'i4':
			return 'int'
		elif cpp_type == 'f4':
			return 'float'
		elif cpp_type == 'u8':
			return 'unsigned __int64'
		elif cpp_type == 'datetime':
			return 'KDateTime'
		else:
			return str(cpp_type)

	def CovertType_Cpp2Xml(self, xml_type):
		if xml_type == 'unsigned int':
			return 'U4'
		elif xml_type == 'int':
			return 'I4'
		elif xml_type == 'float':
			return 'String'
		elif xml_type == 'unsigned __int64':
			return 'U4'
		elif xml_type == 'KDateTime':
			return 'String'
		elif xml_type == 'string':
			return 'String'
		else:
			return str(xml_type)

	def __init__(self, xml_type, name):
		self.name = name
		self.cpp_type = self.CovertType_Xml2Cpp(xml_type.lower())

	def GetXmlElemant(self):
		xml = '<' + self.name + ' KGS_TYPE="' + self.CovertType_Xml2Cpp(self.cpp_type) + ' KGS_ITEM_NUMBER="' + str(len(self.name)) + '">'
		return xml

	def SetKXmlItem(self, kxmlitem_var_name):
		return kxmlitem_var_name + '.ItemsByLevelName["' + self.name + '"].As' + self.CovertType_Cpp2Xml(self.cpp_type)

	def GetKXmlItem(self, kxmlitem_var_name):
		return kxmlitem_var_name + '.ItemsByName["' + self.name + '"].As' + self.CovertType_Cpp2Xml(self.cpp_type)

class Constructor:
	def __init__(self, className):
		self.className = className

	def GetClassNameNum(self, num):
		return self.className + str(num)

	def dotHCode(self, tab_level):
		code = '	' * tab_level + self.GetClassNameNum(1) + '(KDoTransaction* const m_Transaction = 0);\n'
		code += '	' * tab_level + self.GetClassNameNum(1) + '(KDo' + self.className + '* m_KDataObject, KDoTransaction* const m_Transaction = 0);\n'
		return code

	def dotCppCode(self, tab_level, main_code_list):
		#code = self.dotHCode()
		function_title1 = '	' * tab_level + self.GetClassNameNum(1) + '(KDoTransaction* const m_Transaction);\n'
		code  = '	' * tab_level + self.GetClassNameNum(1) + '::' + function_title1[0:function_title1.index(';')] + ':\n'
		code += '	' * tab_level + 'KDoProxy1(KDo' + self.GetClassNameNum(1) + '::CreateObject()), cv_Transaction(m_Transaction)\n'
		code += '	' * tab_level + '{\n'
		tab_level += 1
		for main_code in main_code_list:
			code += '	' * tab_level + main_code
		tab_level -= 1
		code += '}\n'
		code += '\n'
		function_title2 = '	' * tab_level + self.GetClassNameNum(1) + '(KDo' + self.className + '* m_KDataObject, KDoTransaction* const m_Transaction);\n'
		code += '	' * tab_level + self.GetClassNameNum(1) + '::' + function_title2[0:function_title2.index(';')] + ':\n'
		code += '	' * tab_level + 'KDoProxy1(m_KDataObject), cv_Transaction(m_Transaction)\n'
		code += '	' * tab_level + '{\n'
		tab_level += 1
		for main_code in main_code_list:
			code += '	' * tab_level + main_code
		tab_level -= 1
		code += '}\n'
		return code

class xmlFunction:
	def __init__(self, class_name, return_type, function_name, parameter_list):
		self.className = class_name
		self.returnType = return_type
		self.functionName = function_name
		self.parameterList = parameter_list


class xml2Class:
	def _InitCollection(self):
		self.include_list = []
		self.include_stdlib_list = []
		self.using_namespace = []

	def __init__(self, name):
		self._InitCollection()
		self.member_dict = {}
		self.className = name
		self.construct = Constructor(self.className)

	def AddMemberVariable(self, type, name):
		self.member_dict[name] = xml2Variable(type, name)

	def GetClassNameNum(self, num):
		return self.className + str(num)
	def GetClassNameListNum(self, num):
		return self.className + 'List' + str(num)

	#.cpp file
	def _init_AddTransaction(self, tab_level):
		head = '	'
		code_list = []
		code_list.append(head * tab_level + 'if (cv_Transaction != 0)\n')
		code_list.append(head * tab_level + '{\n')
		code_list.append(head * (tab_level+1) + 'if (!cv_Transaction->AddObject(GetDataObject()))\n')
		code_list.append(head * (tab_level+1) + '{\n')
		code_list.append(head * (tab_level+2) + 'throw new FablinkException(ERROR_FABLINK_START_TRANSACTION_FALSE);\n')
		code_list.append(head * (tab_level+1) + '}\n')
		code_list.append(head * tab_level + '}\n')
		return code_list

	def dotCppGetPtrFunction(self, tab_level):
		code = ''
		code += '	' * tab_level + 'KDoEmpLoginHistoryRelation* ' + self.GetClassNameNum(1) + '::GetDataObject() const\n'
		code += '	' * tab_level + '{\n'
		tab_level += 1
		code += '	' * tab_level + 'return (KDo' + self.className + '*)GetBaseObject();\n'
		tab_level -= 1
		code += '	' * tab_level + '}\n'
		code += '	' * tab_level + '\n'
		code += '	' * tab_level + 'KDoEmpLoginHistoryRelation* ' + self.GetClassNameNum(1) + '::operator->() const\n'
		code += '	' * tab_level + '{\n'
		tab_level += 1
		code += '	' * tab_level + 'return GetDataObject();\n'
		tab_level -= 1
		code += '	' * tab_level + '}\n'
		#code += '	' * tab_level +
		return code

	def SetData2TableFunction(self, tab_level, funciton_event):
		xml_var_name = 'm_XmlInfo'
		code  = '	' * tab_level + 'void ' + self.GetClassNameNum(1) + '::' + funciton_event + 'ToTable(KXmlItem& ' + xml_var_name + ')\n'
		code += '	' * tab_level + '{\n'
		tab_level += 1
		code += '	' * tab_level + '//this function was refactoried not yet....\n'
		for var in self.member_dict.values():
			code += '	' * tab_level + 'GetDataObject()->' + var.name + ' = ' +  var.GetKXmlItem(xml_var_name) + ';\n';
		tab_level -= 1
		code += '	' * tab_level + '}\n'
		return code

	def Delete2TableFunction(self, tab_level):
		code  = '	' * tab_level + 'void ' + self.GetClassNameNum(1) + '::Delete()\n'
		code += '	' * tab_level + '{\n'
		tab_level += 1
		code += '	' * tab_level + '//this function was refactoried not yet....\n'
		if 'ActiveFlag' in self.member_dict:
			code += '	' * tab_level + 'GetDataObject()->ActiveFlag = aftInactive;\n'
		else:
			code += '	' * tab_level + 'GetDataObject()->DeleteObject();\n';
		tab_level -= 1
		code += '	' * tab_level + '}\n'
		return code

	def KXmlItemInfo(self, tab_level):
		code = ''
		code += '	' * tab_level + 'KXmlItem ' + self.GetClassNameNum(1) + '::GetXml_' + self.className + 'Info(const string& m_InfoName) const\n'
		code += '	' * tab_level + '{\n'
		tab_level += 1
		code += '	' * tab_level + '//this function was refactoried not yet....\n'
		code += '	' * tab_level + 'KXmlItem xml;\n'
		code += '	' * tab_level + 'xml.Name = m_InfoName;\n'
		code += '	' * tab_level + 'xml.ItemType = itxList;\n'
		code += '	' * tab_level + '\n'
		#code += '	' * tab_level +
		for var in self.member_dict.values():
			code += '	' * tab_level + var.SetKXmlItem('xml') + ' = ' + 'GetDataObject()->' + var.name + ';\n'
		code += '	' * tab_level + '\n'
		code += '	' * tab_level + 'return xml;\n'
		tab_level -= 1
		code += '	' * tab_level + '}\n'
		return code

	def CppListClassConstructor(self, tab_level):
		code = ''
		code += '	' * tab_level + self.GetClassNameListNum(1) + '::' + self.GetClassNameListNum(1)+ '(const FilterType& m_FilterType, const QueryByPaging1& m_Filter, KDoTransaction* const m_Transaction):\n'
		code += '	' * tab_level + 'cv_TotalFilterObj(0)\n'
		code += '	' * tab_level + '{\n'
		tab_level += 1
		code += '	' * tab_level + 'list<KDo' + self.className + '*> obj_list;\n'
		code += '	' * tab_level + 'list<string> order_condition;\n'
		code += '	' * tab_level + 'order_condition.push_back(KDoLogBatchModifyStationCt::Field_SystemKey);\n'
		code += '	' * tab_level + 'switch(m_FilterType)\n'
		code += '	' * tab_level + '{\n'
		code += '	' * tab_level + 'case ftOr:\n'
		tab_level += 1
		code += '	' * tab_level + 'obj_list= KDo' + self.className + '::GetDoObjectsByFilter(m_Filter.GetOrCondition(),\n'
		code += '	' * tab_level + '	m_Filter.GetLikeField(), m_Filter.GetStartIndex(), m_Filter.GetPagingCount(), order_condition, true);\n'
		code += '	' * tab_level + 'break;\n'
		tab_level -= 1
		code += '	' * tab_level + 'case ftAnd:\n'
		tab_level += 1
		code += '	' * tab_level + 'obj_list= KDo' + self.className + '::GetDoObjectsByFilter(m_Filter.GetAndCondition(),\n'
		code += '	' * tab_level + '	m_Filter.GetLikeField(), m_Filter.GetStartIndex(), m_Filter.GetPagingCount(), order_condition, true);\n'
		code += '	' * tab_level + 'break;\n'
		tab_level -= 1
		code += '	' * tab_level + 'case ftAssign:\n'
		tab_level += 1
		code += '	' * tab_level + 'obj_list= KDo' + self.className + '::GetDoObjectsByFilter(m_Filter.GetAssignCondition(),\n'
		code += '	' * tab_level + '	m_Filter.GetLikeField(), m_Filter.GetStartIndex(), m_Filter.GetPagingCount(), order_condition, true);\n'
		code += '	' * tab_level + 'break;\n'
		tab_level -= 1
		code += '	' * tab_level + '}\n'
		code += '	' * tab_level + 'InitialList(obj_list);\n'
		tab_level -= 1
		code += '	' * tab_level + '}\n'
		return code

	def CppListClassInitislList(self, tab_level):
		code = ''
		code += '	' * tab_level + 'void ' + self.GetClassNameListNum(1) + '::InitialList(list<KDo' + self.className + '>& obj_list )\n'
		code += '	' * tab_level + '{\n'
		tab_level += 1
		code += '	' * tab_level + 'cv_List.reserve(obj_list.size());\n'
		code += '	' * tab_level + 'for (list<KDo' + self.className + '*>::iterator it = obj_list.begin(); it != obj_list.end(); ++it)\n'
		code += '	' * tab_level + '{\n'
		tab_level += 1
		code += '	' * tab_level + self.GetClassNameNum(1) + ' obj(*it);\n'
		code += '	' * tab_level + 'cv_List.push_back(obj);\n'
		tab_level -= 1
		code += '	' * tab_level + '}\n'
		tab_level -= 1
		code += '	' * tab_level + '}\n'
		return code

	def CppListClassSize(self, tab_level):
		code = ''
		code += '	' * tab_level + 'const unsigned int& ' + self.GetClassNameListNum(1) + '::Size() const\n'
		code += '	' * tab_level + '{\n'
		tab_level += 1
		code += '	' * tab_level + 'return cv_TotalFilterObj;\n'
		tab_level -= 1
		code += '	' * tab_level + '}\n'
		return code

	def CppListClassKXmlItemList(self, tab_level):
		code =''
		code += '	' * tab_level + 'KXmlItem ' + self.GetClassNameListNum(1) + '::GetXml_' + self.className + 'List(const string& m_ListName) const\n'

		code += '	' * tab_level + '{\n'
		tab_level += 1
		code += '	' * tab_level + 'KXmlItem xml;\n'
		code += '	' * tab_level + 'xml.Name = m_ListName;\n'
		code += '	' * tab_level + 'xml.ItemType = itxList;\n'
		code += '	' * tab_level + '\n'
		code += '	' * tab_level + 'int i(0);\n'
		code += '	' * tab_level + 'for (vector<' + self.GetClassNameNum(1) + '>::const_iterator it = cv_List.begin(); it != cv_List.end(); ++it)\n'
		code += '	' * tab_level + '{\n'
		tab_level += 1
		code += '	' * tab_level + 'xml.Items[i] = it->GetXml_' + self.className + 'Info();\n'
		code += '	' * tab_level + '++i;\n'
		tab_level -= 1
		code += '	' * tab_level + '}\n'
		code += '	' * tab_level + 'return xml;\n'
		tab_level -= 1
		code += '	' * tab_level + '}\n'

		return code

	def PrintDotCppFile(self):
		code = '#include "stdafx.h"\n'
		code += '#include "FablinkException.h"\n'
		code += '#include "SuMsgErrorCode.h"\n'
		code += '#include "' + self.GetClassNameNum(1) + '.h"\n\n'
		code += '//this file was refactoried not yet....\n\n'
		code += self.construct.dotCppCode(0, self._init_AddTransaction(0)) + '\n'
		code += self.dotCppGetPtrFunction(0) + '\n'
		code += self.SetData2TableFunction(0, 'Create') + '\n'
		code += self.SetData2TableFunction(0, 'Modify') + '\n'
		code += self.Delete2TableFunction(0) + '\n'
		code += self.KXmlItemInfo(0) + '\n'
		code += '//----------------------------------------------------------------\n'
		code += self.CppListClassConstructor(0) + '\n'
		code += self.CppListClassInitislList(0) + '\n'
		code += self.CppListClassSize(0) + '\n'
		code += self.CppListClassKXmlItemList(0) + '\n'

		#for var in self.member_dict.values():
			#print(var.SetKXmlItem('xml'), var.GetXmlElemant(), var.GetKXmlItem('xml'))

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
		dot_h_include += '#include <vector>\n'
		for std_namespace in set(self.include_stdlib_list):
			dot_h_include += '#include <' + std_namespace + '>\n'
		return dot_h_include

	def HUsingNameSpace(self):
		dot_h_using_namespace = ''
		dot_h_using_namespace += 'using std::vector;\n'
		for namespace in set(self.using_namespace):
			dot_h_using_namespace += 'using ' + namespace + ';\n'
		return dot_h_using_namespace

	def ditHTableBaseEvent(self, tab_level):
		code = ''
		code += '	' * tab_level + 'void CreateToTable(KXmlItem& m_XmlInfo);\n'
		code += '	' * tab_level + 'void ModifyToTable(KXmlItem& m_XmlInfo);\n'
		code += '	' * tab_level + 'void Delete();\n'
		return code

	def HInfoClassCode(self, tab_level):
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
		out += '	' * tab_level + 'KXmlItem GetXml_' + self.className + 'Info(const string& m_InfoName) const;\n'
		tab_level -= 1
		out += '};\n'
		return out

	def HListClassCode(self, tab_level):
		out =''
		out += 'class ' + self.GetClassNameListNum(1) + '\n'
		out += '{\n'
		tab_level += 1
		out += '	' * tab_level + 'unsigned int cv_TotalFilterObj;\n'
		out += '	' * tab_level + 'KDoTransaction* cv_Transaction;\n'
		out += '	' * tab_level + 'vector<' + self.GetClassNameNum(1) + '> cv_List;\n'
		out += '	' * tab_level + 'void InitialList(list<KDo' + self.className + '*>& m_List);\n'
		out += 'public:\n'
		out += '	' * tab_level + self.GetClassNameListNum(1) + '(const FilterType& m_FilterType, const QueryByPaging1& m_Filter, KDoTransaction* const m_Transaction = 0);\n'
		out += '	' * tab_level + 'const unsigned int& Size() const;\n'
		out += '	' * tab_level + 'KXmlItem GetXml_' + self.className + 'List(const string& m_ListName) const;\n'
		tab_level -= 1
		out += '};\n'
		return out

	def PrintDotHFile(self):
		dot_h_code  = '#ifndef ' + self.className + '_H\n'
		dot_h_code += '#define ' + self.className + '_H\n\n'
		dot_h_code += '//this file was refactoried not yet....\n'
		dot_h_code += self.HInclude() + '\n'
		dot_h_code += self.HUsingNameSpace() + '\n'
		dot_h_code += self.HInfoClassCode(0)
		dot_h_code += '//----------------------------------------------------------------\n'
		dot_h_code += self.HListClassCode(0)
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
	classX.Write2DotHFile('')
	classX.Write2DotCppFile('')
