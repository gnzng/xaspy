#imports:
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
#####



        
####XMCD######
def XMCD(pdat,mdat,ene,det,mon,
         log=False,xmin=None,xmax=None,xsize=10000, norm='edge_jump',eshift=0):
    '''
    xray magnetic circular dichroism function

    Arguments
    ---------
        
        pdat    = positive list of pandas objects
        mdat    = negative list of pandas objects
        ene     = energy column name of pandas object
        det     = detector column name of pandas object
        mon     = monitor column -> if no monitor wanted, put 'False'
        log     = boolean, use logarithm for transmission experiments
        xmin    = adjust minimum energy 
        xmax    = adjust maximum energy
        xsize   = number of points for interpolation default 10000 
                  ! be careful: low point density can lead to ValueErrors due to 
                  ! rounding numbers
        norm    = choose normalization from ['white_line', 'edge_jump', 'pre_edge','None']
        eshift  = shift in energy, added to pdat values, default 0

    Returns
    --------

    energy, plus_xas, minus_xas, averaged_xas, xmcd

    Notes
    --------

    no notes 
    '''
    from scipy import interpolate
    t2pdat = pdat
    t2mdat = mdat
    #photon energies: 
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
    
    #used energy range:
    if xmin == None:
        xmin = np.max(pmin+mmin)
    if xmax == None:
        xmax = np.min(pmax+mmax)
    
    # energy interpolation range:
    xx = np.linspace(xmin+0.1,xmax-0.1,xsize) 
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
        if mon == False:
            v2 = np.array(t2pdat[n][det])
        try:
            t3pdat.append(interpolate.interp1d(v1,v2)(xx+float(eshift)/1000)) 
        except:
            raise ValueError('eshift to large for interpolation range? max Eshift ca. 100meV')
    t3mdat=[]
    for n in range(len(t2mdat)):
        v1  = np.array(t2mdat[n][ene])
        if mon != False:
            v21 = np.array(t2mdat[n][det])
            v22 = np.array(t2mdat[n][mon])
            if log == True:
                v2  = np.log(v22/v21)
            else:
                v2  = v21/v22
        if mon == False:
            v2 = np.array(t2mdat[n][det])
        t3mdat.append(interpolate.interp1d(v1,v2)(xx))
        
    #merging same helicities: 
    t4pdat=[] # all from +hel merged
    for k in range(0,len(xx)):
        t4pdat.append(np.sum([t3pdat[s][k] for s in range(len(t3pdat))])/int(len(t3pdat)))
    t4mdat=[] # all from -hel merged
    for k in range(0,len(xx)):
        t4mdat.append(np.sum([t3mdat[s][k] for s in range(len(t3mdat))])/int(len(t3mdat)))
    t5pdat= np.array(t4pdat)
    t5mdat= np.array(t4mdat)
    pdm = t5pdat/t5mdat    #plus signal divided by minus signal
    
    
    #correlation of plus and minus signal via two linear functions: 
    corrpre = np.poly1d(np.polyfit(xx[:int(len(xx)*0.1)],pdm[:int(len(xx)*0.1 )],1))
    corrpost = np.poly1d(np.polyfit(xx[int(len(xx)-len(xx)*0.1):],pdm[int(len(xx)-len(xx)*0.1):],1))
    x1 = xx[2]
    x2 = xx[-2]
    cfy1 = corrpre(x1) #corr intens. at 
    cfy2 = corrpost(x2)
    
    #correlated signal with pmerged: 
    t5mdat = (t5mdat*(cfy1-x1*(cfy1-cfy2)/(x1-x2)+xx*(cfy1-cfy2)/(x1-x2)))
    #####
    xas = (t5pdat+t5mdat)/2
    
    #Subtracting backgrounds now:
    linbkg = np.poly1d(np.polyfit(xx[:int(len(xx)*0.1)],xas[:int(len(xx)*0.1 )],1))(xx)
    xas    = xas    - linbkg
    pxas   = t5pdat - linbkg
    mxas   = t5mdat - linbkg
    
    ### normalization:

    norm_opt = ['white_line', 'edge_jump', 'pre_edge','None',None]

    #choose factor: 
    
    try:
        if norm == 'white_line':
             norm_factor = float(np.max(xas))
        
        elif norm == 'edge_jump':
            last_values  = int(xsize*0.05)
            norm_factor  = np.mean(xas[:-last_values])
        
        elif norm == 'pre_edge':
            last_values  = int(xsize*0.02)
            norm_factor  = np.mean(xas[last_values:])
        
        elif norm in ['None',None]:
            norm_factor = 1.0

    except:
        raise ValueError('normalization not clear, use {}'.format(norm_opt))
    
    xas = np.array(xas)/norm_factor
    pxas = np.array(pxas)/norm_factor
    mxas = np.array(mxas)/norm_factor
    xmcd = np.array(pxas-mxas)    
    
    return xx, pxas, mxas, xas, xmcd
### 


########### HSYT functions:

# mHYST
#
### new in 0.1.10, developed for many (mHYST) loops in one file:
### added log option in 0.1.13

class mHYST:
    '''
    Arguments
    ---------
        
        df      = pandas dataframe of multiple Hyst loops
        ene     = energy column name of pandas object
        det     = detector column name of pandas object
        mon     = monitor column -> if no monitor wanted, put 'False'
        ene_cut = energy cutoff, choose somewhere between both 
                  measured energies
        ratio   = either divide higher/lower or lower/higher energy
        log     = neg. logarithm for tranmission experiments, default False
    
    Returns
    --------
    Nothing, but contains multiple functions:
        - average_loops(), average specific loops
        - plot_seperated(), plots all loops seperated
        
    Notes
    --------
    no notes 
    
    '''
    
    def __init__(self, df, ene, det, mon, ene_cut, ratio='higher/lower',log=False):
        import pandas as pd
        if not isinstance(df, pd.DataFrame):
            raise ValueError('df is not a pd.DataFrame')
        t1      = df
        self.df = df
        
        try: 
            #t2 at higher energy -> usually l2 edge, l3 at lower energies:
            # normalizing signal to clock
            t2, t3 = t1[t1[ene] >= ene_cut] , t1[t1[ene] <= ene_cut]
            t2 = t2.reset_index()
            t3 = t3.reset_index()
        except:
            raise ValueError('energy cut off failed')
        
        try:
            if mon == False: 
                t2['normlzd'] = t2[det]
                t3['normlzd'] = t3[det]
            elif log == True:
                t2['normlzd'] = -np.log(t2[det]/t2[mon])
                t3['normlzd'] = -np.log(t3[det]/t3[mon])
            else:
                t2['normlzd'] = t2[det]/t2[mon]
                t3['normlzd'] = t3[det]/t3[mon]
        except:
            raise ValueError('normalization failed')
        
        # now use t2 to continue algortithm
        try:
            if ratio == 'higher/lower':
                t2['divided'] = t2['normlzd']/t3['normlzd']
            elif ratio == 'lower/higher':
                t2['divided'] = t3['normlzd']/t2['normlzd']
        except:
            raise ValueError('please choose a valid ratio')
       
        try:
            len_t2  = len(t2)
            
            self.t2 = t2
            
            self.slope_ct = self.slope_count(t2).astype(int)
            
            self.len_per_loop = (len_t2/self.slope_ct).astype(int)
            
        except:
            raise ValueError('could not build Hysteresis loop. different number of scans ? ')
    
    def slope_count(self,df):
        '''
        function returns the number of slopes in HYST loops
        '''
        df = df
        magfield = np.array(df['Magnet Field'])
        mag_sign = np.sign(magfield)
        signchange = ((np.roll(mag_sign, 1) - mag_sign) != 0).astype(int)
        return (np.sum(signchange)/4).astype(int)
    
    def plot_seperated(self):
        for n in range(self.slope_ct):
            plt.figure()
            plt.title('loop {}'.format(n))
            plt.plot(self.t2['Magnet Field'][n*self.len_per_loop:(n+1)*self.len_per_loop], 
                     self.t2['divided'][n*self.len_per_loop:(n+1)*self.len_per_loop])
            plt.show()
    def average_loops(self,av_list,return_data=False):
        
        ''' 
        takes number of loops, check before with plot_seperated()
        set return_data to True to get data as tuple(field, signal)
        non plot mode otherwise returns plot of average loops
        '''
        self.av_list = av_list
        toaverage = []
        for n in av_list:
            toaverage.append(self.t2['divided'][n*self.len_per_loop:(n+1)*self.len_per_loop])
        averaged = np.mean(toaverage,axis=0)
        self.std      = np.std(toaverage,axis=0) 
        field = self.t2['Magnet Field'][:self.len_per_loop]
        
        if return_data == False:
            plt.figure()
            plt.title(f'average loops {*av_list,}')
            plt.plot(field,averaged)
            plt.show()
        
        elif return_data == True:
            return (np.array(field),np.array(averaged))
        
        else:
            raise ValueError('return_data mode not clear. use False or True')




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
