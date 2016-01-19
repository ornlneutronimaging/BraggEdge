import unittest
import os
from braggedge.braggedges_handler.structure_handler import StructureHandler


class TestBraggEdgesHandler(unittest.TestCase):

    def setUp(self):
        pass

    def test_calling_with_wrong_structure(self):
        """checking that calling an unknown structure raises an error"""
        self.assertRaises(ValueError, StructureHandler, "HCC")
        
    def test_getting_the_right_first_hkl_for_BCC(self):
        """assert that the first h,k,l values are correct"""
        _handler = StructureHandler("BCC", 1)
        _list_hkl = _handler.hkl 
        self.assertEqual([1, 0, 0], _list_hkl[0])

    def test_getting_the_right_amount_of_hkl_for_BCC(self):
        """assert that the right number of hkl set is returned for BCC"""
        _handler = StructureHandler("BCC", 10)
        _list_hkl = _handler.hkl
        _nbr_hkl = len(_list_hkl)
        self.assertEqual(10, _nbr_hkl)
        
    def test_getting_the_right_first_hkl_value(self):
        """assert that the first few hkl set calculated are correct for BCC"""
        _handler = StructureHandler("BCC", 10)
        _list_hkl = _handler.hkl
        _nbr_hkl = len(_list_hkl)
        self.assertEqual([1, 1, 1], _list_hkl[1])
        self.assertEqual([2, 1, 0], _list_hkl[2])
        self.assertEqual([2, 2, 1], _list_hkl[3])
        self.assertEqual([3, 0, 0], _list_hkl[4])
        

if __name__ == '__main__':
    unittest.main()
