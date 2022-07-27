# module imports:
import pandas as pd 
import numpy as np
import os
import pickle
import warnings
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
    
    def __init__(self,string:str):    
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
    
    def __init__(self,string:str):    
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
def guess_scan(df:pd.DataFrame,check:bool = False) -> str:
    
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



####### 
# Make scanfiles 



def print_mesh(mesh_fields,i=0,  line='', outfile=None):
	if i<len(mesh_fields):
		for v in mesh_fields[i]["Values"]:
			if v == "file":
				outfile.write("file")
				outfile.write("\r\n")
			else:
				# Use join next time
				if i == 0: 
					tab = ""
				else:
					tab = "\t"
				print_mesh(mesh_fields, i+1, line + tab +str(v),outfile)
	else:
		outfile.write(line)
		outfile.write("\r\n")

        
def XMCD_scanpair(field:float, energy:list, step=0.1, velocity=1.0, pairs:int=4) -> list:
    '''
    
    Produces a Trajectory Scan File for Beamlines 6.3.1 and 4.0.2 at the ALS
    
    Arguments
    ---------
        
        field    = field for XMCD in Tesla
        energy   = takes energy range as list, e.g. [765,815]
        step     = stepsize for flying Energy scans, default 0.1
        velocity = velocity for flying Energy scans, default 1.0
        pairs    = number of XMCD pairs, has to be an integer, default 4
    
    Returns
    --------

    list of strings, input for mesh_fields

    Notes
    --------

    - new file will be created after two opposite fields
    - fields will be like + - - + if more than 1 pair
    
    '''

    if abs(field) > 1.9:
        raise Warning('Most probably not possible for this setup, check the magnetic field value again.')

    if not isinstance(pairs,int):
        pairs = int(pairs)
        raise Warning('Number of pairs must be an integer value, e.g. 4., continued with {} pairs'.format(pairs))

    if len(energy) != 2:
        raise ValueError('Number of energy range has to be 2, takes energy range as list, e.g. [765,815]')

    if energy[0] > energy[1]:
        warnings.warn('Scan is running backwards in energy.')
    elif energy[0] == energy[1]:
        warnings.warn('Same point for start and stop energy.')

    sl = list()
    for i in range(pairs):
        sl.append("{}{}\tflying({},{},{},{})".format(["+","-"][i%2], field, energy[0], energy[1], step, velocity))
        sl.append("{}{}\tflying({},{},{},{})".format(["-","+"][i%2], field, energy[0], energy[1], step, velocity))
        sl.append("file")
    return(sl)
 
def HYST_scanpair():
    '''
    DUMMY for HYST scans
    '''
    pass
        

def make_scanfile(mesh_fields, outfilename):
    with open(outfilename, "w", newline='') as outfile:
        if "flying" in str(mesh_fields):
            if "Energy" in str(mesh_fields):
                # Energy is set explicitly, so assume Hysteresis with flying field
                # dummy values to introduce the right flying scan
                outfile.write("flying Magnet Field(0.41, -0.41, 0.01,0.1)\t\r\n",)
            else:
                # Energy is not set explicitly, so assume that is what we are flying for XAS or XMCD
                # dummy values to introduce the right flying scan
                outfile.write("flying Energy(700, 800, 0.1,1)\r\n",)            
        for h in mesh_fields:
            outfile.write(h["Header"])
        outfile.write("\r\n")
        print_mesh(mesh_fields, outfile=outfile)
