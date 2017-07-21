import cPickle as pickle
import os

cwd = '/home/cwp/EMC/data/authors/'
basedir = '/home/cwp/EMC/lib/analysis/variation/temporal'

authors={}
for filename in os.listdir(cwd):
    with open(cwd+filename, 'rb') as input:
        authors[filename[:-4]] = pickle.load(input)

N = []
S = []

for name, observer in authors.items():
    if len(observer.locationAttr.keys()) != 0:
        if "LatitudeGMAP" in observer.locationAttr.keys():
            try:
                if float(observer.locationAttr["LatitudeGMAP"]) > 0:
                    N.append(name)
                else:
                    S.append(name)
            except:
                if observer.locationAttr["LatitudeGMAP"][:-1] == "N":
                    N.append(name)

        elif "Latitude" in observer.locationAttr.keys():
            if observer.locationAttr["Latitude"][-1] == "N":
                N.append(name)
            elif observer.locationAttr["Latitude"][-1] == "S":
                S.append(name)

print(len(S)+len(N))

with open(basedir+'/Nobservers.txt', 'w') as f:
    for observer in N:
        f.write(observer)
        f.write('\n')
    f.close()

with open(basedir+'/Sobservers.txt', 'w') as f:
    for observer in S:
        f.write(observer)
        f.write('\n')
    f.close()
