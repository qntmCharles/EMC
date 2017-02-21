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

plotDict = {}
errsDict = {}

ind = np.arange(12)
width=0.35

colors = ['b','r','g']
ylabs = ["Peak hour", "Detection count", "Detection count", "Detection count", "Standard error", "Sum of parameter covariance", "Skewness"]
titles = ["Mean peak hour for diurnal shift", "Mean hourly detection count", "Maximum hourly detection count", "Minimum hourly detection count", "Mean standard error in detection count", "Measure of fit to an optimised sine curve", "Skew of daily counts"]


for index in range(7):
    fig, ax = plt.subplots(figsize=(12,9))
    for name in names:
        plotDict[name] = [dataList[i][name] for i in range(len(dataList))]
        errsDict[name] = [errsList[i][name] for i in range(len(errsList))]

    rects = ax.bar(ind+width*0.5, plotDict[names[index]], width, yerr = errsDict[names[index]],color='b', error_kw=dict(ecolor='k'))

    ax.set_xticks(ind+width)
    ax.set_xticklabels(antennas, rotation=16, ha='right')
    #ax.set_title(titles[index]+", averaged for antenna type", y=1.05)
    ax.set_xlabel("Antenna type", fontsize=20)
    ax.set_ylabel(ylabs[index], fontsize=20)
    #plt.show()
    plt.savefig('/home/cwp/EMC/plots/variation/antenna/'+names[index], dpi=500)
    plt.clf()
#plt.savefig('/home/cwp/EMC/plots/variation/antenna/meanmaxmin.png', dpi=500)
