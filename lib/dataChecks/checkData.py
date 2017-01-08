import cPickle as pickle
import numpy as np
import os, csv
from matplotlib import pyplot as plt

authors={}

#Define directories
cwd = '/home/cwp/EMC/data/authors/'
filenames = os.listdir(cwd)
#print(filenames)

#Load files
for filename in filenames:
    with open(cwd+filename,'rb') as input:
        #print(filename[:-4])
        authors[filename[:-4]] = pickle.load(input)

for name, observer in authors.items():
    for date, entry in observer.data.items():
        entry.loadData()
        for day, data in entry.data.items():
            for item in data[:-1]:
                try:
                    int(item)
                except:
                    print('------Error!------')
                    print('Observer: '+name)
                    print('Date: '+date)
                    print('Day: '+day)
                    print('Hour: '+str(data.index(item)))
                    print('Item: '+item)
                    raw_input()
                    break
