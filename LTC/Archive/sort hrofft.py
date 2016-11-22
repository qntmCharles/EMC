import os, shutil, glob
from os.path import isfile, join
from os import listdir
from datetime import timedelta, date

def daterange(start_date,end_date):
    for n in range(int((end_date-start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2016,2,5)
end_date = date(2016,9,19)

for single_date in daterange(start_date,end_date):
    try:
        date2 = single_date.strftime('%Y%m%d')
        date1 = single_date.strftime('%Y%m')
        path='E:\\Archive\\hrofft\\'+date1+'\\'+date2+'\\a\\'
        dst ='E:\\Archive\\hrofft\\'+date1+'\\'+date2+'\\'
        print(dst)
        #onlyfiles = [f for f in listdir(path) if isfile(join(path,f))]
        #for file in onlyfiles:
            #print(path+file,dst+file)
            #shutil.copy(path+file,dst+file)
        shutil.rmtree('E:\\Archive\\hrofft\\'+date1+'\\'+date2+'\\a')
    except Exception as e:
        print(e)