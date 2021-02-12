# xaspy - framework for xray absorption spectroscopy
[in beta and development phase]

Small module for doing xray absorption spectroscopy analysis and pre evaluation on beam time using python. More detailed information will follow soon. 


## installation with PyPi
xaspy can be installed from shell via PyPi
```bash
pip install xaspy
```

You can update to the newest version with: 

```bash
pip install xaspy -U
```

## basic functions

This section will be extended and the implemented functions, whenever I find something useful.

### XMCD investigation

The function XMCD merges and interpolates the spectra for same spin angular momentum of the photon. Correlates the curves on top of each other and builds the XMCD and XAS signal. After that subtraction of different backgrounds is possible (linear, stepfunctions, ...).  

### read in functions for experimental ASCII data 

Different read in functions for special beamlines: e.g. VEKMAG/PM3 at BESSY II in Berlin. Dealing with large SPECS files. 

### read in function for theoretical calculations

read in functions for output files for programs like FEFF, multiX, xraylarch, quanty ...

### despiking of data

This function is to remove spikes from data while loading the data into the RAM.  It does not change the raw data. This module creates '.spike' file with list of rows to avoid, which will automatically be dropped while reading data in. Please use a basic read in function as follows:

```python
#function for read in a is number of scan
def rd(a,raw=False):
    path = '../path/to/'
    file = path + 'file'
    a = a
    dff = pd.read_csv(path+'file_{0:03}'.format(a), delim_whitespace=True,skiprows=[1]) # example readin
    if raw==False:
        try:
            with open(file+'.spike','rb') as f:
                b = pickle.load(f)
                if a in b:
                    todrop = b[a]
                    dff = dff.drop(todrop) #returns cleaned pandas file if .spike is existent and has an entry for scan number
        except:
            pass
    else: 
        pass
    return dff #returns pandas file 
```
Alternatively you can also load the raw or spiked data with:

```python 
rd(nr, raw=True)
```



# Todo, coming soon:

[ ] improve despiking on site 
