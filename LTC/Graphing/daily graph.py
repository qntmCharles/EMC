import matplotlib.pyplot as plt
import datetime
import calendar

def checkyear():
    now = datetime.datetime.now()
    if calendar.isleap(now.year) == True:
        day = 29
    else:
        day = 28
    return day
    
def findTime():
    now = datetime.datetime.now()
    day = now.day - 1
    month_options = {1:31,2:checkyear(),3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
    if day == 0:
        month = now.month - 1
        if month == 0:
            month = 12
        day = month_options[month]
    else:
        month = now.month
    if len(str(month))==1:
        month = "0"+str(month)
    if len(str(day)) == 1:
        day = "0"+str(day)
    year = str(now.year)
    month = str(month)
    date = str(year+month+"\\"+year+month+str(day)+"\\")
    return date,month,day,year
    
xdata=[]
ydata=[]
timedata=[]
date,month,day,year = findTime()
averagesfilepath = "Z:\\2D\\"+str(year)+str(month)+"\\"+str(year)+str(month)+str(day)+"\\averages.txt"
timesfilepath = "Z:\\2D\\"+str(year)+str(month)+"\\"+str(year)+str(month)+str(day)+"\\times.txt"
averages = open(averagesfilepath,'r')
times = open(timesfilepath,'r')
with open(averagesfilepath) as f:
    ydata = f.read().splitlines()
with open(timesfilepath) as f:
    timedata = f.read().splitlines() 
for line in timedata:
    print(line)
    print(datetime.datetime.strptime(line,'%Y:%m:%d:%H:%M'))
    time = datetime.datetime.strptime(line,'%Y:%m:%d:%H:%M')
    xdata.append(time)
     
print(xdata)
print(ydata)
plt.plot(xdata,ydata)
plt.show()