# 🔬 xaspy - framework for X-ray absorption spectroscopy

This small python module [xaspy](https://github.com/gnzng/xaspy) wants to help with X-ray absorption spectroscopy analysis and pre-evaluation during and after beam times. Similar software and strongly inspired by (but mostly for EXAFS): [larch](https://github.com/xraypy/xraylarch). Strong focus on X-ray magnetic circular dichroism [XMCD](https://en.wikipedia.org/wiki/X-ray_magnetic_circular_dichroism).

1. [installation](#installation)
2. [telegram bot](#telegram-bot)
3. [XAS](#xas)
4. [import data](#import-data)
5. [despiking of data](#despiking-of-data)
6. [next steps](#next-steps)

# installation

## install via pip

xaspy can be installed via PyPi or downloaded here from github as the source code.

The necessary requirements can be found in requirement.txt file. Install via pip:

```bash
pip install xaspy
```

Use cell magic in jupyter notebook. You may need to restart the kernel, after updating.

```bash
%pip install xaspy
```

## update via pip

Update to the newest version with:

```bash
pip install -U xaspy
```

# XMCD

The function XMCD merges and interpolates the spectra for same spin angular momentum of the photon. Correlates the curves on top of each other and builds the XMCD and XAS signal. After that subtraction of different backgrounds is possible (linear, stepfunctions, ...). Also different normalization factors are possible.

## hysteresis loops

For multiple hysteresis curves in one file use class `mHYST` with included functions. Use `plot_separated()` to plot multiple hysteresis loops separated. Function `average_loops()` takes the loop numbers and averages them.

## backgrounds

the `xaspy.xas.backgrounds` module provides multiple possible backgrounds to correct the measured data.

# import data

## beam lines

### VEKMAG/PM3 at BESSY

Different read in functions for special beamlines: e.g. VEKMAG/PM3 at BESSY II in Berlin.

### 6.3.1 at ALS

## SPECS files

Large SPECS files usually contain multiple runs in one large ASCII file. A very useful SPECS file splitter (split.py) can be found in folder utils. For usage see the docstring in the file header.

## Mössbauer

First functions for the implementation of the Pi program for Mössbauer analysis. `readin.PiMoss('path/filename')` can no be used to import plotting data from the .dat-files generated from [Pi](https://git.uni-due.de/hm243ho/pi). Different implemented plotting functions can be called from the class.

I would recommend using the following saving procedures:

| extension        | content                              |
| ---------------- | ------------------------------------ |
| filename.mos     | raw data from measurement            |
| filename.mos.rtf | fitting information important for Pi |
| filename.dat     | exported ascii data table            |

## import of theoretical calculations and simulations

Reading functions for output files for programs like FEFF, multiX, xraylarch, quanty ...

# despiking of data

This function is to remove spikes from data while loading the data into the RAM. It does not change the raw data. This function creates '.spike' file with list of columns to avoid, which will automatically be dropped while reading data in via a pandas df. Please use a basic read in function as follows:

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

# next steps (maybe/hopefully)

- [ ] write (better) docs
- [ ] improve telegram bot
- [ ] continous integration and testing
- [ ] Total Electron Yield measurement correction
- [ ] Luminescence 2nd order correction
- [ ] improve fast despiking
- [ ] fit convolution and energy shift between theoretic and measured spectrum
- [ ] working with .rtf-files for Mössbauer spectra from Pi
- [x] write unittests
- [x] plot Mössbauer spectra from Pi
- [x] fast and basic XMCD evaluation
- [x] added telegram bot
