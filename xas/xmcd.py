#imports:
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import pandas
import pickle
#####


###################
####XMCD######
def XMCD(pdat,mdat,ene,det,mon,log):
    '''
    XMCD function:
    pdat = positive lists
    mdat = negative list 
    ene = energy column
    det = detector column
    mon = monitor column
    '''
    t2pdat = pdat
    t2mdat = mdat
    pmin=[]
    pmax=[]
    for n in range(len(t2pdat)):
        pmin.append(np.min(t2pdat[n][ene]))
        pmax.append(np.max(t2pdat[n][ene]))
    mmin=[]
    mmax=[]
    for n in range(len(t2mdat)):
        mmin.append(np.min(t2mdat[n][ene]))
        mmax.append(np.max(t2mdat[n][ene]))
    xmin = np.max(pmin+mmin)
    xmax = np.min(pmax+mmax)
    xx = np.linspace(xmin+0.01,xmax-0.01,10000) # energy interpolation range
    t3pdat=[] # alles interpolierte
    for n in range(len(t2pdat)):
        v1  = np.array(t2pdat[n][ene])
        if mon != False:
            v21 = np.array(t2pdat[n][det])
            v22 = np.array(t2pdat[n][mon])
            if log == True:
                v2  = np.log(v22/v21)
            else:
                v2  = v21/v22
        if mon ==False:
            v2 = np.array(t2pdat[n][det])
        t3pdat.append(interpolate.interp1d(v1,v2)(xx)) 
    t3mdat=[]
    for n in range(len(t2mdat)):
        v1  = np.array(t2mdat[n][ene])
        if mon != False:
            v21 = np.array(t2mdat[n][det])
            v22 = np.array(t2mdat[n][mon])
            v2  = v21/v22
        if mon == False:
            v2 = np.array(t2mdat[n][det])
        t3mdat.append(interpolate.interp1d(v1,v2)(xx))
    t4pdat=[] # all from +hel merged
    for k in range(0,len(xx)):
        t4pdat.append(np.sum([t3pdat[s][k] for s in range(len(t3pdat))])/int(len(t3pdat)))
    t4mdat=[] # all from -hel merged
    for k in range(0,len(xx)):
        t4mdat.append(np.sum([t3mdat[s][k] for s in range(len(t3mdat))])/int(len(t3mdat)))
    t5pdat= np.array(t4pdat)
    t5mdat= np.array(t4mdat)
    pdm = t5pdat/t5mdat    #plus signal divided by minus signal
    #correlation of plus and minus signal
    corrpre = np.poly1d(np.polyfit(xx[:int(len(xx)*0.1)],pdm[:int(len(xx)*0.1 )],1))
    corrpost = np.poly1d(np.polyfit(xx[int(len(xx)-len(xx)*0.1):],pdm[int(len(xx)-len(xx)*0.1):],1))
    x1 = xx[2]
    x2 = xx[-2]
    cfy1 = corrpre(x1) #corr intens. at 
    cfy2 = corrpost(x2)
    #correlated signal with pmerged
    t5mdat = (t5mdat*(cfy1-x1*(cfy1-cfy2)/(x1-x2)+xx*(cfy1-cfy2)/(x1-x2)))
    #####
    xas = (t5pdat+t5mdat)/2 
    #Subtracting backgrounds now:
    linbkg = np.poly1d(np.polyfit(xx[:int(len(xx)*0.1)],xas[:int(len(xx)*0.1 )],1))(xx)
    xas    = xas    - linbkg
    pxas   = t5pdat - linbkg
    mxas   = t5mdat - linbkg
    #### now normalized to XAS maximum
    xmcd = (t5pdat-t5mdat)/np.max(xas)
    return xx, pxas, mxas, xas, xmcd
### 




########### HSYT functions:
###########
####HYST###
def HYST(df,fld, ene, det, mon, Epre, Eedg):
    '''
    HYST : edge/pre_edge
    VEKMAG compatible
    df     = takes pandas data frame
    fld    = column name of field values
    ene    = column name of energy values
    det    = column name of detector values
    mon    = column name of monitor
    Epre    = energy of pre edge point
    Eedg    = energy of edge point
    '''
    df = df
    hyst1  = []
    field1 = []
    for n in np.arange(-6.8,6.8,0.1):
        n   = np.around(n,1)
        t1  = df[np.around(df[ene],1) == Eedg]
        t1  = t1[np.around(t1[fld],1) == n]
        t11 = np.mean(t1[det]/t1[mon])
        t1  = df[np.around(df[ene],1) == Epre]
        t1  = t1[np.around(t1[fld],1) == n]
        t22 = np.mean(t1[det]/t1[mon])
        hyst1.append(t11/t22)
        field1.append(n)
    ############
    return field1,hyst1


###########
####HYST###
def HYST2(df,fld, ene, det, mon, Epre, Eedg):
    '''
    HYST2 : (edge - pre_edge)/pre_edge
    VEKMAG compatible
    df     = takes pandas data frame
    fld    = column name of field values
    ene    = column name of energy values
    det    = column name of detector values
    mon    = column name of monitor
    Epre    = energy of pre edge point
    Eedg    = energy of edge point
    '''
    df = df
    hyst1  = []
    field1 = []
    for n in np.arange(-6.8,6.8,0.1):
        n   = np.around(n,1)
        t1  = df[np.around(df[ene],1) == Eedg]
        t1  = t1[np.around(t1[fld],1) == n]
        t11 = np.mean(t1[det]/t1[mon])
        t1  = df[np.around(df[ene],1) == Epre]
        t1  = t1[np.around(t1[fld],1) == n]
        t22 = np.mean(t1[det]/t1[mon])
        hyst1.append((t11 - t22)/t22)
        field1.append(n)
    ############
    return field1,hyst1

def HYST3en(df,fld, ene, det, mon, Epre, Eedg1, Eedg2):
    '''
    HYST : edge/pre_edge
    VEKMAG compatible
    df     = takes pandas data frame
    fld    = column name of field values
    ene    = column name of energy values
    det    = column name of detector values
    mon    = column name of monitor
    Epre    = energy of pre edge point
    Eedg1   = energy of edge point 1
    Eedg2   = energy of edge point 2 
    '''
    df = df
    hyst1  = []
    hyst2  = []
    field1 = []
    for n in np.arange(-6.8,6.8,0.1):
        n   = np.around(n,1)
        t1  = df[np.around(df[ene],1) == Eedg1]
        t1  = t1[np.around(t1[fld],1) == n]
        t11 = np.mean(t1[det]/t1[mon])
        t2  = df[np.around(df[ene],1) == Eedg2]
        t2  = t2[np.around(t2[fld],1) == n]
        t12 = np.mean(t2[det]/t2[mon])
        t1  = df[np.around(df[ene],1) == Epre]
        t1  = t1[np.around(t1[fld],1) == n]
        t22 = np.mean(t1[det]/t1[mon])
        hyst1.append(t11/t22)
        hyst2.append(t12/t22)
        field1.append(n)
    ############
    return field1,hyst1,hyst2




##########sumrules functions##
def sumrules(xx,xas00, xmcd, px,nh):
    '''
    xx = global energy scale
    xas00 = xas - stepfunction
    xmcd = xmcd
    px = point in energy for p value
    nh = number of electron holes'''
    r=np.max(np.cumsum(xas00))
    q=np.max(np.cumsum(xmcd))
    p=np.cumsum(xmcd)[list(np.around(xx,2)).index(px)]
#print(np.max(np.cumsum(np.linspace(0,1,steps)))/steps)
    lz=nh*2*q/(3*r)
    sz=nh*(3*p-2*q)/(2*r)
    return sz,lz

def LDS(xx, xmcd, px):
    '''
    xx = global energy scale
    xmcd = xmcd
    px = point in energy for p value'''
    q=np.absolute(np.cumsum(xmcd))[-1]
    p=np.absolute(np.cumsum(xmcd)[list(np.around(xx,2)).index(px)])
    #print(q,p)
    lds=(4/3)*q/(3*p-2*q)
    return lds