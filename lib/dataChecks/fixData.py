import os, csv

cwd = '/home/cwp/EMC/data/data/'

"""
# Remove encryption things
for path in os.listdir(cwd):
    for path2 in os.listdir(cwd+path):
        filenames = os.listdir(os.path.join(cwd,path,path2))
        for filename in filenames:
            filepath = os.path.join(cwd,path,path2,filename)
            with open(filepath, 'r') as f:
                readFile = list(csv.reader(f))
                flag = False
                for row in readFile[1:]:
                    try:
                        int(row[0])
                    except:
                        print(filepath)
                        flag = True
                        print(row)
                        readFile.remove(row)
            if flag:
                open(filepath, 'w').close()
                with open(filepath, 'w') as f:
                    filewriter = csv.writer(f)
                    for row in readFile:
                        filewriter.writerow(row)
"""

# Remove '\r's
for path in os.listdir(cwd):
    for path2 in os.listdir(cwd+path):
        filenames = os.listdir(os.path.join(cwd,path,path2))
        for filename in filenames:
            filepath = os.path.join(cwd,path,path2,filename)
            with open(filepath, 'r') as f:
                readFile = list(csv.reader(f))
                flag = False
                for row in readFile[1:]:
                    for i in range(1,len(row)-1):
                        try:
                            int(row[i])
                        except:
                            print(i, len(row), row)
                            row[i] = int(float(row[i]))
                            flag = True
            if flag:
                open(filepath, 'w').close()
                with open(filepath, 'w') as f:
                    filewriter = csv.writer(f)
                    for row in readFile:
                        filewriter.writerow(row)
