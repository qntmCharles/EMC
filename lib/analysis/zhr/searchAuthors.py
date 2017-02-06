import cPickle as pickle
import numpy as np
import os, csv
from matplotlib import pyplot as plt
from datetime import datetime
import datetime as dt

authors = {}

def display(entry, observerName):
    entry.loadData()
    plotData = []
    plotTimes = []
    for day in sorted(entry.data.keys()):
        dayData = entry.data[day]
        for i in range(len(dayData)):
            if dayData[i] != '\r':
                try:
                    if i < 23:
                        dateString = entry.date+'-'+day+':'+'{0:02d}'.format(i)
                        plotTimes.append(\
                                datetime.strptime(dateString, "%Y-%m-%d:%H"))
                        plotData.append(\
                                float(dayData[i]) if dayData[i] != '-1' else None)
                    else:
                        dateString = entry.date+'-'+day+':'+'{0:02d}'.format(23)
                        dateObject = datetime.strptime(dateString, "%Y-%m-%d:%H")
                        dateObject += dt.timedelta(hours=1)
                        plotTimes.append(dateObject)
                        plotData.append(\
                                float(dayData[i]) if dayData[i] != '-1' else None)
                except:
                    pass
    plt.title('Observer: %s' %(observerName))
    plt.plot(plotTimes, plotData, 'b')

# Get directories
cwd = '/home/cwp/EMC/data/authors/'
filenames = os.listdir(cwd)

# Load files
for filename in filenames:
    with open(cwd+filename, 'rb') as input:
        authors[filename[:-4]] = pickle.load(input)

selectedObservers = {}
count = 0
for name, observer in authors.items():
    datesList = []
    for date, entry in observer.data.items():
        if date[-2:] == '10':
            if (date[:-2]+'11' in observer.data.keys()):# and (date[:-2]+'09' in observer.data.keys()):
                if name not in selectedObservers.keys():
                    selectedObservers[name] = [date[:-2]+'10']
                else:
                    selectedObservers[name].append(date[:-2]+'10')

for name, dates in selectedObservers.items():
    with open('/home/cwp/EMC/lib/analysis/zhr/orionids/'+name+'.txt', 'w') as f:
        for date in dates:
            f.write(date)
            f.write('\n')
        f.close()
