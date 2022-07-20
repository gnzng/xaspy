# SPEC file splitter
# 
# author gnzng
# 
# small python program to split a larger SPEC file into individual files
#  
# folder for individual files has to be named: scan_SPECFILENAME and must be in 
# the same directory 
#
# splitted files are .dat files  
# contain first line scan number and command
# second line name of detectors/header


import re 

file = input('Enter Filename:')

def split(file):
    clean=[]
    clst=[]
    with open(file,'r')as f:
        regexp = re.compile(r'^-?\d+\.?\d*')
        for line in f:
            if '#C' in line:
                clst.append(line.replace('\n',''))
            if '#S' in line:
                clean.append(line.replace('\n',''))
                nr = line.split(' ')[1]
            if '#L' in line:
                clean.append(line[3:].replace('\n',''))
            if regexp.search(line):
                clean.append(line.replace('\n',''))
            if not line.strip():
                clean.append('splitsignal')
    for n in range(1,10000):
        if clean[0] == 'splitsignal':
            clean.pop(0)
        else:
            break
    nr=0
    for i in clean:
        if '#S' in i:
            nr = i.split(' ')[1]
            f= open('scans_'+file+'/'+file+'_{0:03}.dat'.format(int(nr)),'w+')
        f= open('scans_'+file+'/'+file+'_{0:03}.dat'.format(int(nr)),'a')
        if i != 'splitsignal':
            f.write(i+'\n')
        if n != 0:
            if i =='splitsignal':
                f.close()

split(file)

print('excuted')