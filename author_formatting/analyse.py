import cPickle as pickle
import os

class author:
    def __init__(self,name=''):
        self.name = name
        self.data = {}

    def add(self,date,batch):
        self.data[date] = batch

authors={}

cwd = os.getcwd() + '/data/authors/'
filenames = os.listdir(cwd)
for filename in filenames:
    with open(cwd+filename,'rb') as input:
        authors[filename[:-4]] = pickle.load(input)

print(authors)
