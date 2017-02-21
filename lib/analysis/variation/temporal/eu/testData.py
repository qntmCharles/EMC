import scipy.stats
from datetime import datetime
from matplotlib import pyplot as plt
import numpy as np
dayData = []
dayTimes = []
nightData = []
nightTimes = []
finalDayData = []
finalNightData = []
finalDayTimes = []
finalNightTimes = []

with open('/home/cwp/EMC/lib/analysis/variation/temporal/asia/DYplotData.txt', 'r') as f:
    datas = f.readlines()
    for i in range(len(datas)):
        try:
            dayData.append(float(datas[i][:-1]))
        except:
            dayData.append(None)

with open('/home/cwp/EMC/lib/analysis/variation/temporal/asia/DYplotTimes.txt', 'r') as f:
    datas = f.readlines()
    for i in range(len(datas)):
        dayTimes.append(float(datas[i]))

with open('/home/cwp/EMC/lib/analysis/variation/temporal/asia/NYplotData.txt', 'r') as f:
    datas = f.readlines()
    for i in range(len(datas)):
        try:
            nightData.append(float(datas[i][:-1]))
        except:
            nightData.append(None)

with open('/home/cwp/EMC/lib/analysis/variation/temporal/asia/NYplotTimes.txt', 'r') as f:
    datas = f.readlines()
    for i in range(len(datas)):
        nightTimes.append(float(datas[i]))


for i in range(len(dayTimes)):
    time = dayTimes[i]
    if (dayData[i] is not None) and (nightData[i] is not None):
        finalDayData.append(float(dayData[i]))
        finalDayTimes.append(dayTimes[i])
        finalNightData.append(float(nightData[i]))
        finalNightTimes.append(nightTimes[i])

maskedNightData = np.ma.masked_object(nightData, None)
maskedDayData = np.ma.masked_object(dayData, None)

plt.plot(nightTimes,maskedNightData)
plt.plot(dayTimes,maskedDayData)
plt.show()

#print(1-scipy.stats.chi2.cdf(scipy.stats.chisquare(finalDayData).statistic,len(finalDayData)-1))
#print(1-scipy.stats.chi2.cdf(scipy.stats.chisquare(finalNightData).statistic,len(finalNightData)-1))
print(scipy.stats.ttest_ind(finalDayData, finalNightData))
print(scipy.stats.wilcoxon(finalDayData, finalNightData))
