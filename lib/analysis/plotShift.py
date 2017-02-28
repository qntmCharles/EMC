from __future__ import division
import matplotlib.pyplot as plt
import math
from math import pi as pi
import datetime as dt
from datetime import datetime
import statistics
import numpy as np
import scipy.optimize
from scipy.optimize import leastsq
sources = ['','variation/temporal/EU','variation/temporal/ASIA','variation/temporal/US']
labels = ['All', 'Europe', 'Asia & Aus.', 'North America']
for src in sources:
    plotTimes = range(0,24)
    plotData = [[] for i in range(0,24)]
    maxs=[]
    mins=[]

    with open('/home/cwp/EMC/lib/analysis/'+src+'plotTimes.txt', 'r') as f:
        prelimTime = f.readlines()
        time = []
        for i in range(len(prelimTime)):
            time.append(datetime.strptime(prelimTime[i].split('\n')[0],"%Y-%m-%d %H:%M:%S"))

    with open('/home/cwp/EMC/lib/analysis/'+src+'plotData.txt', 'r') as f:
        prelimData = f.readlines()
        data = []
        for i in range(len(prelimData)):
            newData = prelimData[i].split('\n')[0]
            newData = [int(x) for x in newData.split(',')]
            data.append(newData)

    for i in range(len(data)):
        if time[i].hour in plotTimes:
            plotData[plotTimes.index(time[i].hour)].extend(data[i])

    for i in range(len(plotTimes)):
        mean = statistics.mean(plotData[i])
        stdev = statistics.stdev(plotData[i])
        error = stdev/math.sqrt(len(plotData[i]))
        plotData[i] = mean
        maxs.append(error)

    plotData = np.array(plotData)
    plotTimes = np.array(plotTimes)

    plt.title("Mean diurnal shift across each observer location category")
    plt.ylabel("Average detection count")
    plt.xlabel("Time from midnight (hours)")
    plt.subplots_adjust(top=0.93,bottom=0.12)
    plt.xlim((0,24))
    np.append(plotTimes, 24)
    plotTimes = np.append(plotTimes, 24)
    plotData = np.insert(plotData, 0, plotData[-1])
    maxs = np.insert(maxs, 0, maxs[-1])
    #mins = np.insert(mins, 0, mins[-1])
    plt.errorbar(plotTimes, plotData, yerr=[maxs, maxs], label=labels[sources.index(src)])
    #plt.plot(plotTimes, plotData, label="Original data")

    #yy = [0.1*math.sin(-0.1+int(x)*2*math.pi/24)+0.5 for x in plotTimes]
    guess_mean = np.mean(plotData*2*pi/24)
    guess_std = 3*np.std(plotData*2*pi/24)/(2**0.5)
    guess_phase = 0

    optimize_func = lambda x: x[0]*np.sin(plotTimes*2*pi/24+x[1])+x[2]-plotData

    result = leastsq(optimize_func, [guess_std,guess_phase,guess_mean], full_output=True)

    est_std,est_phase,est_mean = result[0]

    s_sq = (result[2]['fvec']**2).sum()/(len(plotData)-len(result[0]))

    fit = np.sqrt(np.diagonal(result[1]*s_sq))
    #print(fit)

    data_fit = est_std*np.sin(plotTimes*2*pi/24+est_phase)+est_mean


    #Work out the fit?

    #def func(x, a, b, c, d):
        #return (a*x**3)+(b*x**2)+(c*x)+d

    #params = scipy.optimize.curve_fit(func, plotTimes, plotData)[0]

    #poly_fit = [(params[0]*x**3)+(params[1]*x**2)+(params[2]*x)+params[3] for x in plotTimes]

    #print(est_std, est_phase, est_mean)
    """
    plt.plot(plotTimes, data_fit, 'r', label="Fitted sine curve")
    #plt.plot(plotTimes, yy, 'k')
    #plt.plot(plotTimes, poly_fit, 'g', label="Fitted cubic")
    plt.legend()
    """
    #plt.savefig('/home/cwp/EMC/plots/general/diurnal_shift_fit.png')

plt.legend()
plt.savefig('/home/cwp/EMC/plots/general/all_diurnal_shifts.png',dpi=500)
