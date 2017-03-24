from __future__ import division
from dateutil.relativedelta import relativedelta
import cPickle as pickle
import csv, re
import numpy as np
import datetime as dt
from datetime import datetime
import statistics, os, math, time
from matplotlib import pyplot as plt
from math import pi as pi
from scipy.optimize import leastsq
from geopy.geocoders import Nominatim
import scipy.stats as stats
import pandas
from classes import Entry

def analyse(date, entry):
    shiftTimes = range(0, 24)
    shiftData = [[] for x in range(0, 24)]
    shiftMeans = []
    allData = []
    for day, dayData in entry.items():
        day = '{0:02d}'.format(day)
        for i in range(len(dayData)):
            if dayData[i] not in ['-1', '0', '\r']:
                allData.append(int(dayData[i]))
                if i < 23:
                    try:
                        time = datetime.strptime(date+'-'+day+':'+\
                                '{0:02d}'.format(i),"%Y-%m-%d:%H")
                    except:
                        pass
                else:
                    time = datetime.strptime(date+'-'+day+':'+\
                            str(23),"%Y-%m-%d:%H")

                if time.hour in shiftTimes:
                    shiftData[time.hour].extend([int(dayData[i])])
                else:
                    print('bork')

    meanCount = statistics.mean(allData)
    maxCount = max(allData)
    minCount = min(allData)

    if len(allData) >= 2:
        error = statistics.stdev(allData)/math.sqrt(len(allData))
    else:
        error = None

    for i in range(len(shiftData)):
        try:
            shiftMeans.append(statistics.mean(shiftData[i]))
        except:
            shiftMeans.append(0)

    shiftMeans.append(shiftMeans[0])
    shiftTimes.append(24)
    shiftMeans = np.array(shiftMeans)
    shiftTimes = np.array(shiftTimes)

    skew = stats.skew(pandas.DataFrame(shiftMeans))[0]

    guess_mean = np.mean(shiftMeans*2*pi/24)
    guess_std = 3*np.std(shiftMeans*2*pi/24)/(2**0.5)
    guess_phase = 0

    optimize_func = lambda x: x[0]*np.sin(shiftTimes*2*pi/24+x[1])+x[2]-shiftMeans

    result = leastsq(optimize_func, [guess_std,guess_phase,guess_mean],full_output=True)
    [est_std,est_phase,est_mean] = result[0]

    #residual = optimize_func(results[0], *args)
    #reduced_chi_squared = (residual**2).sum()/len(shiftMeans
    if result[1] != None:
        s_sq = (result[2]['fvec']**2).sum()/(len(shiftMeans)-len(result[0]))

        fit = np.sum(np.sqrt(np.diagonal(result[1]*s_sq)))
    else:
        fit = None

    #plt.plot(shiftTimes, shiftMeans)
    #plt.show()
    #plt.clf()

    peak = shiftTimes[np.argmax(shiftMeans)]

    #Get the fit stuff from plotShift, then do r^2 using some library

    return peak, meanCount, maxCount, minCount, error, fit, skew


startDate = datetime(2000,1,1)
allDates = []
while startDate <= datetime(2016,12,1):
    allDates.append(startDate)
    startDate += relativedelta(months=1)
stuff = {'/variation/temporal/US':'North America','/variation/temporal/EU':'Europe','/variation/temporal/ASIA':'Asia & Australia','':'All'}

for k in range(5,6):
    for location in ['/variation/temporal/US','/variation/temporal/EU','/variation/temporal/ASIA','']:

        with open('/home/cwp/EMC/lib/analysis/'+location+'plotData.txt', 'r') as f:
            datas = f.readlines()
            for i in range(len(datas)):
                datas[i] = datas[i][:-1]

        with open('/home/cwp/EMC/lib/analysis/'+location+'plotTimes.txt', 'r') as f:
            times = f.readlines()
            for i in range(len(times)):
                times[i] = times[i][:-1]

        currentData = {}
        currentYear = 2000
        currentMonth = 1
        currentDay = 1
        plotData = []
        plotTimes = []

        for i in range(len(times)):
            time = datetime.strptime(times[i], "%Y-%m-%d %H:%M:%S")
            if time.year != currentYear:
                if len(currentData) != 0:
                    date = '20{0:02d}'.format(int(str(currentYear)[2:]))+'-'+'{0:02d}'.format(currentMonth)
                    plotData.append(analyse(date, currentData))
                    plotTimes.append(datetime.strptime(date,"%Y-%m"))
                currentYear = time.year
                currentMonth = time.month

            if time.month == currentMonth:
                if time.day not in currentData.keys():
                    currentData[time.day] = [statistics.mean([int(x) for x in datas[i].split(',')])]
                else:
                    currentData[time.day].append(statistics.mean([int(x) for x in datas[i].split(',')]))
            else:
                #analyse(str(currentYear)+'-'+str(currentMonth),currentData)
                date = '20{0:02d}'.format(int(str(currentYear)[2:]))+'-'+'{0:02d}'.format(currentMonth)
                print(date)
                plotData.append(analyse(date, currentData))
                plotTimes.append(datetime.strptime(date,"%Y-%m"))
                currentMonth = time.month
                currentData = {}
                currentData[time.day] = [statistics.mean([int(x) for x in datas[i].split(',')])]


        titles=['Time variation of peak hour for diurnal shift for all observers',
                'Time variation of mean detection count for all observers',
                'Time variation of maximum detection count for all observers',
                'Time variation of minimum detection count for all observers',
                'Time variation of standard error in detection counts for all observers',
                'Time variation of sine-wave diurnal shift fit for all observers',
                'Time variation of skew in daily detections for all observers']
        ylabels=['Hour', 'Detection count', 'Detection count', 'Detection count', 'Standard error', 'Sum of parameter standard deviation', 'Skewness']
        filenames = ['peak', 'mean', 'max', 'min', 'err', 'fit', 'skew']

        finalData = []
        #print(plotTimes)
        for j in range(len(allDates)):
            if allDates[j] in plotTimes:
                #print(allDates[j])
                finalData.append(plotData[plotTimes.index(allDates[j])][k])
            else:
                finalData.append(None)

        finalData = np.ma.array(finalData)
        finalDataMasked = np.ma.masked_where(finalData == None, finalData)

        plt.title(titles[k], y=1.05)
        plt.ylabel(ylabels[k])
        plt.xlabel('Date')
        plt.plot(allDates,finalDataMasked, label=stuff[location])
    plt.legend()
    plt.savefig('/home/cwp/EMC/plots/variation/temporal/analyses/COMBINED'+filenames[k], dpi=500)
    plt.clf()

"""
for i in [1,2,3]:
    finalData = []
    #print(plotTimes)
    for j in range(len(allDates)):
        if allDates[j] in plotTimes:
            finalData.append(plotData[plotTimes.index(allDates[j])][i])
        else:
            finalData.append(None)

    finalData = np.ma.array(finalData)
    finalDataMasked = np.ma.masked_where(finalData == None, finalData)

    plt.title(titles[i], y=1.05)
    plt.ylabel(ylabels[i])
    plt.xlabel('Date')
    plt.plot(allDates,finalDataMasked, label=filenames[i])
    plt.legend()
plt.savefig('/home/cwp/EMC/plots/variation/temporal/analyses/counts.png', dpi=500)
"""
