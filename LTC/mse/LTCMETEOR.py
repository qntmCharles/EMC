from PIL import Image, ImageFilter, ImageChops #used in image import, analysis and export process
import math, operator, functools, os, glob, time, datetime, calendar #general use
import tkinter as Tkinter
from tkinter import filedialog as tkFileDialog

"""#####Clear shell function##### - clears shell screen"""
def cls():
    os.system(['clear','cls'][os.name=='nt'])

"""#####Date input#####"""
def checkyear():
    now = datetime.datetime.now()
    if calendar.isleap(now.year) == True:
        day=29
    else:
        day=28
    return day
def findTime():
    now = datetime.datetime.now()
    day = now.day - 1
    month_options = {1:31,2:checkyear(),3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:31,12:31}
    if day == 0:
        month = now.month - 1
        if month == 0:
            month = 12
        day = month_options[month]
    else:
        month = now.month
    if len(str(month)) == 1:
        month = "0"+str(month)
    if len(str(day)) == 1:
        day = "0"+str(day)
    year = str(now.year)
    month = str(month)
    date = str(year+month+"\\"+year+month+str(day)+"\\")
    return date

"""##### Directory size function##### - returns size of directory"""
def count_files(in_directory):
    joiner= (in_directory + os.path.sep).__add__
    return sum(
        os.path.isfile(filename)
        for filename
        in map(joiner, os.listdir(in_directory))
    )
def directorySize(directory):
    filesCount = count_files(directory)
    print("Number of files in ", directory, ":", filesCount)
    filelog.write("Number of files in "+ directory+ ":"+ str(filesCount)+"\n")
    return filesCount

"""##### RMS Difference Function #####"""
def rmsdiff(file1,file2):
    h = ImageChops.difference(file2,file1).histogram()
    #calculating RMS
    return math.sqrt(functools.reduce(operator.add,
        map(lambda h, i: h*(i**2), h, range(256))
    ) / (float(file1.size[0]) * file2.size[1]))

"""#####Geometric Mean Function #####"""
def geomean(inputlist,n,y): #inputlist - differences list, n - x point moving average, y - inputlist starting index
    valueslist=[]
    for x in range(0,n):
        valueslist.append(inputlist[y+x])
        print(valueslist)
    filelog.write("Past 5 image geomean: "+str(valueslist[n-1])+"\n")
    runningtotal=1
    for x in range(0,n):
        runningtotal = valueslist[x]*runningtotal
    geometric_mean=runningtotal**(1/n)
    return geometric_mean

"""##### Main program #####"""
folders=["a","b","c"]

for x in range(0,3):
    folder = folders[x]
    imagesdirectory = "C:\\Archive\\2D\\"+findTime()+folder
    filedirectory = "C:\\Archive\\2D\\"+findTime()
    if x == 0:
        if os.path.exists(filedirectory+"_log.txt"):
            open(filedirectory+"_log.txt","w").close()
        if os.path.exists(filedirectory+"averages.txt"):
            open(filedirectory+"averages.txt","w").close()
        if os.path.exists(filedirectory+"statistics.txt"):
            open(filedirectory+"statistics.txt","w").close()
        if os.path.exists(filedirectory+"times.txt"):
            open(filedirectory+"times.txt","w").close()
    filelog = open(filedirectory+"_log.txt","a")
    minaverage = open(filedirectory+"averages.txt","a")
    averagelog = open(filedirectory+"statistics.txt","a")
    times = open(filedirectory+"times.txt","a")
    print(imagesdirectory)
    filelog.write(imagesdirectory+"\n")
    image_list = []
    dir_list = []
    size = directorySize(imagesdirectory)
    filelog.write("Files in directory:"+str(size)+"\n")
    print(size)

    for filename in glob.glob(imagesdirectory+"\\*.jpg"):
        im=Image.open(filename)
        image_list.append(im)
        dir_list.append(filename)
        truncated = filename[-17:]
        date = truncated[:8]
        datetruncated = date[:6]
        month = datetruncated[-2:]
        day = date[-2:]
        timetruncated = truncated[-8:]
        timestr = timetruncated[:4]
        year = date[:4]
        hour = timestr[:2]
        minute = timestr[-2:]
        times.write(str(year)+":"+str(month)+":"+str(day)+":"+str(hour)+":"+str(minute)+"\n")
    print('--All images imported--')
    filelog.write('--All images imported--\n')

    for x in range(len(image_list)):  #Converting image modes
        if image_list[x].mode not in ("L","RGB"):
            image_list[x] = image_list[x].convert("RGB")

    for x in range(len(dir_list)):
        string = dir_list[x]
        stringlist = []
        stringlist = list(string)
        count = 0
        while count != 21:
            del stringlist[0]
            count = count+1
        del stringlist[8]
        del stringlist[8]
        string = "".join(stringlist)
        dir_list[x] = string

    baseimage = Image.open("C:\\Archive\\2D\\Averages\\2015\\20150101.png")

    """##### Analysis Section #####"""
    differences = []
    geomeans=[]
    for x in range(size):
        difference = rmsdiff(baseimage,image_list[x])
        differences.append(difference)
        print(x,":",difference)
        filelog.write(str(x)+":"+str(difference)+"\n")
        minaverage.write(str(difference)+"\n")
        #times.write()
        if ((x+1)%5 == 0):
            ans = geomean(differences,5,(x-4))
            geomeans.append(ans)
    print(differences)
    filelog.write("Differences list: ")
    for x in range(len(differences)):
        filelog.write(str(differences[x])+", ")
    filelog.write("\n")
    print("Average: ",sum(differences)/len(differences))
    filelog.write("Average: "+str(sum(differences)/len(differences))+"\n")
    averagelog.write(str(sum(differences)/len(differences))+"\n")
    print("Minimum: ", min(differences))
    filelog.write("Minimum: "+ str(min(differences))+"\n")
    averagelog.write(str(min(differences))+"\n")
    print("Maximum: ", max(differences))
    filelog.write("Maximum: "+ str(max(differences))+"\n")
    averagelog.write(str(max(differences))+"\n")
    var1 = sorted(range(len(geomeans)), key=lambda i: geomeans[i], reverse=True)[:5]
    print(var1)
    filelog.write(str(var1)+"\n")

    for x in range(len(var1)):
        var1[x]=((var1[x]+1)*5)-3

    for x in range(0,5):
        print(var1[x])
        filelog.write(str(var1[x])+"\n")

    max_list = ["","","","",""]
    for x in range(0,5):
        max_list[x] = dir_list[var1[x]]

    new_max_list=[]
    for n in range(0,5):
        variable = list(max_list[n])
        for x in range(1,10):
            del variable[0]
        new_max_list.append("".join(variable))

    if os.path.exists(imagesdirectory+"\\processed\\") is False:
        os.mkdir(imagesdirectory+"\\processed\\")

    for x in range(0,5):
        image_list[var1[x]].save(imagesdirectory+"\\processed\\"+new_max_list[x])
    time.sleep(10)
    filelog.close()
    times.close()
    averagelog.close()
    minaverage.close()
