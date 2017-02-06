import cPickle as pickle
import numpy as np
import os, csv
from matplotlib import pyplot as plt

authors={}

# Define directories
cwd = '/home/cwp/EMC/data/authors/'
filenames = os.listdir(cwd)

# Load files
for filename in filenames:
    with open(cwd+filename,'rb') as input:
        #print(filename[:-4])
        authors[filename[:-4]] = pickle.load(input)

choice = str(raw_input('Enter observer: '))
print('Observer has '+str(len(authors[choice].data.values()))+' entries')
for date, entry in authors[choice].data.items():
    print('Date: '+date)
    entry.loadData()
    dates = sorted(entry.data.keys())
    for date in dates:
        print(date, entry.data[date])
    raw_input('Show next?')
