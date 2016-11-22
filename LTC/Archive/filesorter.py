import datetime, time
from PIL import Image, ImageFilter, ImageChops #used in image import, analysis and export process
import math, operator, functools, os, glob, time, datetime, calendar #general use
import tkinter as Tkinter
from tkinter import filedialog as tkFileDialog
from shutil import copy

"""##### Initialise Function #####"""
def initialise():
    option = int(input('Choose range as months (1) or days (0)?'))
    if option == 1:
        monthrange_l = int(input('Start month (numerical): '))
        monthrange_u = int(input('End month (numerical): '))
        yearrange_l = int(input('Start year (from 2014 = 1) (numerical): '))
        yearrange_u = int(input('End year (from 2014 = 1) (numerical): '))
        dayrange_l = int(input('Start day date:'))
        dayrange_u = int(input('End day date:'))
    elif option == 0:
        yearrange_l = int(input('Start year (from 2014 = 1) (numerical): '))
        yearrange_u = int(input('End year (from 2014 = 1) (numerical): '))
        monthrange_u = int(input('Month (numerical): '))
        monthrange_l=monthrange_u
        dayrange_l = int(input('Start day date:'))
        dayrange_u = int(input('End day date:'))
    elif option == 2:
        yearrange_l = 1
        yearrange_u = 3
        monthrange_l = 1
        monthrange_u = 12
        dayrange_l = 1
        dayrange_u = 31
    if len(str(monthrange_u)):
        monthrange_u="0"+str(monthrange_u)
    if len(str(monthrange_l)):
        monthrange_l="0"+str(monthrange_l)
    if len(str(dayrange_u)):
        dayrange_u="0"+str(dayrange_u)
    if len(str(dayrange_l)):
        dayrange_l="0"+str(dayrange_l)
    return dayrange_l,dayrange_u,monthrange_l,monthrange_u,yearrange_l,yearrange_u

"""##### Main program #####"""

dayrange_l,dayrange_u,monthrange_l,monthrange_u,yearrange_l,yearrange_u = initialise()
for z in range(int(yearrange_l)-1,int(yearrange_u)):
    try:
        print('pass')
        for y in range(int(monthrange_l)-1,int(monthrange_u)):
            try:
                print('pass')
                for x in range(int(dayrange_l)-1,int(dayrange_u)):
                    try:
                        print('pass')
                        years = ["2014","2015","2016"]
                        months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
                        dates = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
                        #folder = folders[x]
                        imagesdirectory = "C:\\Archive\\2D\\"+years[z]+months[y]+"\\"+years[z]+months[y]+dates[x]+"\\"
                        t1 = datetime.datetime(int(years[z]),int(months[y]),int(dates[x]),7,00,0)
                        t2 = datetime.datetime(int(years[z]),int(months[y]),int(dates[x]),15,00,0)
                        t3 = datetime.datetime(int(years[z]),int(months[y]),int(dates[x]),23,2,0)
                        if not os.path.exists(imagesdirectory+"a"):
                            os.mkdir(imagesdirectory+"a")
                        if not os.path.exists(imagesdirectory+"b"):
                            os.mkdir(imagesdirectory+"b")
                        if not os.path.exists(imagesdirectory+"c"):
                            os.mkdir(imagesdirectory+"c")
                        for filename in glob.glob(imagesdirectory+"\\*.jpg"):
                            #im=Image.open(filename)
                            trunc1 = filename[-15:]
                            trunc3 = trunc1[:6]
                            trunc4 = trunc3[-4:]
                            print(trunc3,trunc4)
                            year = '20'+trunc3[:2]
                            month = trunc4[:2]
                            date = trunc4[-2:]
                            print('Processing image: ','20'+trunc1)
                            trunc2 = trunc1[-8:]
                            time = trunc2[:4]
                            file_t = datetime.datetime(int(year),int(month),int(date),int(time[:2]),int(time[-2:]),0)
                            print('Timestamp: ',file_t)
                            if file_t <= t1:
                                print('Sorted to t1')
                                os.rename(filename,imagesdirectory+"a\\"+filename[-30:])
                            elif file_t <= t2:
                                print('Sorted to t2')
                                os.rename(filename,imagesdirectory+"b\\"+filename[-30:])
                            elif file_t <= t3:
                                print('Sorted to t3')
                                os.rename(filename,imagesdirectory+"c\\"+filename[-30:])
                            else:
                                print('Image not sorted.')
                            print('---------------')
                    except:
                        print('day break')
            except:
                print('month break')
    except:
        print('year break')