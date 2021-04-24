
#imports:
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import pandas
import pickle
#####



def linprebkg(xx,xas,x1,x2):
    '''
    xx = global energy scale
    xas = xas
    use from x1 to x2 for cutting background region'''
    return np.poly1d(np.polyfit(xx[list(np.around(xx,2)).index(x1):list(np.around(xx,2)).index(x2)], xas[list(np.around(xx,2)).index(x1):list(np.around(xx,2)).index(x2)],1))(xx)



def norm01(xx,xas,energy1,a1): #a1 nimmt list object norm to one at energy1
    faktor = 1/xas[list(np.around(xx,2)).index(energy1)]
    return a1*faktor



def smooth(y, box_pts):
    '''
    smoothing function
    y =  function to smooth
    box_pts = points to average 
    '''
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

#step function for branching ratio
def step(a,tp,energy,slope=None):
    '''
    takes:
    a      = step hight
    tp     = turning point of step function
    energy = numpy array
    #optional:
    slope = slope factor
    
    returns:
    step function as a np.array 
    '''
    if slope == None:
        return np.array(a*(1/(1+np.exp(tp - energy))))
    
    if type(slope) == float:
        return np.array(a*(1/(1+np.exp(slope*(tp - energy)))))
    else:
        raise ValueError('slope factor has to be float, e.g. 2.0, 2.3, etc.')



    
###index function
def idx(a1, b1):
    '''find index of value a1 in list b1'''
    return list(np.around(b1,2)).index(a1)
