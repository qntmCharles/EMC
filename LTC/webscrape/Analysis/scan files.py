import numpy as np
import os
from matplotlib import pyplot as plt
from datetime import datetime

years = map(str,map(int,np.linspace(1993,2016,24)))
months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
linelengths=[]
times=[]

for year in years:
    for month in months:
        directory = "/home/cwp/ext/RMOB/"+year+"/"+month+"/"
        if os.path.exists(directory):
            with open(directory+"text.txt","r") as f:
                linelengths.append(len(f.read().splitlines()))
                times.append(datetime.strptime(year+month,"%Y%m"))


plt.plot(times,linelengths)
plt.show()
