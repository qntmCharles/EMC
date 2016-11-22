from bs4 import BeautifulSoup
import urllib, os
import numpy as np



url = urllib.urlopen("http://rmob.org/visualrmob.php","lxml").read()
soup = BeautifulSoup(url,"lxml")

with open("F:\\RMOBtxt\\webpage.txt","w") as f:
    f.write(soup.encode('utf-8'))
    f.close()
    
#for link in soup.find_all('a'):
#    print(link.get('href'))