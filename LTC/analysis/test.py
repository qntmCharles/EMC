from datetime import datetime
from matplotlib import pyplot as plt
import numpy as np
import datetime as dt
import statistics
from scipy import stats

rmobData = []
rmobTimes = []

for year in ['2014','2015','2016']:
    with open('/home/cwp/EMC/LTC/rmob/data/'+year+'rmobdata.txt', 'r') as f:
        yearRmobData = f.readlines()
        for i in range(len(yearRmobData)):
            yearRmobData[i] = int(yearRmobData[i].split('\n')[0])

    with open('/home/cwp/EMC/LTC/rmob/data/'+year+'rmobtimes.txt','r') as f:
        yearRmobTimes = f.readlines()
        for i in range(len(yearRmobTimes)):
            yearRmobTimes[i] = datetime.strptime(yearRmobTimes[i].split('\n')[0], "%Y-%m-%d %H:%M:%S")

    rmobData.extend(yearRmobData)
    rmobTimes.extend(yearRmobTimes)

with open('/home/cwp/EMC/LTC/mse/data.txt','r') as f:
    mseData = f.readlines()
    for i in range(len(mseData)):
        mseData[i] = mseData[i].split('\r')[0]

with open('/home/cwp/EMC/LTC/mse/times.txt','r') as f:
    mseTimes = f.readlines()
    for i in range(len(mseTimes)):
        mseTimes[i] = datetime.strptime(mseTimes[i].split('\n')[0], "%Y-%m-%d %H:%M:%S")

year = 2014
month = 10
day = 31
hour = 23
finalMseData = []
finalMseTimes = []
currentData = []
for i in range(len(mseTimes)):
    time = mseTimes[i]
    if (time.year == year) and (time.month == month) and (time.day == day) and\
            (time.hour == hour):
        currentData.append(float(mseData[i]))
    else:
        if len(currentData) > 0:
            dateObject = datetime.strptime(str(year)+'-'+str(month)+'-'+\
                    str(day)+' '+str(hour), "%Y-%m-%d %H")
            dateObject += dt.timedelta(hours=1)
            finalMseTimes.append(dateObject)
            finalMseData.append(statistics.mean(currentData))
        year = time.year
        month = time.month
        day = time.day
        hour = time.hour
        currentData = []

print(finalMseTimes[0], finalMseTimes[len(finalMseTimes)-1])
print(rmobTimes[0], rmobTimes[len(rmobTimes)-1])
count = 0

x = []
y = []

def dateRange(start,end):
    dates = []
    while start <= end:
        dates.append(start)
        start += dt.timedelta(hours=1)

    return dates

badTimes = []
badTimes.extend(dateRange(datetime(2016,7,1,0),datetime(2016,7,9,23)))
badTimes.extend(dateRange(datetime(2016,8,13,11),datetime(2016,8,22,23)))
badTimes.extend(dateRange(datetime(2016,10,7,0),datetime(2016,11,12,23)))
badTimes.extend(dateRange(datetime(2015,10,30,0),datetime(2015,11,4,23)))
badTimes.extend(dateRange(datetime(2016,11,25,0),datetime(2016,12,1,23)))
badTimes.extend(dateRange(datetime(2015,10,7,0),datetime(2015,10,8,23)))
badTimes.extend(dateRange(datetime(2016,1,1,0),datetime(2016,1,2,23)))
badTimes.extend(dateRange(datetime(2015,10,25,6),datetime(2015,10,26,18)))
badTimes.extend(dateRange(datetime(2015,11,7,8),datetime(2015,11,7,15)))
badTimes.extend(dateRange(datetime(2016,12,24,4),datetime(2016,12,24,7)))

count = 0
for time in finalMseTimes:
    if time in rmobTimes:
        count += 1
        if time not in badTimes:
            x.append(rmobData[rmobTimes.index(time)])
            y.append(finalMseData[finalMseTimes.index(time)])

"""
plotTimes = []
plotData = []

allDates = dateRange(rmobTimes[0],rmobTimes[len(rmobTimes)-1])
for date in allDates:
    if (date in rmobTimes):
        plotTimes.append(date)
        plotData.append(rmobData[rmobTimes.index(date)])
    else:
        plotTimes.append(date)
        plotData.append(None)

plotTimesMasked = np.ma.masked_object(plotTimes, None)
plotDataMasked = np.ma.masked_object(plotData, None)
fig, ax = plt.subplots()
plt.plot(plotTimesMasked, plotDataMasked)
plt.xlabel('Time')
plt.ylabel('Meteor detection count')
fig.autofmt_xdate()
plt.savefig('/home/cwp/EMC/plots/img/rmob.png',dpi=500)
plt.savefig('/home/cwp/ltx/report/images/img/rmob.png',dpi=500)
plt.show()

plt.scatter(x,y)
plt.xlabel('RMOB count')
plt.ylabel('MSE value')
plt.savefig('/home/cwp/EMC/plots/img/before.png',dpi=500)
plt.savefig('/home/cwp/ltx/report/images/img/before.png',dpi=500)
"""

print(np.corrcoef(x,y))
print(stats.pearsonr(x,y))
