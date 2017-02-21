from __future__ import division
import math as math
from matplotlib import pyplot as plt
import os, csv
import datetime as dt
from datetime import datetime
import cPickle as pickle
import numpy as np
from math import sin
from math import cos
from math import radians as d2r
from astropy.time import Time

# Get all authors
cwd = '/home/cwp/EMC/data/authors/'
filenames = os.listdir(cwd)
authors = {}
basedir = '/home/cwp/EMC/lib/analysis/zhr/'

for filename in filenames:
    with open(cwd+filename, 'rb') as input:
        authors[filename[:-4]] = pickle.load(input)

# Get shower data
def getObservers(filepath):
    base = filepath
    toReturn = {}

    for filename in os.listdir(filepath):
        toReturn[filename[:-4]] = []

        with open(base + filename, 'r') as f:
            for line in f.readlines():
                toReturn[filename[:-4]].append(line.split('\n')[0])

        #os.remove(base+filename)

    return toReturn

def getShowerInfo(filepath):
    data = {}
    with open(basedir+filepath, 'r') as f:
        readFile = list(csv.reader(f))
        for line in readFile:
            data[int(line[0])] = {'ra':float(line[1]),\
                    'dec':float(line[2]), 'peak':line[3], 'start':line[4], \
                    'end':line[5], 'r':float(line[6]), 'zhr_exp':int(line[7]),\
                    'zhr_max':int(line[8])}

    return data

# Get active range
def getDateRange(start,end,startYear,endYear):
    startDate = datetime(startYear, int(start.split('/')[1]), \
            int(start.split('/')[0]))

    endDate = datetime(endYear, int(end.split('/')[1]), \
            int(end.split('/')[0]))

    dates = []

    while startDate <= endDate:
        dates.append(startDate)
        startDate += dt.timedelta(days=1)

    return dates

showers = ['perseids', 'leonids', 'quadrantids', 'geminids', 'orionids', \
        'eta_aquariids']

def baseline(entries, activeRange):
    allData = []
    allTimes = []

    for entry in entries:
        entry.loadData()
        for day, dayData in entry.data.items():
            dayData = dayData[:-1]
            for i in range(len(dayData)):
                if dayData[i] not in ['-1', '0']:
                    try:
                        # Find date
                        if i < 23:
                            dateString = date + '-' + day
                            dateObject = datetime.strptime(dateString, \
                                    "%Y-%m-%d")
                            dateString = datetime.strftime(dateObject, \
                                    "%Y-%m-%d")

                        else:
                            dateString = date + '-' + day
                            dateObject = datetime.strptime(dateString, \
                                    "%Y-%m-%d")
                            dateObject += dt.timedelta(days=1)

                        if dateObject not in activeRange:
                            allData.append(int(dayData[i]))
                            allTimes.append(dateObject)

                    except Exception as e:
                        print(e)

    if len(allData) == 0:
        b = 0

    elif len(allData) < 4:
        b = min(allData)

    else:
        sortedData = sorted(allData)[:len(allData)//4]
        b = sum(sortedData)/len(sortedData)

    return round(b)


def calculateZHR(HR, lat, long, date, RA, dec, r, b):
    if HR == 0:
        return None, None

    # Compute LST
    t = Time(date, format='iso', scale='utc', \
            location=(str(long)+'d',str(lat)+'d'))
    LST = t.sidereal_time('apparent').hourangle*15

    # Compute zenith distance
    z = math.acos(sin(d2r(lat))*sin(d2r(dec)) + cos(d2r(lat))*cos(\
            d2r(dec))*cos(d2r(LST-RA)))

    # Compute radiant altitude correction factor
    hR = d2r(90-math.degrees(z))
    cc = 0.5+(hR/(2*math.pi))

    # Compute ZHR
    zhr = (HR-b)/cc

    # Compute ZHR error
    error = zhr/math.sqrt(HR)

    return zhr, error

showerObservers = {}

for shower in showers:
    showerObservers[shower] = getObservers(basedir+'dates/'+shower+'/')

# Iterate through shower
for shower, observers in showerObservers.items():
    print(shower)
    showerData = getShowerInfo(shower+'radiant.txt')

    # Iterate through observers
    for observer, observerDates in observers.items():
        print(observer)
        errs = []
        zhrs = []
        hRs = []
        plotDates = []

        try:
            latitude = float(authors[observer].locationAttr['LatitudeGMAP'])
            longitude = float(authors[observer].locationAttr['LongitudeGMAP'])
        except:
            latitude = None
            longitude = None

        if (longitude is not None) and (latitude is not None):
            # Iterate through observer's dates
            for date in sorted(observerDates):
                print(date)
                entry = authors[observer].data[date]
                entry.loadData()

                sortedEntry = [(x,entry.data[x]) for x in sorted(\
                        entry.data.keys())]

                year = int(date[:4])

                if shower != 'quadrantids':
                    activeRange = getDateRange(showerData[year]['start'],\
                            showerData[year]['end'], year, year)
                else:
                    activeRange = getDateRange(showerData[year]['start'],\
                            showerData[year]['end'], year, year+1)

                # Compute baseline
                if shower == 'quadrantids':
                    geminidData = getShowerInfo('geminidsradiant.txt')
                    activeRange.append(getDateRange(\
                            geminidData[year]['start'],\
                            geminidData[year]['end'],\
                            year, year))

                if shower == 'geminids':
                    quadData = getShowerInfo('quadrantidsradiant.txt')
                    activeRange.append(getDateRange(quadData[year]['start'],\
                            quadData[year]['end'], year, year+1))

                if shower == 'orionids':
                    leonidData = getShowerInfo('leonidsradiant.txt')
                    activeRange.append(getDateRange(leonidData[year]['start'],\
                            leonidData[year]['end'], year, year))

                if shower == 'leonids':
                    orionidData = getShowerInfo('orionidsradiant.txt')
                    activeRange.append(getDateRange(orionidData[year]['start'],\
                            orionidData[year]['end'], year, year))

                entries = [entry]
                for bDate in sorted(observerDates):
                    if (bDate[:-3] == str(year)) and (bDate != date):
                        entries.append(authors[observer].data[bDate])

                print(entries)
                b = baseline(entries, activeRange)
                print(b)

                # Get radiant co-ordinates
                RA = showerData[year]['ra']
                dec = showerData[year]['dec']
                r = showerData[year]['r']

                # Iterate through days in entry
                for day, dayData in sortedEntry:
                    if len(day) == 2:
                        dayData = dayData[:-1]

                        # Iterate through hours in day
                        for i in range(len(dayData)):
                            if dayData[i] not in ['-1', '0']:
                                try:
                                    # Find date
                                    if i < 23:
                                        dateString = date + '-' + day + \
                                                ' {0:02d}'.format(i+1)
                                        dateObject = datetime.strptime(dateString, \
                                                "%Y-%m-%d %H")
                                        dateString = datetime.strftime(dateObject, \
                                                "%Y-%m-%d %H:%M:%S")
                                    else:
                                        dateString = date + '-' + day + \
                                                ' {0:02d}'.format(23)
                                        dateObject = datetime.strptime(dateString, \
                                                "%Y-%m-%d %H")
                                        dateObject += dt.timedelta(hours=1)
                                        dateString = datetime.strftime(dateObject, \
                                                "%Y-%m-%d %H:%M:%S")

                                    # Compute ZHR
                                    zhr, err = calculateZHR(int(dayData[i]), \
                                            latitude, longitude, dateString, RA, \
                                            dec, r, b)

                                    zhrs.append(zhr)
                                    errs.append(err)
                                    #plotDates.append(dateString)
                                    plotDates.append(dateObject)

                                except Exception as e:
                                    print(e)

            with open('/home/cwp/EMC/lib/analysis/zhr/data/'+shower+'/'+\
                    observer+'.txt', 'a') as f:
                w = csv.writer(f)
                for i in range(len(plotDates)):
                    w.writerow([plotDates[i],zhrs[i],errs[i]])
