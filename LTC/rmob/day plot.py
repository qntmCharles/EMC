from __future__ import division
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
def getdata(filepath):
    a=[]
    year = filepath[24:28]
    month = open(filepath,'r').readline().rstrip().split("|")[0]
    for  line in open(filepath,'r'):
        p = line.rstrip().split('|') #get rid of newlines, whitespace, and split into hour segments from 00h to 23h
        q=[]
        for i in p:
            q.append(i[1:]) #get rid of whitespace
        a.append(q[:-1]) #get rid of ''
    array = a[1:-17] #remove dates and guff at end
    return array,month,year
ydata=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
a,month,year = getdata('/home/cwp/ext/Colorgramme Lab/rmob/2015/Lockyer_Observatory_032015rmob.TXT')
count=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
for line in a:
    for x in range(1,len(line)):
        ydata[x-1] += int(line[x])
        count[x-1] += 1
for x in range(len(ydata)):
    ydata[x] = ydata[x]/count[x]
print(ydata)
start = pd.Timestamp(datetime(1900,1,1,1))
end = pd.Timestamp(datetime(1900,1,2,0))
t = np.linspace(start.value,end.value,24)
t = pd.to_datetime(t)
plt.plot(t,ydata)
