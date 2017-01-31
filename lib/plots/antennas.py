import cPickle as pickle
import numpy as np
import os, csv
from matplotlib import pyplot as plt

authors={}

#Define directories
cwd = '/home/cwp/EMC/data/authors/'
filenames = os.listdir(cwd)

#Load files
for filename in filenames:
    with open(cwd+filename,'rb') as input:
        #print(filename[:-4])
        authors[filename[:-4]] = pickle.load(input)
base = '/home/cwp/EMC/lib/analysis/variation/antenna/'
filesList = os.listdir('/home/cwp/EMC/lib/analysis/variation/antenna/')

def fileLength(filename):
    with open(filename, 'r') as f:
        return len(f.readlines())

filesList.remove('misc.txt')

lengths = {}
for file in filesList:
    if file.split('.')[-1] == 'txt':
        lengths[file.split('.')[0]] = fileLength(base+file)

histList = []
for key, value in lengths.items():
    histList.append((key,value))

antennasOrdered = []
countsOrdered = []
for x in sorted(histList, key=lambda tup: tup[1]):
    antennasOrdered.append(x[0])
    countsOrdered.append(x[1])

antennasOrdered.reverse()
countsOrdered.reverse()
print(antennasOrdered)
print(countsOrdered)

indices = np.arange(len(antennasOrdered))
width = 0.6
fig, ax = plt.subplots()
rects1 = ax.bar(indices+width, countsOrdered, width, color='b', align='center')
ax.set_xticks(indices+width)
ax.set_xticklabels(antennasOrdered, rotation = 45, ha='right')
fig.suptitle('Locations of observers (where known)', fontsize = 15, fontweight = 'bold')
ax.set_xlabel('Country', fontsize = 15)
ax.set_ylabel('Number of observers', fontsize = 15)

plt.tight_layout()

plt.show()

"""
    dC, hC = analyseAuthor(authorobj)

    #For IRC stuff
    with open('/home/cwp/EMC/stats/'+name+'.txt', 'w') as f:
        f.write(str(hC)+';')
        f.write(str(dC))
        f.close()
"""
