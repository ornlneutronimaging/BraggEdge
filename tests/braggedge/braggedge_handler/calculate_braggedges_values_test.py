import unittest
import os
from braggedge.braggedges_handler.braggedge_values_calculator import BraggEdgeValuesCalculator


class TestBraggEdgesHandler(unittest.TestCase):

    def setUp(self):
        pass

    def test_calling_without_arguments(self):
        """Testing that class can be called with default arguments from python2 and 3"""
        _handler = BraggEdgeValuesCalculator()
        self.assertEqual("FCC", _handler.structure)
        
    def test_right_structure_name_is_passed_in_constructor(self):
        """Assert that structure name passed in constructor is correctly used"""
        _structure_name = "BCC"
        _handler = BraggEdgeValuesCalculator(structure_name = _structure_name)
        self.assertEqual("BCC", _handler.structure)
        
    def test_right_structure_name_is_passed_in_assigned(self):
        """Assert that structure name assigned is correctly saved"""
        _structure_name = "BCC"
        _handler = BraggEdgeValuesCalculator()
        _handler.structure = _structure_name
        self.assertEqual("BCC", _handler.structure)
        
    def test_right_hkl_number_calculated_for_BCC(self):
        """Assert that the right number of hkl sets is returned for BCC"""
        _structure_name = "BCC"
        _handler = BraggEdgeValuesCalculator(structure_name = _structure_name, 
                                             number_of_set = 5)
        _handler.calculate_hkl()
        _hkl = _handler.hkl
        self.assertEqual(5, len(_hkl))
        
    def test_right_hkl_number_calculated_for_FCC(self):
        """Assert that the right number of hkl sets is returned for FCC"""
        _structure_name = "FCC"
        _handler = BraggEdgeValuesCalculator(structure_name = _structure_name, 
                                             number_of_set = 5)
        _handler.calculate_hkl()
        _hkl = _handler.hkl
        self.assertEqual(5, len(_hkl))

    def test_right_hkl_set_is_calculated_for_FCC(self):
        """Assert that the right set of hkl sets is returned for FCC"""
        _structure_name = "FCC"
        _handler = BraggEdgeValuesCalculator(structure_name = _structure_name, 
                                             number_of_set = 5)
        _handler.calculate_hkl()
        _hkl = _handler.hkl
        self.assertEqual([1, 1, 1], _hkl[0])
        self.assertEqual([2, 0, 0], _hkl[1])
        self.assertEqual([2, 2, 0], _hkl[2])
        self.assertEqual([2, 2, 2], _hkl[3])
        self.assertEqual([3, 1, 1], _hkl[4])    
           
    def test_right_hkl_number_calculated_for_BCC(self):
        """Assert that the right number of hkl sets is returned for BCC"""
        _structure_name = "BCC"
        _handler = BraggEdgeValuesCalculator(structure_name = _structure_name, 
                                             number_of_set = 5)
        _handler.calculate_hkl()
        _hkl = _handler.hkl
        self.assertEqual(5, len(_hkl))

    def test_right_hkl_set_is_calculated_for_BCC(self):
        """Assert that the right set of hkl sets is returned for BCC"""
        _structure_name = "BCC"
        _handler = BraggEdgeValuesCalculator(structure_name = _structure_name, 
                                             number_of_set = 5)
        _handler.calculate_hkl()
        _hkl = _handler.hkl
        self.assertEqual([1, 0, 0], _hkl[0])
        self.assertEqual([1, 1, 1], _hkl[1])
        self.assertEqual([2, 1, 0], _hkl[2])
        self.assertEqual([2, 2, 1], _hkl[3])
        self.assertEqual([3, 0, 0], _hkl[4])

    def test_calculate_bragg_edges_algorithm_fail_when_no_lattice_given(self):
        """Assert that ValueError is correctly raised when no lattice is provided"""
        _handler = BraggEdgeValuesCalculator(structure_name = "BCC")
        self.assertRaises(ValueError, _handler.calculate_bragg_edges)

    def test_d_spacing_for_first_hkl_of_bcc(self):
        """Assert the bragg edge values for the first BCC structure are correct"""
        _handler = BraggEdgeValuesCalculator(structure_name = "BCC", lattice=1.)
        _handler.calculate_hkl()
        _handler.calculate_bragg_edges()
        self.assertEqual(2.0, _handler.bragg_edges[0])
        self.assertAlmostEqual(1.1547, _handler.bragg_edges[1], delta=0.0001)
        self.assertAlmostEqual(0.8944, _handler.bragg_edges[2], delta=0.0001)

    def test_d_spacing_for_first_hkl_of_fcc(self):
        """Assert the bragg edge values for the first FCC structure are correct"""
        _handler = BraggEdgeValuesCalculator(structure_name = "FCC", lattice=1.)
        _handler.calculate_hkl()
        _handler.calculate_bragg_edges()
        self.assertAlmostEqual(1.1547, _handler.bragg_edges[0], delta=0.0001)
        self.assertAlmostEqual(1.0, _handler.bragg_edges[1], delta=0.0001)
        self.assertAlmostEqual(0.7071, _handler.bragg_edges[2], delta=0.0001)


if __name__ == '__main__':
    unittest.main()
