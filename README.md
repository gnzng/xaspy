# 🔬 xaspy - framework for xray absorption spectroscopy

🚧🚧🚧 (always) under construction, developing parallel to my PhD journey 🚧🚧🚧

Small python module for xray absorption spectroscopy analysis and pre-evaluation during beam times. Similar software (mostly for EXAFS): [larch](https://github.com/xraypy/xraylarch). Mostly magnetic circular dichroism.

# table of contents

1. [installation](#installation)
2. [telegram bot](#telegram-bot)
3. [XAS](#xas)
4. [import data](#import-data)
5. [despiking of data](#despiking-of-data)
6. [next steps](#next-steps)

# installation

xaspy can be installed from shell via PyPi or downloaded here from github as the source code.

```bash
pip install xaspy
```

You can update to the newest version with:

```bash
pip install xaspy -U
```

# telegram bot

The telegram bot can be added via link to you contacts: [t.me/xaspy_bot](https://t.me/xaspy_bot), or writing to @xaspy_bot. First implementations are returning X-ray absorption edges of specific elements. It uses [XrayDB](https://github.com/xraypy/XrayDB).

# XAS

## XMCD

The function XMCD merges and interpolates the spectra for same spin angular momentum of the photon. Correlates the curves on top of each other and builds the XMCD and XAS signal. After that subtraction of different backgrounds is possible (linear, stepfunctions, ...).

# import data

## beam lines

Different read in functions for special beamlines: e.g. VEKMAG/PM3 at BESSY II in Berlin. Dealing with large SPECS files.

## Mössbauer

First functions for the implementation of the Pi program for Mössbauer analysis. `readin.PiMoss('path/filename')` can no be used to import plotting data from the .dat-files generated from [Pi](https://www.uni-due.de/~hm236ap/hoersten/home.html). Different implemented plotting funtions can be called from the class.

I would recommend using the following saving procedures:

| extension        | content                              |
| ---------------- | ------------------------------------ |
| filename.mos     | raw data from measurement            |
| filename.mos.rtf | fitting information important for Pi |
| filename.dat     | exported ascii data table            |

## read in function for theoretical calculations

read in functions for output files for programs like FEFF, multiX, xraylarch, quanty ...

# despiking of data

This function is to remove spikes from data while loading the data into the RAM. It does not change the raw data. This module creates '.spike' file with list of rows to avoid, which will automatically be dropped while reading data in. Please use a basic read in function as follows:

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

# next steps (maybe)

- [ ] write docs
- [ ] continous integration and testing
- [ ] improve fast despiking
- [ ] fit convolution and energy shift between theoretic and measured spectrum
- [ ] working with .rtf-files for Mössbauer spectra from Pi
- [x] write unittests
- [x] plot Mössbauer spectra from Pi
- [x] fast and basic XMCD evaluation
- [x] added telegram bot
