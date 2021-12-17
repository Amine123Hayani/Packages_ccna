import platform,struct
from Partition import Partition
from PartitionGPT import GptPartition

diskName = {
    'Windows': '\\\\.\\PHYSICALDRIVE0',
    'Linux': '/dev/sda',
    'Darwin': '/dev/disk0'
}


class Mbr:
    def __init__(self):
        self.diskPlatform = diskName[platform.system()]
        disk = open(self.diskPlatform, 'rb')
        self.mbr = disk.read(512)
        disk.close()
        self.magicNumber = struct.unpack('<H', self.mbr[510:512])[0] #2 octet
        self.bootLoader = struct.unpack('446B', self.mbr[0:446])

        self.partitions = []
        self.partitions.append(Partition(self.mbr[446:462]))
        self.partitions.append(Partition(self.mbr[462:478]))
        self.partitions.append(Partition(self.mbr[478:494]))
        self.partitions.append(Partition(self.mbr[494:510]))

        self.gptPartitions = []

    def isMBR(self):
        return self.magicNumber == 0xaa55

    def parted(self):
        numPart = 0
        for p in self.partitions:
            if p.getType() != 'Vide':
                if p.isGPT():
                    self.processGPT(p)
                    break
                if p.isExtended():
                    Mbr.processEBR(p)
                print('%d\t\t%s\t\t%.3f %s ' %(numPart, p.getType(), p.getSize()[0],p.getSize()[1]))
            numPart += 1

    def processGPT(self,partition):
        d = open(self.diskPlatform, 'rb')
        d.seek(1024)
        entry = d.read(128*128)
        d.close()
        self.gptPartitions = []
        for i in range(0,128*128,128):
            p = GptPartition(entry[i:i+128])
            if p.type == 0:
                break
            self.gptPartitions.append(p)
            print(p)

    @staticmethod
    def processEBR(partition):
        pass
