import cPickle as pickle
import os, math

cwd = '/home/cwp/EMC/data/authors/'
basedir = '/home/cwp/EMC/lib/analysis/variation/temporal'

authors={}
for filename in os.listdir(cwd):
    with open(cwd+filename, 'rb') as input:
        authors[filename[:-4]] = pickle.load(input)

lats = {}
for i in range(-9,10):
    lats[i] = []

for name, observer in authors.items():
    if len(observer.locationAttr.keys()) != 0:
        if "LatitudeGMAP" in observer.locationAttr.keys():
            try:
                index=math.floor(float(observer.locationAttr["LatitudeGMAP"])/15)
                lats[index].append(name)
            except:
                continue

for key, item in lats.items():
    print(key)
    if len(item) > 0:
        for name in item:
            print(name, authors[name].locationAttr["LatitudeGMAP"])
        with open(basedir+'/NS/lat/'+str(key)+'.txt','w') as f:
            for name in item:
                f.write(name)
                f.write('\n')
            f.close()
