import unittest
import os
from braggedge.braggedge import BraggEdge


class TestBraggEdge(unittest.TestCase):

    def setUp(self):
        pass

    def test_calling_without_arguments(self):
        """Testing that class can be called with default arguments from python2 and 3"""
        _handler = BraggEdge(material='Si')
        print(_handler.metadata)


if __name__ == '__main__':
    unittest.main()
