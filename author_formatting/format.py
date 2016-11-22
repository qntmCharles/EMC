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
    if not os.path.exists(destination):
        os.makedirs(destination)
    with open(destination+filename,'w') as f:
        d = data.split('\n')
        filewriter = csv.writer(f)
        for row in d:
            #For each row, split in between |
            out = row.split("|")
            out_ = []
            for i in range(len(out)):
                #For each item in each row
                item = out[i]
                if len(item) != 0:
                    #Provided item isn't 0
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
                    out_.append(np.nan)
                elif len(item) != 0:
                    #If not of 0 length, add to csv
                    out_.append(item)
            if len(out_) > 1:
                filewriter.writerow(out_) #Write to csv
                print(out_)
            else:
                print('Error, output length <= 1. ',out_)
