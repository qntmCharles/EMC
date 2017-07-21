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
        option = "peak"
        tuples.append((data[option][year][0],otherData[year][1]))

# Peak (0.458444, 0.001750365)
# Close peak (0.0300942, 0.0471403)
# All (0.116687, 0.4506597)

x = [float(i[0]) for i in tuples]
y = [float(j[1]) for j in tuples]

mean = np.mean(x)
std =np.std(x)

xs = []
ys = []

for i in range(len(x)):
    item = x[i]
    if (item > mean+2*std) or (item < mean-2*std):
        xs.append(item)

for i in range(len(y)):
    item = y[i]
    if (item > mean+2*std) or (item < mean-2*std):
        ys.append(item)

x_new = []
y_new = []

x_outliers = []
y_outliers = []

for i,j in zip(x,y):
    if (i in xs) or (j in ys):
        x_outliers.append(i)
        y_outliers.append(j)
    else:
        x_new.append(i)
        y_new.append(j)

print(x,y)
print("==============")
print(x_new,y_new)

print(len(x_new))
plt.scatter(x_new,y_new,color='b')
plt.scatter(x_outliers, y_outliers, color="b",marker="+")

plt.xlabel("Radio ZHR")
plt.ylabel("Visual ZHR")

plt.plot(np.unique(x_new), np.poly1d(np.polyfit(x_new, y_new, 1))(np.unique(x_new)), 'b:')
#plt.scatter([np.mean(x_new)],[np.mean(y_new)], color='k')
print(np.mean(x_new), np.mean(y_new))

#plt.savefig('/home/cwp/EMC/plots/zhr/figures/all_scatter.png',dpi=500)
plt.savefig('/home/cwp/ltx/papers/zhr/images/peak_scatter.png', dpi=500)

print(np.corrcoef(x_new,y_new))
print(stats.pearsonr(x_new,y_new))
