import cPickle as pickle
import numpy as np
import os, csv
from matplotlib import pyplot as plt
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
def getAttr(attr, authorobj, attrType):
    if attrType == 'Location':
        attrDict = authorobj.locationAttr
    elif attrType == 'Setup':
        attrDict = authorobj.setupAttr
    else:
        print('Unknown attribute type')

    if attr in attrDict.keys():
        return attrDict[attr]
    else:
        return 'Unknown'

hist = {}

for name,authorobj in authors.items():
    result = getAttr('Country', authorobj, 'Location')
    if result in ['Unknown', '']:
        continue

    if result in ['GreatBritain', 'unitedkingdom', 'UnitedKingdom']:
        result = 'UK'

    if result in ['FranceBRETAGNE', 'France']:
        result = 'France'

    if result in ['USA', 'UnitedStatesofAmerica']:
        result = 'USA'

    if result in ['Canada', 'CanadaV2K5N9']:
        result = 'Canada'

    if result in ['Czechrepublic', 'CzechRepublic']:
        result = 'Czech Republic'

    if result == 'RussianFederation':
        result = 'Russia'

    if result in ['spain']:
        result = 'Spain'

    if result not in hist.keys():
        hist[result] = 1
    else:
        hist[result] += 1

histList = []
for key, value in hist.items():
    histList.append((key,value))

countriesOrdered = []
countsOrdered = []
for x in sorted(histList, key=lambda tup: tup[1]):
    countriesOrdered.append(x[0])
    countsOrdered.append(x[1])

countriesOrdered.reverse()
countsOrdered.reverse()
print(countriesOrdered)
print(countsOrdered)

indices = np.arange(len(countriesOrdered))
width = 0.6
fig, ax = plt.subplots()
rects1 = ax.bar(indices+width, countsOrdered, width, color='b', align='center')
ax.set_xticks(indices+width)
ax.set_xticklabels(countriesOrdered, rotation = 45, ha='right')
fig.suptitle('Locations of observers (where known)', fontsize = 15, fontweight = 'bold')
ax.set_xlabel('Country', fontsize = 15)
ax.set_ylabel('Number of observers', fontsize = 15)

plt.tight_layout()

plt.show()

"""
    dC, hC = analyseAuthor(authorobj)

    #For IRC stuff
    with open('/home/cwp/EMC/stats/'+name+'.txt', 'w') as f:
        f.write(str(hC)+';')
        f.write(str(dC))
        f.close()
"""
