from __future__ import division
import os, csv, time
from datetime import datetime
import datetime as dt
import cPickle as pickle
from matplotlib import pyplot as plt

cwd = '/home/cwp/EMC/data/data/'
cwd2 = '/home/cwp/EMC/data/authors/'
basedir = '/home/cwp/EMC/lib/analysis/variation/temporal/'

authors={}
for filename in os.listdir(cwd2):
    with open(cwd2+filename, 'rb') as input:
        authors[filename[:-4]] = pickle.load(input)

def findlocalmidnightingmt(longitude):
    midnight = (0 - (float(longitude)/15))%24
    return round(midnight)

def isNight(do,long):
    mid = int(findlocalmidnightingmt(long))

    maxtime1 = datetime(do.year,do.month,do.day,mid)+dt.timedelta(hours=6)
    mintime1 = datetime(do.year,do.month,do.day,mid)-dt.timedelta(hours=6)

    maxtime2 = datetime(do.year,do.month,do.day,mid)-dt.timedelta(days=1)+dt.timedelta(hours=6)
    mintime2 = datetime(do.year,do.month,do.day,mid)-dt.timedelta(days=1)-dt.timedelta(hours=6)

    return ((do > mintime1) and (do <= maxtime1)) or ((do>mintime2) and (do <= maxtime2))

filesPrelim = os.listdir('/home/cwp/EMC/lib/analysis/variation/temporal/NS/lat/')
files = []

for thing in filesPrelim:
    if thing[-4:] == '.txt':
        files.append(thing)

allListedAuthors = {}
for filepath in files:
    allListedAuthors[filepath[:-4]] = []
    with open(basedir+'/NS/lat/'+filepath, 'r') as f:
        allStuff = f.readlines()
        for item in allStuff:
            allListedAuthors[filepath[:-4]].append(item.split('\n')[0])

for category, currentAuthors in allListedAuthors.items():
    allDayData = {}
    allNightData = {}
    count = 0
    for year in sorted(os.listdir(cwd)):
        print('======='+year+'=======')
        for month in sorted(os.listdir(os.path.join(cwd,year))):
            print(year+'-'+month)
            newAuthors = os.listdir(os.path.join(cwd,year,month))
            for author in newAuthors:
                path = os.path.join(cwd,year,month,author)
                if author[:-4] in currentAuthors:
                    long = authors[author[:-4]].locationAttr["LongitudeGMAP"]
                    with open(path, 'r') as f:
                        monthData = list(csv.reader(f))[1:]
                        f.close()

                    for day in monthData:
                        if (len(set(day[1:]))==1) and (list(set(day[1:]))[0]=='-1'):
                            pass
                        else:
                            try:
                                for i in range(1,len(day)):
                                    if day[i] not in ['-1', '0', '\r']:
                                        dateString = year+'-'+month+'-'+day[0]+':'
                                        if i < 24:
                                            dateString += '{0:02d}'.format(i)
                                            dateObject=datetime.strptime(dateString,\
                                                    "%Y-%m-%d:%H")
                                        else:
                                            dateString += '23'
                                            dateObject=datetime.strptime(dateString,\
                                                    "%Y-%m-%d:%H")
                                            dateObject+=dt.timedelta(hours=1)

                                        if isNight(dateObject,long):
                                            if dateObject not in allNightData.keys():
                                                allNightData[dateObject] = [int(day[i])]
                                            else:
                                                allNightData[dateObject].append(int(day[i]))
                                        else:
                                            if dateObject not in allDayData.keys():
                                                allDayData[dateObject] = [int(day[i])]
                                            else:
                                                allDayData[dateObject].append(int(day[i]))
                            except Exception as e:
                                print(e)
                                print(year, month, author)
                                print(day)

    keys = sorted(allDayData.keys())
    DplotData = []
    DplotTimes = []

    for key in keys:
        DplotData.append(allDayData[key])
        DplotTimes.append(key)

    with open(basedir+'NS/lat/'+category+'DplotData.txt', 'w') as f:
        for item in DplotData:
            f.write(','.join([str(x) for x in item]))
            f.write('\n')
        f.close()

    with open(basedir+'NS/lat/'+category+'DplotTimes.txt', 'w') as f:
        for item in DplotTimes:
            f.write(str(item)+'\n')
        f.close()

    keys = sorted(allNightData.keys())
    NplotData = []
    NplotTimes = []

    for key in keys:
        NplotData.append(allNightData[key])
        NplotTimes.append(key)

    with open(basedir+'NS/lat/'+category+'NplotData.txt', 'w') as f:
        for item in NplotData:
            f.write(','.join([str(x) for x in item]))
            f.write('\n')
        f.close()

    with open(basedir+'NS/lat/'+category+'NplotTimes.txt', 'w') as f:
        for item in NplotTimes:
            f.write(str(item)+'\n')
        f.close()
