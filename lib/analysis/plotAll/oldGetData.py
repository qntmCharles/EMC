from __future__ import division
import numpy as np
from matplotlib import pyplot as plt
from plotting import plotFullMonth
import datetime as dt
from datetime import datetime
import os
import cPickle as pickle

authors = {}
allData = {}
allCounts = {}

#Define directories
cwd = '/home/cwp/EMC/data/authors/'
filenames = os.listdir(cwd)

#Load files
for filename in filenames:
    with open(cwd+filename,'rb') as input:
        #print(filename[:-4])
        authors[filename[:-4]] = pickle.load(input)

print(len(authors.keys()))
raw_input()

#Run through observers
for name, observer in authors.items():
    try:
        dates = sorted(observer.data.keys())

        for date in dates:
            entry = observer.data[date]
            entry.loadData()

            if entry.date.split('-')[1] in ['09', '04', '06', '11']:
                if len(entry.data.keys()) == 31:
                    del entry.data['31']

            if entry.date.split('-')[1] == '02':
                if entry.date.split('-')[0] in ['2004','2008','2012','2016']:
                    if len(entry.data.keys()) == 30:
                        del entry.data['30']
                    if len(entry.data.keys()) == 31:
                        del entry.data['30']
                        del entry.data['31']
                else:
                    if len(entry.data.keys()) == 31:
                        del entry.data['29']
                        del entry.data['30']
                        del entry.data['31']
                    if len(entry.data.keys()) == 30:
                        del entry.data['30']
                        del entry.data['29']
                    if len(entry.data.keys()) == 29:
                        del entry.data['29']

            for day, dataList in entry.data.items():
                entry.data[day] = dataList[:-1]

        keys = ['{0:02d}'.format(int(x)) for x in entry.data.keys()]

        days = sorted(keys)
        for day in days:
            dateString = entry.date+'-'+'{0:02d}'.format(int(day))
            try:
                data = entry.data[day]
            except:
                data = entry.data[str(int(day))]
            for i in range(len(data)):
                if int(data[i]) >= 0:
                    if i<23:
                        fullTime = dateString+':'+'{0:02d}'.format(i+1)
                        dateObject = datetime.strptime(fullTime, '%Y-%m-%d:%H')

                    else:
                        fullTime = dateString+':'+'{0:02d}'.format(23)
                        dateObject = datetime.strptime(fullTime, '%Y-%m-%d:%H')
                        dateObject += dt.timedelta(hours=1)

                    if dateObject not in allData.keys():
                        allData[dateObject] = int(data[i])
                        allCounts[dateObject] = 1

                    else:
                        allData[dateObject] += int(data[i])
                        allCounts[dateObject] += 1
                    print(dateObject)
                    print(data[i])

    except Exception as e:
        print(e)

keys = sorted(allData.keys())
plotData = []
plotTimes = []

for key in keys:
    plotData.append(allData[key]/allCounts[key])
    plotTimes.append(key)

with open('/home/cwp/EMC/lib/analysis/plotData.txt', 'w') as f:
    for item in plotData:
        f.write(str(item)+'\n')
    f.close()

with open('/home/cwp/EMC/lib/analysis/plotTimes.txt', 'w') as f:
    for item in plotTimes:
        f.write(str(item)+'\n')
    f.close()

plt.plot(plotTimes, plotData)
plt.show()
