import unittest
import os
from braggedge.braggedge import BraggEdge


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
        self.assertAlmostEqual(2.0345, _d_spacing[0], delta=0.001)
        self.assertAlmostEqual(1.7619, _d_spacing[1], delta=0.001)
        self.assertAlmostEqual(1.2459, _d_spacing[2], delta=0.001)
        
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
        self.assertAlmostEqual(4.0537, _bragg_edges[0], delta=0.001)
        self.assertAlmostEqual(2.8664, _bragg_edges[1], delta=0.001)
        self.assertAlmostEqual(2.3404, _bragg_edges[2], delta=0.001)

if __name__ == '__main__':
    unittest.main()
