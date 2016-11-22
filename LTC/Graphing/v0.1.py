import matplotlib.pyplot as plt
from datetime import datetime
averages = []
timecount = []
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
                            start = 0
                            end = 3
                            if int(monthrange_u) <= 7:
                                start = 3
                                end = 4
                            for n in range(start,end):
                                years = ["2015","2016"]
                                months=["01","02","03","04","05","06","07","08","09","10","11","12"]
                                dates=["01","02","03","04","05","06","07","08","09","10","11","12","13",
                    "14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
                                file=["a","b","c",""]
                                if int(monthrange_u) <= 7:
                                    n=3
                                logdirectory="Z:\\2D\\"+years[z]+months[y]+"\\"+years[z]+months[y]+dates[x]+"\\_log.txt"
                                date = dates[x]+"/"+months[y]+"/"+years[z]
                                timestamp = datetime.strptime(date, "%d/%m/%Y")
                                print(logdirectory)
                                count = 10
                                with open(logdirectory) as searchfile:
                                    sepcount = 0
                                    for line in searchfile:
                                        left,sep,right = line.partition('Average: ')
                                        if sep:
                                            sepcount += 1
                                            print(right[:count])
                                            if sepcount == 1:
                                                averages.append(right[:count])
                                                timecount.append(timestamp)
                                            if sepcount == 2:
                                                print(right[:count]) #plot
                                            if sepcount == 3:
                                                print(right[:count]) #plot
                                flag = 0 
                    except:
                        print('day break')

            except:
                print('month break') 

    except:
        print('year break')

                
print(timecount)            
f1 = plt.figure()
plt.scatter(timecount, averages)
f2 = plt.figure()
plt.plot(timecount,averages)
plt.show()

#to implement: 
#plotting long term - saving data onto a text file for permanent storage
#seperate program to plot
#seperate program to get data and save it

#analyse data from 2014 onwards
