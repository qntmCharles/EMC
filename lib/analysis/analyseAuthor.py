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

#Display
#print(authors)

def analyseAuthor(authorobj, verbose):
    totalHourCount = 0
    totalDayCount = 0
    print('Author: ',authorobj.username)
    for date,entry in authorobj.data.items():
        #Initialise data
        entry.loadData()
        dayCount, daysList = entry.calculateActiveDays()
        daysList.sort()
        if verbose:
            print('Date: '+date)
            print('Active on '+str(dayCount)+' days: '+', '.join(daysList))
        #For each active day, check active hours
        for num in daysList:
            hourCount, hoursList = entry.calculateActiveHours(num)
            if verbose and (hourCount != 0):
                print('     On day '+str(num)+' there were '+str(hourCount)+\
                        ' active hours: '+', '.join([str(x) for \
                        x in hoursList]))
            totalHourCount += hourCount
        totalDayCount += dayCount

    return totalDayCount, totalHourCount

for name, authorobj in authors.items():
    print(name)
