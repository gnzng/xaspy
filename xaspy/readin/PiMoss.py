#import:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class PiMoss:
    '''
    ---under construction---
    class to create Mossbauer measurement class from pi software package: 
    https://www.uni-due.de/~hm236ap/hoersten/home.html
    takes path to .dat file. do not use .dat extension in name
    '''
    
    def __init__(self,path):
        def impspec(a):
            '''
            function to import the plot data as a pandas DataFrame
            '''
            return pd.read_csv(a, sep='\t',engine='python',skiprows=1,
                            na_values='-',header=None)        
        try:
            self.df   = impspec(path + '.dat')
            self.v    = np.array(self.df[0])  #returns velocity as numpy array
            self.m    = np.array(self.df[1])  #returns measurement as numpy array
            self.err  = np.array(self.df[2])  #returns velocity as numpy array
            self.lsfit= []                    #list of np.arrays for the fit models
            for n in range(len(self.df.columns)-3):
                self.lsfit.append(np.array(self.df[n+3]))
        except:
            raise IOError('File not found. Make sure it is a .dat-file')

    def plot(self,kind='all'):
        '''
        fast plotting functions functions:
        input string: 
        'all'        errorbar measurement + all fit models
        'err'        errorbar measurement
        'noerr'      measurement no errorbar
        'allnoerr'   all fit models + measurement no errorbar
        '''
    
        plotlist = ['all','err','noerr','allnoerr']
        
        if kind not in plotlist:
            raise ValueError('Plot option not in list. Please choose from {}'.format(plotlist))
        if kind == 'all':
            plt.errorbar(self.v,self.m,self.err)
            for n in self.lsfit:
                plt.plot(self.v,n)
        if kind == 'err':
            plt.errorbar(self.v,self.m,self.err)
        if kind == 'noerr':
            plt.plot(self.v,self.m)
        if kind == 'allnoerr':
            plt.plot(self.v,self.m)
            for n in self.lsfit:
                plt.plot(self.v,n)
        plt.xlabel('velocity [mm/s]'),plt.ylabel('absorption [arb. units]')
 
