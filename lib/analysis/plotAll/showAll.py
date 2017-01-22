from __future__ import division
import numpy as np
import statistics
from matplotlib import pyplot as plt
from datetime import datetime
maxs = []
mins = []
stdevs = []
means = []

with open('/home/cwp/EMC/lib/analysis/plotTimes.txt', 'r') as f:
    prelimTime = f.readlines()
    time = []
    for i in range(len(prelimTime)):
        time.append(datetime.strptime(prelimTime[i].split('\n')[0],"%Y-%m-%d %H:%M:%S"))

with open('/home/cwp/EMC/lib/analysis/plotData.txt', 'r') as f:
    prelimData = f.readlines()
    data = []
    for i in range(len(prelimData)):
        newData = prelimData[i].split('\n')[0]
        newData = [int(x) for x in newData.split(',')]
        data.append(newData)

for i in range(len(data)):
    """
    if len(data[i]) > 1:
        stdevs.append(statistics.stdev(data[i]))
    else:
        stdevs.append(0)
    """

    means.append(statistics.mean(data[i]))
    maxs.append(max(data[i])-means[i])
    mins.append(means[i]-min(data[i]))

plt.errorbar(time, means, yerr=[mins, maxs])
plt.xlabel('Date')
plt.ylabel('Average detection count')
plt.title('Average detection counts for all available data')
plt.show()
