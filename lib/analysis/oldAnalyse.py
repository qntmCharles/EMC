import cPickle as pickle
import numpy as np
import os, csv
from difflib import SequenceMatcher
from matplotlib import pyplot as plt
#from classes import Author#,Entry

def analyseAuthor(authorobj, verbose):
    totalHourCount = 0
    totalDayCount = 0
    print('Author: ',authorobj.username)
    for date,entry in authorobj.data.items():
        #Initialise data
        entry.loadData()
        dayCount, daysList = entry.calculateActiveDays()
        daysList.sort()
        if verbose:
            print('Date: '+date)
            print('Active on '+str(dayCount)+' days: '+', '.join(daysList))
        #For each active day, check active hours
        for num in daysList:
            hourCount, hoursList = entry.calculateActiveHours(num)
            if verbose and (hourCount != 0):
                print('     On day '+str(num)+' there were '+str(hourCount)+\
                        ' active hours: '+', '.join([str(x) for \
                        x in hoursList]))
            totalHourCount += hourCount
        totalDayCount += dayCount

    return totalDayCount, totalHourCount

authors={}

#Define directories
cwd = '/home/cwp/EMC/data/authors/'
filenames = os.listdir(cwd)
#print(filenames)

#Load files
for filename in filenames:
    with open(cwd+filename,'rb') as input:
        #print(filename[:-4])
        authors[filename[:-4]] = pickle.load(input)

#Open files and display
#print(authors)

def mergeAuthors(finalAuthorName, mergeAuthorName, finalAuthor, mergeAuthor):
    #If both authors have data for the same month, cannot merge
    for key, value in mergeAuthor.data.items():
        if key in finalAuthor.data.keys():
            print('Error: multiple entries for same month. Cannot merge authors.')
            return None

    #Change text file names
    for date, entry in mergeAuthor.data.items():
        srcFile = entry.dataSrc
        print(srcFile)
        dstFile = os.path.split(entry.dataSrc)[0]+'/'+finalAuthorName+'.csv'
        print(dstFile)
        entry.dataSrc = dstFile
        os.rename(srcFile, dstFile)

    #Merge attributes
    for key, value in mergeAuthor.locationAttr.items():
        if key in finalAuthor.locationAttr.keys():
            if finalAuthor.locationAttr[key] != mergeAuthor.locationAttr[key]:
                print('Attribute conflict. Attribute: '+key)
                print('Final author (1): '+finalAuthor.locationAttr[key])
                print('Merge author (2): '+mergeAuthor.locationAttr[key])
                choice = int(raw_input('Choose (1) or (2) to keep: '))
                if choice == 2:
                    finalAuthor.locationAttr[key] = value
        else:
            finalAuthor.locationAttr[key] = value

    for key, value in mergeAuthor.setupAttr.items():
        if key in finalAuthor.setupAttr.keys():
            if finalAuthor.setupAttr[key] != mergeAuthor.setupAttr[key]:
                print('Attribute conflict. Attribute: '+key)
                print('Final author (1): '+finalAuthor.setupAttr[key])
                print('Merge author (2): '+mergeAuthor.setupAttr[key])
                choice = int(raw_input('Choose (1) or (2) to keep: '))
                if choice == 2:
                    finalAuthor.setupAttr[key] = value
        else:
            finalAuthor.setupAttr[key] = value

    for name in mergeAuthor.name:
        if name not in finalAuthor.name:
            finalAuthor.name.append(name)

    #Merge data
    for key, value in mergeAuthor.data.items():
        finalAuthor.data[key] = value

    #Delete line from authors text file
    #Get all authors
    with open('/home/cwp/EMC/lib/authors.txt','r') as f:
        authorsList = f.readlines()
        f.close()

    #Wipe file
    open('/home/cwp/EMC/lib/authors.txt', 'w').close()

    #Remove author then re-write to file
    authorsList.remove(mergeAuthorName+'\n')

    with open('/home/cwp/EMC/lib/authors.txt', 'w') as f:
        for line in authorsList:
            f.write(line)
        f.close()

    #Delete file from authors folder
    os.remove('/home/cwp/EMC/data/authors/'+mergeAuthorName+'.pkl')

    #Delete from program
    authors[mergeAuthorName] = None

    #Pickle
    with open('/home/cwp/EMC/data/authors/'+finalAuthorName+'.pkl', 'w') as f:
        f.close()

    with open('/home/cwp/EMC/data/authors/'+finalAuthorName+'.pkl', 'wb') as f:
        pickle.dump(finalAuthor, f, pickle.HIGHEST_PROTOCOL)

toMerge={}
with open('/home/cwp/EMC/lib/collections.txt', 'r') as f:
    toMerge1 = f.readlines()
    for entry in toMerge1:
        toMerge[entry.split(';')[0]] = entry.split(';')[1:-1]
print(toMerge)

for name, authorobj in authors.items():
    if name in toMerge.keys():
            print('-------------------------------------------------------------')
            print('Found author to merge: '+name)
            print('Options: '+','.join(toMerge[name]))
            for option in toMerge[name][:]:
                print('Merging with: '+option)
                print('Names:')
                print(authorobj.name)
                print(authors[option].name)
                print('Shared active months:')
                intersec = sorted(set(authorobj.data.keys()).intersection(authors[option].data.keys()))
                print(intersec)
                if (set(intersec) == set(authorobj.data.keys())) or (set(intersec) == set(authors[option].data.keys())):
                    print('This is the same as all the data in one of these observers.')
                    choice = int(raw_input('Delete author?: '))
                    if choice == 1:
                        for date, entry in authors[option].data.items():
                            os.remove(entry.dataSrc)

                        #Delete line from authors text file
                        #Get all authors
                        with open('/home/cwp/EMC/lib/authors.txt','r') as f:
                            authorsList = f.readlines()
                            f.close()

                        #Wipe file
                        open('/home/cwp/EMC/lib/authors.txt', 'w').close()

                        #Remove author then re-write to file
                        authorsList.remove(option+'\n')

                        with open('/home/cwp/EMC/lib/authors.txt', 'w') as f:
                            for line in authorsList:
                                f.write(line)
                            f.close()

                        #Delete file from authors folder
                        os.remove('/home/cwp/EMC/data/authors/'+option+'.pkl')

                        #Delete from program
                        authors[option] = None
                else:

                    print('Location attributes:')
                    print(authorobj.locationAttr)
                    print(authors[option].locationAttr)
                    print('Setup attributes:')
                    print(authorobj.setupAttr)
                    print(authors[option].setupAttr)
                    choice2 = int(raw_input('Continue to merge?: '))
                    if choice2 == 1:
                        mergeAuthors(name, option, authorobj, authors[option])

"""
for name, authorobj in authors.items():
    for date, entry in authorobj.data.items():
        if not os.path.exists(entry.dataSrc):
            print(name)
            print(entry.dataSrc)
            rootDir,fileStr = os.path.split(entry.dataSrc)
            entry.dataSrc = os.path.join(rootDir, name+'.csv')

            #Pickle
            with open('/home/cwp/EMC/data/authors/'+name+'.pkl', 'w') as f:
                f.close()

            with open('/home/cwp/EMC/data/authors/'+name+'.pkl', 'wb') as f:
                pickle.dump(authorobj, f, pickle.HIGHEST_PROTOCOL)

for name, authorobj in authors.items():
    dC, hC = analyseAuthor(authorobj)

    #For IRC stuff
    with open('/home/cwp/EMC/stats/'+name+'.txt', 'w') as f:
        f.write(str(hC)+';')
        f.write(str(dC))
        f.close()
        """
