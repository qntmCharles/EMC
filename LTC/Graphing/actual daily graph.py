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
#date,month,day,year = findTime()
option = int(input('Choose range as months (1) or days (0)?'))
if option == 1:
    monthrange_l = int(input('Start month (numerical): '))
    monthrange_u = int(input('End month (numerical): '))
    yearrange_l = int(input('Start year (from 2015 =1) (numerical): '))
    yearrange_u = int(input('End year (from 2015 =1) (numerical): '))
    dayrange_l = int(input('Start day date:'))
    dayrange_u = int(input('End day date:'))
elif option == 0:
    yearrange_l = int(input('Start year (from 2015 =1) (numerical): '))
    yearrange_u = int(input('End year (from 2015 =1) (numerical): '))
    monthrange_u = int(input('Month (numerical): '))
    monthrange_l=monthrange_u
    dayrange_l = int(input('Start day date:'))
    dayrange_u = int(input('End day date:'))
elif option == 2:
    yearrange_l = 1
    yearrange_u = 2
    monthrange_l = 1
    monthrange_u = 12
    dayrange_l = 1
    dayrange_u = 31
if len(str(monthrange_u)):
    monthrange_u="0"+str(monthrange_u)
if len(str(monthrange_l)):
    monthrange_l="0"+str(monthrange_l)
if len(str(dayrange_u)):
    dayrange_u="0"+str(dayrange_u)
if len(str(dayrange_l)):
    dayrange_l="0"+str(dayrange_l)
for z in range(int(yearrange_l)-1,int(yearrange_u)):
    try:
        print('pass')        
        for y in range(int(monthrange_l)-1,int(monthrange_u)):
            try:
                print("pass")
                for x in range(int(dayrange_l)-1,int(dayrange_u)):
                    try:
                        years = ["2015","2016"]
                        months=["01","02","03","04","05","06","07","08","09","10","11","12"]
                        dates=["01","02","03","04","05","06","07","08","09","10","11","12","13",
                    "14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
                        averagesfilepath = "Z:\\2D\\"+years[z]+months[y]+"\\"+years[z]+months[y]+dates[x]+"\\averages.txt"
                        timesfilepath = "Z:\\2D\\"+years[z]+months[y]+"\\"+years[z]+months[y]+dates[x]+"\\times.txt"
                        averages = open(averagesfilepath,'r')
                        times = open(timesfilepath,'r')
                        with open(averagesfilepath) as f:
                            newydata = f.read().splitlines()
                        for i in newydata:
                            ydata.append(i)
                        with open(timesfilepath) as f:
                            timedata = f.read().splitlines() 
                        for line in timedata:
                            print(line)
                            print(datetime.datetime.strptime(line,'%Y:%m:%d:%H:%M'))
                            time = datetime.datetime.strptime(line,'%Y:%m:%d:%H:%M')
                            xdata.append(time)
                    except:
                        print('day break')

            except:
                print('month break') 

    except:
        print('year break')

print(xdata)
print(ydata)
print(len(xdata))
print(len(ydata))
plt.plot(xdata,ydata)
plt.show()

#check it's plotting stuff okay