import cPickle as pickle
import os,csv
import numpy as np

"""class author:
    def __init__(self,name=''):
        self.name = name
        self.data = {}

    def add(self,date,batch):
        self.data[date] = batch

with open('data/authors/aillaud.pkl','rb') as input:
    data = pickle.load(input)

cwd = os.getcwd()

d=data.data
d=d[d.keys()[0]]
d = d.split('\n')"""

def format(data,destination,filename):
    #If path doesn't exist, make it
    if not os.path.exists(destination):
        os.makedirs(destination)

    #Open file
    with open(destination+filename,'w') as f:
        attributes={}
        #Seperate lines of data
        d = data.split('\n')
        filewriter = csv.writer(f)

        #For each row of data...
        for row in d:
            #For each row, split in between |
            out = row.split("|")
            out_ = []
            #For each item in each row
            for i in range(len(out)):
                item = out[i]
                #Provided item isn't 0
                if len(item) != 0:
                    indices=[]
                    flag = 0
                    for x in range(len(item)):
                        if item[x] == ' ': #Mark whitespace for removal
                             indices.append(x)
                        if item[x] == '?': #Mark empty data
                             flag = 1
                    if len(indices) > 1: #If length is more than 1, reverse
                        indices.reverse()
                    for index in indices:
                        #Remove all items marked for removal
                        item = item[:index]+item[(index+1):]
                if flag == 1:
                    #If data is empty, enter as NaN
                    out_.append(-1)
                elif len(item) != 0:
                    #If not of 0 length, add to csv
                    out_.append(item)
            if len(out_) > 1:
                filewriter.writerow(out_) #Write to csv
                #print(out_)
            else:
                attributes = findAttributes(out_, attributes)
                #print('Error, output length <= 1: ',out_)

    return attributes

def findAttributes(text, attributesDict):
    #Get name of row
    try:
        text = ''.join(text)
        text = text.split(']')
        ident = text[0][1:]
        text = text[1].split('\r')[0]
        if ident in ['Observer', 'Country', 'City', 'Longitude', 'Latitude', 'LongitudeGMAP', 'LatitudeGMAP', 'Frequencies', 'Antenna', 'AzimutAntenna', 'ElevationAntenna', 'Pre-Amplifier', 'Receiver', 'ObservingMethod', 'Remarks', 'SoftFTP', 'Computer', 'Location', 'Azimuth', 'Elevation', 'Pre-amplifier', 'Observingmethod', 'REMARK', 'OBSERVER', 'COUNTRY', 'LATITUDE', 'LONGITUDE', 'CITY', 'FREQUENCY', 'ANTENNA', 'AZIMUTANTENNA', 'ELEVATIONANTENNA', 'REMARKS', 'PRE-AMPLIFIER', 'RECEIVER', 'OBSERVINGMETHOD']:
            attributesDict[ident] = text
        elif ident in ['E', '']:
            pass
        else:
            print('Unidentified ident: ', ident)
            with open('/home/cwp/EMC/lib/idents.txt', 'w') as f:
                f.write(ident + '\n')
                f.close()
    except:
        if text not in [[''], [-1]]:
            print('Error: ',text)
    return attributesDict



