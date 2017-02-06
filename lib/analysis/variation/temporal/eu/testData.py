import scipy.stats
dayData = []
nightData = []

with open('/home/cwp/EMC/lib/analysis/variation/temporal/asia/DYMplotData.txt', 'r') as f:
    datas = f.readlines()
    for i in range(len(datas)):
        if datas[i][:-1] != 'None':
            dayData.append(float(datas[i][:-1]))

with open('/home/cwp/EMC/lib/analysis/variation/temporal/asia/NYMplotData.txt', 'r') as f:
    datas = f.readlines()
    for i in range(len(datas)):
        if datas[i][:-1] != 'None':
            nightData.append(float(datas[i][:-1]))

print(scipy.stats.ttest_ind(dayData, nightData))
