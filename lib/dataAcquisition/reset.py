import os, shutil

with open('/home/cwp/EMC/lib/upTo.txt', 'w') as f:
    f.truncate()
    f.write('0\n')
    f.write('January\n')
    f.write('0\n')
    f.write('0\n')
    f.close()

filenames = os.listdir('/home/cwp/EMC/data/authors/')
for path in filenames:
    os.remove('/home/cwp/EMC/data/authors/'+path)

filenames = os.listdir('/home/cwp/EMC/data/data/')
for path in filenames:
    shutil.rmtree('/home/cwp/EMC/data/data/'+path)
