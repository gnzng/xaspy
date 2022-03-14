import unittest

import pickle
import numpy as np
from polarized import orbital_to_spin_ratio 
from xas import group


testgroup = group()

testgroup.xmcd = pickle.load(open('xas/test_spectra/xmcd_co.pickle','rb'))

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


