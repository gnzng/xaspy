# xaspy
[in beta and development phase]

Small module for doing xray absorption spectroscopy analysis using python. More detailed information will follow soon. 



## installation
```bash
pip install xaspy
```

## XMCD investigation

Function XMCD merges and interpolates the spectra for same spin angular momentum of the photon. Lies then the curves on top of each other and builds the XMCD and XAS signal. After that subtraction of different backgrounds is possible (linear, stepfunctions, ...).  

## read in functions for experimental ASCII data 

read in functions for special beamlines: e.g. VEKMAG at BESSY II in Berlin

## read in function for theoretical calculations

read in functions for output files for programs like FEFF, multiX, xraylarch, quanty ...

## despiking of data

removes spikes from data while loading the data, without changing the raw data ... coming soon
