from datetime import datetime

allData = {}

with open('/home/cwp/EMC/lib/analysis/plotData.txt', 'r') as f:
    data = f.readlines()

with open('/home/cwp/EMC/lib/analysis/plotTimes.txt', 'r') as f:
    time = f.readlines()

for i in range(len(data)):
    newData = data[i].split(',')
    newData[-1] = newData[-1].split('\n')[0]
    newTime = datetime.strptime(time[i].split('\n')[0], "%Y-%m-%d %H:%M:%S")
    allData[newTime] = newData
    print(newTime, newData)
    raw_input()
