import os 

from bl631 import TrajScan, SigScan


path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.split(path_to_current_file)[0]
path_to_file = os.path.join(current_directory, "../test_files")


def test_imports():
    TrajScan.path = path_to_file
    TrajScan('31914-001_0001').df
    TrajScan('31914-001_0001').header
    TrajScan('31914-001_0001').scantype



### TODO local tests / test files for import 

'''
test_list_TrajScan = []

datapath = "Y:\\BCS Setup Data\\"
for n in os.listdir(datapath):
    files   = datapath + "{}".format(n)
    try:
        file = os.listdir(files)
        for i in (file):
            if i.startswith("TrajScan"):
                strng = i.strip("TrajScan.txt")
                test_list_TrajScan.append(strng)
    except:
        pass
    
test_list_SigScan = []

datapath = "Y:\\BCS Setup Data\\"
for n in os.listdir(datapath):
    files   = datapath + "{}".format(n)
    try:
        file = os.listdir(files)
        for i in (file):
            if i.startswith("SigScan"):
                strng = i.strip("SigScan.txt")
                test_list_SigScan.append(strng)
    except:
        pass

'''
