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
geolocator = Nominatim()

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

    #Get the fit stuff from plotShift, then do r^2 using some library

    return peak, meanCount, maxCount, minCount, error, fit, skew

cwd = '/home/cwp/EMC/data/authors/'
filenames = os.listdir(cwd)
authors={}

for filename in filenames:
    with open(cwd+filename, 'rb') as input:
        authors[filename[:-4]] = pickle.load(input)

count = 0
startTime = time.time()

def convert(string):
    if len(string) != 2:
        if len(string.split('\xc2')[0]) == len(string):
            deg = '{0:03d}'.format(int(string.split('d')[0]))
            remainder = string.split('d')[1]
            mins = remainder[:2]
            secs = remainder[2:4]
            EorW = remainder[-1:]
        else:
            deg = '{0:03d}'.format(int(string.split('\xc2')[0]))
            remainder = string.split('\xc2')[1][1:]
            mins = remainder[:2]
            secs = remainder[2:4]
            EorW = remainder[-1:]

    if len(secs) != 2:
        secs = '00'

    if len(mins) != 2:
        mins = '00'

    if mins >= '60':
        return None

    if secs >= '60':
        return None

    return ''.join([EorW,deg,'d',mins,"\'",secs])

with open('/home/cwp/EMC/lib/analysis/variation/data.csv','a') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(['LAT','LONG','PEAK','MEAN','MAX','MIN','ERR','FIT'])

badLocations = {}
badLocations["PagosaSprings,Colorado"] = "Pagosa Springs, Colorado"
badLocations["Sandown,NH"] = "Sandown, NH"
badLocations["Jaromer"] = "Jaromer Czech Republic"
badLocations["PolignanoaMare(Bari)"] = "Bari Italy"
badLocations["CeskeBudejovice"] = "Ceske Budejovice Czech Republic"
badLocations["Townville,SC"] = "Townville, SC"
badLocations["Sobeslav"] = "Sobeslav"
badLocations["Upice"] = "Upice"
badLocations["SurfsideBeach"] = "Surfside Beach"

def dd2dms(dd,latlong):
    if latlong == 'Lat':
        if dd >= 0:
            EorW = 'E'
        else:
            EorW = 'W'
    if latlong == 'Long':
        if dd >= 0:
            EorW = 'N'
        else:
            EorW = 'S'

    mins,secs = divmod(dd*3600,60)
    deg,mins = divmod(mins,60)

    return ''.join([EorW,'{0:03d}'.format(int(deg)),'d','{0:02d}'.format(int(mins)),"\'",'{0:02d}'.format(int(secs))])

for name, observer in authors.items():
    attr = ['LongitudeGMAP', 'LatitudeGMAP']
    flag = False
    for attribute in attr:
        if attribute in observer.locationAttr.keys():
            flag = True
        else:
            flag = False

    if flag == True:
        count += 1
        long = observer.locationAttr['LongitudeGMAP']
        lat = observer.locationAttr['LatitudeGMAP']
        """
        if (len(long) > 2) and (len(lat) > 2):
            long = convert(long)
            lat = convert(lat)
            if (long is None) or (lat is None) or (count in [43, 58, 59, 60, 107, 150, 184]):
                if 'City' in observer.locationAttr.keys():
                    city = observer.locationAttr['City']
                if 'Country' in observer.locationAttr.keys():
                    country = observer.locationAttr['Country']
                location = geolocator.geocode(city+' '+' '.join([x for x in re.split(r'([A-Z][a-z]*)',country) if x]))
                if location is None:
                    location = geolocator.geocode(badLocations[city])

                lat = dd2dms(location.latitude, 'Lat')
                long = dd2dms(location.longitude, 'Long')

        if count == 52:
            long = long.replace('-','')

        if count in [55, 79, 114, 217]:
            long = long.replace('-', '0')
        """

        print('Observer: '+name)
        print('Lat: ', lat)
        print('Long: ', long)

        results=list(analyse(observer.data))
        print('Results: ',results)
        toWrite = [lat, long]
        toWrite.extend(results)


        with open('/home/cwp/EMC/lib/analysis/variation/data.csv','a') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(toWrite)

print(count)
