#Modifying and combining transcriptions
"""
data = open('data.txt','w+')
fm = open("male.txt", "r")
rm = fm.readlines()
ff = open("female.txt", "r")
rf = ff.readlines()

for line in rm:
    fline = 'm'+line.split()[1]+'-=-'+(' '.join(line.split()[2:len(line)-1])[1:-3])
    data.write(fline+'\n')

for line in rf:
    fline = 'f'+line.split()[1]+'-=-'+(' '.join(line.split()[2:len(line)-1])[1:-3])
    data.write(fline+'\n')

data.close()
"""
"""
#Rename audio files
import os  
def main(fname, apc): 
    root = os.path.join(os.path.dirname(__file__), fname)
    for count, filename in enumerate(os.listdir(root)): 
        print(filename)
        src = os.path.join(root,filename)
        dst = os.path.join(root,apc+filename)
        os.rename(src, dst) 

if __name__ == '__main__': 
    fname1 = 'male'
    apc1 = 'm'
    fname2 = 'female'
    apc2 = 'f'
    main(fname1, apc1)
    main(fname2, apc2)
"""
"""
import os
root = os.path.join(os.path.dirname(__file__), 'data')
transcript_path = os.path.join(root, 'data.txt')
fr = (open(transcript_path, 'r')).readlines()
for line in fr:
    print(fr)
"""
"""
import csv 
f = open('RecordsMT500.txt', 'r')
lines = f.readlines()
flst = []
for line in lines:
    fname, phrase = line.split('-=-')
    flst.append([fname+'.wav', phrase])

filename = "data500.csv"
fields = ['file_name', 'phrase'] 
# writing to csv file  
with open(filename, 'w', newline='') as csvfile:    
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)    
    csvwriter.writerows(flst)
"""

"""
import os  
def main(fname): 
    root = os.path.join(os.path.dirname(__file__), fname)
    for count, filename in enumerate(os.listdir(root)):
        filepath =  os.path.join(root, filename)
        if('.wav.wav' not in filename):
            os.remove(filepath)
        else:
            src = os.path.join(root,filename)
            dst = os.path.join(root,filename[:-4])
            os.rename(src, dst) 

if __name__ == '__main__': 
    fname = 'mtrec'
    main(fname)
"""

"""
#for mt
import csv 
f = open('RecordsMT.txt', 'r')
#f1 = open('RecordsMT1.txt', 'w+')
lines = f.readlines()
flst = []
c = 1
for line in lines:
    if(c>740):
        break
    #f1.write(str(c)+'.wav-=-'+line)
    fname, phrase = str(c)+'.wav', line
    flst.append([fname, phrase])
    c +=1
print(c)


filename = "datamt.csv"
fields = ['file_name', 'phrase'] 
# writing to csv file  
with open(filename, 'w', newline='') as csvfile:    
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)    
    csvwriter.writerows(flst)
"""
"""
#coverting mp3 to wavss
import os  
def main(fname): 
    root = os.path.join(os.path.dirname(__file__), fname)
    for count, filename in enumerate(os.listdir(root)):
        filepath =  os.path.join(root, filename)
        if('.mp3.wav' not in filename):
            os.remove(filepath)
        else:
            src = os.path.join(root,filename)
            dst = os.path.join(root,filename[:-8]+filename[-4:])
            os.rename(src, dst) 

if __name__ == '__main__': 
    fname = 'datapolly'
    main(fname)
"""

import csv 
f = open('RecordsMT500.txt', 'r')
lines = f.readlines()
flst = []
c = 1
for line in lines:
    fname = str(c)+'.mp3'
    phrase = line
    flst.append([fname, phrase])
    c += 1

filename = "data500.csv"
fields = ['file_name', 'phrase'] 
# writing to csv file  
with open(filename, 'w', newline='') as csvfile:    
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)    
    csvwriter.writerows(flst)