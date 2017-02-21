from __future__ import division
import os, csv, math
import matplotlib.dates as mdates
import statistics
from scipy.stats import scoreatpercentile
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime
import datetime as dt

showerObservers = {}
basedir = '/home/cwp/EMC/lib/analysis/zhr/'
showers = ['perseids', 'leonids', 'quadrantids', 'geminids', 'orionids', \
        'eta_aquariids']

def per(aList):
    return scoreatpercentile(aList,90)

def err(aList):
    if len(aList) > 1:
        return statistics.stdev(aList)/math.sqrt(len(aList))
    else:
        return 1/math.sqrt(len(aList))

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
    print('=========='+shower+'==========')

    showerData = getShowerInfo(shower+'radiant.txt')

    literallyAllData = {}

    literallyAllPeakData = {}

    literallyAllClosePeakData = {}

    for observer, observerDates in observers.items():
        try:
            print('====='+observer+'=====')
            plotData = []
            plotErr = []
            plotTimes = []

            with open(basedir+'data/'+shower+'/'+observer+'.txt', 'r') as f:
                readFile = list(csv.reader(f))
                for line in readFile:
                    dateObject = datetime.strptime(line[0],"%Y-%m-%d %H:%M:%S")

                    year = dateObject.year

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

            # Find all years for observer
            observerYears = []
            for item in plotTimes:
                year = item.year
                if year not in observerYears:
                    observerYears.append(year)

            # Iterate through years to process data for each single year
            for year in sorted(observerYears):
                finalData = []
                finalTimes = []
                finalErr = []

                meanList = []

                peakData = []

                closePeakData = []

                if shower != 'quadrantids':
                    activeRange = getHourDateRange(showerData[year]['start'],\
                            showerData[year]['end'], year, year)
                else:
                    activeRange = getHourDateRange(showerData[year]['start'],\
                            showerData[year]['end'], year, year+1)

                peakDates = getHourDateRange(showerData[year]['peak'], \
                        showerData[year]['peak'],year,year)

                closePeakDates = getClosePeakRange(showerData[year]['peak'], \
                        year)

                for selectedDate in activeRange:
                    if selectedDate in plotTimes:
                        meanList.append(plotData[plotTimes.index(selectedDate)])
                        if year not in literallyAllData.keys():
                            literallyAllData[year] = [plotData[plotTimes.index(selectedDate)]]
                        else:
                            literallyAllData[year].append(plotData[plotTimes.index(selectedDate)])
                        finalTimes.append(selectedDate)
                        finalData.append(plotData[plotTimes.index(selectedDate)])
                        finalErr.append(plotErr[plotTimes.index(selectedDate)])
                    else:
                        finalTimes.append(selectedDate)
                        finalData.append(None)
                        finalErr.append(None)

                for selectedDate in peakDates:
                    if selectedDate in plotTimes:
                        peakData.append(plotData[plotTimes.index(selectedDate)])
                        if year not in literallyAllPeakData.keys():
                            literallyAllPeakData[year] = [plotData[plotTimes.index(selectedDate)]]
                        else:
                            literallyAllPeakData[year].append(plotData[plotTimes.index(selectedDate)])

                for selectedDate in closePeakDates:
                    if selectedDate in plotTimes:
                        closePeakData.append(plotData[plotTimes.index(selectedDate)])
                        if year not in literallyAllClosePeakData.keys():
                            literallyAllClosePeakData[year] = [plotData[plotTimes.index(selectedDate)]]
                        else:
                            literallyAllClosePeakData[year].append(plotData[plotTimes.index(selectedDate)])

                average = statistics.mean(meanList)
                per_ = per(meanList)
                err_ = err(meanList)
                print('Year: ',year, '| Average: ',average,' | Err: ',err_,'| UQ: ',per_)

                # Save statistics for whole year to file
                with open('/home/cwp/EMC/lib/analysis/zhr/finalData/allData/'+shower+'/'+observer+'.txt', 'a') as f:
                    f.write(str(year)+','+str(average)+','+str(err_)+','+str(per_))
                    f.write('\n')

                # Save statistics for peak to file
                with open('/home/cwp/EMC/lib/analysis/zhr/finalData/peakData/'+shower+'/'+observer+'.txt', 'a') as f:
                    if len(peakData) > 0:
                        print('Mean of peak: ',str(statistics.mean(peakData)))
                        print('Err of peak: ',str(err(peakData)))
                        print('UQ of peak: ',str(per(peakData)))
                        f.write(str(year)+','+str(statistics.mean(peakData))+','+str(err(peakData))+','+str(per(peakData)))
                        f.write('\n')

                # Save statistics for close to peak to file
                with open('/home/cwp/EMC/lib/analysis/zhr/finalData/closePeakData/'+shower+'/'+observer+'.txt', 'a') as f:
                    if len(closePeakData) > 0:
                        print('Mean of close to peak: ',str(statistics.mean(closePeakData)))
                        print('Err of close to peak: ',str(err(closePeakData)))
                        print('UQ of close to peak: ',str(per(closePeakData)))
                        f.write(str(year)+','+str(statistics.mean(closePeakData))+','+str(err(closePeakData))+','+str(per(closePeakData)))
                        f.write('\n')


                # Mask data
                finalErrMasked = np.ma.masked_object(finalErr, None)
                finalDataMasked = np.ma.masked_object(finalData, None)

                """
                # Make plot and save
                fig, ax = plt.subplots(figsize=(15,9))
                plt.title('Observer: '+observer+' | Year: '+str(year)+' | Shower: '+shower, y=1.05, fontsize=20)
                xfmt = mdates.DateFormatter('%d/%m %H:%M')
                ax.xaxis.set_major_formatter(xfmt)
                plt.ylabel('Zenithal Hourly Rate',fontsize=18)
                plt.xlabel('Date',fontsize=18)
                plt.tick_params(labelsize=15)
                plt.errorbar(finalTimes, finalDataMasked, yerr=finalErrMasked)
                fig.autofmt_xdate()
                plt.savefig('/home/cwp/EMC/plots/zhr/'+shower+'/'+observer+str(year)+'.png', dpi=500)
                plt.close(fig)
                """

        except Exception as e:
            print(e)

    # Save statistics for all observers in shower to file
    for year in sorted(literallyAllData.keys()):
        with open('/home/cwp/EMC/lib/analysis/zhr/finalData/final/'+str(year)+shower+'.txt', 'w') as f:
            f.write('Average of all: '+str(statistics.mean(literallyAllData[year])))
            f.write('\n')
            f.write('Err of all: '+str(err(literallyAllData[year])))
            f.write('\n')
            f.write('UQ of all: '+str(per(literallyAllData[year])))
            f.write('\n')

            if year in literallyAllPeakData.keys():
                f.write('Average of peak: '+str(statistics.mean(literallyAllPeakData[year])))
                f.write('\n')
                f.write('Err of peak: '+str(err(literallyAllPeakData[year])))
                f.write('\n')
                f.write('UQ of peak: '+str(per(literallyAllPeakData[year])))
                f.write('\n')

            if year in literallyAllClosePeakData.keys():
                f.write('Average of close peak: '+str(statistics.mean(literallyAllClosePeakData[year])))
                f.write('\n')
                f.write('Err of close peak: '+str(err(literallyAllClosePeakData[year])))
                f.write('\n')
                f.write('UQ of close peak: '+str(per(literallyAllClosePeakData[year])))
                f.write('\n')
