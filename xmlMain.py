import xml.etree.ElementTree as ET
import XmlObj as XmlTableObj
import XmlKDoMock as XmlKDataObject
from XmlKDoMock import xml2Class as xml2class
from xml2.references import References as xml2ref
from xml2.references import ExtendReferences as xml2extdref
from xml2.references import ExternalReferences as xml2extlref

tree = ET.ElementTree(file='DB.xml')
root = tree.getroot()

kdo_class_list = {}
for class_element in root:
	kdo_class_obj = xml2class(class_element.attrib["Name"])
	kdo_class_list[ class_element.attrib["Name"] ] = kdo_class_obj

for class_element in root:
	#print(class_element.attrib["Name"])
	curr_class_name = class_element.attrib["Name"]
	kdo_class_obj = kdo_class_list[curr_class_name]
	for class_chirld in class_element:
		if class_chirld.tag == 'ExternalReferences':
			for external_reference_element in class_chirld:
				extl_obj = xml2extlref(curr_class_name, external_reference_element.attrib['SourceName'], external_reference_element.attrib['TargetName'], external_reference_element.attrib['ClassName'])
				kdo_class_obj.AddBeforeClass(extl_obj.MyBeforeClass())
				kdo_class_obj.AddReference(extl_obj.MyDotHCode())
				kdo_class_obj.AddCollectionFunction(extl_obj.MyDotHCollectionFunction())
				kdo_class_obj.AddRelListFunction(extl_obj.MyDotCppCollectionFunction())
				kdo_class_obj.AddInitRef(extl_obj.MyInitDotCppCode())

				rel_kdo_class_obj = kdo_class_list[extl_obj.RelClassName()]
				rel_kdo_class_obj.AddBeforeClass(extl_obj.RelBeforeClass())
				rel_kdo_class_obj.AddReference(extl_obj.RelDotHCode())
				rel_kdo_class_obj.AddCollectionFunction(extl_obj.RelDotHCollectionFunction())
				rel_kdo_class_obj.AddRelListFunction(extl_obj.RelDotCppCollectionFunction())
				rel_kdo_class_obj.AddInitRef(extl_obj.RelInitDotCppCode())
				kdo_class_list[extl_obj.RelClassName()] = rel_kdo_class_obj

		if class_chirld.tag == 'ExtendReferences':
			for extend_reference_element in class_chirld:
				extd_obj = xml2extdref(curr_class_name, extend_reference_element.attrib['SourceName'], extend_reference_element.attrib['TargetName'], extend_reference_element.attrib['ClassName'], extend_reference_element.attrib['Relation'])
				kdo_class_obj.AddBeforeClass(extd_obj.MyBeforeClass())
				kdo_class_obj.AddReference(extd_obj.MyDotHCode())
				kdo_class_obj.AddRefField(extd_obj.RelDotHField_Syskey())
				kdo_class_obj.AddInitRefField(extd_obj.RelDotCppField_Syskey())
				kdo_class_obj.AddInitRef(extd_obj.MyInitDotCppCode())

				rel_kdo_class_obj = kdo_class_list[extd_obj.RelClassName()]
				rel_kdo_class_obj.AddBeforeClass(extd_obj.RelBeforeClass())
				rel_kdo_class_obj.AddReference(extd_obj.RelDotHCode())

				rel_kdo_class_obj.AddCollectionFunction(extd_obj.RelDotHCollectionFunction())
				rel_kdo_class_obj.AddRelListFunction(extd_obj.RelDotCppCollectionFunction())
				kdo_class_list[extd_obj.RelClassName()] = rel_kdo_class_obj

		if class_chirld.tag == 'References':
			for reference_element in class_chirld:
				ref_obj = xml2ref(curr_class_name, reference_element.attrib['Name'], reference_element.attrib['Type'], reference_element.attrib['Relation'])
				kdo_class_obj.AddBeforeClass(ref_obj.MyBeforeClass())
				kdo_class_obj.AddReference(ref_obj.MyDotHCode())
				kdo_class_obj.AddInitRef(ref_obj.MyInitDotCppCode())
				if curr_class_name == 'ManufactureProcess':
					print(ref_obj.my_class_name)
				kdo_class_obj.AddRefField(ref_obj.RelDotHField_Syskey())
				kdo_class_obj.AddInitRefField(ref_obj.RelDotCppField_Syskey())

				rel_kdo_class_obj = kdo_class_list[ref_obj.RelClassName()]
				rel_kdo_class_obj.AddBeforeClass(ref_obj.RelBeforeClass())
				rel_kdo_class_obj.AddReference(ref_obj.RelDotHCode())
				rel_kdo_class_obj.AddCollectionFunction(ref_obj.RelDotHCollectionFunction())
				rel_kdo_class_obj.AddInitRef(ref_obj.RelInitDotCppCode())
				rel_kdo_class_obj.AddRelListFunction(ref_obj.RelDotCppCollectionFunction())
				kdo_class_list[ref_obj.RelClassName()] = rel_kdo_class_obj

		if class_chirld.tag == 'Properties':
			for property_element in class_chirld:
				#print('    ', property_element.attrib["Type"], property_element.attrib["Name"])
				kdo_class_obj.AddMemberVariable(property_element.attrib["Type"], property_element.attrib["Name"])
	kdo_class_list[curr_class_name] = kdo_class_obj



print('--------------------------')
for class_name, stub_obj in kdo_class_list.items():
	#stub_obj.Write2File('KDataObject\\')
	stub_obj.Write2DotHFile('KDataObject\\')
	stub_obj.Write2DotCppFile('KDataObject\\')
	#stub_obj.Write2DotHFile('')
	#stub_obj.Write2DotCppFile('')
print('----------生成TableObj----------')
table_obj_list = []
for class_element in root:
	#print(class_element.attrib["Name"])
	table_obj_class_obj = XmlTableObj.xml2Class(class_element.attrib["Name"])
	for class_chirld in class_element:
		#if class_chirld.tag == 'References':
			#for reference_element in class_chirld:
				##print('    ', reference_element.attrib['Name'], reference_element.attrib['Type'], reference_element.attrib['Relation'])
				#table_obj_class_obj.AddReference(reference_element.attrib['Name'], reference_element.attrib['Type'], reference_element.attrib['Relation'])
		if class_chirld.tag == 'Properties':
			for property_element in class_chirld:
				#print('    ', property_element.attrib["Type"], property_element.attrib["Name"])
				table_obj_class_obj.AddMemberVariable(property_element.attrib["Type"].lower(), property_element.attrib["Name"])

	table_obj_list.append(table_obj_class_obj);

print('--------------------------')
for obj in table_obj_list:
	#obj.Write2File('KDataObject')
	obj.Write2DotHFile('TableObj')
	obj.Write2DotCppFile('TableObj')
report = '生成' + str(len(table_obj_list)) + '個KDataObject.h檔案\n'
report += '生成' + str(len(table_obj_list)) + '個KDataObject.cpp檔案\n'
report += '生成' + str(len(table_obj_list)) + '個TableObj.h檔案\n'
report += '生成' + str(len(table_obj_list)) + '個TableObj.cpp檔案\n'
print(report)
'''檔案生成，資料夾要保留，才會順利生成。'''