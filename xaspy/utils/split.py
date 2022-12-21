# SPEC file splitter
#
# author gnzng
#
# small python program to split a larger SPEC file into individual files
#
# new empty folder for individual scans has to be created in the same directory. eg. scans_individual
#
# splitted files are .dat files
# contain first line scan number and command
# second line name of detectors/header


import re


# input parameters:
file = input("Enter Filename:")
output_folder = input('write scans to folder (folder has to already exist):')
# end input parameters

# split to remove extension from filename
filename = file.split('.')[0]


def split(file):
    clean = []
    clst = []
    with open(file, "r") as f:
        regexp = re.compile(r"^-?\d+\.?\d*")
        for line in f:
            if "#C" in line:
                clst.append(line.replace("\n", ""))
            if "#S" in line:
                clean.append(line.replace("\n", ""))
                nr = line.split(" ")[1]
            if "#L" in line:
                clean.append(line[3:].replace("\n", ""))
            if regexp.search(line):
                clean.append(line.replace("\n", ""))
            if not line.strip():
                clean.append("splitsignal")
    for n in range(1, 10000):
        if clean[0] == "splitsignal":
            clean.pop(0)
        else:
            break
    nr = 0
    for i in clean:
        if "#S" in i:
            nr = i.split(" ")[1]
            f = open(
                output_folder + "/" + filename + "_{0:03}.dat".format(int(nr)),
                "w+",
            )
        f = open(
            output_folder + "/" + filename + "_{0:03}.dat".format(int(nr)), "a"
        )
        if i != "splitsignal":
            f.write(i + "\n")
        if n != 0:
            if i == "splitsignal":
                f.close()


split(file)

print("excuted")
