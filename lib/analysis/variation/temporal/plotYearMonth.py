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

def analyse(entriesList):
    shiftTimes = range(0, 24)
    shiftData = [[] for x in range(0, 24)]
    shiftMeans = []
    allData = []
    for date, entry in entriesList.items():
        entry.loadData()
        for day, dayData in entry.data.items():
            for i in range(len(dayData)):
                if dayData[i] not in ['-1', '0', '\r']:
                    allData.append(int(dayData[i]))
                    try:
                        if i < 23:
                            time = datetime.strptime(date+'-'+day+':'+\
                                    '{0:02d}'.format(i+1),"%Y-%m-%d:%H")
                        else:
                            time = datetime.strptime(date+'-'+day+':'+\
                                    str(23),"%Y-%m-%d:%H")
                            time += dt.timedelta(hours=1)

                        if time.hour in shiftTimes:
                            shiftData[time.hour].extend([int(dayData[i])])
                        else:
                            print('bork')
                    except:
                        pass

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

    shiftMeans = np.insert(shiftMeans, len(shiftMeans), shiftMeans[-1])
    shiftTimes = np.insert(shiftTimes, len(shiftTimes), shiftTimes[-1])

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

    return peak, meanCount, maxCount, minCount, error, fit, skew

with open('/home/cwp/EMC/lib/analysis/plotData.txt', 'r') as f:
    datas = f.readlines()
    for i in range(len(datas)):
        datas[i] = datas[i][:-1]

with open('/home/cwp/EMC/lib/analysis/plotTimes.txt', 'r') as f:
    times = f.readlines()
    for i in range(len(times)):
        times[i] = times[i][:-1]

plotTimes = []
plotData = []
plotErr = []

for year in range(2000,2017):
    """
    print(year)
    for month in range(1,13):
        print(month)
    """
    currentData = []

    for i in range(len(datas)):
        currentDate = datetime.strptime(times[i], "%Y-%m-%d %H:%M:%S")
        if (currentDate.year == year):
            if (currentDate.hour <= 18) and (currentDate.hour > 6):
                currentData.extend([int(x) for x in datas[i].split(',')])

    if len(currentData) != 0:
        #plotTimes.append(datetime.strptime(str(year)+'-'+'{0:02d}'.format(month), "%Y-%m"))
        plotTimes.append(year)
        plotData.append(statistics.mean(currentData))
        if len(currentData) > 1:
            plotErr.append(statistics.stdev(currentData)/math.sqrt(len(currentData)))
        else:
            plotErr.append(1)
    else:
        plotErr.append(None)
        plotData.append(None)
        plotTimes.append(year)
        #plotTimes.append(datetime.strptime(str(year)+'-'+'{0:02d}'.format(month), "%Y-%m"))

finalData = np.ma.masked_object(plotData, None)
finalErr = np.ma.masked_object(plotErr, None)

plt.title('Detection count trend by year for all observers (hours 07-18)', y=1.05)
plt.xlabel('Year', fontsize=20)
plt.ylabel('Mean detection count', fontsize=20)
plt.errorbar(plotTimes, finalData, yerr= finalErr)
#plt.xlim(datetime(1999,6,1),datetime(2017,6,1))
plt.xlim(1999.5,2016.5)
plt.savefig('/home/cwp/EMC/plots/variation/temporal/day_year.png',dpi=500)

with open('/home/cwp/EMC/lib/analysis/variation/temporal/DYplotData.txt', 'w') as f:
    for item in finalData:
        f.write(str(item))
        f.write('\n')
    f.close()

with open('/home/cwp/EMC/lib/analysis/variation/temporal/DYplotTimes.txt', 'w') as f:
    for item in plotTimes:
        f.write(str(item))
        f.write('\n')
    f.close()

with open('/home/cwp/EMC/lib/analysis/variation/temporal/DYplotErr.txt', 'w') as f:
    for item in finalErr:
        f.write(str(item))
        f.write('\n')
    f.close()
