
class References:
	def __init__(self, my_class_name, rel_class_name, ref_type, ref_relation):
		self.my_class_name = my_class_name
		self.rel_class_name = rel_class_name
		self.is_rel_list = False
		self._init_type(ref_type)
	'''
		比較
		Type="Unique"
		Type="Link"

		    <Class Name="Organization" ParentClass="">
		        <References>
		            <Reference Name="CalendarBelongRelation" Type="Unique" Relation="Link"/>
		        </References>
		class KDoOrganization
		        KDoCalendarBelongRelation* CalendarBelongRelation;
		class KDoCalendarBelongRelation
		        KDoOrganization* Organization;

		    <Class Name="Tool" ParentClass="">
		        <References>
		            <Reference Name="ToolAlarmGroup" Type="Link" Relation="Link"/>
		        </References>
		class KDoTool
		        KDoToolAlarmGroup* ToolAlarmGroup;

		class KDoToolAlarmGroup
				list<KDoTool*> ToolCollection;

	'''
	def _init_type(self, ref_type):
		if ref_type == 'Unique':  #一對一
			self.is_rel_list = False
		elif ref_type == 'Link':  #一對多, 別人那還要給Add, Remove, RemoveAll, DeleteAll
			self.is_rel_list = True
	'''
		    <Class Name="Area" ParentClass="">
		        <References>
		            <Reference Name="Layout" Type="Link" Relation="Link"/>
		        </References>
		class KDoArea
		        KDoLayout* Layout;


		    <Class Name="AreaPoint" ParentClass="">
		        <References>
		            <Reference Name="Area" Type="Link" Relation="Has"/>
		        </References>
		class KDoAreaPoint
				KDoArea* Area;

			#此屬性無需關注
			def _init_relation(self, ref_relation):
				if ref_relation == 'Has':
					pass
				elif ref_relation == 'Link':
					pass
	'''
	def RelClassName(self):
		return self.rel_class_name
	######
	def MyDotHCode(self):
		return 'KDo' + self.rel_class_name + ' *' + self.rel_class_name + ';'

	def MyInitDotCppCode(self):
		code = ''
		code += self.rel_class_name + '= new ' + 'KDo' + self.rel_class_name + '();'
		return code
	######
	def MyBeforeClass(self):
		return 'class KDo' + self.rel_class_name + ';'

	def RelBeforeClass(self):
		return 'class KDo' + self.my_class_name + ';'
	######
	def RelDotHCode(self):
		if self.is_rel_list is True:
			return 'list<KDo' + self.my_class_name + '*> ' + self.my_class_name + 'Collection;'
		else:
			return 'KDo' + self.my_class_name + '* ' + self.my_class_name + ';'

	def RelDotHField_Syskey(self):
		return 'static const string Field_' + self.rel_class_name + '_SystemKey;'

#	def RelDotCppField(self):
#		return 'static const string Field_' + self.my_class_name + '_SystemKey;'

	def RelInitDotCppCode(self):
		code = ''
		if self.is_rel_list is not True:
			code += self.my_class_name + ' = new ' + 'KDo' + self.my_class_name + '();'
		return code
	######
	def RelDotHCollectionFunction(self):
		code = ''
		if self.is_rel_list is True:
			tab_level = '	'
			code += '\n'
			code += tab_level + 'bool Add' + self.my_class_name + '( KDo' + self.my_class_name + '* m_Object);\n'
			code += tab_level + 'bool Remove' + self.my_class_name + '( KDo' + self.my_class_name + '* m_Object);\n'
			code += tab_level + 'bool RemoveAll' + self.my_class_name + '();\n'
			code += tab_level + 'bool DeleteAll' + self.my_class_name + '();\n'
		return code

	def RelDotCppCollectionFunction(self):
		code = ''
		if self.is_rel_list is True:
			tab_level = '	'
			code += '\n'
			code += 'bool ' + self.rel_class_name + '::Add' + self.my_class_name + '( KDo' + self.my_class_name + '* m_Object)\n{\n}\n'
			code += 'bool ' + self.rel_class_name + '::Remove' + self.my_class_name + '( KDo' + self.my_class_name + '* m_Object)\n{\n}\n'
			code += 'bool ' + self.rel_class_name + '::RemoveAll' + self.my_class_name + '()\n{\n}\n'
			code += 'bool ' + self.rel_class_name + '::DeleteAll' + self.my_class_name + '()\n{\n}\n'
		return code


class ExtendReferences:  #一對多
	def __init__(self, my_class_name, source_name, target_name, rel_class_name, relation):
		self.my_class_name = my_class_name
		self.rel_class_name = rel_class_name
		self.source_name = source_name
		self.target_name = target_name
		#self.relation = relation
	'''
	    <Class Name="BCPrintPagesRulParameter" ParentClass="">
	        <ExtendReferences>
	            <Reference SourceName="InputLabel" TargetName="ParameterList" ClassName="StationInputLabel" Relation="Has"/>
	            <Reference SourceName="OutputLabel" TargetName="ParameterList" ClassName="StationOutputLabel" Relation="Has"/>
	        </ExtendReferences>

	class KDoBCPrintPagesRulParameter
	        KDoStationInputLabel* InputLabel;
	        KDoStationOutputLabel* OutputLabel;

	class KDoStationInputLabel
			list<KDoBCPrintPagesRulParameter*> ParameterList;
	class KDoStationOutputLabel
			list<KDoBCPrintPagesRulParameter*> ParameterList;

	'''
	def RelClassName(self):
		return self.rel_class_name
	def MyDotHCode(self):
		return 'KDo' + self.rel_class_name + ' *' + self.source_name + ';'

#	def RelDotCppField(self):
#		return 'static const string Field_' + self.rel_class_name + '_SystemKey;'

	def MyInitDotCppCode(self):
		code = ''
		code += self.source_name + ' = new ' + 'KDo' + self.rel_class_name + '();'
		return code
	def MyBeforeClass(self):
		return 'class KDo' + self.rel_class_name + ';'
	def RelBeforeClass(self):
		return 'class KDo' + self.my_class_name + ';'
	def RelDotHCode(self):
		return 'list<KDo' + self.my_class_name + '*> ' + self.target_name + ';'
	def RelDotHCollectionFunction(self):
		code = ''
		tab_level = '	'
		code += '\n'
		code += tab_level + 'bool Add' + self.target_name + '( KDo' + self.my_class_name + '* m_Object);\n'
		code += tab_level + 'bool Remove' + self.target_name + '( KDo' + self.my_class_name + '* m_Object);\n'
		code += tab_level + 'bool RemoveAll' + self.target_name + '();\n'
		code += tab_level + 'bool DeleteAll' + self.target_name + '();\n'
		return code

	def RelDotCppCollectionFunction(self):
		code = ''
		tab_level = '	'
		code += '\n'
		code += 'bool ' + self.rel_class_name + '::Add' + self.target_name + '( KDo' + self.my_class_name + '* m_Object)\n{\n}\n'
		code += 'bool ' + self.rel_class_name + '::Remove' + self.target_name + '( KDo' + self.my_class_name + '* m_Object)\n{\n}\n'
		code += 'bool ' + self.rel_class_name + '::RemoveAll' + self.target_name + '()\n{\n}\n'
		code += 'bool ' + self.rel_class_name + '::DeleteAll' + self.target_name + '()\n{\n}\n'
		return code
'''
    <Class Name="DispatchListStatusRelation" ParentClass="">
        <ExternalReferences>
            <Reference SourceName="ReleaseReason" TargetName="ReleaseStatus" ClassName="ManufactureProcessReleaseHoldReason"/>
            <Reference SourceName="HoldReason" TargetName="HoldStatus" ClassName="ManufactureProcessHoldReason"/>
        </ExternalReferences>

class KDoDispatchListStatusRelation
		list<KDoManufactureProcessReleaseHoldReason*> ReleaseReason;
		list<KDoManufactureProcessHoldReason*> HoldReason;

class KDoManufactureProcessHoldReason
		list<KDoDispatchListStatusRelation*> HoldStatus;
class KDoManufactureProcessReleaseHoldReason
		list<KDoDispatchListStatusRelation*> ReleaseStatus;
'''
class ExternalReferences:  #多對多
	def __init__(self, my_class_name, source_name, target_name, rel_class_name):
		self.my_class_name = my_class_name
		self.rel_class_name = rel_class_name
		self.source_name = source_name
		self.target_name = target_name

	def RelClassName(self):
		return self.rel_class_name
	def MyDotHCode(self):
		return 'list<KDo' + self.rel_class_name + '*> ' + self.source_name + ';'
	def MyDotHCollectionFunction(self):
		code = ''
		tab_level = '	'
		code += '\n'
		code += tab_level + 'bool Add' + self.source_name + '( KDo' + self.rel_class_name + '* m_Object);\n'
		code += tab_level + 'bool Remove' + self.source_name + '( KDo' + self.rel_class_name + '* m_Object);\n'
		code += tab_level + 'bool RemoveAll' + self.source_name + '();\n'
		code += tab_level + 'bool DeleteAll' + self.source_name + '();\n'
		return code

	def MyDotCppCollectionFunction(self):
		code = ''
		tab_level = '	'
		code += '\n'
		code += 'bool ' + self.rel_class_name + '::Add' + self.source_name + '( KDo' + self.rel_class_name + '* m_Object)\n{\n}\n'
		code += 'bool ' + self.rel_class_name + '::Remove' + self.source_name + '( KDo' + self.rel_class_name + '* m_Object)\n{\n}\n'
		code += 'bool ' + self.rel_class_name + '::RemoveAll' + self.source_name + '()\n{\n}\n'
		code += 'bool ' + self.rel_class_name + '::DeleteAll' + self.source_name + '()\n{\n}\n'
		return code
	def MyBeforeClass(self):
		return 'class KDo' + self.rel_class_name + ';'
	def RelBeforeClass(self):
		return 'class KDo' + self.my_class_name + ';'
	def RelDotHCode(self):
		return 'list<KDo' + self.my_class_name + '*> ' + self.target_name + ';'
	def RelDotHCollectionFunction(self):
		code = ''
		tab_level = '	'
		code += '\n'
		code += tab_level + 'bool Add' + self.target_name + '( KDo' + self.my_class_name + '* m_Object);\n'
		code += tab_level + 'bool Remove' + self.target_name + '( KDo' + self.my_class_name + '* m_Object);\n'
		code += tab_level + 'bool RemoveAll' + self.target_name + '();\n'
		code += tab_level + 'bool DeleteAll' + self.target_name + '();\n'
		return code

	def RelDotCppCollectionFunction(self):
		code = ''
		tab_level = '	'
		code += '\n'
		code += 'bool ' + self.rel_class_name + '::Add' + self.target_name + '( KDo' + self.my_class_name + '* m_Object)\n{\n}\n'
		code += 'bool ' + self.rel_class_name + '::Remove' + self.target_name + '( KDo' + self.my_class_name + '* m_Object)\n{\n}\n'
		code += 'bool ' + self.rel_class_name + '::RemoveAll' + self.target_name + '()\n{\n}\n'
		code += 'bool ' + self.rel_class_name + '::DeleteAll' + self.target_name + '()\n{\n}\n'
		return code
