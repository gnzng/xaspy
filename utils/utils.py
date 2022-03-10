def toggle(**kws):
    '''
    removed in version 0.2.1:
        toggles cell in Jupyter notebook;
        makes button with label 'a' 
    '''
    return print('this has been removed in version 0.2.1')

def showspeccom(a):
    '''
    a = SPEC file
    returns list with commands/comments #C and #S
    '''
    clst=[]
    with open(a,'r')as f:
        for line in f:
            if '#C' in line:
                clst.append(line.replace('\n',''))
            if '#S' in line:
                clst.append(line.replace('\n',''))
    return clst