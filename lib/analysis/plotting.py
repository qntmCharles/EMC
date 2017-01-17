from __future__ import division
import cPickle as pickle
import numpy as np
import pandas as pd
import os, csv, sys, math
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

def plotFullMonth(entry, observer):
    # Load entry data
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


    # Remove the '\r' at the end of all lines
    for day, dataList in entry.data.items():
        # Uncomment to display data in terminal
        #print(day, dataList)
        entry.data[day] = dataList[:-1]

    keys = ['{0:02d}'.format(int(x)) for x in entry.data.keys()]

    # Sort days
    days = sorted(keys)
    times  = []
    xaxis = []
    finalData = []
    for day in days:
        dateString = entry.date+'-'+'{0:02d}'.format(int(day))
        try:
            data = entry.data[day]
        except:
            data = entry.data[str(int(day))]
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
    plt.xlabel('Date')
    plt.ylabel('Number of meteors detected')
    plt.xticks(rotation=15, ha="right", fontsize=9)
    #plt.title('Observer '+observer+', Date: '+entry.date)
    plt.title('Observer: '+observer)
    plt.subplots_adjust(top=0.93,bottom=0.12)
    plt.plot(times,finalDataMasked, 'b')

def plotMonthWithSameDay(entry, observer):
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
        finalDataMasked = []
        dateString = entry.date+'-'+'{0:02d}'.format(int(day))
        data = [int(x) for x in entry.data[day]]
        for i in range(len(data)):
            try:
                maxData = max(data)
                if int(data[i]) >= 0:
                    if i < 23:
                        fullTime = '2000-01-01'+':{0:02d}'.format(i+1)
                        dateObject = datetime.strptime(fullTime, '%Y-%m-%d:%H')
                        times.append(dateObject)
                        finalData.append(data[i]/maxData)
                        #finalData.append(data[i])
                    else:
                        fullTime = '2000-01-01:23'
                        dateObject = datetime.strptime(fullTime, '%Y-%m-%d:%H')
                        dateObject += dt.timedelta(hours=1)
                        times.append(dateObject)
                        finalData.append(data[i]/maxData)
                        #finalData.append(data[i])
            except:
                continue

        finalData = np.ma.array(finalData)
        finalDataMasked = np.ma.masked_where(finalData == '-1', finalData)
        plt.title('Observer: '+observer.username+', Date: '+entry.date)
        plt.ylabel('Detection count')
        plt.xticks(rotation=15, ha="right", fontsize=10)
        plt.xlabel('Time (hours)')
        plt.subplots_adjust(top=0.93,bottom=0.12)
        plt.plot(times, finalDataMasked, 'b')
        #yy = [0.5*np.sin(x.hour*math.pi/12)+0.5 for x in times]
        #plt.plot(times, yy, 'r')

    """
    saveDir = '/home/cwp/EMC/plots/authors/'+observer.username+'/'
    if not os.path.exists(saveDir):
        os.mkdir(saveDir)
    plt.savefig(saveDir+entry.date+'.png')
    """

def plotAverageCounts(entry, observer):
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
    finalData = {}
    counts= {}
    plotData = []
    plotTimes = []

    for i in range(24):
        finalData[i] = 0
        counts[i] = 0

    for day in days:
        dateString = entry.date+'-'+'{0:02d}'.format(int(day))
        data = [int(x) for x in entry.data[day]]


        for i in range(len(data)):
            try:
                maxData = max(data)
                if int(data[i]) >= 0:
                    if i < 23:
                        fullTime = '2000-01-01'+':{0:02d}'.format(i+1)
                        dateObject = datetime.strptime(fullTime, '%Y-%m-%d:%H')
                        times.append(dateObject)
                        finalData[i] += data[i]/maxData
                        counts[i] += 1
                    else:
                        fullTime = '2000-01-01:23'
                        dateObject = datetime.strptime(fullTime, '%Y-%m-%d:%H')
                        dateObject += dt.timedelta(hours=1)
                        times.append(dateObject)
                        finalData[i] += data[i]/maxData
                        counts[i] += 1
            except:
                continue

    return finalData, counts

if __name__ == "__main__":
    plotTimes = []
    plotData = []
    finalData = {}
    counts = {}
    count = 0

    for i in range(24):
        finalData[i] = 0
        counts[i] = 0

    for name, observer in authors.items():
        count += 1

        dates = sorted(observer.data.keys())

        for date in dates:
            #try:
                #saveDir = '/home/cwp/EMC/plots/countsSameDay/'+observer.username+'/'
                #if not os.path.exists(saveDir):
                    #os.mkdir(saveDir)
                entry = observer.data[date]
                finalDataNew, countsNew = plotAverageCounts(entry, observer)

                for key, value in finalDataNew.items():
                    finalData[key] += value

                for key, value in countsNew.items():
                    counts[key] += value

        print(count)

    for i in range(24):
        if counts[i] != 0:
            plotData.append(finalData[i]/counts[i])
            plotTimes.append(i+1)

    plt.title("Mean diurnal shift across all authors")
    plt.ylabel('Average normalized detection count')
    #plt.xticks(rotation=15, ha="right", fontsize=10)
    plt.xlabel('Time from midnight (hours)')
    plt.subplots_adjust(top=0.93,bottom=0.12)
    plt.xlim((1,24))
    plt.plot(plotTimes, plotData, 'b')
    plt.show()
    #yy = [0.1*math.sin(-0.1+x*2*math.pi/24)+0.5 for x in plotTimes]
    #plt.plot(plotTimes, yy, 'r')

"""
    with open('/home/cwp/EMC/plots/general/plottimes.txt','w') as f:
        for i in plotTimes:
            f.write(str(i)+'\n')
        f.close()

    with open('/home/cwp/EMC/plots/general/plotdata.txt', 'w') as f:
        for i in plotData:
            f.write(str(i)+'\n')
        f.close()
"""
    #plt.savefig('/home/cwp/EMC/plots/general/diurnal_shift.png')
