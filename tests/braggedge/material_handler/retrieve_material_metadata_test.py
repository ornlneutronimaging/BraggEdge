import unittest
import os
from python.braggedge.material_handler import config
from python.braggedge.material_handler.retrieve_material_metadata import RetrieveMaterialMetadata
#from braggedge.material_handler import config
#from braggedge.material_handler.retrieve_material_metadata import RetrieveMaterialMetadata


class TestRetrieveMaterialMetadata(unittest.TestCase):

    def setUp(self):
        pass

    def test_retrieve_lattice_of_si(self):
        """assert value of lattice retrieved from Si"""
        retrieve_material = RetrieveMaterialMetadata(material='Si')
        lattice_expected = 5.431
        self.assertEqual(lattice_expected, retrieve_material.lattice)

if __name__ == '__main__':
    unittest.main()
