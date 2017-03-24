import os, statistics

showers = ['geminids', 'leonids', 'orionids', 'perseids', 'quadrantids',\
        'eta_aquariids']

files = ['allData', 'closePeakData', 'peakData']

basedir = '/home/cwp/EMC/lib/analysis/zhr/finalData/'

possibilities = ['Average of all: ','Err of all: ','UQ of all: ',\
        'Average of peak: ','Err of peak: ','UQ of peak: ',\
        'Average of close peak: ','Err of close peak: ','UQ of close peak: ']

for shower in showers:
    print('===========%s===========' % shower)
    avgs = {}
    pers = {}
    errs = {}
    for directory in files:
        avgs[directory]={}
        pers[directory]={}
        errs[directory]={}

        for observerFile in os.listdir(basedir+directory+'/'+shower+'/'):
            with open(basedir+directory+'/'+shower+'/'+observerFile, 'r') as f:
                allLines = f.readlines()
                for line in allLines:
                    year = line.split(',')[0]
                    avgZhr = float(line.split(',')[1])
                    errZhr = float(line.split(',')[2])
                    perZhr = float(line.split(',')[3].split('\n')[0])

                    if year not in avgs[directory].keys():
                        avgs[directory][year] = [avgZhr]
                    else:
                        avgs[directory][year].append(avgZhr)

                    if year not in errs[directory].keys():
                        errs[directory][year] = [errZhr]
                    else:
                        errs[directory][year].append(errZhr)

                    if year not in pers[directory].keys():
                        pers[directory][year] = [perZhr]
                    else:
                        pers[directory][year].append(perZhr)


    for year in ['2005','2006','2007','2010','2011','2012','2013','2014','2015','2016']:
        print('Year: ',year)
        try:
            with open(basedir+'final/'+year+shower+'.txt', 'r') as f:
                lines = f.readlines()

            for i in range(len(lines)):
                print(lines[i])

        except:
            pass

        """
        for directory in files:
            try:
                print(directory)
                print('Mean mean: ',statistics.mean(avgs[directory][year]))
                print('Mean err: ',statistics.mean(errs[directory][year]))
                print('Mean 90th percentile: ',statistics.mean(pers[directory][year]))
            except:
                pass
        """
        raw_input()
