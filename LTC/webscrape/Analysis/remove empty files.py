import numpy as np
import os, shutil

years = map(str,map(int,np.linspace(1993,2016,24)))
months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
flag=[]

for year in years:
    for month in months:
        directory = "F:\\RMOB\\"+year+"\\"+month+"\\"
        if os.path.exists(directory):
            with open(directory+"text.txt","r") as f:
                text = f.read().splitlines()
            for line in text:
                if line == '404 Not Found':
                    shutil.rmtree("F:\\RMOB\\"+year+"\\"+month)