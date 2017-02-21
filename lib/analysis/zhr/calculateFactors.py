from __future__ import division
import os, statistics, math

showers = ['geminids', 'leonids', 'orionids', 'perseids', 'quadrantids',\
        'eta_aquariids']

files = ['allData', 'closePeakData', 'peakData']

basedir = '/home/cwp/EMC/lib/analysis/zhr/finalData/'

possibilities = ['Average of all: ','Err of all: ','UQ of all: ',\
        'Average of peak: ','Err of peak: ','UQ of peak: ',\
        'Average of close peak: ','Err of close peak: ','UQ of close peak: ']

for shower in showers:
    print('===========%s===========' % shower)
    data = {}
    ms = []
    ks = []

    with open('/home/cwp/EMC/lib/analysis/zhr/'+shower+'radiant.txt', 'r') as f:
        for line in f.readlines():
            wholeLine = line.split(',')
            data[wholeLine[0]] = [wholeLine[8].split('\n')[0],
                    wholeLine[6]]

    for year in ['2005','2006','2007','2010','2011','2012','2013','2014','2015','2016']:
        try:
            with open(basedir+'final/'+year+shower+'.txt', 'r') as f:
                lines = f.readlines()

            mean = float(lines[3].split('\n')[0].split(': ')[1])
            exp = float(data[year][0])
            r = float(data[year][1])

            k =  1 - (mean/exp)
            if k > 0:
                ks.append(k)

            val = (pow(r,6.5)*mean)/exp
            m = math.log(val,r)
            if m > 6.5:
                ms.append(m)

        except:
            pass

    if len(ms) > 0:
        print('m')
        print(statistics.mean(ms))
        if len(ms) > 1:
            std = statistics.stdev(ms)
        else:
            std = 1
        print(std/len(ms))

    if len(ks) > 0:
        print('k')
        print(statistics.mean(ks))
        if len(ks) > 1:
            std = statistics.stdev(ks)
        else:
            std = 1
        print(std/len(ks))
