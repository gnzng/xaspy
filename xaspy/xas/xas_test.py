from xas import group

import unittest

import numpy as np

xmcd_141_ = group('test', lds=0.7)
xmcd_141_.energy = np.linspace(0,1,5000)
xmcd_141_.energy_interp = np.linspace(0,1,10000)
xmcd_141_.plus_xas = np.array([1,2,3,4,5])
xmcd_141_.minus_xas = np.array([1,2,3,4,5])

assert xmcd_141_                        ,'group should be existent'
assert xmcd_141_.lds == 0.7             ,'should be 0.7'
assert xmcd_141_.__name__ == 'test'     ,'name should be test'


class Test(unittest.TestCase):

    def test_1(self):
        self.assertEqual(xmcd_141_.lds, 0.7, 'should be 0.7')
        
    def test_2(self):    
        self.assertEqual(xmcd_141_.__name__, 'test', 'name should be test')



if __name__ == '__main__':
    unittest.main()


