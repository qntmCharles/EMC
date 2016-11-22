from bs4 import BeautifulSoup
import urllib, os
import numpy as np

years = map(str,map(int,np.linspace(1993,2016,24)))
months = ["01","02","03","04","05","06","07","08","09","10","11","12"]

for year in years:
    for month in months:
        if not os.path.exists("F:\\RMOB\\"+year):
            os.mkdir("F:\\RMOB\\"+year)
        if not os.path.exists("F:\\RMOB\\"+year+"\\"+month+"\\"):
            os.mkdir("F:\\RMOB\\"+year+"\\"+month+"\\")
            url = 'http://rmob.org/rmobtext/rmob'+year[2:]+month+'.txt'
            r = urllib.urlopen(url,"lxml").read()
            soup = BeautifulSoup(r,"lxml")
            soup_text = soup.getText()
            with open("F:\\RMOB\\"+year+"\\"+month+"\\file.txt","w") as f:
                f.write(soup.encode('utf-8'))
                f.close()
            with open("F:\\RMOB\\"+year+"\\"+month+"\\text.txt","w") as f:
                f.write(soup_text.encode('utf-8'))
                f.close()