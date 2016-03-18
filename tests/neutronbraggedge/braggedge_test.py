import unittest
import os
import numpy as np
from neutronbraggedge.braggedge import BraggEdge


class TestBraggEdge(unittest.TestCase):

    def setUp(self):
        pass

    def test_retrieving_correct_metadata_for_Ni(self):
        """Assert the correct metadata are returned for Ni"""
        _handler = BraggEdge(material = 'Ni')
        _metadata = _handler.metadata
        self.assertAlmostEqual(3.5238, _metadata['lattice'], delta = 0.01)
        self.assertEqual('FCC', _metadata['crystal_structure'])
    
    def test_retrieving_correct_number_and_first_2_values_hkl_for_Si(self):
        """Assert the correct hkl first 2values are returned for Si, and the correct number"""
        _handler = BraggEdge(material = 'Si', number_of_bragg_edges = 4)
        _hkl = _handler.hkl
        self.assertEqual([1, 1, 1], _hkl[0])
        self.assertEqual([2, 0, 0], _hkl[1])
        self.assertEqual(4, len(_hkl))

    def test_calculating_d_spacing_values_for_Ni(self):
        """Assert the first 3 d_spacing are correct for Ni"""
        _handler = BraggEdge(material = 'Ni', number_of_bragg_edges = 4)
        _d_spacing = _handler.d_spacing
        self.assertAlmostEqual(2.0345, _d_spacing[0], delta = 0.001)
        self.assertAlmostEqual(1.7619, _d_spacing[1], delta = 0.001)
        self.assertAlmostEqual(1.2459, _d_spacing[2], delta = 0.001)
        
    def test_retrieving_first_2_values_hkl_for_Fe(self):
        """Assert the correct hkl first 2 values are returned for Fe """
        _handler = BraggEdge(material = 'Fe', number_of_bragg_edges = 4)
        _hkl = _handler.hkl
        self.assertEqual([1, 1, 0], _hkl[0])
        self.assertEqual([2, 0, 0], _hkl[1])
        self.assertEqual([2, 1, 1], _hkl[2])
        self.assertEqual([2, 2, 0], _hkl[3])

    def test_calculating_bragg_edges_for_Fe(self):
        """Assert the first 3 bragg_edges are correct for Fe"""
        _handler = BraggEdge(material = 'Fe', number_of_bragg_edges = 4)
        _bragg_edges = _handler.bragg_edges
        self.assertAlmostEqual(4.0537, _bragg_edges[0], delta = 0.001)
        self.assertAlmostEqual(2.8664, _bragg_edges[1], delta = 0.001)
        self.assertAlmostEqual(2.3404, _bragg_edges[2], delta = 0.001)
        
    def test_printing_report(self):
        """Assert the metadata/hkl/braggedges are correctly output"""
        _handler = BraggEdge(material = 'Ni', number_of_bragg_edges = 5)
        print(_handler)

    def test_create_export_csv_no_file_raise_error(self):
        """Assert the IOError is raised when no file name given"""
        _handler = BraggEdge(material = 'Fe', number_of_bragg_edges = 4)
        self.assertRaises(IOError, _handler.export)

    def test_create_export_csv_metadata(self):
        """Assert the correct metadata data are created for Fe when using create output file"""
        _handler = BraggEdge(material = 'Fe', number_of_bragg_edges = 4)
        _metadata = _handler._format_metadata()
        self.assertEqual("Material: Fe", _metadata[0])
        self.assertEqual("Lattice : 2.8664Angstroms", _metadata[1])
        self.assertEqual("Crystal Structure: BCC", _metadata[2])
        self.assertEqual("Using local metadata Table: True", _metadata[3])
        
    def test_create_export_csv_data(self):
        """Assert the correct data are created for Fe when using create output file"""
        _handler = BraggEdge(material = 'Fe', number_of_bragg_edges = 4)
        _data = _handler._format_data()
        self.assertEqual(1, _data[0][0])
        self.assertAlmostEqual(2.02685, _data[0][3], delta = 0.0001)
        self.assertAlmostEqual(4.05370, _data[0][4], delta = 0.0001)
        self.assertAlmostEqual(1.17020, _data[2][3], delta = 0.0001)
        self.assertAlmostEqual(2.34041, _data[2][4], delta = 0.0001)
    
    def test_create_export_csv_file_created(self):
        """Assert the correct output CSV file is created"""
        _handler = BraggEdge(material = 'Fe', number_of_bragg_edges = 4)
        _filename = 'remove_me.txt'
        _handler.export(filename = _filename, file_type = 'csv')
        self.assertTrue(os.path.isfile(_filename))
        os.remove(_filename) #cleanup temp file
    
    def test_create_export_unsuported_file_raise_error(self):
        """Assert in BraggEdge - NotImplementedError raised when trying to create unsuported output format"""
        _handler = BraggEdge(material = 'Fe', number_of_bragg_edges = 4)
        _filename = 'remove_me.txt'
        self.assertRaises(NotImplementedError, _handler.export, _filename, 'do_not_exist_yet')

    def test_calculate_experimental_lattice_with_no_input_provided(self):
        """Assert in BraggEdge - calculate exp. lattice - ValueError raised if no experimental bragg edge array provided """
        _handler = BraggEdge(material = 'Fe', number_of_bragg_edges = 4)
        self.assertRaises(ValueError, _handler.get_experimental_lattice_parameter)
        
    def test_calculate_experimental_lattice_with_value_and_error_different_size(self):
        """Assert in BraggEdge - bragg edge value and error have different sizes"""
        _handler = BraggEdge(material = 'Fe', number_of_bragg_edges = 4)
        exp_bragg_value = np.array([1,2,3])
        exp_bragg_error = np.array([0.1, 0.2])
        self.assertRaises(ValueError, _handler.get_experimental_lattice_parameter, exp_bragg_value,
                          exp_bragg_error)
        
        


if __name__ == '__main__':
    unittest.main()
