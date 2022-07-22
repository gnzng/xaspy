# module imports:
import pandas as pd 
import numpy as np
import os
import pickle
#####

## readin functions
## for beamline 6.3.1 at ALS, Berkeley

def count_lines(file):
    header = []
    f = open(file)
    ct = 0
    for n in range(50):
        line = str(f.readline())
        if line.startswith("Time of Day"):
            break
        ct += 1
        header.append(line)
    t1      = pd.read_csv(file, skiprows=ct-1,sep='\t',engine='python')
    f.close()
    return t1,header

def SS_indexing():
    datapath = "Y:\\BCS Setup Data\\"
    SigScans_indexed = {}
    for root, dirs, files in os.walk(datapath):
        for name in files:
            if name.startswith("SigScan"):
                strng = name.replace(".txt","")
                strng = strng.replace("SigScan","")
                SigScans_indexed.update({strng:  os.path.join(root,name)})
    return SigScans_indexed 
                                
def TS_indexing():
    datapath = "Y:\\BCS Setup Data\\"
    TrajScans_indexed = {}
    for root, dirs, files in os.walk(datapath):
        for name in files:
            if name.startswith("TrajScan"):
                strng = name.replace(".txt","")
                strng = strng.replace("TrajScan","")
                TrajScans_indexed.update({strng:  os.path.join(root,name)})
    return TrajScans_indexed 


class SigScan:
    ### "bl_comp" working at beam line computer with access to all scans
    path = "bl_comp"
    # import using the beam line computer
    
    def __init__(self,string):    
        if self.path == "bl_comp":
            try:
                indexed = pickle.load(open("_SS_index.p","rb"))
                file_to_open   = indexed[string]
        
            except:
                raise ValueError("could not find Single Scan " + string + ". Typo? Indexing server running?")
            try:
                ct_lines = count_lines(file_to_open)
                self.df = ct_lines[0]
                self.header = ct_lines[1]
            except:
                raise ValueError("error while reading or finding file")
            try: 
                self.scantype = guess_scan(self.df)
            except:
                self.scantype = "could not indentify scan type"

        ###
        # import on local machine
        if self.path != "bl_comp":
            if os.path.isdir(self.path) != True:
                raise ValueError("could not find local path")
                
            for root, dirs, files in os.walk(self.path):
                for name in files:
                    if name.startswith("SigScan"):
                        if string in name:
                            ct_lines = count_lines(os.path.join(root,name))
                            self.df = ct_lines[0]
                            self.header = ct_lines[1]
                            try: 
                                self.scantype = guess_scan(self.df)
                            except:
                                self.scantype = "could not indentify scan type"

                                

class TrajScan:
    ### "bl_comp" working at beam line computer with access to all scans
    path = "bl_comp"
    # import using the beam line computer
    
    def __init__(self,string):    
        if self.path == "bl_comp":
            try:
                indexed = pickle.load(open("_TS_index.p","rb"))
                file_to_open   = indexed[string]
        
            except:
                raise ValueError("could not find Trajectory Scan " + string + ". Typo? Indexing server running?")
            try:
                ct_lines = count_lines(file_to_open)
                self.df = ct_lines[0]
                self.header = ct_lines[1]
            except:
                raise ValueError("error while reading or finding file")
            try: 
                self.scantype = guess_scan(self.df)
            except:
                self.scantype = "could not indentify scan type"

        ###
        # import on local machine
        if self.path != "bl_comp":
            if os.path.isdir(self.path) != True:
                raise ValueError("could not find local path")
                
            for root, dirs, files in os.walk(self.path):
                for name in files:
                    if name.startswith("TrajScan"):
                        if string in name:
                            ct_lines = count_lines(os.path.join(root,name))
                            self.df = ct_lines[0]
                            self.header = ct_lines[1]
                            try: 
                                self.scantype = guess_scan(self.df)
                            except:
                                self.scantype = "could not indentify scan type"



# returns type of scan
# this can be written more elegant
def guess_scan(df,check = False):
    
    """
    guesses scan from pandas input base on number of unique scan values
    
    returns None if no column was written
    
    """
    
    len_magfield = (len(np.unique(np.around(df['Magnet Field'],3))))
    try:
        len_energy   = (len(np.unique(np.around(df['Energy'],1))))
    except:
        len_energy = 1
    len_x        = (len(np.unique(np.around(df['X'],2))))
    len_y        = (len(np.unique(np.around(df['Y'],2))))
    len_z        = (len(np.unique(np.around(df['Z'],2))))
    len_theta    = (len(np.unique(np.around(df['Theta'],2))))
    
    if check == True:
        print('magnetic field points: {}'.format(len_magfield))
        print('energy points: {}'.format(len_energy))
        print('xmotor points: {}'.format(len_x))
        print('ymotor points: {}'.format(len_y))
        print('zmotor points: {}'.format(len_z))
        print('theta motor points: {}'.format(len_theta))
    
    
    parameter_list = [len_magfield,len_energy,len_x,len_y,len_z,len_theta]
    
    if 0 in parameter_list:
        return None
    
    most_changed = parameter_list.index(max(parameter_list))
    
    answers = ["Magnetic Field","Energy","X","Y","Z","Theta"]
    
    return answers[most_changed]



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
        raise ValueError('unknown Scan')
