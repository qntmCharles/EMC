from __future__ import division
import os, csv
from datetime import datetime
import datetime as dt
from matplotlib import pyplot as plt

cwd = '/home/cwp/EMC/data/data/'

allData = {}
allCounts = {}

for year in sorted(os.listdir(cwd)):
    print('======='+year+'=======')
    for month in sorted(os.listdir(os.path.join(cwd,year))):
        print(year+'-'+month)
        newAuthors = os.listdir(os.path.join(cwd,year,month))
        for author in newAuthors:
            path = os.path.join(cwd,year,month,author)

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

                                if dateObject not in allData.keys():
                                    allData[dateObject] = [int(day[i])]
                                else:
                                    allData[dateObject].append(int(day[i]))
                    except Exception as e:
                        print(e)
                        print(year, month, author)
                        print(day)

keys = sorted(allData.keys())
plotData = []
plotTimes = []

for key in keys:
    plotData.append(allData[key])
    plotTimes.append(key)

with open('/home/cwp/EMC/lib/analysis/plotData.txt', 'w') as f:
    for item in plotData:
        f.write(','.join([str(x) for x in item]))
        f.write('\n')
    f.close()

with open('/home/cwp/EMC/lib/analysis/plotTimes.txt', 'w') as f:
    for item in plotTimes:
        f.write(str(item)+'\n')
    f.close()

#plt.plot(plotTimes, plotData)
