from mechanize import Browser
from bs4 import BeautifulSoup
from format import format as formatAndGetAttributes
import urllib,os,time
import numpy as np
import cPickle as pickle
from classes import Author, Entry

def save_object(obj,filename):
    #Need to make it create the file, maybe?
    with open(filename,'wb') as output:
        pickle.dump(obj,output,pickle.HIGHEST_PROTOCOL)

# Create a browser instance for url
b = Browser()
b.set_handle_robots(False)
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

allauthors = []
authorCount = 0
entryCount = 0
yearCount = 0
startFlag = True
startMonth = 'January'

with open('/home/cwp/EMC/lib/upTo.txt', 'r') as f:
    idx = f.readlines()
    yearCount = idx[0].split('\n')[0]
    startMonth = idx[1].split('\n')[0]
    authorCount = int(idx[2].split('\n')[0])
    entryCount = int(idx[3].split('\n')[0])

print('Starting from: '+startMonth+" 20{0:02d}".format(int(yearCount)))

#List all filenames in given directory
filenames = os.listdir('/home/cwp/EMC/data/authors/')

#For each path in filenames...
for path in filenames:
    #Open cwd + path
    with open('/home/cwp/EMC/data/authors/'+path, 'rb') as newInput:
        print('Loaded: '+path[:-4])
        #Unpickle the file
        authors[path[:-4]] = pickle.load(newInput)

#For each year...
for i in range(int(yearCount),17): #range should be 0,17
    for month in months:
        if (month != startMonth) and startFlag:
            continue
        startFlag = False

        with open('/home/cwp/EMC/lib/upTo.txt', 'w') as f:
            f.write(str(i)+'\n')
            f.write(month+'\n')
            f.write(str(authorCount)+'\n')
            f.write(str(entryCount)+'\n')
            f.close()

        # Format year
        year = "20{0:02d}".format(i)
        print(month, year)
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
                try:
                    fullLink = link.get('href')
                    name = fullLink.split('/')[2][:-15]
                    date = fullLink.split('/')[2][-14:][:6]
                    month = date[:2]
                    year = date[2:]
                    dateString = year+'-'+month

                    #print('Author: '+name+'-')
                    data[name] = ('http://rmob.org/'+fullLink, dateString)
                except:
                    print('Error')

        for name,attributes in data.items():
            #print('----New Data----')
            #print('Author: '+name)
            link=attributes[0]
            #print(link)
            date=attributes[1]
            #print(date)
            batch = scrape(link).encode('utf-8')
            #print(batch)

            attr = formatAndGetAttributes(batch,str('/home/cwp/EMC/data/data/'+year+'/'+month+'/'),str(name+'.csv'))

            #Prevent the internet from thinking it's hax0rs
            time.sleep(2)

            if name == '':
                continue

            if name not in authors:
                print('Found new author: ',name)
                authorCount += 1
                allauthors.append(name)
                authors[name] = Author(name)
                authors[name].addAttr(attr)

            print('Adding data to author: '+name)

            newEntry = Entry(str('/home/cwp/EMC/data/data/'+year+'/'+month+'/'+name+'.csv'), date)
            entryCount += 1
            authors[name].add(date,newEntry)

        print('Current list of new authors: ',allauthors)
        for name, authorobj in authors.items():
            #print(name, authorobj)
            save_object(authorobj,  str('/home/cwp/EMC/data/authors/'+name+'.pkl'))

        with open('/home/cwp/EMC/lib/authors.txt', 'a+') as f:
            listOfAuthors = f.read().splitlines()
            for author in allauthors:
                if author not in listOfAuthors:
                    f.write(author+'\n')
            f.close()

"""for name, authorobj in authors.items():
    print(name, authorobj.data)

#Pickle dump all author objects to file
for name, authorobj in authors.items():
    save_object(authorobj,str('/home/cwp/EMC/data/authors/'+name+'.pkl'))"""
