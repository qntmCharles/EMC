from __future__ import division
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
                    time = datetime.strptime(date+'-'+day+':'+\
                            '{0:02d}'.format(i),"%Y-%m-%d:%H")
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
    s_sq = (result[2]['fvec']**2).sum()/(len(shiftMeans)-len(result[0]))

    fit = np.sum(np.sqrt(np.diagonal(result[1]*s_sq)))

    #plt.plot(shiftTimes, shiftMeans)
    #plt.show()
    #plt.clf()

    peak = shiftTimes[np.argmax(shiftMeans)]

    #Get the fit stuff from plotShift, then do r^2 using some library

    return peak, meanCount, maxCount, minCount, error, fit, skew

with open('/home/cwp/EMC/lib/analysis/plotData.txt', 'r') as f:
    datas = f.readlines()
    for i in range(len(datas)):
        datas[i] = datas[i][:-1]

with open('/home/cwp/EMC/lib/analysis/plotTimes.txt', 'r') as f:
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

for i in range(7):
    plt.plot(plotTimes,[x[i] for x in plotData])
    plt.show()

#Save these plots, title, label, etc
#Then repeat for month, day
