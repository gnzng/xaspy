import pandas as pd
import json
import numpy as np
import os

# from larch.xafs import autobk
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("echo")
args = parser.parse_args()

# Opening JSON file from input:
filename = args.echo

# Read in the file
with open(filename + ".txt", "r") as file:
    filedata = file.read()

# Replace the target string
filedata = filedata.replace("'", '"')

# Write the file out again
with open(filename + ".txt", "w") as file:
    file.write(filedata)


f = open(filename + ".txt")

data = json.load(f)
f.close()


cutoff = int(len(np.array(data["MCA_3"])) - len(np.array(data["I0"])))

smaller_length = len(np.array(data["I0"]))


# also cut out the last 5 points turned out to be a good approx, for different reasons


for n in list(data):
    if n == "timePP":
        data[n] = np.ones(smaller_length - 5) * data[n]

    elif len(data[n]) != smaller_length:
        data[n] = np.array(data[n])[cutoff:-5]
    else:
        data[n] = np.array(data[n])[:-5]

df = pd.DataFrame.from_dict(data)
# print(len(list(data)))

# check if this is only header by filesize:
if os.stat(filename + ".xdi").st_size <= 20 * 1024:

    with open(filename + ".xdi", "a") as f:
        dfAsString = df.to_string(header=False, index=False)
        f.write(dfAsString)
    f.close()

"""ene = np.array(data['E_enc'])
merge = np.mean([np.array(data['MCA_0'])/np.array(data['I0']),
np.array(data['MCA_1'])/np.array(data['I0']),
np.array(data['MCA_2'])/np.array(data['I0']),
np.array(data['MCA_3'])/np.array(data['I0'])],axis=0)

class class_spec:
    e = ene
    mu = merge

#autobk(energy = class_spec.e,mu = class_spec.mu,group=class_spec,rbkg=1, kw=2)

plt.figure()
plt.plot(ene,merge,linewidth=2)
plt.show()


#plt.figure()
#plt.plot(class_spec.k,class_spec.chi*class_spec.k**2,linewidth=2)
#plt.show()

"""
