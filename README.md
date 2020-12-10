# xaspy
[in beta and development phase]

Small module for doing xray absorption spectroscopy analysis using python. More detailed information will follow soon. 



## installation
```bash
pip install xaspy
```
update with: 

```bash
pip install xaspy -U
```

## XMCD investigation

Function XMCD merges and interpolates the spectra for same spin angular momentum of the photon. Lies then the curves on top of each other and builds the XMCD and XAS signal. After that subtraction of different backgrounds is possible (linear, stepfunctions, ...).  

## read in functions for experimental ASCII data 

read in functions for special beamlines: e.g. VEKMAG at BESSY II in Berlin

## read in function for theoretical calculations

read in functions for output files for programs like FEFF, multiX, xraylarch, quanty ...

## despiking of data

removes spikes from data while loading the data, without changing the raw data ... it creates *.spike file with list of rows to avoid, which will automatically be dropped while reading data in. Please use a basic read in function as follows:

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
load raw/spiked data with 
```python 
rd(nr, raw=True)
```

## toggle cell

this function can be imported from the utils package:

```python
from xaspy.utils import toggle
```
it creates a button with the argument as a a label, which can toggle away the whole cell. 

# Todo, coming soon:

- basic Mössbauer fitting 
