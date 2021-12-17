from Mbr import Mbr
from matplotlib import pyplot as plt

mbr = Mbr()
mbr.parted()
"""labels = []
sizes = []
for p in mbr.gptPartitions:
    labels.append(p.getName())
    sizes.append(p.getSize()[0])
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=0)
plt.show()
"""