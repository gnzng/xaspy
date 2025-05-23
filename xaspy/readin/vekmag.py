import pandas as pd
import pickle


# readin functions from different beamlines:
# VEKMAG### BESSY2
# define get header function from large, unsplit and file
def getheader(b, file):  # its written that b is scan number!
    r = open(file, "r")
    mylist = r.read().splitlines()
    matching = [p for p in mylist if "#L" in p]
    scannr = [p for p in mylist if "#S" in p]
    r.close()
    rscan = []
    for n in scannr:
        v = n.split()[1]
        rscan.append(int(v))
    header = []
    for n in range(len(rscan)):
        t1 = [p for p in matching[n].split() if not "#L" in p]
        for n in range(len(t1)):
            t1[n] = "{}_".format(n + 1) + t1[n]
        header.append(t1)
    c = rscan.index(b)
    return header[c]


def getcommand(b, file):
    r = open(file, "r")
    mylist = r.read().splitlines()
    scannr = [p for p in mylist if "#S" in p]
    r.close()
    rscan = []
    comma = []
    for n in scannr:
        v = n.split()[1]
        w = " ".join(n.split()[2:])
        rscan.append(int(v))
        comma.append(w)
    c = rscan.index(b)
    return comma[c]


# function for read in a is number of scan
def readin(a, file, raw=False):
    a = a
    dff = pd.read_csv(
        file + "_{}.dat".format(a),
        delim_whitespace=True,
        header=0,
        names=getheader(a, file),
        comment="#",
    )
    if raw is False:
        try:
            with open(file + ".spike", "rb") as f:
                b = pickle.load(f)
                if a in b:
                    todrop = b[a]
                    dff = dff.drop(todrop)
        except Exception:
            pass
    else:
        pass
    return dff
