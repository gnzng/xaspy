import pandas as pd
import json
import numpy as np 
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("echo")
args = parser.parse_args()

# Opening JSON file from input: 
filename = args.echo

# Read in the file
with open(filename + '.txt', 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('\'', '\"')

# Write the file out again
with open(filename+'.txt', 'w') as file:
  file.write(filedata)


f = open(filename+'.txt')

data = json.load(f)
f.close()


cutoff = int(len(np.array(data['MCA_3'])) - len(np.array(data['I0'])))

smaller_length = len(np.array(data['I0']))


# also cut out the last 5 points turned out to be a good approx, for different reasons and convenience
for n in list(data):
    if n == 'timePP':
        data[n] = np.ones(smaller_length-5)*data[n]

    elif len(data[n]) != smaller_length:
        data[n] = np.array(data[n])[cutoff:-5]
    else:
        data[n] =np.array(data[n])[:-5]

df = pd.DataFrame.from_dict(data)
#print(len(list(data)))

#check if this is only header by filesize:
if os.stat(filename +'.xdi').st_size <= 20*1024:

    with open(filename + '.xdi', 'a') as f:
        dfAsString = df.to_string(header=False, index=False)
        f.write(dfAsString)
    f.close()
