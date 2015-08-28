class xmlVariable:
    def __init__(self, type, name):
        self.type = type
        self.name = name
    def __str__(self):
       return str(self.type) + ' ' + str(self.name) + ';'

class xml2Class:
    def __init__(self, name):
        self.memberlist = []
        self.className = name

    def AddMemberVariable(self, type, name):
        self.memberlist.append(xmlVariable(type, name))

    def GetPrint(self):
       for i in self.memberlist:
          print (i)

    def __str__(self):
        out = '#ifndef ' + self.className.upper() + '_H\n'
        out += '#define ' + self.className.upper() + '_H\n\n'
        out += self.Code()
        out += '\n#endif'
        return out

    def Code(self):
        out = 'class ' + self.className + '\n{\npublic:\n'
        for member_var in self.memberlist:
            out += '    ' + str(member_var) + '\n'
        return out + '};\n'

    def Write2File(self):
        filename = 'KDo' + self.className + '.h'
        file = open(filename, 'w')
        file.write(str(self))
        file.close()

if __name__ == "__main__":
   classX = xml2Class("Employee")
   classX.AddMemberVariable("string", "Id")
   classX.AddMemberVariable("string", "SystemKey")
   classX.GetPrint()