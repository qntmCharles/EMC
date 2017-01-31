from matplotlib import pyplot as plt
from math import floor
import numpy as np
import csv, math, statistics

names=['peak','mean','max','min','err','fit','skew']

finalData = {}
errsList = []
dataList = []
for i in range(12):
    dataList.append({})
    errsList.append({})
    for name in names:
        dataList[i][name] = []

antennaDict = {'diamond':0, 'dipole':1, 'discone':2, 'fullwaveloop':3, 'gp':4, 'jpole':5, 'logperiodic':6, 'omni':7, 'quad':8, 'turnstile':9, 'vertical':10, 'yagi':11}
antennas = ['Diamond', 'Dipole', 'Discone', 'Full wave loop', 'Ground plane', 'J-pole', 'Log periodic', 'Omni', 'Quad', 'Turnstile', 'Vertical', 'Yagi']

with open('/home/cwp/EMC/lib/analysis/variation/antenna/data.csv','r') as f:
    reader = list(csv.reader(f, delimiter='\t'))
    reader = reader[1:]
    for row in reader:
        for i in range(1, 8):
            try:
                dataList[antennaDict[row[0]]][names[i-1]].append(float(row[i]))
            except:
                pass

for i in range(len(dataList)):
    for analysisType in dataList[i]:
        errsList[i][analysisType] = statistics.stdev(dataList[i][analysisType])/math.sqrt(len(dataList[i][analysisType]))
        dataList[i][analysisType] = statistics.mean(dataList[i][analysisType])

ind = np.linspace(0, 23, 12)
width = 0.25

plotDict = {}
errsDict = {}

fig, ax = plt.subplots()
for name in names:
    plotDict[name] = [dataList[i][name] for i in range(len(dataList))]
    errsDict[name] = [errsList[i][name] for i in range(len(errsList))]

colors=['b', 'g', 'r', 'c', 'm', 'y', 'k']
rects=[]
for i in range(len(plotDict.keys())):
    rects.append(ax.bar(ind+(width*(i)), plotDict[names[i]], width, yerr = errsDict[names[i]], color=colors[i], error_kw=dict(ecolor='k')))

ax.legend([x for x in rects], names)
ax.set_xticks(ind+width/2)
ax.set_xticklabels(antennas, rotation=15)
ax.set_xlim(0, 24)
ax.set_ylim(0, 700)
plt.show()
