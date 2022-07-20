#imports:
import pandas as pd 
#####

####readin functions for different theory/simulation programs:

def multix(a):
    '''
    import multiX output file 
    returns panda file with energy, imaginary part that simulates the xas, and the real part
    '''
    return pd.read(a,header=['energy','img','r'],delim_whitespace=True)

def crispy(a):
    return pd.read_csv(a,delim_whitespace=True,comment='#', header=3)

