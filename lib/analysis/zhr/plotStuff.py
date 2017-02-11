import os, csv
import matplotlib.dates as mdates
import statistics
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime
import datetime as dt

showerObservers = {}
basedir = '/home/cwp/EMC/lib/analysis/zhr/'
showers = ['perseids', 'leonids', 'quadrantids', 'geminids', 'orionids', \
        'eta_aquariids']

def getObservers(filepath):
    base = filepath
    toReturn = {}

    for filename in os.listdir(filepath):
        toReturn[filename[:-4]] = []

        with open(base + filename, 'r') as f:
            for line in f.readlines():
                toReturn[filename[:-4]].append(line.split('\n')[0])

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

def getHourDateRange(start,end,startYear,endYear):
    startDate = datetime(startYear, int(start.split('/')[1]), \
            int(start.split('/')[0]))

    endDate = datetime(endYear, int(end.split('/')[1]), \
            int(end.split('/')[0]))
    endDate += dt.timedelta(days=1)

    dates = []

    while startDate <= endDate:
        dates.append(startDate)
        startDate += dt.timedelta(hours=1)

    return dates

def getClosePeakRange(peak, peakYear):
    peakDate = datetime(peakYear, int(peak.split('/')[1]), \
            int(peak.split('/')[0]))

    startDate = peakDate - dt.timedelta(days=2)
    endDate = peakDate + dt.timedelta(days=2)

    dates = []

    while startDate <= endDate:
        dates.append(startDate)
        startDate += dt.timedelta(hours=1)

    return dates

for shower in showers:
    showerObservers[shower] = getObservers(basedir+'data/'+shower+'/')


for shower, observers in showerObservers.items():
    print(shower)

    allMeans = {}
    literallyAllData = []
    allMaxs = {}

    showerData = getShowerInfo(shower+'radiant.txt')

    for observer, observerDates in observers.items():
        print(observer)
        plotData = []
        plotErr = []
        plotTimes = []

        peakData = []

        closePeakData = []

        with open(basedir+'data/'+shower+'/'+observer+'.txt', 'r') as f:
            readFile = list(csv.reader(f))
            for line in readFile:
                dateObject = datetime.strptime(line[0],"%Y-%m-%d %H:%M:%S")

                year = dateObject.year

                peakDates = getHourDateRange(showerData[year]['peak'], \
                        showerData[year]['peak'],year,year)

                closePeakDates = getClosePeakRange(showerData[year]['peak'], \
                        year)

                if shower != 'quadrantids':
                    activeRange = getHourDateRange(showerData[year]['start'],\
                            showerData[year]['end'], year, year)
                else:
                    activeRange = getHourDateRange(showerData[year]['start'],\
                            showerData[year]['end'], year, year+1)

                if dateObject in activeRange:
                    if float(line[1]) > 0:
                        plotData.append(float(line[1]))
                        plotErr.append(float(line[2]))
                        plotTimes.append(dateObject)

                if dateObject in peakDates:
                    if float(line[1]) > 0:
                        peakData.append(float(line[1]))

                if dateObject in closePeakDates:

        observerYears = []
        for item in plotTimes:
            year = item.year
            if year not in observerYears:
                observerYears.append(year)

        print(observerYears)
        finalData = []
        finalTimes = []
        finalErr = []
        for year in sorted(observerYears):
            meanList = []

            if shower != 'quadrantids':
                activeRange = getHourDateRange(showerData[year]['start'],\
                        showerData[year]['end'], year, year)
            else:
                activeRange = getHourDateRange(showerData[year]['start'],\
                        showerData[year]['end'], year, year+1)

            for selectedDate in activeRange:
                if selectedDate in plotTimes:
                    meanList.append(plotData[plotTimes.index(selectedDate)])
                    literallyAllData.append(plotData[plotTimes.index(selectedDate)])
                    finalTimes.append(selectedDate)
                    finalData.append(plotData[plotTimes.index(selectedDate)])
                    finalErr.append(plotErr[plotTimes.index(selectedDate)])
                else:
                    finalTimes.append(selectedDate)
                    finalData.append(None)
                    finalErr.append(None)

            average = statistics.mean(meanList)
            max_ = max(meanList)

            print('Year: ',year, '| Average: ',average,'| Max: ',max_)

            with open('/home/cwp/EMC/lib/analysis/zhr/finalData/allData/'+shower+'/'+observer+'.txt', 'a') as f:
                f.write(str(year)+','+str(average)+','+str(max_))
                f.write('\n')

            if year not in allMeans.keys():
                allMeans[year] = [average]
                allMaxs[year] = [max_]
            else:
                allMeans[year].append(average)
                allMaxs[year].append(max_)

            finalErrMasked = np.ma.masked_object(finalErr, None)
            finalDataMasked = np.ma.masked_object(finalData, None)

            fig, ax = plt.subplots(figsize=(15,9))
            plt.title('Observer: '+observer+' | Year: '+str(year)+' | Shower: '+shower, y=1.05, fontsize=20)
            xfmt = mdates.DateFormatter('%d/%m %H:%M')
            ax.xaxis.set_major_formatter(xfmt)
            plt.ylabel('Zenithal Hourly Rate',fontsize=18)
            plt.xlabel('Date',fontsize=18)
            plt.tick_params(labelsize=15)
            plt.errorbar(finalTimes, finalDataMasked, yerr=finalErrMasked)
            plt.savefig('/home/cwp/EMC/plots/zhr/'+shower+'/'+observer+str(year)+'.png', dpi=500)
            plt.clf()

    with open('/home/cwp/EMC/lib/analysis/zhr/finalData/final/'+shower+'.txt', 'w') as f:
        f.write('Average: '+str(statistics.mean(literallyAllData)))
        f.write('Maximum: '+str(max(literallyAllData)))
        f.write('Average average: '+str(statistics.mean(allMeans)))
        f.write('Average maximum: '+str(statistics.mean(allMaxs)))
