import os, csv
from matplotlib import pyplot as plt
from datetime import datetime
import datetime as dt

showerObservers = {}
basedir = '/home/cwp/EMC/lib/analysis/zhr/'
showers = ['perseids', 'leonids', 'quadrantids', 'geminids', 'orionids', \
        'eta_aquariids']

def getObservers(filepath):
    base = filepath
    toReturn = {}

    for filename in os.listdir(filepath):
        toReturn[filename[:-4]] = []

        with open(base + filename, 'r') as f:
            for line in f.readlines():
                toReturn[filename[:-4]].append(line.split('\n')[0])

    return toReturn

for shower in showers:
    showerObservers[shower] = getObservers(basedir+shower+'/')


for shower, observers in showerObservers.items():
    for observer, observerDates in observers.items():
        plotData = []
        plotErr = []
        plotTimes = []
        try:
            with open(basedir+'data/'+shower+'/'+observer+'.txt', 'r') as f:
                readFile = list(csv.reader(f))
                for line in readFile:
                    plotData.append(float(line[1]))
                    plotErr.append(float(line[2]))
                    plotTimes.append(datetime.strptime(line[0], "%Y-%m-%d %H:%M:%S"))
        except Exception as e:
            print(e)

        plt.plot(plotTimes, plotData)
        plt.show()
