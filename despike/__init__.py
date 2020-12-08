
import pickle
###########################
###########################
####DESPIKE Functions######
###########################
###########################
def showspikes(file):
    '''
    shows dictionary of spike values saved in file
    file = path to spike file, without -.spike-
    '''
    with open(file+'.spike', 'rb') as f:
        b = pickle.load(f)
    return print(b)

def removespikes(a,file):
    '''
    removes the spike values for scan a
    a = scan number, where all scans are removed
    file = path to spike file, without -.spike-
    '''
    with open(file+'.spike', 'rb') as f:
        b = pickle.load(f)
    try:
        del(b[a])
        with open(file+'.spike', 'wb') as f:   
            pickle.dump(b,f,protocol=pickle.HIGHEST_PROTOCOL)
    except:
        print('{} not in {}'.format(a,file))

def addspike(a,c,file):
    '''
    adds one  spike value c for scan a
    a = scan number, where all scans are removed
    file = path to spike file, without -.spike-
    '''
    try:
        with open(file+'.spike', 'rb') as f:
            b = pickle.load(f)
    except:
        with open(file+'.spike', 'wb') as f:
            pickle.dump({},f,protocol=pickle.HIGHEST_PROTOCOL)
        with open(file+'.spike', 'rb') as f:
            b = pickle.load(f)
    try:
        if a in b:
            if c not in b[a]:
                b[a].append(c)
        else:
            b[a] = [c]
        with open(file+'.spike', 'wb') as f:   
            pickle.dump(b,f,protocol=pickle.HIGHEST_PROTOCOL)
    except:
        print('oops, something went wrong')

