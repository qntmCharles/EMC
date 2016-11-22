from matplotlib import pyplot as plt
from datetime import datetime, timedelta
import numpy as np
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
    a = a[1:-17] #remove dates and guff at end
    return a,month,year

def runningmean(x, N):
    return np.convolve(x,np.ones((N,))/N)[(N-1):]

def plotmonth(month):
    ydata=[]
    xdata=[]
    filepath = 'E:\\Colorgramme Lab\\rmob\\2015\\Lockyer_Observatory_'+month+'2015rmob.txt' 
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
    print(len(xdata))
    print(len(ydata))
    plt.plot(xdata,ydata,'b',alpha=0.5)
    plt.plot(xdata,ydatanew,'r')
    plt.show()
months  = ['01','02','03','04','05','06','07','08']#,'09','10','11','12']
for i in months:
    plotmonth(i)
