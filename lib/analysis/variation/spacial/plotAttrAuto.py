from matplotlib import pyplot as plt
from math import floor
import csv, math, statistics
filenames=['peak','mean','max','min','err','fit','skew']
ylabels=['Hour','Detection count', 'Detection count', 'Detection count', 'Standard error','Sum of parameter covariance', 'Skewness']
titles=['Peak hour of diurnal shift, averaged for grouped longitudes',\
        'Mean detection count, averaged for grouped longitudes',\
        'Maximum detection count, averaged for grouped longitudes',\
        'Minimum detection count, averaged for grouped longitudes',\
        'Variation in hourly detection counts, averaged for grouped longitudes',\
        'Sine-wave diurnal shift fit, averaged for grouped longitudes']

for k in range(8,9):
    hist = {}
    data = []
    #longs = []
    lats = []

    with open('/home/cwp/EMC/lib/analysis/variation/spacial/data.csv','r') as f:
        reader = list(csv.reader(f, delimiter='\t'))
        reader = reader[1:]
        for row in reader:
            lats.append(row[0])
            #data.append(row[8])
            data.append(row[k])

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

    for i in range(len(lats)):
        if len(lats[i]) != 0:
            if (lats[i][-1] == 'N') or (lats[i][-1] == 'S'):
                lats[i] = lats[i][:-1]

            try:
                float(lats[i])
                hist[float(lats[i])] = float(data[i])
            except:
                print(lats[i], data[i])
                pass

    x = sorted(hist.keys())
    y = [hist[i] for i in x]

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
            finalY.append(sum(peaks)/count)
            finalX.append(sum(long)/count)
            if count >= 2:
                err.append(statistics.stdev(peaks)/math.sqrt(count))
            else:
                err.append(0)
            peaks = [y[i]]
            count = 1
            long = [x[i]]
            start = x[i]

    plt.errorbar(finalX,finalY, yerr=err)
    #print(titles[k-2])
    #plt.title(titles[k-2])
    #plt.title('Daily count skewness, averaged for grouped longitudes')
    plt.xlabel('Latitude (degrees)')
    plt.ylabel(ylabels[k-2])
    #plt.ylabel(ylabels[k-2])
    plt.tight_layout()
    plt.savefig('/home/cwp/EMC/plots/variation/spacial/latitude/'+filenames[k-2]+'.png')
    plt.clf()
    #plt.show()
    #plt.savefig('/home/cwp/EMC/plots/variation/spacial/longitude/skew.png')
