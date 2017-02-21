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

antennae = {'yagi':'Yagi', 'dipole':'Dipole', 'gp':'Ground Plane', 'vertical':'Vertical', 'discone':'Discone', 'turnstile':'Turnstile', 'logperiodic':'Log Periodic', 'fullwaveloop':'Full Wave Loop', 'jpole':'J-Pole', 'diamond':'Diamond', 'quad':'Quadrifilar', 'omni':'Omnidirectional'}

for i in range(len(antennasOrdered)):
    antennasOrdered[i] = antennae[antennasOrdered[i]]

indices = np.arange(len(antennasOrdered))
width = 0.6
fig, ax = plt.subplots()
rects1 = ax.bar(indices+width, countsOrdered, width, color='b', align='center')
ax.set_xticks(indices+width)
ax.set_xticklabels(antennasOrdered, rotation = 25, ha='right')
#plt.title('Antenna usage', y=1.05)
ax.set_xlabel('Antenna type', fontsize = 15)
ax.set_ylabel('Number of observers', fontsize = 15)

plt.tight_layout()

plt.savefig('/home/cwp/EMC/plots/general/antennas.png', dpi=500)

"""
    dC, hC = analyseAuthor(authorobj)

    #For IRC stuff
    with open('/home/cwp/EMC/stats/'+name+'.txt', 'w') as f:
        f.write(str(hC)+';')
        f.write(str(dC))
        f.close()
"""
