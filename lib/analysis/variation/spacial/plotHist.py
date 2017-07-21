from matplotlib import pyplot as plt
from math import floor
import csv, math, statistics
from scipy import stats
filenames=['peak','mean','max','min','err','fit']
ylabels=['Hour','Detection count', 'Detection count', 'Detection count', 'Standard error','Sum of parameter covariance']
titles=['Peak hour of diurnal shift, averaged for grouped longitudes',\
        'Mean detection count, averaged for grouped longitudes',\
        'Maximum detection count, averaged for grouped longitudes',\
        'Minimum detection count, averaged for grouped longitudes',\
        'Variation in hourly detection counts, averaged for grouped longitudes',\
        'Sine-wave diurnal shift fit, averaged for grouped longitudes']

#for k in range(2,8):
hist = {}
data = []
#longs = []
lons = []

with open('/home/cwp/EMC/lib/analysis/variation/spacial/data.csv','r') as f:
    reader = list(csv.reader(f, delimiter='\t'))
    reader = reader[1:]
    for row in reader:
        lons.append(row[1])
        data.append(row[2])
        #data.append(row[k])

"""
for i in range(len(longs)):
    if len(longs[i]) != 0:
        if (longs[i][-1] == 'E') or (longs[i][-1] == 'W'):
            longs[i] = longs[i][:-1]

        try:
            float(longs[i])
            hist[float(longs[i])] = float(data[i])
        except:
            print(longs[i], data[i])
            pass
"""

for i in range(len(lons)):
    if len(lons[i]) != 0:
        if (lons[i][-1] == 'E') or (lons[i][-1] == 'W'):
            lons[i] = lons[i][:-1]

        try:
            float(lons[i])
            hist[float(lons[i])] = float(data[i])
        except:
            print(lons[i], data[i])
            pass

x = sorted(hist.keys())
y = [hist[i] for i in x]

finalX = []
finalY = []
for i in range(len(x)):
    corrected = y[i] + (x[i]/15)

    finalX.append(y[i])

    if corrected > 24:
        finalY.append(corrected-24)
    elif corrected < 0:
        finalY.append(corrected+24)
    else:
        finalY.append(corrected)

binss = [0 for i in range(24)]
count = 0

plt.hist(finalY, bins=range(24), color="b", edgecolor="k")
plt.xlabel("Peak hour")
plt.ylabel("Number of observers")
#plt.savefig('/home/cwp/EMC/plots/variation/spacial/longitude/histogram.pdf')
plt.tight_layout()
plt.savefig('/home/cwp/ltx/papers/dishift2/final/figures/hist.pdf')

"""
peaks = [y[0]]
start = x[0]
finalX = []
finalY = []
err=[]
count = 1
long = [x[0]]
for i in range(1,len(x)):
    if abs(x[i]-start) <= 10:
        long.append(x[i])
        peaks.append(y[i])
        count += 1
    else:
        print(len(long))
        print(min(long), max(long))
        mean_lon = sum(long)/count
        mean_peak = sum(peaks)/count
        finalX.append(mean_lon)
        corrected = mean_peak+(mean_lon/15)
        if corrected > 24:
            finalY.append(corrected-24)
        elif corrected < 0:
            finalY.append(corrected+24)
        else:
            finalY.append(corrected)

        if count >= 2:
            err.append(statistics.stdev(peaks)/math.sqrt(count))
        else:
            err.append(0)
        if count == 1:
            err.append(4)
        else:
            err.append(stats.iqr(peaks))
        peaks = [y[i]]
        count = 1
        long = [x[i]]
        start = x[i]

for i in range(len(finalY)):
    finalY[i] = finalY[i]+(finalX[i]/15)
    #err[i] = err[i]/15
    if finalY[i] > 24:
        finalY[i] -= 24
    if finalY[i] < 0:
        finalY[i] += 24

ref = [6 for k in range(len(finalX))]
#plt.errorbar(finalX,finalY, yerr=err)
#plt.plot(finalX, finalY)
plt.errorbar(finalX, finalY, yerr=err)
plt.plot(finalX, ref)
#plt.scatter(finalX, finalY)
plt.ylim(0,24)
#plt.title(titles[k-2])
#plt.title('Daily count skewness, averaged for grouped longitudes')
plt.xlabel('Longitude (degrees)')
plt.ylabel(ylabels[0])
#plt.ylabel(ylabels[k-2])
#plt.savefig('/home/cwp/EMC/plots/variation/spacial/longitude/'+filenames[k-2]+'.png')
plt.tight_layout()
plt.show()

plt.savefig('/home/cwp/EMC/plots/variation/spacial/longitude/skew.png')
"""
