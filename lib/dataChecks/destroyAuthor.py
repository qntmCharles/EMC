authors = {}

#Define directories
cwd = '/home/cwp/EMC/data/authors/'
filenames = os.listdir(cwd)
#print(filenames)

#Load files
for filename in filenames:
    with open(cwd+filename,'rb') as input:
        #print(filename[:-4])
        authors[filename[:-4]] = pickle.load(input)

option = str(raw_input('Enter author to delete: '))
for date, entry in authors[option].data.items():
    os.remove(entry.dataSrc)

with open('/home/cwp/EMC/lib/logs/authors.txt', 'r') as f:
    authorsList = f.readlines()
    f.close()

open('/home/cwp/EMC/lib/logs/authors.txt', 'w').close()

authorsList.remove(option+'\n')

with open('/home/cwp/EMC/lib/logs/authors.txt', 'w') as f:
    for line in authorsList:
        f.write(line)
    f.close()

os.remove('/home/cwp/EMC/data/authors/'+option+'.pkl')

authors[option] = None
