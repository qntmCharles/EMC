from matplotlib import pyplot as plt
from datetime import datetime, timedelta
import numpy as np

def getdata(filepath):
    a=[]
    year = filepath[-12:-8]
    month = open(filepath,'r').readline().rstrip().split("|")[0]
    for  line in open(filepath,'r'):
        p = line.rstrip().split('|') #get rid of newlines, whitespace, and split into hour segments from 00h to 23h
        q=[]
        for i in p:
            q.append(i[1:]) #get rid of whitespace
        a.append(q[:-1]) #get rid of ''
    a = a[1:-17] #remove dates and guff at end
    return a,month,year

def runningmean(x, N):
    return np.convolve(x,np.ones((N,))/N)[(N-1):]

def plotmonth(month):
    ydata=[]
    ydatanew=[]
    xdata=[]
    #filepath = 'E:\\Colorgramme Lab\\rmob\\2015\\Lockyer_Observatory_'+month+'2015rmob.txt'
    filepath = '/home/cwp/rmob/'+YEAR+'/Lockyer_Observatory_'+month+YEAR+'rmob.TXT'
    data,month,year = getdata(filepath)
    count=0
    for line in data:
        count+=1
        for i in range(1,len(line)):
            print(line[i])
            if line[i] != '?? ':
                ydata.append(line[i])
                if i == 24:
                    d= datetime.strptime(str(year)+":"+str(month)+":"+str(count)+":"+"00","%Y:%b:%d:%H")
                    d+= timedelta(days=1)
                    xdata.append(d)
                else:
                    xdata.append(datetime.strptime(str(year)+":"+str(month)+":"+str(count)+':'+str(i),'%Y:%b:%d:%H'))
            else:
                print('Missing data: ',line[i])
    ydatanew = map(int,ydata)
    ydatanew = runningmean(ydatanew,24)
    print('length of x for month ',month,':',len(xdata))
    print('length of y for month ',month,':',len(ydatanew))
    return ydata, ydatanew, xdata

months  = ['01','02','03','04','05','06','07','08','09','10','11','12']

#for YEAR in ['2012','2013','2014','2015','2016']:
for YEAR in ['2015']:
    xdata=[]
    ydata=[]
    run_mean=[]
    for i in months:
        try:
            newydata,runningmeanydata,newxdata = plotmonth(i)
            ydata.extend(newydata)
            run_mean.extend(runningmeanydata)
            xdata.extend(newxdata)
        except Exception as e:
            print(e)

    if len(xdata) != 0:
        with open('/home/cwp/EMC/LTC/rmob/data/'+YEAR+'rmobdata.txt','w') as f:
            for item in ydata:
                f.write(str(item)+'\n')

        with open('/home/cwp/EMC/LTC/rmob/data/'+YEAR+'rmobtimes.txt','w') as f:
            for item in xdata:
                f.write(str(item)+'\n')

        #plt.plot(xdata,ydata,'b',alpha=0.5)
        #plt.show()

#Get this to save the times and counts for all hours between two dates, same for other data set
#Then test correlation
