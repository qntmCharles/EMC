import numpy as np

class Entry:
    def __init__(self, dataSrc, date):
        self.date = date
        self.dataSrc = dataSrc
        self.data = None

    def loadData(self):
        #Load data into program
        import csv
        with open(self.dataSrc, 'r') as f:
            readFile = list(csv.reader(f))
        #Remove the month & hour information
        readFile = readFile[1:]
        #Initialise dictionary
        dataDict = {}

        #Split into day and data for dictionary
        for day in readFile:
            dayNum = day[:1][0]
            dayData = day[1:]
            dataDict[dayNum] = dayData

        self.data = dataDict

    def calculateActiveDays(self):
        count = 0
        days = []
        for dayNum,dayData in self.data.items():
            flag = False
            for i in range(len(dayData)):
                if dayData[i] >= 0:
                    flag = True
            count += 1
            days.append(dayNum)

        return count, days

    def calculateActiveHours(self, dayNum):
        count = 0
        hours=[]
        curData = self.data[dayNum]
        for i in range(len(curData)):
            if curData[i] >= 0:
                count += 1
                hours.append(i)

        return count, hours

class Author:
    def __init__(self,name):
        self.username = name
        self.data = {}
        self.locationAttr = {}
        self.setupAttr = {}
        self.name = []

    def add(self,date,entry):
        self.data[date] = entry

    def addAttr(self, attributesDict):
        for key, value in attributesDict.items():
            if key in ['Country', 'City', 'Latitude', 'Longitude', 'LatitudeGMAP', 'LongitudeGMAP', 'Location', 'COUNTRY', 'LATITUDE', 'LONGITUDE', 'CITY', 'LATITUDE+/-', 'LATITUDEDeg', 'LONGITUDE+/-']:
                if key not in self.locationAttr.keys():
                    self.locationAttr[key] = value
                    print('Added attribute '+key+': '+value)
            if key in ['Antenna', 'Frequencies', 'AzimutAntenna', 'ElevationAntenna', 'Pre-Amplifier', 'Receiver', 'Observing Method', 'Pre-amplifier', 'Azimuth', 'Elevation', 'REMARK', 'REMARKS',  'Remarks', 'Observingmethod', 'FREQUENCY', 'ANTENNA', 'AZIMUTANTENNA', 'ELEVATIONANTENNA', 'PRE-AMPLIFIER', 'RECEIVER', 'OBSERVINGMETHOD', 'WEB']:
                if key not in self.setupAttr.keys():
                    self.setupAttr[key] = value
                    print('Added attribute '+key+': '+value)
            if key == 'Observer' or 'OBSERVER':
                if value not in self.name:
                    self.name.append(value)

    def removeAttr(self, attrType, attrIdent):
        if attrType == 'Location':
            if attrIdent in self.locationAttr.keys():
                del self.locationAttr[attrIdent]
            else:
                print('Error: unknown attribute identifier')

        elif attrType == 'Setup':
            if attrIdent in self.setupAttr.keys():
                del self.setupAttr[attrIdent]
            else:
                print('Error: unknown attribute identifier')

        else:
            print('Error: unknown attribute type')

    def merge(self, otherAuthor):
        for name in otherAuthor.name:
            if name not in self.name:
                self.name.append(name)

        self.addAttr(otherAuthor.locationAttr)
        self.addAttr(otherAuthor.setupAttr)
        self.data = self.data.copy()
        self.data.update(otherAuthor.data)
        #May want to check this works before going ahead
