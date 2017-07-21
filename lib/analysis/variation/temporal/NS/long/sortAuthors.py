import cPickle as pickle
import os, math

cwd = '/home/cwp/EMC/data/authors/'
basedir = '/home/cwp/EMC/lib/analysis/variation/temporal'

authors={}
for filename in os.listdir(cwd):
    with open(cwd+filename, 'rb') as input:
        authors[filename[:-4]] = pickle.load(input)

longs = {}
for i in range(-12,13):
    longs[i] = []

for name, observer in authors.items():
    if len(observer.locationAttr.keys()) != 0:
        if "LongitudeGMAP" in observer.locationAttr.keys():
            try:
                index=math.floor(float(observer.locationAttr["LongitudeGMAP"])/15)
                longs[index].append(name)
            except:
                continue

for key, item in longs.items():
    print(key)
    if len(item) > 0:
        for name in item:
            print(name, authors[name].locationAttr["LongitudeGMAP"])
        with open(basedir+'/NS/long/'+str(key)+'.txt','w') as f:
            for name in item:
                f.write(name)
                f.write('\n')
            f.close()
