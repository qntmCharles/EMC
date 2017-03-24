import os, statistics
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt

showers = ['geminids', 'leonids', 'orionids', 'perseids', 'quadrantids',\
        'eta_aquariids']

files = ['allData', 'closePeakData', 'peakData']

basedir = '/home/cwp/EMC/lib/analysis/zhr/finalData/'

possibilities = ['Average of all: ','Err of all: ','UQ of all: ',\
        'Average of peak: ','Err of peak: ','UQ of peak: ',\
        'Average of close peak: ','Err of close peak: ','UQ of close peak: ']

tuples = []
for shower in showers:
    data = {"peak":{},"all":{},"close peak":{}}
    otherData = {}
    okYears = []
    print('===========%s===========' % shower)


    for year in ['2005','2006','2007','2010','2011','2012','2013','2014','2015','2016']:
        try:
            with open(basedir+'final/'+year+shower+'.txt', 'r') as f:
                lines = f.readlines()

                for option in ["peak", "all", "close peak"]:
                    for i in range(len(lines)):
                        things = lines[i].split(': ')
                        print(things)
                        if things[0] == "Average of "+option:
                            data[option][year] = [float(\
                                    things[1].split('\n')[0])]
                            if (year not in okYears) and (option == "peak"):
                                okYears.append(year)
                        if things[0] == "Err of "+option:
                            data[option][year].append(float(\
                                    things[1].split('\n')[0]))
                            if (year not in okYears) and (option == "peak"):
                                okYears.append(year)
        except Exception as e:
            print(e)

    with open('/home/cwp/EMC/lib/analysis/zhr/'+shower+\
            'radiant.txt', 'r') as f:
        for line in f.readlines():
            exp = float(line.split(',')[7])
            vis = float(line.split(',')[8].split('\n')[0])
            year = line.split(',')[0]
            if year in okYears:
                otherData[year] = [exp, vis]

    expY = []
    expX = []
    visY = []
    visX = []
    optionsY = {}
    optionsX = []

    for year in ['2005','2006','2007','2010','2011','2012','2013','2014','2015','2016']:
        if year in okYears:
            expY.append(otherData[year][0])
            expX.append(year)

            visY.append(otherData[year][1])
            visX.append(year)

            optionsX.append(year)

    options = ["peak", "close peak", "all"]
    fmts = ["b-.", "b:", "b--"]
    """
    plt.figure(figsize=(9,6))

    for option in options:
        print(option)
        print(data[option])
        optionsXX = list(map(int, optionsX))
        plt.errorbar(optionsXX, [data[option][i][0] for i in optionsX],
                fmt=fmts[options.index(option)], \
                yerr = [data[option][i][1] for i in optionsX], \
                label=option)

    plt.plot(expX, expY, "r", label="Expected")
    plt.plot(visX, visY, "b-", label="Visual ZHR$_{max}$")

    plt.legend()

    #plt.title("Radio ZHR results compared to expected and visual ZHR | Shower: "+shower)
    plt.xlabel("Year")
    plt.ylabel("Zenithal Hourly Rate (detections/hour)")
    plt.tight_layout()
    plt.savefig("/home/cwp/EMC/plots/zhr/figures/"+shower+"_notitle.png",dpi=500)
    plt.clf()
    """

    for year in okYears:
        option = "all"
        tuples.append((data[option][year][0],otherData[year][1]))

# Peak (0.458444, 0.001750365)
# Close peak (0.0300942, 0.0471403)
# All (0.116687, 0.4506597)

x = [float(i[0]) for i in tuples]
y = [float(j[1]) for j in tuples]

print(len(x))
plt.scatter(x,y,color='b')
plt.xlabel("Radio ZHR")
plt.ylabel("Visual ZHR")
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)), 'b:')
#plt.scatter([np.mean(x)],[np.mean(y)], color='k')
print(np.mean(x), np.mean(y))

plt.savefig('/home/cwp/EMC/plots/zhr/figures/all_scatter.png',dpi=500)

print(np.corrcoef(x,y))
print(stats.pearsonr(x,y))
