import xml.etree.ElementTree as ET
import XmlObj as XO
import XmlKDoMock as XKDo

tree = ET.ElementTree(file='DB.xml')
root = tree.getroot()

class_list = []
for class_element in root:
	#print(class_element.attrib["Name"])
	class_obj = XKDo.xml2Class(class_element.attrib["Name"])
	for class_chirld in class_element:
		if class_chirld.tag == 'Properties':
			for property_element in class_chirld:
				#print('    ', property_element.attrib["Type"], property_element.attrib["Name"])
				class_obj.AddMemberVariable(property_element.attrib["Type"], property_element.attrib["Name"])

	class_list.append(class_obj);


print('--------------------------')
for obj in class_list:
	#obj.Write2File('KDataObject\\')
	obj.Write2DotHFile('KDataObject\\')
	obj.Write2DotCppFile('KDataObject\\')
