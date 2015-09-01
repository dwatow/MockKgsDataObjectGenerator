import xml.etree.ElementTree as ET
import XmlObj as XO
import XmlKDoMock as XKDo

tree = ET.ElementTree(file='DB.xml')
root = tree.getroot()

kdo_class_list = []
for class_element in root:
	#print(class_element.attrib["Name"])
	kdo_class_obj = XKDo.xml2Class(class_element.attrib["Name"])
	for class_chirld in class_element:
		if class_chirld.tag == 'References':
			for reference_element in class_chirld:
				#print('    ', reference_element.attrib['Name'], reference_element.attrib['Type'], reference_element.attrib['Relation'])
				kdo_class_obj.AddReference(reference_element.attrib['Name'], reference_element.attrib['Type'].lower(), reference_element.attrib['Relation'])
		if class_chirld.tag == 'Properties':
			for property_element in class_chirld:
				#print('    ', property_element.attrib["Type"], property_element.attrib["Name"])
				kdo_class_obj.AddMemberVariable(property_element.attrib["Type"], property_element.attrib["Name"])

	kdo_class_list.append(kdo_class_obj);

print('--------------------------')
for obj in kdo_class_list:
	#obj.Write2File('KDataObject\\')
	obj.Write2DotHFile('KDataObject\\')
	obj.Write2DotCppFile('KDataObject\\')
print('----------生成TableObj----------')
table_obj_list = []
for class_element in root:
	#print(class_element.attrib["Name"])
	table_obj_class_obj = XO.xml2Class(class_element.attrib["Name"])
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
	#obj.Write2File('KDataObject\\')
	obj.Write2DotHFile('TableObj\\')
	obj.Write2DotCppFile('TableObj\\')