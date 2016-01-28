import unittest
import os
from neutronbraggedge.material_handler.retrieve_material_metadata import RetrieveMaterialMetadata


class TestRetrieveMaterialMetadata(unittest.TestCase):

    def setUp(self):
        pass

    def test_retrieve_lattice_of_si(self):
        """assert value of lattice retrieved from Si"""
        retrieve_material = RetrieveMaterialMetadata(material = 'Si',
                                                     use_local_table = False)
        lattice_expected = 5.431
        self.assertEqual(lattice_expected, retrieve_material.lattice)

    def test_raise_nameerror(self):
        """assert NameError is raised when no arguments is given"""
        self.assertRaises(NameError, RetrieveMaterialMetadata)

if __name__ == '__main__':
    unittest.main()
