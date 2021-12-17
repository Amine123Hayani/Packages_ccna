import struct

partitionTypes = {
    0x05: 'Windows Etendue',
    0x0F: 'Windows Etendue',
    0x07: 'Windows NTFS',
    0x82: 'Linux SWAP',
    0x83: 'Linux Native',
    0xEE: 'GPT',
    0xED: 'GPT',
    0x27: 'Recovery',
    0x00: 'Vide'
}

class Partition:
    def __init__(self, entry):
        self.type = struct.unpack('<B', entry[4:5])[0]# get type (1 octect) from the 4 pos
        self.startLBA = struct.unpack('<L', entry[8:12])[0] # logical block adressing : L 4 bytes
        self.size = struct.unpack('<L',entry[12:16])[0]

    def getType(self):
        return partitionTypes[self.type]

    def getSize(self):
        return Partition.unit(self.size * 512) # par secteur on octet

    def isGPT(self):
        return self.type == 0xEE or self.type == 0xED

    def isExtended(self):
        return self.type == 0x05 or self.type == 0x0F

    @staticmethod
    def unit(size):
        if size<10**6:
            return (size / 10 ** 3, " Ko")
        if 10**6<size<10**9:
            return (size/10 ** 6," Mo")
        if 10**9<size<10**12:
            return (size / 10 ** 9, " Go")
        else :
            return (size / 10 ** 12," To")

