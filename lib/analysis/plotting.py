import cPickle as pickle
import numpy as np
import pandas as pd
import os, csv, sys
from matplotlib import pyplot as plt
from datetime import datetime
import datetime as dt

authors={}

#Define directories
cwd = '/home/cwp/EMC/data/authors/'
filenames = os.listdir(cwd)

#Load files
for filename in filenames:
    with open(cwd+filename,'rb') as input:
        #print(filename[:-4])
        authors[filename[:-4]] = pickle.load(input)

def plotMonth(entry):
    # Load entry data
    entry.loadData()

    # Remove the '\r' at the end of all lines
    for day, dataList in entry.data.items():
        # Uncomment to display data in terminal
        #print(day, dataList)
        entry.data[day] = dataList[:-1]

    # Sort days
    days = sorted(entry.data.keys())
    times  = []
    finalData = []
    for day in days:
        dateString = entry.date+'-'+'{0:02d}'.format(int(day))
        data = entry.data[day]
        for i in range(len(data)):
            #if int(data[i]) >= 0:
                if i < 23:
                    fullTime = dateString+':'+'{0:02d}'.format(i+1)
                    dateObject = datetime.strptime(fullTime, '%Y-%m-%d:%H')
                    times.append(dateObject)
                    finalData.append(data[i])
                else:
                    fullTime = dateString+':'+'{0:02d}'.format(23)
                    dateObject = datetime.strptime(fullTime, '%Y-%m-%d:%H')
                    dateObject += dt.timedelta(hours=1)
                    times.append(dateObject)
                    finalData.append(data[i])

    finalData = np.ma.array(finalData)
    finalDataMasked = np.ma.masked_where(finalData == '-1', finalData)
    plt.plot(times, finalDataMasked)

def plotMonthWithSameDay(entry):
    # Load entry data
    entry.loadData()

    # Remove the '\r' at the end of all lines
    for day, dataList in entry.data.items():
        # Uncomment to display data in terminal
        #print(day, dataList)
        entry.data[day] = dataList[:-1]

    # Sort days
    days = sorted(entry.data.keys())
    for day in days:
        times  = []
        finalData = []
        dateString = entry.date+'-'+'{0:02d}'.format(int(day))
        data = entry.data[day]
        for i in range(len(data)):
            maxData = max(data)
            #if int(data[i]) >= 0:
                if i < 23:
                    fullTime = '2000-01-01'+':{0:02d}'.format(i+1)
                    dateObject = datetime.strptime(fullTime, '%Y-%m-%d:%H')
                    times.append(dateObject)
                    finalData.append(data[i]/max)
                else:
                    fullTime = '2000-01-01:23'
                    dateObject = datetime.strptime(fullTime, '%Y-%m-%d:%H')
                    dateObject += dt.timedelta(hours=1)
                    times.append(dateObject)
                    finalData.append(data[i])

        finalData = np.ma.array(finalData)
        finalDataMasked = np.ma.masked_where(finalData == '-1', finalData)
        plt.plot(times, finalDataMasked, 'b')

for name, observer in authors.items():
    dates = sorted(observer.data.keys())
    for date in dates:
        entry = observer.data[date]
        plotMonthWithSameDay(entry)
        plt.show()
