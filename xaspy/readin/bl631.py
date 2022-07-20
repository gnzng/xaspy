# module imports:
import pandas as pd 
import numpy as np
import os
#####

## readin functions
## for beamline 6.3.1 at ALS, Berkeley



### TODO use spectra/files local + option on beam time computer -> switch in  


#import Trajectory Motor Scans by scan number
class SigScan:
    def __init__(self,string):
        datapath = "Y:\\BCS Setup Data\\"
        for n in os.listdir(datapath):
            try:
                files   = datapath + "{}".format(n) + "\\SigScan" + string + ".txt"
                f = open(files)
                ct = 0
                for n in range(50):
                    line = str(f.readline())
                    if line.startswith("Time of Day"):
                        break
                    ct += 1
                t1      = pd.read_csv(files, skiprows=ct-1,sep='\t',engine='python')
                self.df = t1
                f.close()
            except:
                pass


#import Single Motor Scans by scan number
class TrajScan:
    def __init__(self,string):
        datapath = "Y:\\BCS Setup Data\\"
        for n in os.listdir(datapath):
            try:
                files   = datapath + "{}".format(n) + "\\TrajScan" + string + ".txt"
                f = open(files)
                ct = 0
                for n in range(50):
                    line = str(f.readline())
                    if line.startswith("Time of Day"):
                        break
                    ct += 1
                t1      = pd.read_csv(files, skiprows=ct-1,sep='\t',engine='python')
                self.df = t1
                f.close()
            except:
                pass








## checks if imported pd.DataFrame object is a Hysteresis loop measurement
## 
def ishyst(df,check = False):
    len_magfield = (len(np.unique(np.around(df['Magnet Field'],3))))
    len_energy   = (len(np.unique(np.around(df['Energy'],1))))
    
    if check == True:
        print('magnetic field points: {}, energy points: {}'.format(len_magfield,len_energy))
    try: 
        if len_magfield > len_energy:
            return True
        elif len_magfield < len_energy:
            return False
    except: 
        raise ValueError('unknown TrajScan')



