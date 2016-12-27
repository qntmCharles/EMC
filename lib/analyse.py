import cPickle as pickle
import numpy as np
import os, csv
#from classes import Author#,Entry

"""def calculateActiveDays(self):
        count = 0
        days = []
        for dayNum,dayData in self.data.items():
            flag = False
            for i in range(len(dayData)):
                if dayData[i] != np.NaN:
                    flag = True
            count += 1
            days.append(dayNum)

        return count, days

    def calculateActiveHours(self, dayNum):
        count = 0
        curData = self.data[dayNum]
        for i in range(len(curData)):
            if curData[i] != Np.NaN:
                count += 1
                hours.append(i)

        return count, hours"""

def analyseAuthor(authorobj):
    totalHourCount = 0
    totalDayCount = 0
    print('Author: ',authorobj.username)
    for date,entry in authorobj.data.items():
        #Initialise data
        entry.loadData()
        dayCount, daysList = entry.calculateActiveDays()
        daysList.sort()
        #print('Date: '+date)
        #print('Active on '+str(dayCount)+' days: '+', '.join(daysList))
        #For each active day, check active hours
        for num in daysList:
            hourCount, hoursList = entry.calculateActiveHours(num)
            #if hourCount != 0:
                #print('     On day '+str(num)+' there were '+str(hourCount)+' active hours: '+', '.join([str(x) for x in hoursList]))
            totalHourCount += hourCount
        totalDayCount += dayCount

        #Wait to continue
    return totalDayCount, totalHourCount

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

#Open files and display
#print(authors)
for name,authorobj in authors.items():
    print(authorobj.locationAttr)
    print(authorobj.setupAttr)
    print(authorobj.username)
    #print(name, authorobj.data)
    dC, hC = analyseAuthor(authorobj)

"""
    #For IRC stuff
    with open('/home/cwp/EMC/stats/'+name+'.txt', 'w') as f:
        f.write(str(hC)+';')
        f.write(str(dC))
        f.close()
"""
