import os 
from bl631 import TrajScan, SigScan

from bl631 import HYST_scanpair,XMCD_scanpair

import pytest

path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.split(path_to_current_file)[0]
path_to_file = os.path.join(current_directory, "../test_files")


def test_imports():
    TrajScan.path = path_to_file
    TrajScan('31914-001_0001').df
    TrajScan('31914-001_0001').header
    assert TrajScan('31914-001_0001').scantype == "Magnetic Field"


def test_scn_maker():
    HYST_scanpair()
    XMCD_scanpair(1.9,[735,800])
    pass

  
def test_warnings():
    #
    # test if errors are right 
    assert XMCD_scanpair(1.9,[735,734])
    assert XMCD_scanpair(1.9,[735,735])
