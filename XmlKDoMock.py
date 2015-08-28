class xmlVariable:
    def CovertType(self, type):
        if type == 'u4':
            return 'unsigned int'
        elif type == 'i4':
            return 'int'
        elif type == 'f4':
            return 'float'
        else:
            return type

    def __init__(self, type, name):
        self.type = self.CovertType(type.lower())
        self.name = name
    def __str__(self):
       return str(self.type) + ' ' + str(self.name) + ';'

class xml2Class:
    def __init__(self, name):
        self.memberlist = []
        self.className = 'KDo' + name

    def AddMemberVariable(self, type, name):
        self.memberlist.append(xmlVariable(type, name))

    def GetPrint(self):
       for i in self.memberlist:
          print (i)

    def __str__(self):
        out = '#ifndef ' + self.className + '_H\n'
        out += '#define ' + self.className + '_H\n\n'
        out += self.Code()
        out += '\n#endif'
        return out

    def Code(self):
        out = 'class ' + self.className + ' : public KDataPersistentObject' + '\n'
        out += '{\npublic:\n'
        out += '    friend class KDoFactory;\n'

        for member_var in self.memberlist:
            out += '    ' + str(member_var) + '\n'
        return out + '};\n'

    def Write2File(self, filtPath):
        fil_path_ename = filtPath + '\\' + self.className + '.h'
        file = open( fil_path_ename, 'w')
        file.write(str(self))
        file.close()

if __name__ == "__main__":
   classX = xml2Class("Employee")
   classX.AddMemberVariable("string", "Id")
   classX.AddMemberVariable("string", "SystemKey")
   classX.GetPrint()