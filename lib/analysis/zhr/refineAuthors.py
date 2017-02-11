import numpy as np
import os, csv
import cPickle as pickle
from matplotlib import pyplot as plt
from datetime import datetime
import datetime as dt

authors = {}

basedir = '/home/cwp/EMC/lib/analysis/zhr/'

# Get directories
cwd = '/home/cwp/EMC/data/authors/'
filenames = os.listdir(cwd)

for filename in filenames:
    with open(cwd+filename, 'rb') as input:
        authors[filename[:-4]] = pickle.load(input)

def getObservers(filepath):
    base = filepath
    toReturn = {}

    for filename in os.listdir(filepath):
        toReturn[filename[:-4]] = []

        with open(base + filename, 'r') as f:
            for line in f.readlines():
                toReturn[filename[:-4]].append(line.split('\n')[0])

        os.remove(base+filename)

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

showers = ['perseids', 'leonids', 'quadrantids', 'geminids', 'orionids', 'eta_aquariids']
dates = ['2005','2006','2007','2010','2011','2012','2013','2014','2015','2016']

showerObservers = {}
showerObserversFinal = {}

for shower in showers:
    showerObservers[shower] = getObservers(basedir+'dates/'+shower+'/')

for shower, observers in showerObservers.items():
    print('========'+shower+'========')

    showerData = getShowerInfo(shower+'radiant.txt')

    count = 0

    for observer in observers:
        #print(observer)
        okayDates = []

        for date in observers[observer]:
            noNaN = True
            noPeakNaN = True
            year = int(date[:4])

            if year in showerData.keys():
                peakDate = datetime(year,int(\
                        showerData[year]['peak'].split('/')[1]), int(\
                        showerData[year]['peak'].split('/')[0]))

                if shower != 'quadrantids':
                    activeRange = getDateRange(showerData[year]['start'],\
                            showerData[year]['end'], year, year)
                else:
                    activeRange = getDateRange(showerData[year]['start'],\
                            showerData[year]['end'], year, year+1)

                entry = authors[observer].data[date]
                entry.loadData()

                for day, dayData in entry.data.items():
                    try:
                        currentDate = datetime(int(date.split('-')[0]), \
                                int(date.split('-')[1]), int(day))
                        if currentDate in activeRange:
                            dayData = dayData[:-1]

                            for hour in dayData:
                                if hour == '-1':
                                    noNaN += 1
                                if (currentDate == peakDate) and (hour == '-1'):
                                    noPeakNaN = False

                    except:
                        pass

                if (noNaN < 12) and noPeakNaN:
                    okayDates.append(date)

        if len(okayDates) != 0:
            finalDates = []
            if shower == 'quadrantids':
                for aDate in okayDates:
                    if aDate[-2:] == '01':
                        if str(int(aDate[:-3])-1)+'-12' in okayDates:
                            finalDates.append(str(int(aDate[:-3])-1)+'-12')
                            finalDates.append(aDate)

            if shower == 'geminids':
                for aDate in okayDates:
                    finalDates.append(aDate)

            if shower == 'leonids':
                for aDate in okayDates:
                    finalDates.append(aDate)

            if shower == 'orionids':
                for aDate in okayDates:
                    if aDate[-2:] == '10':
                        if aDate[:-2]+'11' in okayDates:
                            finalDates.append(aDate)
                            finalDates.append(aDate[:-2]+'11')

            if shower == 'perseids':
                for aDate in okayDates:
                    if aDate[-2:] == '07':
                        if aDate[:-2]+'08' in okayDates:
                            finalDates.append(aDate)
                            finalDates.append(aDate[:-2]+'08')

            if shower == 'eta_aquariids':
                for aDate in okayDates:
                    if aDate[-2:] == '04':
                        if aDate[:-2]+'05' in okayDates:
                            finalDates.append(aDate)
                            finalDates.append(aDate[:-2]+'05')

            if len(finalDates) != 0:
                count += 1

                with open(basedir+'dates/'+shower+'/'+observer+'.txt', 'w') as f:
                    for date in finalDates:
                        f.write(date)
                        f.write('\n')
    print(count)
