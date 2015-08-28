import xml.etree.ElementTree as ET
import XmlObj as XO
import XmlKDoMock as XKDo

tree = ET.ElementTree(file='DB.xml')
root = tree.getroot()

class_list = []
for class_element in root:
	#print(class_element.attrib["Name"])
	class_obj = XKDo.xml2Class(class_element.attrib["Name"])
	for member_var_element in class_element.iter(tag='Property'):
		#print('    ', member_var_element.attrib["Type"], member_var_element.attrib["Name"])
		class_obj.AddMemberVariable(member_var_element.attrib["Type"], member_var_element.attrib["Name"])
	class_list.append(class_obj);

for obj in class_list:
	obj.Write2File('KDataObject\\')