from mechanize import Browser
from bs4 import BeautifulSoup
from format import format
import urllib,os,time
import cPickle as pickle

def save_object(obj,filename):
    with open(filename,'wb') as output:
        pickle.dump(obj,output,pickle.HIGHEST_PROTOCOL)

class author:
    def __init__(self,name=''):
        self.name = name
        self.data = {}

    def add(self,date,batch):
        self.data[date] = batch

# Create a browser instance for url
b = Browser()
b.open("http://rmob.org/visualrmob.php")

# List of months to work with
months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November",
          "December"]
authors={}

def scrape(url):
       r = urllib.urlopen(url).read()
       soup = BeautifulSoup(r, "html.parser")
       return soup

#For each year...
for i in range(0, 1): #range should be 0,17
    #For each month...
    for month in months:
        # Format year
        year = "20{0:02d}".format(i)
        # Select 3rd form on page
        b.select_form(nr=2)
        # Fill in year and month forms
        b.form['annee'] = [year,]
        b.form['mois'] = [month,]
        # Submit request
        res = b.submit()
        # Read contents of request
        c = res.read()
        #Parse in beautiful soup
        c = BeautifulSoup(c,"html.parser")

        data={}

        for link in c.find_all('a'):
            if link.get('href') and (link.get('href')[:6] == 'visual'):
                data[link.get('href')[12:-15]] = ('http://rmob.org/'+link.get('href'),str(link.get('href')[-12:-8]+'-'+link.get('href')[-14:-12]))

        for name,attributes in data.items():
            link=attributes[0]
            date=attributes[1]
            batch = scrape(link).encode('utf-8')
            time.sleep(10)

            choice = str(raw_input('Format or save as-is? (y/n)'))
            if choice != 'n':
                format(batch,str('/home/cwp/EMC/data/data/'+year+'/'+month+'/'),str(name+'.csv'))
            else:
                pass

            if name not in authors:
                authors[name] = author(name)
            authors[name].add(date,str('/home/cwp/EMC/data/data/'+year+'/'+month+'/'+name+'.csv'))
for name,authorobj in authors.items():
    print(name, authorobj.data)

#Pickle dump all author objects to file
for name,authorobj in authors.items():
    save_object(authorobj,str('data/authors/'+name+'.pkl'))

