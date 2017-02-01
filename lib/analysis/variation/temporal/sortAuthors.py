import cPickle as pickle
import os

cwd = '/home/cwp/EMC/data/authors/'

authors={}
for filename in os.listdir(cwd):
    with open(cwd+filename, 'rb') as input:
        authors[filename[:-4]] = pickle.load(input)

sortedObservers = []
with open('/home/cwp/EMC/lib/analysis/variation/temporal/EUobservers.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        sortedObservers.append(line.split('\n')[0])

with open('/home/cwp/EMC/lib/analysis/variation/temporal/USobservers.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        sortedObservers.append(line.split('\n')[0])

add=[]
for name, observer in authors.items():
    if name not in sortedObservers:
        if len(observer.locationAttr.keys()) != 0:
            print(name)
            print(observer.locationAttr)
            choice = raw_input('Add to list of ASIA observers?')
            if choice == '1':
                add.append(name)
print(add)
with open('/home/cwp/EMC/lib/analysis/variation/temporal/ASIAobservers.txt', 'w') as f:
    for observer in add:
        f.write(observer)
        f.write('\n')
    f.close()
