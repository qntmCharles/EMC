from __future__ import division
import cPickle as pickle
import numpy as np
import pandas as pd
import os, csv, sys, math
from matplotlib import pyplot as plt
from datetime import datetime
import datetime as dt
from plotting import plotFullMonth

authors={}

#Define directories
cwd = '/home/cwp/EMC/data/authors/'
filenames = os.listdir(cwd)

#Load files
for filename in filenames:
    with open(cwd+filename,'rb') as input:
        #print(filename[:-4])
        authors[filename[:-4]] = pickle.load(input)

for name, observer in authors.items():
    dates = sorted(observer.data.keys())
    try:
        saveDir = '/home/cwp/EMC/plots/fullCounts/'+observer.username+'/'
        for date in dates:
        #        if not os.path.exists(saveDir+date+'.png'):
                plotFullMonth(observer.data[date], name)
        if not os.path.exists(saveDir):
            os.mkdir(saveDir)
        plt.savefig(saveDir+observer.username+'FullData.png', dpi=500)
        plt.clf()
    except Exception as e:
        print('Exception for observer '+str(name)+' for entry '+str(date))
        print(e)

#Do this, and look at those errors
