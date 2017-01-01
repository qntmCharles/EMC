from matplotlib import pyplot as plt
import pandas as pd
import os

rootDir = '/home/cwp/EMC/data/data/'
nums = []
dates = []

for i in range(0,17):
    for j in range(1,13):
        try:
            year = '20{0:02d}'.format(i)
            month = '{0:02d}'.format(j)

            fileDir = os.path.join(rootDir,year,month)

            numFiles = len(os.listdir(fileDir))

            nums.append(numFiles)
            date = pd.date_range(end=year+'-'+month, periods=1, freq='M')
            dates.append(date)
        except Exception as e:
            print(e)

fig = plt.figure()
ax = fig.add_subplot(111)
fig.suptitle('Contributing observers for January 2000 - November 2016', fontsize = 15, fontweight = 'bold')
ax.set_xlabel('Year', fontsize = 15)
ax.set_ylabel('Number of observers', fontsize = 15)
ax.plot(dates,nums)

plt.show()
