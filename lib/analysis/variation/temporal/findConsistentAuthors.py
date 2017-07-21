import cPickle as pickle
from matplotlib import pyplot as plt
import os
from datetime import datetime as dt
import datetime

cwd = '/home/cwp/EMC/data/authors/'

authors={}
for filename in os.listdir(cwd):
    with open(cwd+filename, 'rb') as input:
        authors[filename[:-4]] = pickle.load(input)

def isAfter(month1, month2):
    m1 = dt.strptime(month1, "%Y-%m")
    m2 = dt.strptime(month2, "%Y-%m")
    diff = (m1.year - m2.year)*12+m1.month-m2.month
    if diff <= 3:
        return True
    else:
        return False

def findPeriods(months):
    months = sorted(months)
    concurrents = []
    current = [months[0]]
    for i in range(len(months)-1):
        if isAfter(months[i], months[i+1]):
            current.append(months[i+1])
        else:
            concurrents.append(current)
            current = [months[i+1]]
    concurrents.append(current)

    return concurrents

def findRange(concurrents):
    for months in concurrents:
        start = dt.strptime(months[0],"%Y-%m")
        end = dt.strptime(months[-1], "%Y-%m")
        if (start.year <= 2008) and (end.year >= 2010):
            return months

    return None

for name, observer in authors.items():
    if len(observer.locationAttr.keys()) != 0:
        concurrents = findPeriods(observer.data.keys())
        period = findRange(concurrents)
        if period is not None:
            print(period)
            data = []
            times = []
            currentYear = sorted(observer.data.keys())[0][:4]
            for month in sorted(observer.data.keys()):
                count = 0
                total = 0
                print(month)
                observer.data[month].loadData()
                for l in observer.data[month].data.values():
                    for item in l:
                        try:
                            if float(item)>=0:
                                total+=float(item)
                                count += 1
                        except:
                            continue

                if month[:4] != currentYear:
                    times.append(currentYear)
                    data.append(total/count)
                    currentYear = month[:4]

            print(times)
            print(data)
            plt.plot(times, data)
            plt.xlim(2005, 2011)
            plt.show()
