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
from dateutil.relativedelta import relativedelta

plt.figure(figsize=(9,7))
plotLabels = ['Europe',  'Asia & Australia', 'North America', 'All', 'Located']
plotTitles = ['European',  'Asian & Australian', 'North American', 'All', 'Located']
plotSrcs = ['variation/temporal/eu/', 'variation/temporal/asia/', 'variation/temporal/us/', 'variation/temporal/', 'variation/temporal/test/']
for plot in plotSrcs:
    for plotType in ['Y', 'DY', 'NY']:
        print(plot, plotType)
        finalData = []
        finalErr = []
        allTimes = []
        """
        startDate = datetime(2000,1,1,0,0,0)
        while startDate <= datetime(2016,12,1,0,0,0):
            allTimes.append(startDate)
            startDate += relativedelta(months=1)
        """
        startDate = 2000
        while startDate <= 2016:
            allTimes.append(startDate)
            startDate += 1

        #allTimes = range(1, 13)
        with open('/home/cwp/EMC/lib/analysis/'+plot+plotType+'plotData.txt', 'r') as f:
            datas = f.readlines()
            for i in range(len(datas)):
                try:
                    datas[i] = float(datas[i][:-1])
                except:
                    datas[i] = None

        with open('/home/cwp/EMC/lib/analysis/'+plot+plotType+'plotTimes.txt', 'r') as f:
            times = f.readlines()
            for i in range(len(times)):
                times[i] = float(times[i])
                #times[i] = datetime.strptime(times[i][:-1], "%Y-%m-%d %H:%M:%S")

        with open('/home/cwp/EMC/lib/analysis/'+plot+plotType+'plotErr.txt', 'r') as f:
            errs = f.readlines()
            for i in range(len(errs)):
                try:
                    errs[i] = float(errs[i][:-1])
                except:
                    errs[i] = None

        if plotType == 'Y':
            for i in range(len(allTimes)):
                if allTimes[i] in times:
                    finalData.append(datas[times.index(allTimes[i])])
                    finalErr.append(errs[times.index(allTimes[i])])
                else:
                    finalErr.append(None)
                    finalData.append(None)
            finalDataMasked = np.ma.masked_object(finalData, None)
            finalErrMasked = np.ma.masked_object(finalErr, None)
            plt.errorbar(allTimes, finalDataMasked, yerr=finalErrMasked, label='All')
        else:
            finalDataMasked = np.ma.masked_object(datas, None)
            finalErrMasked = np.ma.masked_object(errs, None)
            print(times, len(times))
            if plotType == 'DY':
                plt.errorbar(times, finalDataMasked, yerr=finalErrMasked, label='Day')
            else:
                plt.errorbar(times, finalDataMasked, yerr=finalErrMasked, label='Night')


        #finalData = np.ma.array(finalData)
        #finalDataMasked = np.ma.masked_where(finalData is None, finalData)
        #finalErr = np.ma.array(finalErr)
        #finalErrMasked = np.ma.masked_where(finalErr is None, finalErr)

        #plt.errorbar(allTimes, finalDataMasked, yerr=finalErrMasked, label=plotLabels[plotSrcs.index(plot)])
    #plt.plot(allTimes,finalDataMasked)
    plt.legend()
    #plt.title('Time variation of detection count by year & month for '+plotTitles[plotSrcs.index(plot)]+' observers',y=1.05)
    plt.xlabel('Year')
    plt.ylabel('Mean detection count')
    plt.savefig('/home/cwp/EMC/plots/variation/temporal/Y'+plotLabels[plotSrcs.index(plot)]+'combined.png',dpi=500)
    plt.clf()
    #plt.xlim(0.5,12.5)
    #plt.ylim(0,120)
#plt.show()

"""
plotTimes = []
plotData = []
plotErr = []

for year in range(2000,2017):
    print(year)
    for month in range(1,13):
        print(month)
        currentData = []

        for i in range(len(datas)):
            currentDate = datetime.strptime(times[i], "%Y-%m-%d %H:%M:%S")
            if (currentDate.year == year) and (currentDate.month == month):
                currentData.extend([int(x) for x in datas[i].split(',')])

        if len(currentData) != 0:
            plotTimes.append(datetime.strptime(str(year)+'-'+'{0:02d}'.format(month), "%Y-%m"))
            plotData.append(statistics.mean(currentData))
            if len(currentData) > 1:
                plotErr.append(statistics.stdev(currentData)/math.sqrt(len(currentData)))
            else:
                plotErr.append(1)

plt.title('Detection count trend by year & month')
plt.xlabel('Year', fontsize=20)
plt.ylabel('Mean detection count', fontsize=20)
plt.errorbar(plotTimes, plotData, yerr= plotErr)
#plt.savefig('/home/cwp/EMC/plots/variation/temporal/yearday.png',dpi=500)
plt.show()
"""
