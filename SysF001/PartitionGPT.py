from struct import unpack
from Partition import Partition


class GptPartition:
    def __init__(self, entry):
        self.type = unpack('<4L',entry[0:16])[0]
        self.guid = entry[16:32]
        self.start = unpack('<2L', entry[32:40])[0] * 512
        self.end = unpack('<2L',entry[40:48])[0] * 512
        self.attributes = entry[48:56]
        self.name = entry[56:128].decode('utf-16').rstrip('\x00')#eleminer les caracteres 0 #hexa to utf16

    def getName(self):
        return self.name

    def getStart(self):
        return Partition.unit(self.start)

    def getSize(self):
        return Partition.unit(self.end - self.start)

    def __str__(self):
        return str(self.getStart()[0]) + self.getStart()[1] + "\t\t\t" + str(self.getSize()[0]) + self.getSize()[1] +\
               "\t\t\t" + self.getName()
