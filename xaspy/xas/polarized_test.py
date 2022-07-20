from importlib.resources import path
import unittest

import pickle
import numpy as np
import pandas as pd
import pytest
import os

#imports from xaspy: 
from polarized import (orbital_to_spin_ratio,
mHYST
)
from xas import group




# HYST tests:

path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.split(path_to_current_file)[0]
path_to_file = os.path.join(current_directory, "test_files/pd_dataframe_hyst_example1.pickle")
df = pickle.load(open(path_to_file,'rb'))


def test_import_df():
    # nr: 'TrajScan31914-001_0001.txt'
    assert isinstance(df,pd.DataFrame)

hystclass = mHYST(df,'Magnet Field','Energy','LY','Clock',ratio='lower/higher',
            log=True)

def test_hyst_from_df():
    assert hystclass
    assert isinstance(hystclass.average_loops([n for n in range(1,16)],return_data=True),tuple)

def test_raise_value_error_bc_wrong_column_name():
    with pytest.raises(ValueError):
        mHYST(df,'_non_existent_column','Energy','LY','Clock',ratio='lower/higher',
            log=True).average_loops([n for n in range(1,16)],return_data=True)




# XMCD tests



testgroup = group()

path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.split(path_to_current_file)[0]
path_to_file = os.path.join(current_directory, "test_files/xmcd_co.pickle")
testgroup.xmcd = pickle.load(open(path_to_file,'rb'))

testxmcd = testgroup.xmcd



class Test(unittest.TestCase):
    #in unit test orbital to spin ratio must be imported 
    
    def test_errors(self):
        #
        # test if errors are right
        #
        with self.assertRaises(ValueError):
            orbital_to_spin_ratio(xmcd=testxmcd,orbital='11s')
        with self.assertRaises(ValueError):
            orbital_to_spin_ratio(orbital='11s')
        
    def test_lds(self):
        # 
        # test if orbital_to_spin values yields real values
        # 
        
        # test for xmcd testset: 
        self.assertEqual(np.around(0.10483034490920523,1),
                         np.around(orbital_to_spin_ratio(xmcd = testxmcd ,group = None, 
                                                         xp = 2750, orbital='3d'),1))
        
        # test for group:
        orbital_to_spin_ratio(xmcd = None ,group = testgroup, 
                              xp = 2750, orbital='3d')
        self.assertEqual(np.around(0.10483034490920523,1),np.around(testgroup.lds,1))


if __name__ == '__main__':
    unittest.main()


