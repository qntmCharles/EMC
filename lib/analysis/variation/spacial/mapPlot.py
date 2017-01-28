from mpl_toolkits.basemap import Basemap
from matplotlib import pyplot as plt
from numpy import meshgrid
import numpy as np
import csv

lats = []
longs = []
data = []
with open('/home/cwp/EMC/lib/analysis/variation/data.csv', 'r') as f:
    reader = list(csv.reader(f, delimiter='\t'))
    reader = reader[1:]
    for row in reader:
        try:
            lat = float(row[0][:-1])
            long = float(row[1][:-1])
            datum = row[2]
            lats.append(lat)
            longs.append(long)
            data.append(datum)
        except:
            pass
map = Basemap()

map.drawcoastlines()
map.fillcontinents()

x,y = map(longs, lats)

C = np.zeros((len(x),len(x)))

for i in range(len(x)):
    for j in range(len(y)):
        C[i][j] = 0
        if i == j:
            C[i][j] = data[i]

#for i in range(len(x)):
    #map.plot(x[i], y[i], marker='o',color='b')

map.pcolormesh(x,y,C,cmap='RdBu')

plt.show()
