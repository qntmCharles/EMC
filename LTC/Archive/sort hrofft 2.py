import os, shutil, glob
from os.path import isfile, join
from os import listdir
from datetime import timedelta, date

def daterange(start_date,end_date):
    for n in range(int((end_date-start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2016,1,1)
end_date = date(2016,9,16)

for single_date in daterange(start_date,end_date):
    date2 = single_date.strftime('%Y%m%d')
    date1 = single_date.strftime('%Y%m')
    shutil.rmtree('E:\\Archive\\hrofft\\'+date1+'\\'+date2+'\\a')